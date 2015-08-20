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


@app.route('/map') # should combine this with /search?plants=all
def markers():

	marker_list = []

	plants = Plant.query.all()

	for plant in plants:
		marker = Marker(plant.plant_lat, plant.plant_lon, plant.plant_id, plant.plant_name, plant.plant_description, 'park2')
		marker_list.append(marker)

	marker_collection = geojson.FeatureCollection(marker_list)

	return render_template('map.html', marker_collection=marker_collection)

@app.route('/sign', methods=['GET'])
def sign():
	'''Show sign in/up form'''

	return render_template('sign.html')

@app.route('/signin', methods=['POST'])
def sign_in():
	'''Sign in registered users'''

	username = request.form['username']
	password = request.form['password']

	user = User.query.filter(username=username).first()

	if not user:
		flash('No such username! Please sign up or try again.')
		return redirect('sign.html')

	if user.password != password:
		flash('Wrong password for that username! Please sign up or try again.')
		return redirect('sign.html')

	session['user_id'] = user.user_id

	flash('Welcome back!')

	return render_template('map.html')

@app.route('/signup', methods=['POST'])
def sign_up():
	'''Sign up new users'''

	username = request.form['username']
	password1 = request.form['password1']
	password2 = request.form['password2']

	error = False

	user = User.query.filter(username=username).first()

	if user:
		flash('That username is taken! Please try again')
		error = True

	if password1 != password2:
		flash('Your passwords don\'t match! Please try again.')
		error = True

	if error:
		return redirect('sign.html')
	else:
		new_user = User(username=username, password=password1)
		db.session.add(new_user)
		db.commit

		flash('Welcome to Forager!')

		return render_template('map.html')


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

	plants = names + species

	# go through each and pull out of tuples
	plants_formatted = []

	for plant in plants:
		plants_formatted.append(plant[0])

	# sort alphabetically
	sorted_plants = sorted(plants_formatted)

	# make into json string, pass back
	return json.dumps(sorted_plants)


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/")

# pretty sure I can combine both log-in routes and just check methods
@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""


    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/search')
def search_plants():
	'''Takes search parameters, returns list of matching plants in geoJSON.
	(may be able to combine this route with original /map route?)'''

	# sample search string :/search?plants=all&category=FruitO&category=OtherT&season=Spring
	plants = request.args.getlist('plant')
	categories = request.args.getlist('category')
	seasons = request.args.getlist('season')

	# if no options selected, replace with list of all options possible

	if plants == ['all']:
		# print 'changing plants\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
		names = db.session.query(Plant.plant_name).group_by(Plant.plant_name).all()
		species = db.session.query(Plant.plant_species).group_by(Plant.plant_species).all()

		plants_tuples = names + species

		# go through each and pull out of tuples
		plants = []

		for plant in plants_tuples:
			plant_name = str(plant[0])
			plants.append(plant_name)

	# right now there are only 'tree's in db
	if categories == []:
		categories = ['FruitO', 'FruitT', 'OtherT', 'Herb', 'Vegetable', 'tree']

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

	##### Check things!
	# print 'plants is: %s' % plants
	# print type(plants[0])
	# print type(plants)
	# print 'categories is: %s' % categories
	# print 'seasons is: %s' % seasons
	# print 'spring is: %s' % spring
	# print 'summer is: %s' % summer
	# print 'fall is: %s' % fall
	# print 'winter is: %s' % winter

	marker_list = []

	# query for new plants
	plant_objects = Plant.query.filter((Plant.plant_name.in_(plants)) | (Plant.plant_species.in_(plants))) \
						.filter(Plant.plant_category.in_(categories)) \
						.filter(Plant.plant_spring.in_(spring)) \
						.filter(Plant.plant_summer.in_(summer)) \
						.filter(Plant.plant_fall.in_(fall)) \
						.filter(Plant.plant_winter.in_(winter))

	# plants = Plant.query.all()

	for plant in plant_objects:
		marker = Marker(plant.plant_lat, plant.plant_lon, plant.plant_id, plant.plant_name, plant.plant_description, 'park2')
		marker_list.append(marker)

	marker_collection = geojson.FeatureCollection(marker_list)

	return render_template('map.html', marker_collection=marker_collection)	


if __name__ == "__main__":

	connect_to_db(app)

	app.run(debug=True)

	DebugToolbarExtension(app)



### Graveyard ###

	# I thought about passing plants back this way, but opted to just send markers
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
