from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from PyQuora import app
from exts import db
from models import User, Question, Comment

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
