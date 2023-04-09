from .document import dao_document
from .message import dao_message
from .block import dao_block, dao_approvedblock
from .theme import dao_theme, dao_approvedtheme
from .location import dao_location, dao_approvedlocation

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
