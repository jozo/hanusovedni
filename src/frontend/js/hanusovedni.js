import $ from 'jquery'
import Cookies from 'js-cookie'

$(document).ready(function () {
  $('#cookiesAlert').on('closed.bs.alert', function () {
    Cookies.set('cookiesAccepted', 'yes', { expires: 365 * 10 })    // expires in 10 years
  })

  if (!Cookies.get('cookiesAccepted')) {
    $('#cookiesAlert').removeClass("d-none")
  }

  function userIsLoggedIn () {
    return Cookies.get('user_logged_in') !== undefined
  }

  function showWagtailUserBar () {
    if (userIsLoggedIn()) {
      $('#page-editing-bar').show()
    }
  }

  showWagtailUserBar()
})
