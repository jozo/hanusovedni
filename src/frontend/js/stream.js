import $ from 'jquery'
import Cookies from 'js-cookie'

$(document).ready(function () {
  if ($('body.template-stream').length === 1) {
    showPopups()
    poll()
  }
})

function showPopups () {
  $('#embed-wrapper').addClass('blur')    // blur embedded video
  showOrHideEmailPopup()
  showOrHideDonatePopup()
  showVideoIfPopupsAreClosed()
  setCloseFunctions()
  setSubmitUrlOnForms()
}


function showOrHideEmailPopup () {
  if (Cookies.get('emailForStream')) {
    $('#popup-close-email').closest('.closable').removeClass('d-flex').hide()
  } else {
    $('#popup-wrapper').show()
    $('#email-dialog-bottom').hide()
  }
}

function showOrHideDonatePopup () {
  if (Cookies.get('donationForStream')) {
    $('#popup-close-donation').closest('.closable').removeClass('d-flex').hide()
  } else {
    $('#popup-wrapper').show()
  }
}

function showVideoIfPopupsAreClosed () {
  if ($('.closable:visible').length === 0) {
    $('#popup-wrapper').hide()
    $('#embed-wrapper').removeClass('blur')
  }
}

function setCloseFunctions () {
  $('#popup-close-email').on('click', hideAndSetCookieForEmail)
  $('#popup-close-donation').on('click', hideAndSetCookieForDonation)
}

function hideAndSetCookieForEmail () {
  const popup = $('#popup-close-email').closest('.closable')
  popup.removeClass('d-flex')
  popup.hide()
  showVideoIfPopupsAreClosed()
  $('#email-dialog-bottom').show()
  Cookies.set('emailForStream', 'yes', { expires: 30 })   // expires in 30 days
}

function hideAndSetCookieForDonation () {
  const popup = $(this).closest('.closable')
  popup.removeClass('d-flex')
  popup.hide()
  showVideoIfPopupsAreClosed()
  Cookies.set('donationForStream', 'yes', { expires: 30 })   // expires in 30 days
}

/**
 * We use Google docs to save results from forms (email for stream form)
 * This sets correct action (url) on the form
 */
function setSubmitUrlOnForms () {
  const baseURL = $('#google-form-url').val()
  const submitRef = '&submit=Submit'
  $('#stream-form').one('submit', function () {
    const inputName = encodeURIComponent($('#input-email').val())
    $(this)[0].action = (baseURL + inputName + submitRef)   // set submit url on the form
    hideAndSetCookieForEmail()
  })

  $('#stream-form2').one('submit', function () {
    const inputName = encodeURIComponent($('#input-email2').val())
    $(this)[0].action = (baseURL + inputName + submitRef)   // set submit url on the form
    $('#email-dialog-bottom').hide()
  })
}

/**
 * Polling - every x seconds check if there is a new version of website
 * It's used to refresh website after new video (YouTube link) is replaced in admin
 */
function poll () {
  $.get({
    url: '/api/stream/',
    success: refreshIfNewVersion,
    timeout: 3000
  }).always(function () {
    setTimeout(poll, 5000)
  })
}

function refreshIfNewVersion (data) {
  let revision = parseInt($('#main-div').attr('data-revision'))
  if (data.live_revision !== revision) {
    location.reload()
  }
}
