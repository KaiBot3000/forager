"""Utility file to seed database with filtered and processed FUF data"""
from model import Plant, connect_to_db, db
from server import app

def load_trees():
	"""Loads FUF trees into Plants table"""
	print "I'm loading trees!"

	f = open("tree_data_fuf.csv")

	for line in f:
		split_line = line.split()

		print split_line

		0 = wkt
		1 = st address
		2 = lat 
		3 = lon 
		4 = scientific
		5 = common
		6 = spring
		7 = summ
		8 = fall
		9 = winter
		10 = tree_id

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


if __name__ == "__main__":
	connect_to_db(app)

	load_trees()
