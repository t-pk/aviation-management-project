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

jQuery(function ($) {
  const airports = [];
  const selectElement = $('#id_departure');
  const arrivalSelect = $('#id_arrival');
  let flightIdSelected = '';
  selectElement.find('option').each(function () {
    airports.push({ code: $(this).val(), name: $(this).text() });
  });

  function filterAndPopulateOptions(arrayToClone, filterValue, selectElement) {
    return new Promise((resolve, reject) => {
      const clonedArray = arrayToClone.filter(item => item.code !== filterValue);
      selectElement.empty();
      clonedArray.forEach(option => {
        const newOption = $('<option>', {
          value: option.code,
          text: option.name
        });
        selectElement.append(newOption);
      });
      resolve();
    });
  }
  function fetchFlight() {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: "/aviation/flights/",
        type: "POST",
        data: {
          departure_airport: selectElement.val(),
          arrival_airport: arrivalSelect.val(),
          departure_time: $('#id_departure_time').val()
        },
        success: function (result) {
          $('#id_flight').empty();
          result.flights.forEach(option => {
            const departure_time = new Date(option.departure_time).toLocaleTimeString();
            const arrival_time = new Date(option.arrival_time).toLocaleTimeString();
            const newOption = $('<option>', {
              value: option.id,
              text: `${option.aircraft_code} | ${departure_time} | ${arrival_time}`,
              selected: flightIdSelected === option.id
            });
            $('#id_flight').append(newOption);
          });
          resolve();
        },
        headers: {
          "X-CSRFToken": getCookie("csrftoken")
        },
        error: function (e) {
          console.error(JSON.stringify(e));
          reject(e);
        },
      });
    });
  }

  arrivalSelect.add(selectElement).change(function () {
    const isDepartureSelected = selectElement.val() === arrivalSelect.val();
    if (isDepartureSelected) {
      filterAndPopulateOptions(airports, $(this).val(), isDepartureSelected ? arrivalSelect : selectElement);
    }
    fetchFlight();
    calculateDistance();
  });

  $('#id_departure_time').change(fetchFlight);

  if (airports && airports.length) {
    filterAndPopulateOptions(airports, airports[0].code, arrivalSelect)
      .then(fetchDataForEditing)
      .then(fetchFlight)
      .catch(error => {
        console.error('Error:', error);
      });
  }

  function fetchDataForEditing() {
    return new Promise((resolve, reject) => {
      var currentUrl = window.location.href;
      var match = currentUrl.match(/\/admin\/aviation\/booking\/(\d+)\/change\//);
      if (match) {
        var bookingId = match ? match[1] : null;
        $.ajax({
          url: `/aviation/bookings/${bookingId}/`,
          type: 'GET',
          success: function (data) {
            $('#id_departure').val(data.departure_airport);
            $('#id_arrival').val(data.arrival_airport);
            $('#id_departure_time').val(data.departure_time);
            flightIdSelected = data.flight_id;
            resolve();
          },
          error: function (xhr, textStatus, error) {
            console.error('Error fetching data:', error);
            reject(e);
          }
        });
      }
      resolve();
    })
  }

  function calculateDistance() {
    var departureCode = $('#id_departure').val();
    var arrivalCode = $('#id_arrival').val();
    var totalPassenger = $('#id_total_passenger').val();
    $.ajax({
      url: '/aviation/fares/',
      method: 'GET',
      data: {
        departure_code: departureCode,
        arrival_code: arrivalCode,
        total_passenger: totalPassenger || 0
      },
      success: function (response) {
        $('#id_total_amount').val(response.total_fare)
      },
      error: function (xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  }
  $('#id_total_passenger').on('input', function () {
    calculateDistance();
  });

  function formatCurrency(amount) {
    return amount.toLocaleString('vi-VN', { style: 'currency', currency: 'VND' });
}
})
