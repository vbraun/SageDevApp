import sys
import os

from app.config import config
from app.git_repo import app_repo

def _prepare():
    sage_bootstrap_path = os.path.join(config.data_files.repo.path, 'build')
    if sage_bootstrap_path not in sys.path:
        sys.path.insert(0, sage_bootstrap_path)
    os.environ['SAGE_BOOTSTRAP'] = 'interactive:false,log:debug'

    
_prepare()

import sage_bootstrap
