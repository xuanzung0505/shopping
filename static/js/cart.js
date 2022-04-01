// console.log("hehe")
$(document).ready(function () {

    var csrfToken = $("input[name=csrfmiddlewaretoken]").val()

    $("#cartItemList").on('click', 'button.custom-btn', function (event) {
        // console.log(csrfToken);

        event.stopPropagation(); //the event wont extend to the parent element
        var dataID = $(this).data('id') //data-id of the button
        console.log(dataID)

        $.ajax({
            url: '/shopping/cart/delete/' + dataID + '/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataID
            },
            type: 'post',
            dataType: 'json',
            success: function (response) {
                $('#cartItem[data-id="' + dataID + '"]').remove()
                $('#cartTotalPrice').html(response.cartTotal+'$')
            }
        })
    })

    // $("#quantity").addEventListener('change', function(e){
    //     if (e.target.value == '') {
    //         e.target.value = 1
    //       }
    // })

    $("#cartItemList").on('change', '#quantity', function () {
        var dataID = $(this).data('id') //dataID of the input

        const numInputs = document.querySelectorAll('#quantity') //get all element with id 'quantity'
        numInputs.forEach(function (input) {
            if ($(input).data('id') == dataID){ //if element has data-id = dataID
                quantityInput = $(input).val()
                // console.log($(input).val())
            }
        })

        quantity = parseInt(quantityInput)
        console.log(dataID, quantityInput, quantity)

        $.ajax({
            url: '/shopping/cart/quantityChange/'+dataID+'/'+quantity+'/',
            data:{
                csrfmiddlewaretoken : csrfToken,
                id: dataID
            },
            type:'post',
            dataType: 'json',
            success: function(response){
                $('#cartItemTotalPrice[data-id="'+dataID+'"]').html(response.cartItemTotal+'$')
                $('#cartTotalPrice').html(response.cartTotal+'$')
            }
        })
    })
})