from flask import Flask, render_template, flash, request, redirect, jsonify, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Plant, User, Rating, Marker
from jinja2 import StrictUndefined
import geojson
import pprint

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

	plants = Plant.query.all()
	for plant in plants:
		marker = Marker(plant.plant_lat, plant.plant_lon, plant.plant_id, plant.plant_name, plant.plant_description, 'park2')
		marker_list.append(marker)

	marker_collection = geojson.FeatureCollection(marker_list)

	# new_marker = Marker(-122.411227, 37.772849, 'plant', 'plant from marker class!', 'park2')
	# plant = geojson.dumps(new_marker, sort_keys=True)

	return render_template('detail-play.html', marker_collection=marker_collection)

@app.route('/plant-detail')
def plant_details():
	'''Gets marker/plant id from js, returns proper plant object.'''
	# plant = Plant.query.get(plant_id)

	plant_id = request.args.get('marker')

	print 'In the server route. \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'

	print plant_id

	plant = Plant.query.get(plant_id)
	# need to make desired plant attributes into dictionary, then JSONify dict and pass it.
	# OR, pass completed html. Yes.
	# Passing the object itself will result in errors because it came from SQLAlchemy and has methods attached.

	plant_dict = {
		'id' :plant.plant_id,
		'species': plant.plant_species,
		'name': plant.plant_name,
		
		'category': plant.plant_category,
		'description': plant.plant_description,
		'owner': plant.plant_owner,
		'private': plant.plant_private,

		'address': plant.plant_address,
		'zipcode': plant.plant_zipcode,
		'location': plant.plant_location,
		'lat': plant.plant_lat,
		'lon': plant.plant_lon,

		'spring': plant.plant_spring,
		'summer': plant.plant_summer,
		'fall': plant.plant_fall,
		'winter': plant.plant_winter
	}

	# return jsonify(plant_dict)
	return '<b> Hey, this came from the server! </b>'
	# 'plant id is: %s' % plant_id # JSON plant object for jinja to eat, or just needed info



if __name__ == "__main__":

	connect_to_db(app)

	app.run(debug=True)

	DebugToolbarExtension(app)
