$(document).ready(function () {

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
