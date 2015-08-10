from flask import Flask, render_template, flash, request, redirect, jsonify, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Plant, User, Rating, Marker

app=Flask(__name__)

app.secret_key = 'forage_the_things'


@app.route('/')
def index_page():

	return render_template('home-forager.html')

@app.route('/map')
def markers():
	# get plant objects
	# plants = Plant.query.all()

	# plants = Plant.query.get(1)
	# print "got plants!"
	# print plants


	return render_template('marker-play.html')



if __name__ == "__main__":

	connect_to_db(app)

	app.run(debug=True)

	connect_to_db(app)

	DebugToolbarExtension(app)
