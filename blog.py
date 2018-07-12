from app import flaskapp
from app import db
from app.models import User, Posts


@flaskapp.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Posts}