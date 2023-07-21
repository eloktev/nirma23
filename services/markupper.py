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
# import logging

          
def parse_document(db, document: Document):
    """
    Mock parser
    """
    from main import ml_models
    dao_document.set_marking_up(db, uuid=document.id)
    df = pd.read_excel(io.BytesIO(document.file))

    # df = pd.read_excel('test.xlsx')
    df = df.dropna(subset=['Текст'])

    df[['blocks','block_probs']] = pd.DataFrame(df['Текст'].progress_map(lambda x: ml_models['blocks_model'].run(x)).to_list())

    
    df[['themes','theme_probs']] = pd.DataFrame(df['Текст'].progress_map(lambda x: ml_models['themes_model'].run(x)).to_list())

    df = ml_models['address_model'].run(df,  text_column='Текст')


    for index, row in df.iterrows():
        msg_obj = MessageCreate(
            text= row['Текст'],
            document = document
        )
        msg = dao_message.create(db, obj_in=msg_obj)
        blocks = [block.strip() for block in row['blocks'].split(';')]

        block_probs = [float(block_prob.strip()) for block_prob in row['block_probs'].split(';')]
        for i in range(len(blocks)):
            block_schematized = RecognitionBlockCreate(
                name=blocks[i],
                probability=block_probs[i],
                message_id=msg.id
            )
            dao_block.create(db,obj_in=block_schematized)

        themes = [theme.strip() for theme in row['themes'].split(';')]

        theme_probs = [float(theme_prob.strip()) for theme_prob in row['theme_probs'].split(';')]
        for i in range(len(themes)):
            theme_schematized = RecognitionThemeCreate(
                name=themes[i],
                probability=theme_probs[i],
                message_id=msg.id
            )
            dao_theme.create(db,obj_in=theme_schematized)
        
        
        geo_level = row['level']
        if geo_level == "street":
            street = row["street"].capitalize() if row["street"] else ""
            prob = row['Score']
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



    # messages, events, connections = ml_models['event_model'].run(target_texts, 'Санкт-Петербург', 32636, min_event_size=3)
    # with open('test_events.geojson', 'rb') as e:
    #     with open('test_messages.geojson', 'rb') as m:
    #         events_schematized = EventsCreate(
    #             document=document,
    #             file_events= geojson.dumps(geojson.loads(e.read())).encode() ,
    #             file_messages= geojson.dumps(geojson.loads(m.read())).encode()
    #             )
    #         dao_events.create(db,obj_in=events_schematized)

   
            


    sleep(10)
    dao_document.set_marked_up(db, uuid=document.id)
    return None




