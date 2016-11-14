import os
from flask import Flask

# Flask singleton
class FrancisFlask():

    # Singleton instance.
    __instance = None

    # Instantiation creates/returns the singleton instance.
    def __new__(cls):

        if FrancisFlask.__instance is None:
            print("Initializing flask with __name__=" + str(__name__))
            # FrancisFlask.__instance = object.__new__(cls)
            FrancisFlask.__instance = Flask(__name__)
            FrancisFlask.__instance.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://francisdb:nicebot99@francis-staging.c6yeo5k4ngoz.us-west-2.rds.amazonaws.com:6666/francisdb' # os.environ['FRANCIS_DB_URI']

        return FrancisFlask.__instance

# Place for AWS to send web requests
application = FrancisFlask()