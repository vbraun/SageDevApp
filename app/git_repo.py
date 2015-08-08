
import logging
log = logging.getLogger()

import os
import git

from app.config import config
from app.validate.email import is_valid_email


class GitRepository(object):

    def __init__(self, path=None, branch=None, url=None):
        self.path = path
        self.branch = branch
        self.url = url
        try:
            self._repo = git.Repo(path)
        except Exception:
            self._repo = git.Repo.clone_from(url, path, branch=branch)

    @property
    def repo(self):
        return self._repo
    
    @property
    def git(self):
        return self._repo.git
    
    def update(self):
        self.git.fetch('origin' , self.branch)
        self.git.reset('FETCH_HEAD', hard=True)
                
    def log_emails(self):
        """
        Return set of all email addresses in the log
        """
        all_emails = set(self.git.log(format='%aE').splitlines())
        return frozenset(filter(is_valid_email, all_emails))
                     

        

app_repo = GitRepository(**config.data_files.repo)

