$(document).ready(function () {
    function showAsPercentage(amount) {
        const amount_bank = 0
        const full_amount = $('#target-amount').data("attr-value")
        let display_amount = Math.min(amount + amount_bank, full_amount)
        let percentage = display_amount / full_amount
        const animation_time = 400
        const mercury = $('#mercury')
        mercury.prop('title', (amount + amount_bank) + '€')
        mercury.animate({
            width: (percentage * 100) + "%"
        }, percentage * animation_time * 10)

        // light on candles
        let num_of_candles = Math.min(10, Math.floor(percentage * 10))
        const candle_flames = $('.flame')
        for (let i = 0; i < num_of_candles; i++) {
            $(candle_flames[i]).delay(i * animation_time).animate({width: "30px", opacity: "show"})
        }
    }

    $.ajax('https://api.darujme.sk/v1/feeds/c652ee51-bde3-49ff-b274-362a7d50fd99/donations/?per_page=1')
        .done(function (data) {
            let amount = data['response']['metadata']['total_amount']
            showAsPercentage(amount)
        })
        .fail(function () {
            console.log('Error - can\'t get current amount of €')
            showAsPercentage(0)
        })
})
