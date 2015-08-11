from flask import Flask, render_template, flash, request, redirect, jsonify, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Plant, User, Rating, Marker
from jinja2 import StrictUndefined
import geojson

app=Flask(__name__)

app.secret_key = 'forage_the_things'

# Query database
# convert results to markers via Marker class
# collect markers in feature collection via geojson
# pass feature collection to map



@app.route('/')
def index_page():

	return render_template('home-forager.html')

@app.route('/map')
def markers():

	marker_list = []

	for id in range(2):
		plant = Plant.query.get(id)
		marker = Marker(-10, 30, plant.plant_name, plant.plant_description, 'park2')
		marker_list.append(marker)

	marker_collection = geojson.FeatureCollection(marker_list)
	print marker_collection	

	# new_marker = Marker(-122.411227, 37.772849, 'plant', 'plant from marker class!', 'park2')
	# plant = geojson.dumps(new_marker, sort_keys=True)

	return render_template('marker-play.html', marker_collection=marker_collection)


if __name__ == "__main__":

	connect_to_db(app)

	app.run(debug=True)

	DebugToolbarExtension(app)
