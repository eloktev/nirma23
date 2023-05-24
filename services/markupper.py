from schemas.document import Document
from schemas.message import MessageCreate, MessageSchema
from schemas.block import RecognitionBlockCreate
from schemas.theme import RecognitionThemeCreate
from schemas.location import RecognitionLocationCreate
from dao import dao_block, dao_theme, dao_message,  dao_location, dao_document
from time import sleep
import pandas as pd
import string, secrets, random, io, json

def random_string(type):        
        letters = string.ascii_lowercase+string.ascii_uppercase+string.digits            
        return  type + '_' + ''.join(secrets.choice(letters) for i in range(2))

def get_random(type):
    features = []
    if type == "location":
        for i in range(0, random.randrange(3)):
            if not i == random.randrange(3):
                features.append({"name": random_string("streetname"), 
                                 "location": f"POINT (3{random.randrange(2)}.3117 59.{random.randrange(9999)})",
                                 "probability": random.uniform(0, 1)
                                 })

    else:
        for i in range(0, random.randrange(3)):
            features.append({"name": random_string(type), "probability": random.uniform(0, 1)})
    return features
          



def markup_message(db, message: MessageSchema):
    """
    Mock markupper
    """
    markup = lambda _ : {
                            "themes": get_random("theme"),
                            "blocks": get_random("block"),
                            "locations": get_random("location")
                        }
    markup = markup("_")

    for block in markup["blocks"]:
        block_schematized = RecognitionBlockCreate(
            name=block["name"],
            probability=block["probability"],
            message_id=message.id
        )
        dao_block.create(db,obj_in=block_schematized)
    for theme in markup["themes"]:
        theme_schematized = RecognitionThemeCreate(
            name=theme["name"],
            probability=theme["probability"],
            message_id=message.id
        )
        dao_theme.create(db,obj_in=theme_schematized)
    for location in markup["locations"]:
        location_schematized = RecognitionLocationCreate(
            name=location["name"],
            geometry=location["location"],
            probability=location["probability"],
            message_id=message.id
        )
        dao_location.create(db,obj_in=location_schematized)
    

    # markup = MarkupCreate(
    #     message_id=message.id
    # )
    # dao_markup.create(db, obj_in=markup)
    return markup

def parse_document(db, document: Document):
    """
    Mock parser
    """
    dao_document.set_marking_up(db, uuid=document.id)
    df = pd.read_excel(io.BytesIO(document.file))

    with open('recognition_example.json', 'r') as f:
        markup = json.loads(f.read())

    for item in markup:
        msg = MessageCreate(
            text= item['text'],
            document = document
        )
        for b in item['recognition_blocks']:
            block_schematized = RecognitionBlockCreate(
                name=b["name"],
                probability=b["probability"],
                message_id=msg.id
            )
            dao_block.create(db,obj_in=block_schematized)
        for t in item['recognition_themes']:
            block_schematized = RecognitionThemeCreate(
                name=t["name"],
                probability=t["probability"],
                message_id=msg.id
            )
            dao_theme.create(db,obj_in=block_schematized)
        for l in item['recognition_locations']:
            location_schematized = RecognitionLocationCreate(
                name=l["street_name"],
                geometry=l["location"],
                probability=l["probability"],
                message_id=msg.id
            )
            dao_location.create(db,obj_in=location_schematized)

    # for index, row in df.iterrows():
    #     msg = MessageCreate(
    #         text= row['Текст'],
    #         document = document
    #     )
    #     msg_obj = dao_message.create(db, obj_in=msg)
    #     markup_message(db, msg_obj)
    # for i in range(0, 3):
        # msg = MessageCreate(
        #     text= str(i) + '_text_from_' + document.name,
        #     document = document
        # )
        # msg_obj = dao_message.create(db, obj_in=msg)
        # markup_message(db, msg_obj)

    sleep(10)
    dao_document.set_marked_up(db, uuid=document.id)
    return None




