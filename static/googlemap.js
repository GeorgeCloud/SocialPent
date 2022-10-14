'use strict';
console.log('map is here')
let map, infoWindow;
let pos = {};

map = new google.maps.Map(document.getElementById('google-map'), {
  center: {
    lat: 47.6182,
    lng: -122.3519
  },
  zoom: 10,
  styles: [
    { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
    { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
    { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
    { featureType: "administrative.locality", elementType: "labels.text.fill", stylers: [{ color: "#d59563" }]},
    { featureType: "poi", elementType: "labels.text.fill", stylers: [{ color: "#d59563" }] },
    { featureType: "poi.park", elementType: "geometry", stylers: [{ color: "#263c3f" }]},
    { featureType: "poi.park", elementType: "labels.text.fill", stylers: [{ color: "#6b9a76" }]},
    { featureType: "road", elementType: "geometry", stylers: [{ color: "#38414e" }],},
    { featureType: "road", elementType: "geometry.stroke", stylers: [{ color: "#212a37" }]},
    { featureType: "road", elementType: "labels.text.fill", stylers: [{ color: "#9ca5b3" }]},
    { featureType: "road.highway", elementType: "geometry", stylers: [{ color: "#746855" }]},
    { eatureType: "road.highway", elementType: "geometry.stroke", stylers: [{ color: "#1f2835" }]},
    { featureType: "road.highway", elementType: "labels.text.fill", stylers: [{ color: "#f3d19c" }]},
    { featureType: "transit", elementType: "geometry",stylers: [{ color: "#2f3948" }]},
    { featureType: "transit.station", elementType: "labels.text.fill", stylers: [{ color: "#d59563" }]},
    { featureType: "water", elementType: "geometry", stylers: [{ color: "#17263c" }]},
    { featureType: "water", elementType: "labels.text.fill", stylers: [{ color: "#515c6d" }]},
    { featureType: "water", elementType: "labels.text.stroke", stylers: [{ color: "#17263c" }]},
  ],
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
      fetch(`http://127.0.0.1:5000/events/${pos.lat},${pos.lng}`, {mode: 'no-cors'})
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
  `<h4 id="firstHeading" class="firstHeading"> ${event.name}</h4>
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
