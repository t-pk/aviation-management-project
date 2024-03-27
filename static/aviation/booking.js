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

jQuery(function($) {
  const airports = [];
  const selectElement = $('#id_departure');
  const arrivalSelect = $('#id_arrival');

  selectElement.find('option').each(function() {
    airports.push({ code: $(this).val(), name: $(this).text() });
  });

  function filterAndPopulateOptions(arrayToClone, filterValue, selectElement) {
    const clonedArray = arrayToClone.filter(item => item.code !== filterValue);
    selectElement.empty();
    clonedArray.forEach(option => {
      const newOption = $('<option>', {
        value: option.code,
        text: option.name
      });
      selectElement.append(newOption);
    });
  }

  function fetchFlight() {
    $.ajax({
      url: "/aviation/flights/",
      type: "POST",
      data: {
        departure_airport: selectElement.val(),
        arrival_airport: arrivalSelect.val(),
        departure_time: $('#id_departure_time').val()
      },
      success: function(result) {
        $('#id_flight').empty();
        result.flights.forEach(option => {
          const departure_time = new Date(option.departure_time).toLocaleTimeString();
          const arrival_time = new Date(option.arrival_time).toLocaleTimeString();
          const newOption = $('<option>', {
            value: option.id,
            text: `${option.aircraft_model} | ${departure_time} | ${arrival_time}`
          });
          $('#id_flight').append(newOption);
        });
      },
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      error: function(e) {
        console.error(JSON.stringify(e));
      },
    });
  }

  arrivalSelect.add(selectElement).change(function() {
    const isDepartureSelected = selectElement.val() === arrivalSelect.val();
    if (isDepartureSelected) {
      filterAndPopulateOptions(airports, $(this).val(), isDepartureSelected ? arrivalSelect : selectElement);
    }
    fetchFlight();
  });

  $('#id_departure_time').change(fetchFlight);

  // Initial population and fetching
  filterAndPopulateOptions(airports, airports[0].code, arrivalSelect);
  fetchFlight();
});
