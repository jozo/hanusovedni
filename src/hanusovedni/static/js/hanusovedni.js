$(document).ready(function () {
  $('#cookiesAlert').on('closed.bs.alert', function () {
    Cookies.set('cookiesAccepted', 'yes', { expires: 365 * 10 })    // expires in 10 years
  })

  if (Cookies.get('cookiesAccepted')) {
    $('#cookiesAlert').hide()
  }


  // Stream page
  if (! Cookies.get('emailForStream')) {
    $('#form-wrapper').show()
  }

  $('#stream-form').one('submit', function () {
    const inputName = encodeURIComponent($('#input-email').val())
    const baseURL = $('#google-form-url').val()
    const submitRef = '&submit=Submit'
    const submitURL = (baseURL + inputName + submitRef)
    $(this)[0].action = submitURL
    $('#form-wrapper').hide()
    Cookies.set('emailForStream', 'yes', { expires: 30 })   // expires in 30 days
  })
})
