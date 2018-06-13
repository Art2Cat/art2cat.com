#!/usr/bin/env python3
# encoding=utf-8
import os
from app import create_app, db
from app.models import User, Post
from flask_script import Manager, Shell

#os.getenv('FLASK_CONFIG') or
app = create_app('default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
