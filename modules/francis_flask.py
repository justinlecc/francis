import os
from flask import Flask

# Flask singleton
class FrancisFlask():

    # Singleton instance.
    __instance = None

    # Instantiation creates/returns the singleton instance.
    def __new__(cls):

        if FrancisFlask.__instance is None:
            FrancisFlask.__instance = Flask(__name__)
            FrancisFlask.__instance.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FRANCIS_DB_URI']

        return FrancisFlask.__instance

