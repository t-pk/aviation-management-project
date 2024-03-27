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
  var arrivalSelect = $('#id_arrival');

  function filterAndPopulateOptions(arrayToClone, filterValue, selectElement) {
    var clonedArray = $.extend(true, [], arrayToClone);
    clonedArray = clonedArray.filter((item) => item.code !== filterValue);
  
    selectElement.empty();
    $.each(clonedArray, function (index, option) {
      var newOption = $('<option>', {
        value: option.code,
        text: option.name
      });
      selectElement.append(newOption);
    });
  }
  $(document).ready(function () {

    var selectElement = $('#id_departure');
    var options = selectElement.find('option');
    options.each(function () {
      airports.push({ code: $(this).val(), name: $(this).text() });
    });
  
    filterAndPopulateOptions(airports, airports[0].code, arrivalSelect);

    $("#id_arrival").change(function () {
      selectElement.val() === arrivalSelect.val() && filterAndPopulateOptions(airports, $(this).val(), selectElement)
    })

    $("#id_departure").change(function () {
      selectElement.val() === arrivalSelect.val() && filterAndPopulateOptions(airports, $(this).val(), arrivalSelect)
      //   $.ajax({
      //       url:"/aviation/departure/",
      //       type:"POST",
      //       data:{departure_airport: $(this).val(),},
      //       success: function(result) {
      //           console.log(result);
      //           cols = document.getElementById("id_division");
      //           cols.options.length = 0;
      //           cols.options.add(new Option("Division", "Division"));
      //           for(var k in result){
      //               cols.options.add(new Option(k, result[k]));
      //           }
      //       },
      //       headers: {
      //           "X-CSRFToken": getCookie("csrftoken")
      //       },
      //       error: function(e){
      //           console.error(JSON.stringify(e));
      //       },
      //   });
    });
  });
});