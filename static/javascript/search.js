var marker;
var REVIEW_LEAF_SIZE = 32;


// hide details until plant clicked
function setStartState() {
	// won't let me hide div or delete all the html ...?
	$('#detailsDiv').html(' ');
	// $('#detailsdiv').hide();
	$('#reviewDiv').hide();
	$('#reviewList').empty();
}

setStartState();

// ########## set up search drop-down
dropList = []

$.get('/list-fields', function (results) {
		dropList = JSON.parse(results);
		var dropdown = document.getElementById('plantDropdown');

		for(var i = 0; i < dropList.length; i++) {
			var opt = document.createElement('option');
			opt.innerHTML = dropList[i];
			opt.value = dropList[i];
			dropdown.appendChild(opt);
		}
});

// ########## Search without reloading the page

$('#searchBtn').on('click', function (evt){
	evt.preventDefault();
	alert("A");
	var url = '/search-plants.json?' + $('#searchForm').serialize();
	$.get(url, function (results) {
		markerCollection = results;
		makeMap(mapLocation, markerCollection);
	})	
});	

// ########## Showing Plant info

// When clicked, use marker (need to id from map because button doesn't exist onload)
$('#map').on('click', '.detailsBtn', seeNote);

function seeNote() {

	// get dict of plant details, reverse geocode for address
	$.get('/plant-detail', {'marker': marker}, function (results) {
		var plant = JSON.parse(results); //dict, now object
		var plantLat = plant['lat'];
		var plantLon = plant['lon'];
		var detailHtml;
		var accessToken = 'pk.eyJ1IjoicmlzZWxpa2V0aGVtb29uIiwiYSI6IjI4MjczOTIwNzE5MTY1ODI4YmYxZGVlZGZmYjc4NmI0In0.fiUOgIDwB_ByzxT63VWP-g'

		var geoUrl = 'https://api.mapbox.com/v4/geocode/mapbox.places/'+ plantLon + ',' + plantLat + '.json?access_token=' + accessToken;

		// reverse geocode the address
		$.get(geoUrl, function (results){
			var geo = results;
			address = geo['features'][0]['place_name'];
			console.log(address);
		
			detailHtml = '<p id="plantName">' + plant['name'] + '</p>' + 
							'<p id="plantSpecies">' + plant['species'] + '</p>' + 
							'<p id="plantAddress">Nearest Address: ' + address + '</p>' +  
							'<p id="plantCategory">' + plant['category'] + '</p>' + 
							'<p id="plantDescription">' + plant['description'] + '</p>';

				//display new html in detail div
			$('#detailsDiv').html(detailHtml);

			//make div visible
			$('#detailsDiv').show();
		});
	});

	// get and show reviews
	$.get('/plant-reviews', {'marker': marker}, function (results) {
		// clear any leftover reviews
		$('#reviewList').empty();

		reviews = JSON.parse(results);

		// Grab elements
		var reviewBox = document.getElementById('reviewDiv');
		var reviewUL = document.getElementById('reviewList');

		// cycle through reviews in list
		for(var i = 0; i < reviews.length; i++) {
			var review = reviews[i];
			var reviewSpot = document.createElement('li');

			reviewSpot.innerHTML = '<b>From ' + review['username'] + ':</b><br><span class="leaves">'
									 + review['score'] + '</span>' + '<br>' 
									 + review['description'] + '<br><br><br>';

			// add the review to the html list
			reviewUL.appendChild(reviewSpot);
		}
		// make leaves to illustrate score
		$(function() {
		    $('span.leaves').leaves();
		});

		// show reviews div
		reviewBox.show();

	});
};

// ########### display stars/leaves for reviews
// jQuery method to display leaves based on score in html
$.fn.leaves = function() {
    return $(this).each(function() {
        // Get the score from the html
        var score = parseFloat($(this).html())
        // set width of displayed stars based on score and leaf width
        var leaves = score * REVIEW_LEAF_SIZE;
        // Create stars holder
        var $span = $('<span />').width(leaves).height(REVIEW_LEAF_SIZE);
        // Replace the numerical value with stars
        $(this).html($span);
    });
}

// ########## Handle Add Reviews Events

$('#reviewBtn').on('click', addReview);

$('#cancelBtn').on('click', clearForm);

