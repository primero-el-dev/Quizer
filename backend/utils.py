import re
from wtforms.validators import ValidationError

UUID_REGEX = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}')

def is_valid_uuid(form, field):
    if not UUID_REGEX.match(field.data.lower()):
        raise ValidationError('Invalid UUID')