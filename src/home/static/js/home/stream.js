$(document).ready(function () {
  // Dialog for email
  if (!Cookies.get('emailForStream')) {
    $('#popup-wrapper').show()
    $('#embed-wrapper').hide()
    $('#popup-wrapper2').hide()
    $('#bg-image').addClass('blur')
  } else {
    $('#popup-close-email').closest('.closable').removeClass('d-flex').hide()
  }

  if (!Cookies.get('donationForStream')) {
    $('#popup-wrapper').show()
    $('#embed-wrapper').hide()
    $('#bg-image').addClass('blur')
  } else {
    $('#popup-close-donation').closest('.closable').removeClass('d-flex').hide()
  }

  $('#stream-form').one('submit', function () {
    const inputName = encodeURIComponent($('#input-email').val())
    const baseURL = $('#google-form-url').val()
    const submitRef = '&submit=Submit'
    const submitURL = (baseURL + inputName + submitRef)
    $(this)[0].action = submitURL
    hideEmailPopup()
  })

  $('#stream-form2').one('submit', function () {
    const inputName = encodeURIComponent($('#input-email2').val())
    const baseURL = $('#google-form-url').val()
    const submitRef = '&submit=Submit'
    const submitURL = (baseURL + inputName + submitRef)
    $(this)[0].action = submitURL
    $('#popup-wrapper2').hide()
  })

  // Popup closing
  function showEmbedAfterPopupsClosed () {
    if ($('.closable:visible').length === 0) {
      $('#popup-wrapper').hide()
      $('#embed-wrapper').show()
      $('#bg-image').removeClass('blur')
    }
  }

  function hideEmailPopup () {
    const popup = $('#popup-close-email').closest('.closable')
    popup.hide()
    popup.removeClass('d-flex')
    showEmbedAfterPopupsClosed()
    $('#popup-wrapper2').show()
    Cookies.set('emailForStream', 'yes', { expires: 30 })   // expires in 30 days
  }

  $('#popup-close-email').on('click', hideEmailPopup)

  $('#popup-close-donation').on('click', function () {
    const popup = $(this).closest('.closable')
    popup.hide()
    popup.removeClass('d-flex')
    showEmbedAfterPopupsClosed()
    Cookies.set('donationForStream', 'yes', { expires: 30 })   // expires in 30 days
  })

  // Polling
  function refreshIfNewVersion (data) {
    let revision = parseInt($('#main-div').attr('data-revision'))
    if (data.live_revision !== revision) {
      location.reload()
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
