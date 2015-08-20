"""Models and database functions for Forager"""

import geojson

from flask_sqlalchemy import SQLAlchemy

# use sqla to access db
db = SQLAlchemy()

class Plant(db.Model):
	"""Plants in the database"""

	__tablename__ = 'plants'

	plant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	plant_species = db.Column(db.String(75))
	plant_name = db.Column(db.String(75))
	
	plant_category = db.Column(db.String(50))
	plant_description = db.Column(db.String(250))
	plant_owner = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	plant_private = db.Column(db.Boolean, default=False)

	plant_address = db.Column(db.String(100))
	plant_zipcode = db.Column(db.Integer)
	plant_location = db.Column(db.String(100))
	plant_lat = db.Column(db.Integer)
	plant_lon = db.Column(db.Integer)

	plant_spring = db.Column(db.Boolean, default=False)
	plant_summer = db.Column(db.Boolean, default=False)
	plant_fall = db.Column(db.Boolean, default=False)
	plant_winter = db.Column(db.Boolean, default=False)


	def __repr__(self):
		"""What to show when plant object printed"""

		return '<Plant id: %s, species: %s, location: %s, lat: %s, lon: %s>' % (self.plant_id, 
															self.plant_species, 
															self.plant_location,
															self.plant_lat,
															self.plant_lon)

	def wkt_to_lonlat(self):
		'''Converts wkt format coordinates to a latitude and longitude
			Takes plant object, reads its wkt, converts, and adds that to lat and lon fields. 
			Updates plant. Ot returns lonlat_list
		'''

		wkt = self.plant_location

			#wkt is 'POINT (xxxxxx xxxxxx)'
		wkt_initialtrim = wkt.replace('POINT (', '')
			#wkt is 'xxxxxx xxxxxx)'
		wkt_finaltrim = wkt_initialtrim.replace(')', '')
			#wkt is 'xxxxxx xxxxxx'
		lonlat_list = wkt_finaltrim.split(' ')
			# latlon_list = ['xxxxxx', 'xxxxxx']

		lon, lat = lonlat_list
		self.plant_lon = lon
		self.plant_lat = lat
		print "Latitude: %s" % lat
		print "Longitude: %s" % lon
		db.session.commit()

		# return lonlat_list

	def address_to_latlon(address):
		'''Converts wkt format coordinates to a latitude and longitude via api call'''
		# I'll need this if users want to add a plant by address

class User(db.Model):
	"""Forager registered users"""

	__tablename__ = 'users'

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	user_password = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		"""What to show when user object printed"""

		return '<User id:%s, username: %s>' % (self.user_id, self.username)


class Rating(db.Model):
	"""User Ratings for Plants"""

	__tablename__ = 'ratings'

	rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	rating_user = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	rating_plant = db.Column(db.Integer, db.ForeignKey('plants.plant_id'))
	rating_score = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		"""What to show when rating printed"""

		return '<%s rated plant %s a %s>' % (self.rating_user, 
											self.rating_plant, 
											self.rating_score)


# converts plant objects into geoJSON string for marker
class Marker():

	def __init__(self, lat, lon, plant_id, title, description, symbol):
		self.lat = lat
		self.lon = lon
		self.plant_id = plant_id
		self.title = title
		self.description = description
		self.symbol = symbol

	@property
	def __geo_interface__(self):
		
		return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': \
				[self.lon, self.lat]}, 'id': self.plant_id, 'properties': {'title': self.title, 'description': \
				self.description, 'marker-size': 'small', 'marker-symbol': self.symbol}}
 

def connect_to_db(app):
	"""Connects the db to flask app"""

	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forager.db'
	db.app = app
	db.init_app(app)


if __name__ == "__main__":

	from server import app
	connect_to_db(app)
	print "Connected to DB."