import os

DEBUG = True

SECRET_KEY = 'Af29k21E04'

abs_dir = os.path.dirname(os.path.abspath(__file__))

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'