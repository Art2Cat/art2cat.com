#!/usr/bin/env python3
# encoding=utf-8
import os
from app import create_app, db
from app.models import User, Post, Role
from flask_script import Manager, Shell
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(verbose=True)
env_path = Path.home() / 'rorschach-config' / 'rorscat' / 'dev.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path, verbose=True)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
