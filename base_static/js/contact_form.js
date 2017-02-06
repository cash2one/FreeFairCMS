$('#contact-form').on('submit', function (event) {
  event.preventDefault();

  send_form();
});

function send_form() {
  clear_alerts();

  var data = {
    name: $('#contact-name').val(),
    email: $('#contact-email').val(),
    message: $('#contact-message').val(),
    recaptcha: grecaptcha.getResponse()
  };

  $.ajax({
    url: "/contact/send/",
    type: "POST",
    data: data,
    success: function (json) {
      clear_form();

      console.log(json);

      $('#contact-success').text(json.message);  
    },
    error: function (xhr, errmsg, err) {
      console.log(xhr.status + ': ' + xhr.responseText);
      $('#contact-error').text(xhr.responseText); 
    }
  });
}

function clear_form() {
  $('#contact-name').val('');
  $('#contact-email').val('')
  $('#contact-message').val('');
}

function clear_alerts() {
  $('#contact-success').empty();
  $('#contact-error').empty();
}
