var centerLat = 37.75768707689704;
var centerLon = -122.44279861450195;
var mapLocation = [centerLat, centerLon]; 
var mapZoom = 12; //12 is ideal for showing SF, 15 shows markers for testing
var southWest = L.latLng(37.7, -122.541);
var northEast = L.latLng(37.815, -122.335);
var bounds = L.latLngBounds(southWest, northEast);
var plantLocation; // this becomes a position object, with lat and long keys.
var plantDragged = false;

// this is public on purpose
L.mapbox.accessToken = 'pk.eyJ1IjoicmlzZWxpa2V0aGVtb29uIiwiYSI6IjI4MjczOTIwNzE5MTY1ODI4YmYxZGVlZGZmYjc4NmI0In0.fiUOgIDwB_ByzxT63VWP-g';

var map = L.mapbox.map('map', 'riselikethemoon.4b711c00', {maxBounds: bounds, minZoom: mapZoom})
    .setView(mapLocation, mapZoom) 
    .addLayer(L.mapbox.tileLayer('riselikethemoon.4b711c00'))
    .fitBounds(bounds);

// code to generate marker
var marker = L.marker(new L.LatLng(centerLat, centerLon), {
    icon: L.mapbox.marker.icon({
        'marker-color': 'ff8888'
    }),
    draggable: true
});
var popupContent = '<b>Drag me to the plant\'s location</b>';

marker.bindPopup(popupContent);
marker.addTo(map);


// gets location of dragged marker, allows user to submit
marker.on('dragend', function(evt){
    plantLocation = marker.getLatLng();
    plantDragged = true;
    document.getElementById('formLat').value = plantLocation['lat']
    document.getElementById('formLon').value = plantLocation['lng']

    console.log('plant dragged to ' + plantLocation['lat'] + ', ' + plantLocation['lng']);
});

// ########## set up list for autocomplete of plant name/species
autoList = []

$.get('/list-fields', function (results) {
        autoList = JSON.parse(results);
        // var dropdown = document.getElementById('');

        // for(var i = 0; i < autoList.length; i++) {
        //     var opt = document.createElement('option');
        //     opt.innerHTML = autoList[i];
        //     opt.value = autoList[i];
        //     dropdown.appendChild(opt);
        // }
});

// ########## Validate form before submission

//var addBtn = document.getElementById('addBtn')
// function validate(evt) {
//     evt.preventDefault();
//     console.log('validating');

//     // if a category isn't checked, alert to check it
//     // if season isn't checked, alert to check it

//     // if marker isn't dragged, alert to drag it
//     if (!plantDragged) {
//         console.log('plant not dragged yet');
//         alert('Please drag the marker to the plant\'s location');
//     };
//     // else, submit
// };

// this isn't grabbing the click like it should :(
console.log('click it!');
$('.addBtn').on('click', function(){
    evt.preventDefault();
    console.log('validating');

    // if a category isn't checked, alert to check it
    // if season isn't checked, alert to check it
    // if marker isn't dragged, alert to drag it
    if (!plantDragged) {
        console.log('plant not dragged yet');
        alert('Please drag the marker to the plant\'s location');
    };
    // else, submit
});



