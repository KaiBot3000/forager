from flask import Flask, render_template, flash, request
from flask_debugtoolbar import DebugToolbarExtension

app=Flask(__name__)

app.secret_key = 'forage_the_things'


@app.route('/')
def index_page():

	return render_template('forager-home.html')





if __name__ == "__main__":
	app.run(debug=True)