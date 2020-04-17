$(document).ready(function () {
    $.ajax('https://old.darujme.sk/sk/campaign/feed/2393/key/9c2db08baa7b78bef1927a3c7342fffb/')
      .done(function (data) {
        let amount = parseFloat(/.*;el.innerHTML="(\d+\.\d+)".*/g.exec(data)[1])
        let amount_bank = 2500
        let full_amount = 5000
        let percentage = (amount + amount_bank) / full_amount
        $('#mercury').height(percentage * 500)
        $('#mercury').prop('title', (amount + amount_bank) + '€')
      })
      .fail(function () {
        console.log('Error - can\'t get current amount of €')
      })
  })
