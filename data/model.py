"""Models and database functions for Forager"""

# import sqla
from flask_sqlalchemy import SQLAlchemy

# use sqla to access db
db = SQLAlchemy()

class Plant(db.Model):
	"""Plants in the database"""
	# Planning on putting seasons in plant, as a boolean. Also, rework lat/long to be string coded correctly?

	# how we refer to the table
	__tablename__ = 'plants'

	# Make plant_id a column, that's a pk number which autoincrements
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
	plant_autumn = db.Column(db.Boolean, default=False)


	def __repr__(self):
		"""What to show when plant object printed"""

		return '<Plant id: %s, species: %s, location: %s>' % (self.plant_id, 
															self.plant_species, 
															self.location)


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

# class Season(db.Model):
# 	"""Seasons a plant can have"""

# 	__tablename__ = 'seasons'

# 	season_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
# 	season_name = db.Column(db.String(10), nullable=False, unique=True)

# 	def __repr__(self):
# 	"""What to show when season printed"""

# 		return '<%s, aka %s>' % (self.season_id, self.season_name)

# class Edible_time(db.Model):
# 	"""Matches plants and seasons"""

# 	__tablename__ = 'edible_times' 

# 	edible_time_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
# 	edible_plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'))
# 	edible_season_id = db.Column(db.Integer, db.ForeignKey('season.season_id'))

# 	def __repr__(self):
# 	"""What to show when edible_time object printed"""

# 		return '<%s is ripe in %s>' % (self.edible_plant_id, self.edible_season_id)

