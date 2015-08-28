from flask import Flask, render_template, flash, request, redirect, jsonify, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Plant, User, Review #, Marker
from jinja2 import StrictUndefined
import json
import geojson
import pprint

# import requests - makes it much easier to format requests for external api's
# usaddress for getting addresses geocoded properly

app=Flask(__name__)

app.secret_key = 'forage_the_things'


@app.route('/')
def index_page():


	return render_template('home.html')


# @app.route('/modal')
# def modal():

# 	return render_template('modal.html')

def fun_test(a, b):
	'''
	>>> fun_test(2, 3)
	5

	>>> fun_test(-1, 0)
	-1
	'''
	return (a + b)



@app.route('/sign', methods=['GET'])
def sign():
	'''Show sign in/up form'''

	return render_template('sign.html')


@app.route('/signin', methods=['POST'])
def sign_in():
	'''Sign in registered users'''

	username = request.form['username']
	password = request.form['password']

	user = User.query.filter_by(username=username).first()

	if not user:
		flash('No such username! Please sign up or try again.')
		return redirect('/sign')

	if user.user_password != password:
		flash('Wrong password for that username! Please sign up or try again.')
		return redirect('/sign')

	session['user_id'] = user.user_id

	flash('Welcome back, %s!' % username)

	return redirect('/search')


@app.route('/signup', methods=['POST'])
def sign_up():
	'''Sign up new users'''

	username = request.form['username']
	password1 = request.form['password1']
	password2 = request.form['password2']

	error = False

	user = User.query.filter_by(username=username).first()

	if user:
		flash('That username is taken! Please try again')
		error = True

	if password1 != password2:
		flash('Your passwords don\'t match! Please try again.')
		error = True

	if error:
		return redirect('/sign')
	else:
		new_user = User(username=username, user_password=password1)
		db.session.add(new_user)
		db.session.commit()

		session['user_id'] = user.user_id

		flash('Welcome to Forager, %s!' % username)

		return redirect('/search')


@app.route('/signout')
def signout():
    '''Sign out.'''

    if 'user_id' in session:
    	del session['user_id']
    	flash('Signed Out.')
    	return redirect('/')
    else:
    	flash('You need to sign in first')
    	return redirect('/sign')


@app.route('/list-fields')
def list_fields():
	'''Returns dictionary with list of possible fields for plant names and species.'''

	# get possible names and species (returned as list of one-entry tuples)
	names = db.session.query(Plant.plant_name).group_by(Plant.plant_name).all()
	#species = db.session.query(Plant.plant_species).group_by(Plant.plant_species).all()

	plants = names #+ species

	# go through each and pull out of tuples
	plants_formatted = []

	for plant in plants:
		plants_formatted.append(plant[0])

	# sort alphabetically
	sorted_plants = sorted(plants_formatted)

	# make into json string, pass back
	return json.dumps(sorted_plants)


@app.route('/search')
def search_display():
	'''Displays initial search screen populated with markers'''
	
	marker_list = []

	plant_objects = Plant.query.all()

	for plant in plant_objects:
		marker = plant.make_marker()
		marker_list.append(marker)

	marker_collection = geojson.FeatureCollection(marker_list)

	return render_template('search.html', marker_collection=marker_collection)


@app.route('/search-plants.json')
def search_plants():
	'''Takes search parameters, returns list of matching plants in geoJSON.'''

	marker_list = []

	# sample search string :/search?plant=all&category=FruitO&category=OtherT&season=Spring
	plants = request.args.getlist('plant')
	categories = request.args.getlist('category')
	seasons = request.args.getlist('season')

	# if no options selected, replace with list of all options possible
	if plants == ['all']:
		names = db.session.query(Plant.plant_name).group_by(Plant.plant_name).all()
		species = db.session.query(Plant.plant_species).group_by(Plant.plant_species).all()

		plants_tuples = names + species

		# go through each and pull out of tuples
		plants = []

		for plant in plants_tuples:
			plant_name = str(plant[0])
			plants.append(plant_name)

	if categories == []:
		categories = ['fruit', 'nut', 'herb', 'vegetable']

	# Initialize defaults for seasons
	spring = [0, 1]
	summer = [0, 1]
	fall = [0, 1]
	winter = [0, 1]

	if seasons is not []:
		if 'Spring' in seasons:
			spring = [1]
		if 'Summer' in seasons:
			summer = [1]
		if 'Fall' in seasons:
			fall = [1]
		if 'Winter' in seasons:
			winter = [1]

	# query for new plants
	plant_objects = Plant.query.filter((Plant.plant_name.in_(plants)) | (Plant.plant_species.in_(plants))) \
						.filter(Plant.plant_category.in_(categories)) \
						.filter(Plant.plant_spring.in_(spring)) \
						.filter(Plant.plant_summer.in_(summer)) \
						.filter(Plant.plant_fall.in_(fall)) \
						.filter(Plant.plant_winter.in_(winter))

	for plant in plant_objects:
		marker = plant.make_marker()
		marker_list.append(marker)

	marker_collection = geojson.FeatureCollection(marker_list)
	return jsonify(marker_collection)

