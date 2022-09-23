let current_page = 1;
let records_per_page = 9;

function findNumPages(data)
{
    return Math.ceil(data.length / records_per_page);
}

function resetPagination(data){
    var numPages = findNumPages(data);
    
    console.log("data length: "+data.length)
    console.log("number of pages: "+numPages)
    
    const pagiItem = document.querySelectorAll('#pagiItem') //get all element with id 'pagiItem'
    pagiItem.forEach(function () {
        $(pagiItem).remove() //remove all
    })
}

function renderPagination(data){
    var numPages = findNumPages(data);
    $("#pagi").append('<li class="page-item disabled" id="pagiItem" name="prev"><a class="page-link" href="#'
    +'aria-label="Previous"><span aria-hidden="true">«</span></a></li>')
    $("#pagi").append('<li class="page-item active" id="pagiItem" value="'+1+'"><a class="page-link" href="#">'+1+'</a></li>')
    for(var page = 2; page <= numPages; page++){
        $("#pagi").append('<li class="page-item" id="pagiItem" value="'+page+'"><a class="page-link" href="#">'+page+'</a></li>')
    }
    $("#pagi").append('<li class="page-item" id="pagiItem" name="next"><a class="page-link" href="#" aria-label="Next"><span'+
    'aria-hidden="true">»</span></a></li>')
}

function resetData(tag){
    const products = document.querySelectorAll(tag) //get all element with id 'product'
    products.forEach(function (product) {
        $(product).remove() //remove all
    })
}

function renderData(data){
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
}

function init(){
    //init
    var data = JSON.parse(document.getElementById('json-data').textContent);
    // console.log(data)
    
    //reset pagination
    resetPagination(data)

    //render pagination
    renderPagination(data)
}

$(document).ready(function () {
    // $("#pagi").on('click', '.page-item', function(){
    //     console.log("hehe")
        
    //     //event here
    // })

    init()

    // var productList = JSON.parse('{{ productlist }}');

    // var obj = jQuery.parseJSON(JSON.stringify('{{productlist}}')); //better JSON
    //                 // console.log(typeof obj)
    //                 // console.log(obj)


    var csrfToken = $("input[name=csrfmiddlewaretoken]").val()

    $("#search").on('click', 'button', function () {
        var dataID = $(this).data('id') //dataID of the input
        // console.log(csrfToken)

        var searchQuery = $.trim($("#searchInfo").val())
        console.log("search query: "+searchQuery)

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
                    // console.log(typeof obj)
                    // console.log(obj)

                    var data = JSON.parse(obj);

                    // const productList = document.querySelectorAll('#productlist') //get all element with id 'productList'

                    //reset products
                    resetData('#product')
                    
                    //reset pagination
                    resetPagination(data)

                    //render pagination
                    renderPagination(data)

                    //render new products
                    renderData(data);

                    const category_inputs = document.querySelectorAll('#category0') //get all element with above id
                    category_inputs.forEach(function (category_input) {
                        // $(product).remove() //remove all
                        // console.log("hehe")
                        $(category_input).prop('checked', true) //set all #category 0 to 'checked'
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

                //reset products
                resetData('#product')
                    
                //reset pagination
                resetPagination(data)

                //render pagination
                renderPagination(data)

                //render new products
                renderData(data);

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

                //reset products
                resetData('#product')
                    
                //reset pagination
                resetPagination(data)

                //render pagination
                renderPagination(data)

                //render new products
                renderData(data);

                $("#searchInfo").val("")
            }
        })
    })
})