$(document).ready(function () {
  function showPercentage (amount) {
    const amount_bank = 0
    const full_amount = $('.n-top').data("attr-value")
    let display_amount = Math.min(amount + amount_bank, full_amount)
    let percentage = display_amount / full_amount
    $('#mercury').height(percentage * 500)
    $('#mercury').prop('title', (amount + amount_bank) + '€')
  }

  $.ajax('https://api.darujme.sk/v1/feeds//donations/?per_page=1')
    .done(function (data) {
      let amount = data['response']['metadata']['total_amount']
      showPercentage(amount)
    })
    .fail(function () {
      console.log('Error - can\'t get current amount of €')
      showPercentage(281)
    })
})
