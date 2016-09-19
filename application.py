import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from db import Person

# from flask_sqlalchemy import SQLAlchemy
# from db import Person
# App instance
application = Flask(__name__)
app = application

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FRANCIS_DB_URI']

db = SQLAlchemy(app)


@app.route("/") # take note of this decorator syntax, it's a common pattern
def hello():

	output_html = 'hello world'

	# persons = Person.query.order_by(Person.email).all()
	
	# for person in persons:
	# 	output_html += '<div>' + person.email + '</div>'

	return output_html

if __name__ == "__main__":
    app.run()