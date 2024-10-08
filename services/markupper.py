from schemas.document import Document
from schemas.message import MessageCreate, MessageSchema
from schemas.block import RecognitionBlockCreate
from schemas.theme import RecognitionThemeCreate
from schemas.location import RecognitionLocationCreate
from schemas.events import EventsCreate
from dao import dao_block, dao_theme, dao_message,  dao_location, dao_document, dao_events
from time import sleep
import io, json
# import geojson
# from shapely.geometry import shape
import pandas as pd
# import torch
import warnings
warnings.simplefilter('ignore')
import logging
import geojson

logger = logging.getLogger("gunicorn.error")

class NoParsingFilter(logging.Filter):
    patterns = ["block_not_found"]
    def filter(self, record):
        return not "blob" in record.getMessage()

logger.addFilter(NoParsingFilter())

          
def parse_document(db, document: Document):
    logger.info(f"start document {document.name} markup")
    from main import ml_models
    dao_document.set_marking_up(db, uuid=document.id)
    # try: 
    df = pd.read_excel(io.BytesIO(document.file))

    # df = pd.read_excel('test.xlsx')
    df = df.dropna(subset=['Текст'])

    df[['blocks','block_probs']] = pd.DataFrame(df['Текст'].progress_map(lambda x: ml_models['blocks_model'].run(x)).to_list())

    logger.info(f"{document.name} blocks marked up")
    df[['themes','theme_probs']] = pd.DataFrame(df['Текст'].progress_map(lambda x: ml_models['themes_model'].run(x)).to_list())
    logger.info(f"{document.name} themes marked up")
    df = ml_models['address_model'].run(df,  text_column='Текст')
    df = df.drop_duplicates(subset='Текст').reset_index()
    
    with open(f'models_df_{document.name}.pickle', 'wb') as f:
        df.to_pickle(f)

    logger.info(f"{document.name} locations marked up")
    df["Дата и время"] = ""
    df["message_id"] = ""
    df["cats"] = ""
    for index, row in df.iterrows():
        # logger.error(type(row['Дата создания']))
        msg_obj = MessageCreate(
            created_at = row['Дата создания'],
            text= row['Текст'],
            document = document,
            external_id = row['ID']
        )
        msg = dao_message.create(db, obj_in=msg_obj)
        blocks = row['blocks']
        if pd.isna(blocks):
            logger.error(f"Empty blocks for message: {msg.text}")
            continue
        else:
            try:
                blocks = [block.strip() for block in row['blocks'].split(';')]
                df.iloc[index, df.columns.get_loc('message_id')] = str(msg.id)
                df.iloc[index, df.columns.get_loc('Дата и время')] = msg.created_at.strftime("%Y.%m.%d %H:%M")
                df.iloc[index, df.columns.get_loc('cats')] = blocks[0] if blocks else None
                block_probs = [float(str(block_prob).strip()) for block_prob in row['block_probs'].split(';')]
            except AttributeError:
                logger.error(f"blocks:  { row['blocks']}")
                logger.error(f"block_probs:  { row['block_probs']}")
                blocks = [row['blocks'] ]
                df.iloc[index, df.columns.get_loc('message_id')] = str(msg.id)
                df.iloc[index, df.columns.get_loc('Дата и время')] = msg.created_at.strftime("%Y.%m.%d %H:%M")
                df.iloc[index, df.columns.get_loc('cats')] = blocks[0] if blocks else None
                block_probs = [float(row['block_probs'])]
            
            for i in range(len(blocks)):
                block_schematized = RecognitionBlockCreate(
                    name=blocks[i],
                    probability=block_probs[i],
                    message_id=msg.id
                )
                dao_block.create(db,obj_in=block_schematized)

        themes = row['themes']
        if pd.isna(themes):
            logger.error(f"Empty themes for message: {msg.text}")
            continue
        else:
            try:
                themes = [theme.strip() for theme in themes.split(';')]

                theme_probs = [float(str(theme_prob).strip()) for theme_prob in row['theme_probs'].split(';')]
            except AttributeError:
                logger.error(f"themes:  { themes}")
                logger.error(f"theme_probs: {row['theme_probs']}")
                
                themes = [row['themes'].strip()]
                theme_probs = [float(row['theme_probs'])]
            for i in range(len(themes)):
                theme_schematized = RecognitionThemeCreate(
                    name=themes[i],
                    probability=theme_probs[i],
                    message_id=msg.id
                )
                dao_theme.create(db,obj_in=theme_schematized)
        
        
        geo_level = row['level']
        if not pd.isna(row["Location"]):
            street = row["Location"].capitalize() if row["Location"] else ""
            prob = row['Score']
        # elif geo_level == "street":
        #     street = row["Street"].capitalize() if row["Street"] else ""
        #     prob = row['Score']
        else:
            prob = None
            street = None
        geometry = str(row['geometry']) if row['geometry'] else None

            # g1 = geojson.loads(geometry)
            # g2 = shape(g1)
            # geometry = g2.wkt
            
        location_schematized = RecognitionLocationCreate(
                name=street,
                geometry=geometry,
                probability=prob,
                message_id=msg.id
        )
        dao_location.create(db,obj_in=location_schematized)

    df = df.rename(columns = {"Текст": "Текст комментария"})
    messages, events, connections = ml_models['event_model'].run(df, 'services/SOIKA/data/raw/population.geojson', 'Санкт-Петербург', 32636, min_event_size=3)
    events_schematized = EventsCreate(
                document=document,
                file_events= geojson.dumps(geojson.loads(events.to_json())).encode(),
                file_messages= geojson.dumps(geojson.loads(messages.to_json())).encode(),
                file_connections= geojson.dumps(geojson.loads(connections.to_json())).encode()
    )
    logger.info(f"{document.name} mark up finished")
    dao_events.create(db,obj_in=events_schematized)

    dao_document.set_marked_up(db, uuid=document.id)
            
    # except Exception as e:
    #     logger.error(e)
    #     dao_document.set_failed(db, uuid=document.id)
    
    return None




