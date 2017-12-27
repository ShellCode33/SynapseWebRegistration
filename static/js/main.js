//Initialize Tooltips
$(function () {
  $('[data-toggle="tooltip"]').tooltip();

  $("#submit-button").click(function(event) {

    var postData = {
      'username' :          $('input[name=username]').val(),
      'email' :             $('input[name=email]').val(),
      'password' :          $('input[name=password]').val(),
      'confirm_password' :  $('input[name=confirm_password]').val()
    };

    $.ajax({
      method: "POST",
      url: "/register",
      data: postData
    }).done(function(error) {
      if(error !== "null") {
        console.log("registration error");
        $("#error").html("<strong>Oups, something went wrong !</strong> " + error);
        $("#error").removeAttr("hidden");
      }

      // No error, redirect
      else {
        window.location.replace("/thanks");
      }
    });
  });
})