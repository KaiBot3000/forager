import geojson


class Marker():

	def __init__(self, lat, lon, title, description, symbol):
		self.lat = lat
		self.lon = lon
		self.title = title
		self.description = description
		self.symbol = symbol
	@property
	def __geo_interface__(self):
		return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [self.lat, self.lon]}, 'properties': {'title': self.title, 'description': self.description, 'marker-size': 'small', 'marker-symbol': self.symbol}}

print 'making new marker class object!'

new_marker = Marker(37.772849, -122.411227, 'plant', 'plant from marker class!', 'park2')
print 'marker object'
print new_marker
print 'printing marker!'
print geojson.dumps(new_marker, sort_keys=True)