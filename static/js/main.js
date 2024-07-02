// function initMap() {
//     var location = { lat: -34.397, lng: 150.644 };
//     var map = new google.maps.Map(document.getElementById('map'), {
//         zoom: 8,
//         center: location
//     });
//     var marker = new google.maps.Marker({
//         position: location,
//         map: map
//     });
// }

// Cart count
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.add-to-cart').forEach(function(button) {
        button.addEventListener('click', function() {
            const menuItemId = this.dataset.id;

            fetch(`/add-to-cart/${menuItemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update the cart icon or any cart display
                }
            });
        });
    });

    document.querySelectorAll('.remove-from-cart').forEach(function(button) {
        button.addEventListener('click', function() {
            const cartItemId = this.dataset.id;

            fetch(`/remove-from-cart/${cartItemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Remove the item from the cart display
                }
            });
        });
    });

    document.querySelectorAll('.update-cart-item').forEach(function(button) {
        button.addEventListener('click', function() {
            const cartItemId = this.dataset.id;
            const action = this.dataset.action;

            fetch(`/update-cart-item/${cartItemId}/${action}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update the item quantity display
                }
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
