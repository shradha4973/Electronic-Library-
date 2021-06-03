// removing alert after 15 sec or onclick
/* Id must be alert and that element should have display none */
$(document).ready(function() {
  if ($("#alert").length == 1) {
    $("#alert").slideDown();
    setTimeout(function() {
      $("#alert").slideUp();
      setTimeout(function() {
        $("#alert").remove();
      }, 1000);
    }, 15000);
  }
  $("#closealert").click(function() {
    $("#alert").slideUp();
    setTimeout(function() {
      $("#alert").remove();
    }, 1000);
  });
});
