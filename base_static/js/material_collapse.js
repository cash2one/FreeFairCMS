$(document).ready(function() {
  $('.collapse.in').prev('.panel-heading').addClass('active');
  $('.accordion-group')
    .on('show.bs.collapse', function(a) {
      $(a.target).prev('.panel-heading').addClass('active');
    })
    .on('hide.bs.collapse', function(a) {
      $(a.target).prev('.panel-heading').removeClass('active');
    });
});
