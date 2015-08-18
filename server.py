from flask import Flask, render_template, flash, request, redirect, jsonify, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Plant, User, Rating, Marker
from jinja2 import StrictUndefined
import json
import geojson
import pprint

app=Flask(__name__)

app.secret_key = 'forage_the_things'


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

	return render_template('map.html', marker_collection=marker_collection)


@app.route('/plant-detail')
def plant_details():
	'''Gets marker/plant id from js, returns proper plant object.'''

	plant_id = request.args.get('marker')
	print plant_id
	plant = Plant.query.get(plant_id)

	# need to make desired plant attributes into dictionary, then JSONify dict and pass it.
	# OR, pass completed html. Yes.
	# Passing the object itself will result in errors because it came from SQLAlchemy and has methods attached.

	# Make series of if functions for attributes, appending new html onto string for each existing attr.
	detail_html = '<div class="header"><b> %s <i> (%s)</i></b></div> <br> <p><b>Address:</b> %s <p class="description"> <b> Description:</b> %s </p> <p><b>Category:</b> %s' % (plant.plant_name, 
		plant.plant_species, 
		plant.plant_address, 
		plant.plant_description, 
		plant.plant_category)

	return detail_html


@app.route('/list-fields')
def list_fields():
	'''Returns dictionary with list of possible fields for plant names and species.'''

	# get possible names and species (returned as list of one-entry tuples)
	names = db.session.query(Plant.plant_name).group_by(Plant.plant_name).all()
	species = db.session.query(Plant.plant_species).group_by(Plant.plant_species).all()

	# names_list = []

	# for name in names:
	# 	names_list.append(name[0])

	# print names_list

	# return json.dumps(names_list)

	# combine
	plants = names + species

	# go through each and pull out of tuples
	plants_formatted = []

	for plant in plants:
		plants_formatted.append(plant[0])

	# sort alphabetically
	sorted_plants = sorted(plants_formatted)

	# make into json string, pass back
	return json.dumps(sorted_plants)


if __name__ == "__main__":

	connect_to_db(app)

	app.run(debug=True)

	DebugToolbarExtension(app)



### Graveyard ###

	# plant_dict = {
	# 	'id' :plant.plant_id,
	# 	'species': plant.plant_species,
	# 	'name': plant.plant_name,
		
	# 	'category': plant.plant_category,
	# 	'description': plant.plant_description,
	# 	'owner': plant.plant_owner,
	# 	'private': plant.plant_private,

	# 	'address': plant.plant_address,
	# 	'zipcode': plant.plant_zipcode,
	# 	'location': plant.plant_location,
	# 	'lat': plant.plant_lat,
	# 	'lon': plant.plant_lon,

	# 	'spring': plant.plant_spring,
	# 	'summer': plant.plant_summer,
	# 	'fall': plant.plant_fall,
	# 	'winter': plant.plant_winter
	# }
		# return jsonify(plant_dict)
