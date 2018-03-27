import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # needed by flask wtf for CSRC
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YOU WILL NEVER GUESS'
    USERS = [('user1','user1'), ('user2','user2'), ('user3','user3')]