function addReview(evt) {
	evt.preventDefault();

	review_score = addReviewForm.elements['score'].value;
	review_description = addReviewForm.elements['review'].value;

	// use that url to get info
	$.post('/add-review', {'score': review_score, 'review': review_description, 'marker': marker}, function (results) {
		seeNote();
	});
};

function clearForm() {
	$('#addReviewForm').trigger('reset');
}




// var centerLat = 37.75768707689704;
// var centerLon = -122.44279861450195;
// var mapLocation = [centerLat, centerLon]; 

// var southWest = L.latLng(37.7, -122.541);
// var northEast = L.latLng(37.815, -122.335);
// var bounds = L.latLngBounds(southWest, northEast);

// var markerCollection = {{ marker_collection | safe }};

// var mapZoom = 12; //12 is ideal for showing SF, 15 shows markers for testing
// var maxClusterZoom = 16; // When I want clustering to end

// // this is public on purpose
// L.mapbox.accessToken = 'pk.eyJ1IjoicmlzZWxpa2V0aGVtb29uIiwiYSI6IjI4MjczOTIwNzE5MTY1ODI4YmYxZGVlZGZmYjc4NmI0In0.fiUOgIDwB_ByzxT63VWP-g';

// var map = L.mapbox.map('map', 'riselikethemoon.4b711c00', {maxBounds: bounds, minZoom: mapZoom})
// 	.setView(mapLocation, mapZoom) 
// 	.addLayer(L.mapbox.tileLayer('riselikethemoon.4b711c00'))
//     .fitBounds(bounds)

function makeMap(mapLocation, markerCollection) {
	// clear old map
	map.remove();

	// draw new map	
	map = L.mapbox.map('map', 'riselikethemoon.4b711c00', {maxBounds: bounds, minZoom: mapZoom})
		.setView(mapLocation, mapZoom) 
		.addLayer(L.mapbox.tileLayer('riselikethemoon.4b711c00'))
		 	.fitBounds(bounds)
		 	.on('click', setStartState);

	// 	// this part isn't working
	// 	var mapMarker = L.icon({
	//     iconUrl: 'marker.png',
	//     shadowUrl: 'marker.png',

	//     iconSize:     [38, 95], // size of the icon
	//     shadowSize:   [50, 64], // size of the shadow
	//     iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
	//     shadowAnchor: [4, 62],  // the same for the shadow
	//     popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
	// });

	var markers = new L.MarkerClusterGroup({
		disableClusteringAtZoom: maxClusterZoom})
		.on('popupopen', function (evt) {
			setStartState();
			marker = evt.popup._source.feature.id;
			// make the review btn reference this marker
			//document.getElementById('reviewMarker').value = marker;
			console.log(marker);
		});	

	// make new marker layer
	var markerLayer = L.geoJson(markerCollection);
	// for each marker (layer) in the cluster, add custom popup and change icon
	markerLayer.eachLayer(function(layer) {
        var popupContent = '<b>' + layer.feature.properties.title + "</b><br><button type='button' value='plants!' class='detailsBtn'> Details </button> ";

        // can modify based on properties of feature! Will use to handle undefined features?
        if (layer.feature.properties.category === 'fruit') {
        	layer.setIcon(L.mapbox.marker.icon({'marker-color': '#76bd4a'})); //#FFCC00
        } else if (layer.feature.properties.category === 'nut') {
        	layer.setIcon(L.mapbox.marker.icon({'marker-color': '#76bd4a'})); //#7A5200
        } else if (layer.feature.properties.category === 'herb') {
        	layer.setIcon(L.mapbox.marker.icon({'marker-color': '#76bd4a'})); //#669900
        } else if (layer.feature.properties.category === 'vegetable') {
        	layer.setIcon(L.mapbox.marker.icon({'marker-color': '#76bd4a'})); //#751975
        } else {
        	layer.setIcon(L.mapbox.marker.icon({'marker-color': '#999966'}));
        }

    	layer.bindPopup(popupContent, 
    		className = 'markerPopup'); // can add other options
    });

	markers.addLayer(markerLayer);
	map.addLayer(markers);

	// centers and zooms the map around markers
	map.fitBounds(markerLayer.getBounds()); 
		// can add ', {padding: [25, 25]}' to pad results, but looks bad at low zoom. 
};

// Initialize map with markers!
// makeMap(mapLocation, markerCollection);
