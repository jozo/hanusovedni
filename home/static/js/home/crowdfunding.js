$(document).ready(function () {
    $.ajax('https://old.darujme.sk/sk/campaign/feed/2393/key/a8c712f6adb34f9b718969f3d1c7b517/')
      .done(function (data) {
        let amount = parseFloat(/.*;el.innerHTML="(\d+\.\d+)".*/g.exec(data)[1])
        let full_amount = 5000
        let percentage = amount / full_amount
        $('#mercury').height(percentage * 500)
        $('#mercury').prop('title', amount + '€')
      })
      .fail(function () {
        console.log('Error - can\'t get current amount of €')
      })
  })
