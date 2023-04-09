import $ from 'jquery'
import Cookies from 'js-cookie'

$(document).ready(function () {
  $('#cookiesAlert').on('closed.bs.alert', function () {
    Cookies.set('cookiesAccepted', 'yes', { expires: 365 * 10 })    // expires in 10 years
  })

  if (!Cookies.get('cookiesAccepted')) {
    $('#cookiesAlert').removeClass("d-none")
  }

  // Display menu when clicked on button
  $("#nav-btn").on("click", function () {
    $("#nav-menu").toggleClass("hidden")
  })
})
