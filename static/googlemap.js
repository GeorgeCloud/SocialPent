'use strict';
console.log('map is here')
let map, infoWindow;
let pos = {};

map = new google.maps.Map(document.getElementById('google-map'), {
  center: {
    lat: 47.6182,
    lng: -122.3519
  },
  zoom: 10
});
infoWindow = new google.maps.InfoWindow();

// Use HTML5 geolocation.
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    function(position) {
      pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      // User's current location
      let marker = new google.maps.Marker({
        position: pos,
        icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', // image,
        animation: google.maps.Animation.DROP,
        map: map
      });
      map.setCenter(pos);

      fetch('http://127.0.0.1:5000/events')
        .then((response) => response.json())
        .then((events) => {
          for (let i=0; i<events.length; i++){
            createMarker(events[i])
          }
        });
    },
    function() {
      handleLocationError(true, infoWindow, map.getCenter());
    }
  );
} else {
  // Browser doesn't support Geolocation
  handleLocationError(false, infoWindow, map.getCenter());
}

function createMarker(event) {
  let marker = new google.maps.Marker({
    position: {
      lat: parseFloat(event.coordinates.latitude),
      lng: parseFloat(event.coordinates.longitude)
    },
    map: map
  });

  const contentString =
  `<h1 id="firstHeading" class="firstHeading"> ${event.name}</h1>
  <p>${event.address}</p>
  <a href="${event.url}" target="_blank">event details</a>`

// Google Maps marker info
  google.maps.event.addListener(marker, 'click', function() {
    infoWindow.setContent(contentString);
    infoWindow.open(map, this);
  });
}

// Warn user when geolocation fails
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
    'Error: The Geolocation service failed.' :
    'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}
