def wkt_to_latlon(plant):
	'''Converts wkt format coordinates to a latitude and longitude
		Takes plant object, reads its wkt, converts, and adds that to lat and lon fields. 
		Returns updated object.
	'''
	wkt = plant # test line- feed it a location string directly
	#wkt = plant['location']

	#wkt is 'POINT (xxxxxx xxxxxx)'
	wkt_trim = wkt.replace('POINT (', '')
	#wkt is 'xxxxxx xxxxxx)'
	wkt_final = wkt_trim.replace(')', '')
	#wkt is 'xxxxxx xxxxxx'
	latlon_list = wkt_final.split(' ')
	# latlon_list = ['xxxxxx', 'xxxxxx']
	lat, lon = latlon_list
	print "Latitude: %s" % lat
	print "Longitude: %s" % lon


point = 'POINT (123 -456.00)'

wkt_to_latlon(point)

































# import geojson
# from model import connect_to_db, db, Plant, User, Rating

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


# # Connects to database w/ engine
# engine = create_engine('sqlite:///forager.db', echo=True)

# # bind session to engine
# Session = sessionmaker(bind=engine)

# # start a new session
# session = Session()





# TEST ZONE

# connect to db (must be a better way to do this)


# Test the things








# if __name__ == "__main__":


#     db_connection.close()