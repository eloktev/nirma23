from schemas.document import Document
from schemas.message import MessageCreate, MessageSchema
from schemas.block import RecognitionBlockCreate
from schemas.theme import RecognitionThemeCreate
from schemas.location import RecognitionLocationCreate
from schemas.events import EventsCreate
from dao import dao_block, dao_theme, dao_message,  dao_location, dao_document, dao_events
from time import sleep
import pandas as pd
import io, json
import geojson
from shapely.geometry import shape

          
def parse_document(db, document: Document):
    """
    Mock parser
    """
    dao_document.set_marking_up(db, uuid=document.id)
    df = pd.read_excel(io.BytesIO(document.file))

    with open('test_events.geojson', 'rb') as e:
        with open('test_messages.geojson', 'rb') as m:
            events_schematized = EventsCreate(
                document=document,
                file_events= e.read(),
                file_messages= m.read()
                )
            dao_events.create(db,obj_in=events_schematized)

    with open('recognition_example.json', 'r') as f:
        markup = json.loads(f.read())
    for item in markup[0:10]:
        msg_obj = MessageCreate(
            text= item['text'],
            document = document
        )
        msg = dao_message.create(db, obj_in=msg_obj)
        for b in item.get('recognition_blocks', []):
            block_schematized = RecognitionBlockCreate(
                name=b["name"],
                probability=b["probability"],
                message_id=msg.id
            )
            dao_block.create(db,obj_in=block_schematized)
        for t in item.get('recognition_themes', []):
            block_schematized = RecognitionThemeCreate(
                name=t["name"],
                probability=t["probability"],
                message_id=msg.id
            )
            dao_theme.create(db,obj_in=block_schematized)
        for l in item.get('recognition_locations', []):
            geometry = l.get("geometry", None)
            if geometry:
                g1 = geojson.loads(geometry)
                g2 = shape(g1)
                geometry = g2.wkt
            location_schematized = RecognitionLocationCreate(
                name=l.get("street_name", None),
                geometry=geometry,
                probability=l["probability"],
                message_id=msg.id
            )
            dao_location.create(db,obj_in=location_schematized)
        
   
            


    sleep(10)
    dao_document.set_marked_up(db, uuid=document.id)
    return None




