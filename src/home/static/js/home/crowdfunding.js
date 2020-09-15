$(document).ready(function () {
  function showPercentage (amount) {
    let amount_bank = 1885
    let full_amount = 10000
    let display_amount = Math.min(amount + amount_bank, full_amount)
    let percentage = display_amount / full_amount
    $('#mercury').height(percentage * 500)
    $('#mercury').prop('title', (amount + amount_bank) + '€')
  }

  $.ajax('https://api.darujme.sk/v1/feeds/277106b7-917d-4726-913d-26e331e69ed2/donations/?per_page=1')
    .done(function (data) {
      let amount = data['response']['metadata']['total_amount']
      showPercentage(amount)
    })
    .fail(function () {
      console.log('Error - can\'t get current amount of €')
      showPercentage(5600)
    })
})
