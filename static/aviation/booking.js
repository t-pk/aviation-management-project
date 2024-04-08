const getCookie = (name) => {
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
};

const get_booking_information = () => {
  const departure = document.getElementById('id_departure').value;
  const arrival = document.getElementById('id_arrival').value;
  const departure_time = document.getElementById('id_departure_time').value;
  const quantity = document.getElementById('id_quantity').value;

  const params = new URLSearchParams({ departure, arrival, departure_time, quantity });
  const url = `${window.location.origin}/aviation/get-booking-information/?${params}`;

  const csrftoken = getCookie('csrftoken');

  fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken  // Include CSRF token in request headers
    }
  })
    .then(response => response.json())
    .then(data => {
      const select = document.getElementById('id_flight');
      select.innerHTML = '';
      data.forEach(flight => {
        const option = document.createElement('option');
        option.value = flight.pk;
        option.text = flight.__str__;
        select.appendChild(option);
      });
    });
};
