"""Utility file to seed database with filtered and processed FUF data"""
from model import Plant, connect_to_db, db
from server import app

def load_trees():
	"""Loads edited plants into Plants table"""
	print "I'm loading trees!"

	f = open('tree_data_fuf.csv')

	# I tried to do 'for line in f, split line' but it wasn't splitting correctly.
	# TODO - fix this mess.
	line_list = list(f)[0].split('\r')
	for line in line_list:
		split_line = line.split(',')

		print split_line
		print '\n\n'

		if split_line[5] == '':
			new_tree = Plant(plant_species=split_line[1],
				plant_name=split_line[2],
				plant_category="tree",
				plant_address=split_line[3],
				plant_location=split_line[4],
				plant_spring=split_line[7],
				plant_summer=split_line[8],
				plant_fall=split_line[9],
				plant_winter=split_line[10])
		else:
			new_tree = Plant(plant_species=split_line[1],
							plant_name=split_line[2],
							plant_category="tree",
							plant_address=split_line[3],
							plant_location=split_line[4],
							plant_lat=split_line[5],
							plant_lon=split_line[6],
							plant_spring=split_line[7],
							plant_summer=split_line[8],
							plant_fall=split_line[9],
							plant_winter=split_line[10])

		db.session.add(new_tree)

	db.session.commit()

def load_plants():
	"""Loads edited plants into Plants table"""
	print "I'm loading plants!"

	f = open('plants_tab.txt')

	line_list = list(f)[0].split('\r')
	for line in line_list:
		split_line = line.strip().split('\t')

		print split_line
		print '\n'

		index = 0;
		for item in split_line:
			print "%s: %s" % (index, item)
			index += 1

		print '\n\n'

		new_tree = Plant(plant_species=split_line[0],
			plant_name=split_line[1],
			plant_category=split_line[2],
			plant_description=split_line[3],

			plant_address=split_line[6],
			plant_location=split_line[8],
			plant_lat=split_line[9],
			plant_lon=split_line[10],

			plant_spring=split_line[11],
			plant_summer=split_line[12],
			plant_fall=split_line[13],
			plant_winter=split_line[14])

		db.session.add(new_tree)

	# new_tree = Plant(plant_species='fred',
	# 	plant_name='apple',
	# 	plant_category='alien',
	# 	plant_description='from mars',

	# 	plant_address='123 fred st',
	# 	plant_location='fence',
	# 	plant_lat=23.88,
	# 	plant_lon=45.77,

	# 	plant_spring=1,
	# 	plant_summer=1,
	# 	plant_fall=1,
	# 	plant_winter=1)

	# db.session.add(new_tree)

	db.session.commit()



if __name__ == "__main__":
	connect_to_db(app)

	load_plants()
