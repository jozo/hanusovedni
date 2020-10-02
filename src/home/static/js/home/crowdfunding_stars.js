$(document).ready(function () {
  function showPercentage(amount) {
    let amount_bank = 345
    let full_amount = 5000
    let display_amount = Math.min(amount + amount_bank, full_amount)
    let percentage = display_amount / full_amount
    $('#mercury').height(percentage * 500)
    $('#mercury').prop('title', (amount + amount_bank) + '€')

    // Set size of stars backgrounds
    $('#grey-overlay-1').height((1 - percentage) * 500 + "px")
    $('#grey-overlay-1').css('bottom', percentage * 500 + "px")
    $('#grey-overlay-2').height((1 - percentage) * 500 + "px")
    $('#grey-overlay-2').css('bottom', percentage * 500 + "px")
  }

    $.ajax('https://api.darujme.sk/v1/feeds/7ac2c2c2-65ef-4d7b-b4a4-e43cc0c9a296/donations/?per_page=1')
      .done(function (data) {
        let amount = data["response"]["metadata"]["total_amount"]
        showPercentage(amount)
      })
      .fail(function () {
        console.log('Error - can\'t get current amount of €')
        showPercentage(120)
      })
  })
