$(document).ready(function () {
    $.ajax('https://old.darujme.sk/sk/campaign/feed/2785/key/8277e0e414c8b5089c657c6bedd182e5/')
      .done(function (data) {
        let amount = parseFloat(/.*;el.innerHTML="(\d+\.\d+)".*/g.exec(data)[1])
        let amount_bank = 0
        let full_amount = 10000
        let display_amount = Math.min(amount + amount_bank, full_amount)
        let percentage = display_amount / full_amount
        $('#mercury').height(percentage * 500)
        $('#mercury').prop('title', (amount + amount_bank) + '€')

        // Set size of stars backgrounds
        $('#grey-overlay-1').height((1 - percentage) * 500 + "px")
        $('#grey-overlay-1').css('bottom', percentage * 500 + "px")
        $('#grey-overlay-2').height((1 - percentage) * 500 + "px")
        $('#grey-overlay-2').css('bottom', percentage * 500 + "px")
      })
      .fail(function () {
        console.log('Error - can\'t get current amount of €')
      })
  })
