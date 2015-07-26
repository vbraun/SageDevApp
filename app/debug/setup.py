"""
Debug settings
"""

from app.config import config
from app.auth.user_model import User


def add_sample_user():
    user = User.create_from_registration('Nicolas Bourbaki', 'nick@ens.fr', '57')
    user.email_validated = True
    user.save()





if not config.debug:
    raise ImportError('this module can only be imported in debug mode')
else:
    add_sample_user()
    
