from flask import Flask, render_template, flash, request, redirect, jsonify, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Plant, User, Review 
from jinja2 import StrictUndefined
import json
import geojson
import pprint


app=Flask(__name__)

app.secret_key = 'forage_the_things'


@app.route('/')
def index():

	return render_template('home.html')


@app.route('/sign')
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

	# get possible names (returned as list of one-entry tuples)
	names = db.session.query(Plant.plant_name).group_by(Plant.plant_name).all()
	names_formatted = []

	for name in names:
		names_formatted.append(name[0])

	sorted_names = sorted(names_formatted)

	return json.dumps(sorted_names)


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

	plant_dict = make_plant_dict(plant)

	return json.dumps(plant_dict)


@app.route('/plant-reviews')
def plant_reviews():
	'''Gets marker/plant id from js, returns html with review buttom and plant reviews.'''

	plant_id = request.args.get('marker')

	# Get ratings for that plant
	reviews = Review.query.filter_by(review_plant=plant_id).all()

	# Make them into dicionaries
	reviews_list = make_review_dict(reviews)

	return json.dumps(reviews_list)	


@app.route('/add-review', methods=['POST'])
def add_review():

	score = request.form['score']
	review = request.form['review']
	plant_id = request.form['marker']
	user_id = session['user_id']

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

		new_plant = Plant(name, species, description, category, season_list, lat, lon)

		if real:
			db.session.add(new_plant)
			db.session.commit()
			flash('Thanks for adding a %s.' % name)
		else:
			flash('Thanks for adding a fake %s.' % name)

		return render_template('add.html')


########## Helper functions

def make_review_dict(reviews):
	reviews_list = []
	for review in reviews:
		review_dict = {}
		user = User.query.filter_by(user_id=review.review_user).first()
		review_dict['username'] = user.username
		review_dict['score'] = review.review_score
		review_dict['description'] = review.review_description

		reviews_list.append(review_dict)
	return reviews_list

def make_plant_dict(plant):
	plant_dict = {}
	plant_dict['name'] = plant.plant_name
	plant_dict['species'] = plant.plant_species
	plant_dict['category'] = plant.plant_category
	plant_dict['description'] = plant.plant_description
	plant_dict['lat'] = plant.plant_lat
	plant_dict['lon'] = plant.plant_lon
	return plant_dict


if __name__ == "__main__":

	connect_to_db(app)

	app.run(debug=True)

	# DebugToolbarExtension(app)






