// document.addEventListener('DOMContentLoaded', function() {
//     var toggleButton = document.getElementById('toggle-button');
//     var senderForm = document.getElementById('sender-form');
//     var initialData = {{ initial_data|safe }};
    
//     toggleButton.addEventListener('click', function() {
//         senderForm.style.display = 'block';
//         if (toggleButton.textContent === 'Use Previous Details') {
//             for (var key in initialData) {
//                 if (initialData.hasOwnProperty(key)) {
//                     var field = senderForm.querySelector('[name=' + key + ']');
//                     if (field) {
//                         field.value = initialData[key];
//                     }
//                 }
//             }
//             toggleButton.textContent = 'Enter New Details';
//         } else {
//             senderForm.reset();
//             toggleButton.textContent = 'Use Previous Details';
//         }
//     });
// });

// Google Map
function initMap() {
    // Default location in case geolocation fails
    var defaultLocation = { lat: -34.397, lng: 150.644 };
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: defaultLocation
    });

    document.getElementById('get-location').addEventListener('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var lat = position.coords.latitude;
                var lng = position.coords.longitude;
                var location = { lat: lat, lng: lng };

                map.setCenter(location);

                new google.maps.Marker({
                    position: location,
                    map: map
                });

                // Set the form fields
                document.getElementById('latitude').value = lat;
                document.getElementById('longitude').value = lng;

                // Show the form
                document.getElementById('location-form').style.display = 'block';
            }, function(error) {
                alert('Error getting location: ' + error.message);
            });
        } else {
            alert('Geolocation is not supported by this browser.');
        }
    });
}
