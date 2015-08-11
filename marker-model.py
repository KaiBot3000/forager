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
		# return '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [self.lat, self.lon]}, "properties": {"title": self.title, "description": self.description, "marker-size": "small", "marker-symbol": self.symbol}}'
		return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [self.lat, self.lon]}, 'properties': {'title': self.title, 'description': self.description, 'marker-size': 'small', 'marker-symbol': self.symbol}}







