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
	palatable = db.Column(db.Integer)
	fruit_period = db.Column(db.String(100))


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fuf_trees.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

