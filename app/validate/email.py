

import re

EMAIL_RE = re.compile('[a-z0-9!#$%&\'*+/=?^_`{|}~.-]+@[a-z0-9-]+(\.[a-z0-9-]+)*')



def is_valid_email(email):
    return EMAIL_RE.fullmatch(email) is not None
