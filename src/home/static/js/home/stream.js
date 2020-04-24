$(document).ready(function () {
  // Dialog for email
  if (! Cookies.get('emailForStream')) {
    $('#form-wrapper').show()
    $('#embed-wrapper').hide()
  }

  $('#stream-form').one('submit', function () {
    const inputName = encodeURIComponent($('#input-email').val())
    const baseURL = $('#google-form-url').val()
    const submitRef = '&submit=Submit'
    const submitURL = (baseURL + inputName + submitRef)
    $(this)[0].action = submitURL
    $('#form-wrapper').hide()
    $('#embed-wrapper').show()
    Cookies.set('emailForStream', 'yes', { expires: 30 })   // expires in 30 days
  })

  $('#continue-without-email').on('click', function () {
    $('#form-wrapper').hide()
    $('#embed-wrapper').show()
    Cookies.set('emailForStream', 'yes', { expires: 30 })   // expires in 30 days
  })


  // Polling
  function refreshIfNewVersion (data) {
    let revision = parseInt($('#main-div').attr('data-revision'))
    if (data.live_revision !== revision) {
      history.go(0)
    }
  }

  function poll () {
    $.get({
      url: '/api/stream/',
      success: refreshIfNewVersion,
      timeout: 10000
    }).always(function () {
      setTimeout(poll, 30000)
    })
  }

  poll()
})
