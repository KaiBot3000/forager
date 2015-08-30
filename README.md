![image](/static/images/screenshot-map.png)
# Forager

Need a few sprigs of rosemary for your recipe? It doesn't get more local than just around the corner. Forager allows users to locate food plants growing in their area, fostering a sense of connection to their urban environment. Users can seach from thousands of plants pulled from a San Francisco plant census, and search by criteria such as harvest season. They can then...
  - View plants on an interactive map
  - Review plants to help other users find what they need
  - Add new plants

### The Stack
* [SQLite] - Database contains thousands of plants, users, and plant reviews
* [SQLAlchemy] - Streamlines database queries
* [Python] - Backend code that manipulates incoming data, controls access to the database, and serves data to the webpage through a framework.
* [Flask] - Lightweight web framework which also provides support for jinja templating and unittests
* [Javascript] - Frontend code which allows for dynamic webpages
* [jQuery] - Creates event handlers for user interation
* [AJAX] - Gets information from server without reloading the page, allowing for more dynamic pages and faster loading times
* [Leaflet/Mapbox API] - Uses geoJSON passed from the server to create dynamic plant maps, and reverse geocoding to translate coordinates to the nearest addresses.
* [HTML] - Displays information
* [CSS] - Styles webpages
* [Twitter Bootstrap] - Frontend UI framework for quick styling

### The Data
Forager is seeded with data from the 2012 San Francisco tree census,  a project led by Friends of the Urban Forest (http://www.fuf.net/) and the Davey Research Group.

### Installation

Clone repo:
```sh
$ git clone [git-repo-url] forager
$ cd forager
```

Install dependencies:
```sh
$ pip install -r requirements.txt
```

Run Forager server:
```sh
$ python server.py
```

