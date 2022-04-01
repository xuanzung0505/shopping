$(document).ready(function () {

    var csrfToken = $("input[name=csrfmiddlewaretoken]").val()

    $("#search").on('click', 'button', function () {
        var dataID = $(this).data('id') //dataID of the input
        // console.log(csrfToken)

        var searchQuery = $.trim($("#searchInfo").val())
        console.log(searchQuery)

        if (searchQuery == '') {
            window.location.href = "/shopping/catalog/"
        }
        else {
            $.ajax({
                url: '/shopping/catalog/search/' + searchQuery + '/',
                data: {
                    csrfmiddlewaretoken: csrfToken,
                },
                type: 'post',
                dataType: 'json',
                success: function (response) {
                    console.log(JSON.stringify(response));
                    var obj = jQuery.parseJSON(JSON.stringify(response)); //better JSON

                    console.log(typeof obj)
                    console.log(obj)

                    var data = JSON.parse(obj);

                    // const productList = document.querySelectorAll('#productlist') //get all element with id 'productList'

                    const products = document.querySelectorAll('#product') //get all element with id 'product'
                    products.forEach(function (product) {
                        $(product).remove() //remove all
                    })

                    jQuery(data).each(function (i, item) {
                        console.log(item.pk, item.fields.title, item.fields.price, item.fields.product_img)
                        $("#productList").append('<div class="col-12 col-md-6 col-lg-4" id="product">' +
                            '<div class="clean-product-item">' +
                            '<div class="image"><a href="' + "/shopping/detail/" + item.pk + '"><img class="img-fluid d-block mx-auto" src="/static/' + item.fields.product_img + '"></a></div>' +
                            '<div class="product-name"><a href="' + "/shopping/detail/" + item.pk + '">' + item.fields.title + '</a></div>' +
                            '<div class="about">' +
                            '<div class="rating"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star-half-empty.svg"><img src="/static/assets/img/star-empty.svg"></div>' +
                            '<div class="price">' +
                            '<h3>' + Number(item.fields.price).toFixed(1) + '$</h3>' +
                            '</div>' +
                            '</div>' +
                            '</div>' +
                            '</div>')
                    })
                    const category_inputs = document.querySelectorAll('#category0') //get all element with above id
                    category_inputs.forEach(function (category_input) {
                        // $(product).remove() //remove all
                        // console.log("hehe")
                        $(category_input).prop('checked', true) //set all to checked
                    })
                }
            })
        }

    })

    $("input[name='category']").change(function () {
        // console.log($(this).attr("id"))

        var category_id = '#' + $(this).attr("id") //get id of this element

        const category_inputs = document.querySelectorAll(category_id) //get all element with above id
        category_inputs.forEach(function (category_input) {
            // $(product).remove() //remove all
            // console.log("hehe")
            $(category_input).prop('checked', true) //set all to checked
        })

        var dataID = $(this).val()
        // console.log(dataID)
        $.ajax({
            url: '/shopping/catalog/filter/' + dataID + '/',
            data: {
                csrfmiddlewaretoken: csrfToken
            },
            type: 'post',
            dataType: 'json',
            success: function (response) {
                console.log(JSON.stringify(response));
                var obj = jQuery.parseJSON(JSON.stringify(response)); //better JSON

                console.log(typeof obj)
                console.log(obj)

                var data = JSON.parse(obj);

                // const productList = document.querySelectorAll('#productlist') //get all element with id 'productList'

                const products = document.querySelectorAll('#product') //get all element with id 'product'
                products.forEach(function (product) {
                    $(product).remove() //remove all
                })

                jQuery(data).each(function (i, item) {
                    console.log(item.pk, item.fields.title, item.fields.price, item.fields.product_img)
                    $("#productList").append('<div class="col-12 col-md-6 col-lg-4" id="product">' +
                        '<div class="clean-product-item">' +
                        '<div class="image"><a href="' + "/shopping/detail/" + item.pk + '"><img class="img-fluid d-block mx-auto" src="/static/' + item.fields.product_img + '"></a></div>' +
                        '<div class="product-name"><a href="' + "/shopping/detail/" + item.pk + '">' + item.fields.title + '</a></div>' +
                        '<div class="about">' +
                        '<div class="rating"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star-half-empty.svg"><img src="/static/assets/img/star-empty.svg"></div>' +
                        '<div class="price">' +
                        '<h3>' + Number(item.fields.price).toFixed(1) + '$</h3>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>')
                })

                $("#searchInfo").val("")
            }
        })
    })

    $("input[name='category_col']").change(function () {
        // console.log($(this).val())

        var category_id = '#' + $(this).attr("id") //get id of this element

        const category_inputs = document.querySelectorAll(category_id) //get all element with above id
        category_inputs.forEach(function (category_input) {
            // $(product).remove() //remove all
            // console.log("hehe")
            $(category_input).prop('checked', true) //set all to checked
        })

        var dataID = $(this).val()
        // console.log(dataID)
        $.ajax({
            url: '/shopping/catalog/filter/' + dataID + '/',
            data: {
                csrfmiddlewaretoken: csrfToken
            },
            type: 'post',
            dataType: 'json',
            success: function (response) {
                console.log(JSON.stringify(response));
                var obj = jQuery.parseJSON(JSON.stringify(response)); //better JSON

                console.log(typeof obj)
                console.log(obj)

                var data = JSON.parse(obj);

                // const productList = document.querySelectorAll('#productlist') //get all element with id 'productList'

                const products = document.querySelectorAll('#product') //get all element with id 'product'
                products.forEach(function (product) {
                    $(product).remove() //remove all
                })

                jQuery(data).each(function (i, item) {
                    console.log(item.pk, item.fields.title, item.fields.price, item.fields.product_img)
                    $("#productList").append('<div class="col-12 col-md-6 col-lg-4" id="product">' +
                        '<div class="clean-product-item">' +
                        '<div class="image"><a href="' + "/shopping/detail/" + item.pk + '"><img class="img-fluid d-block mx-auto" src="/static/' + item.fields.product_img + '"></a></div>' +
                        '<div class="product-name"><a href="' + "/shopping/detail/" + item.pk + '">' + item.fields.title + '</a></div>' +
                        '<div class="about">' +
                        '<div class="rating"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star-half-empty.svg"><img src="/static/assets/img/star-empty.svg"></div>' +
                        '<div class="price">' +
                        '<h3>' + Number(item.fields.price).toFixed(1) + '$</h3>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>')
                })

                $("#searchInfo").val("")
            }
        })
    })
})