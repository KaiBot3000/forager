"""Models and database functions for Forager"""

# import sqla
from flask_sqlalchemy import SQLAlchemy

# use sqla to access db
db = SQLAlchemy()

class Plant(db.Model):
	"""Plants in the database"""

	# how we refer to the table
	__tablename__ = 'plants'

	# Make plant_id a column, that's a pk number which autoincrements
	plant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	plant_species = db.Column(db.String(75), nullable=False)
	# may need to make nullable so I can *get* the lat/long when address entered
	plant_lat = db.Column(db.Integer, nullable=False)
	plant_long = db.Column(db.Integer, nullable=False)
	plant_category = db.Column(db.String(50))
	plant_zipcode = db.Column(db.Integer)
	# not sure the boolean will work
	plant_private = db.Column(db.Boolean, default=False)
	plant_address = db.Column(db.String(100))
	plant_description = db.Column(db.String(250))
	plant_owner = db.Column(db.Integer, db.ForeignKey('users.user_id'))

	def __repr__(self):
		"""What to show when plant object printed"""

		return '<Plant id: %s, species: %s, zipcode: %s>' % (self.plant_id, 
															self.plant_species, 
															self.plant_zipcode)


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

class Season(db.Model):
	"""Seasons a plant is edible"""

	__tablename__ = 'seasons'

	