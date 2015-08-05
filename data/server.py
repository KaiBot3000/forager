
"""Data Importer."""

from flask import Flask, session

from fuf_model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"




if __name__ == "__main__":
	
    connect_to_db(app)
    app.run()