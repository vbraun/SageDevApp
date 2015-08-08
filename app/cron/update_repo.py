

from app.git_repo import app_repo
from app.auth.known_email_model import KnownEmail, update_known_emails


def update_repo():
    app_repo.update()
    output = [app_repo.git.show()]
    update_known_emails(app_repo.log_emails())
    output.append('/n/nKnown Emails:')
    output.extend(model.email for model in KnownEmail.select())
    print(KnownEmail.select())
    return '\n'.join(output)



    
    