@app.route('/plant-detail')
def plant_details():
	'''Gets marker/plant id from js, returns html with plant details.'''

	plant_id = request.args.get('marker')
	print plant_id
	plant = Plant.query.get(plant_id)

	# need to make desired plant attributes into dictionary, then JSONify dict and pass it.
	# OR, pass completed html. Yes.
	# Passing the object itself will result in errors because it came from SQLAlchemy and has methods attached?

	# # Make series of if functions for attributes, appending new html onto string for each existing attr.
	# detail_html = '<div class="header"><b> %s <i> (%s)</i></b></div> <br> <p><b>Address:</b> %s <p class="description"> <b> Description:</b> %s </p> <p><b>Category:</b> %s' % (plant.plant_name, 
	# 	plant.plant_species, 
	# 	plant.plant_address, 
	# 	plant.plant_description, 
	# 	plant.plant_category)

	# return detail_html	

	plant_dict = {}
	plant_dict['name'] = plant.plant_name
	plant_dict['species'] = plant.plant_species
	plant_dict['category'] = plant.plant_category
	plant_dict['description'] = plant.plant_description
	plant_dict['lat'] = plant.plant_lat
	plant_dict['lon'] = plant.plant_lon

	return json.dumps(plant_dict)


@app.route('/plant-reviews')
def plant_reviews():
	'''Gets marker/plant id from js, returns html with review buttom and plant reviews.'''

	plant_id = request.args.get('marker')

	# Get ratings for that plant
	reviews = Review.query.filter_by(review_plant=plant_id).all()

	########## Could be a seperate function
	reviews_list = []
	for review in reviews:
		review_dict = {}
		user = User.query.filter_by(user_id=review.review_user).first()
		review_dict['username'] = user.username
		review_dict['score'] = review.review_score
		review_dict['description'] = review.review_description

		reviews_list.append(review_dict)

	return json.dumps(reviews_list)	


@app.route('/add-review', methods=['POST'])
def add_review():

	score = request.form['score']
	review = request.form['review']
	plant_id = request.form['marker']
	user_id = session['user_id']

	# user, plant, score, description
	new_review = Review(review_user=user_id, 
						review_plant=plant_id, 
						review_score=score, 
						review_description=review)

	db.session.add(new_review)
	db.session.commit()
	# flash('Thanks for reviewing plant %s' % plant_id)

	return 'review added!'


# TODO this should be add-plant, to avoid confusion wth reviews
@app.route('/add', methods=['GET', 'POST'])
def add():
	'''Gets form information, adds plant to db'''

	if request.method == 'GET':
		return render_template('add.html')
	else:
		name = request.form['name']
		species = request.form['species']
		description = request.form['description']
		category = request.form['category']
		season_list = request.form.getlist('seasons')
		lat = request.form['formLat']
		lon = request.form['formLon']
		real = request.form.get('real')

		def make_plant_from_form(name, species, description, category, season_list, lat, lon):
			spring_string = 'spring'
			summer_string = 'summer'
			fall_string = 'fall'
			winter_string = 'winter'

			if spring_string in season_list:
				spring = True
			else:
				spring = False

			if summer_string in season_list:
				summer = True
			else:
				summer = False
			
			if fall_string in season_list:
				fall = True
			else:
				fall = False

			if winter_string in season_list:
				winter = True
			else:
				winter = False		

			# print '%s, %s, %s, %s, %s, %s, %s' % (name, species, description, category, spring, lat, lon)

			new_plant = Plant(name=name,
							species=species,
							description=description,
							category=category,
							spring=spring,
							summer=summer,
							fall=fall,
							winter=winter,
							lat=lat,
							lon=lon)
			return new_plant

		new_plant = make_plant_from_form(name, species, description, category, season_list, lat, lon)
		print new_plant

		if real:
			db.session.add(new_plant)
			db.session.commit()
			flash('Thanks for adding a %s.' % name)
		else:
			flash('Thanks for adding a fake %s.' % name)

		return render_template('add.html')

import unittest
import doctest
import server

# Also runs docTests in file
# def load_tests(loader, tests, ignore):
#     """Also run our doctests and file-based doctests."""

#     tests.addTests(doctest.DocTestSuite(server))
#     tests.addTests(doctest.DocFileSuite("tests.txt"))
#     return tests

class ForagerUnitTestCase(unittest.TestCase):

    def test_fun_test(self):
        self.assertEqual(fun_test(1, -1), 0)


if __name__ == "__main__":

	connect_to_db(app)

	app.run(debug=True)

	DebugToolbarExtension(app)

	unittest.main()


