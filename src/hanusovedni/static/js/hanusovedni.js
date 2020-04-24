$(document).ready(function () {
  $('#cookiesAlert').on('closed.bs.alert', function () {
    Cookies.set('cookiesAccepted', 'yes', { expires: 365 * 10 })    // expires in 10 years
  })

  if (Cookies.get('cookiesAccepted')) {
    $('#cookiesAlert').hide()
  }
})
