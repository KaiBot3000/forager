from flask import Flask, render_template, flash, request, redirect, jsonify, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Plant, User, Rating
from jinja2 import StrictUndefined
import geoconvert
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
		# changed reference for class, not toally sure it still works
		marker = geoconvert.Marker(-10, 30, plant.plant_name, plant.plant_description, 'park2')
		marker_list.append(marker)

	marker_collection = geojson.FeatureCollection(marker_list)
	print marker_collection	
	# new_marker = Marker(-122.411227, 37.772849, 'plant', 'plant from marker class!', 'park2')

	# plant = geojson.dumps(new_marker, sort_keys=True)


	return render_template('marker-play.html', plant=plant)


# converts plant objects into geoJSON string for marker
class Marker():

	def __init__(self, lat, lon, title, description, symbol):
		self.lat = lat
		self.lon = lon
		self.title = title
		self.description = description
		self.symbol = symbol

	@property
	def __geo_interface__(self):
		# return '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [self.lat, self.lon]}, "properties": {"title": self.title, "description": self.description, "marker-size": "small", "marker-symbol": self.symbol}}'
		return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': \
				[self.lat, self.lon]}, 'properties': {'title': self.title, 'description': \
				self.description, 'marker-size': 'small', 'marker-symbol': self.symbol}}
 


if __name__ == "__main__":

	connect_to_db(app)

	app.run(debug=True)

	DebugToolbarExtension(app)

