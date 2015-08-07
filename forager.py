from flask import Flask, render_template, flash, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Plant, User, Rating

app=Flask(__name__)

app.secret_key = 'forage_the_things'


@app.route('/')
def index_page():

	return render_template('home-forager.html')

@app.route('/map')
def markers():
		# get plant objects
		# pass plant objects

	return render_template('map-play.html') #and plant objects



if __name__ == "__main__":
	app.run(debug=True)