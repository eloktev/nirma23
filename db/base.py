# Import all the models, so that Base has them before being
# imported by Alembic
from db.base_class import Base  # noqa
from models.document import Document  # noqa
from models.message import Message  # noqa
from models.block import Block, RecognitionBlock, ApprovedBlock  # noqa
from models.theme import Theme, RecognitionTheme, ApprovedTheme # noqa
from models.location import Location, RecognitionLocation, ApprovedLocation # noqa

