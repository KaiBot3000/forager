"""Models for seeding the db from FUF"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions


class Tree(db.Model):
	"""Trees!"""

	__tablename__ = 'trees'

	tree_id = db.Column(db.Integer, primary_key=True)
	tree_species_id = db.Column(db.Integer, db.ForeignKey("species.species_id"))
	tree_plot_id = db.Column(db.Integer, db.ForeignKey("plots.plot_id"))


class Plot(db.Model):
	"""Plots!"""

	__tablename__ = 'plots'

	plot_id = db.Column(db.Integer, primary_key=True)
	wkt = db.Column(db.String(100))
	address_street = db.Column(db.String(100))
	address_geocoded = db.Column(db.String(100))
	lat_geocoded = db.Column(db.Integer)
	lon_geocoded = db.Column(db.Integer)


class Specie(db.Model):
	"""Species!"""

	__tablename__ = 'species'

	species_id = db.Column(db.Integer, primary_key=True)
	scientific_name = db.Column(db.String(100))
	common_name = db.Column(db.String(100))
	fruit_period = db.Column(db.String(100))


