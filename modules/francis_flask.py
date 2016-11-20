import os
from flask import Flask

# Flask singleton
class FrancisFlask():

    # Singleton instance.
    __instance = None

    # Instantiation creates/returns the singleton instance.
    def __new__(cls):

        if FrancisFlask.__instance is None:
            # print("Initializing flask with __name__=" + str(__name__))
            # print("Initializing flask with __name__=" + str("__main__"))
            # FrancisFlask.__instance = object.__new__(cls)
            # FrancisFlask.__instance = Flask(__name__)
            # print("jl package name:")
            # print(__name__.split('.')[0])
            # print("-------------")
            FrancisFlask.__instance = Flask("modules.francis_flask")
            FrancisFlask.__instance.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FRANCIS_DB_URI']

        return FrancisFlask.__instance

# Place for AWS to send web requests
application = FrancisFlask()