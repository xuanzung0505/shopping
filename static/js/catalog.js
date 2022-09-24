var numPages;
var current_page;
var records_per_page = 9;
var pageData;

function findNumPages()
{
    return Math.ceil(pageData.length / records_per_page);
}

function resetPagination(){
    numPages = findNumPages();
    
    // console.log("data length: "+pageData.length)
    // console.log("number of pages: "+numPages)
    
    const pagiItem = document.querySelectorAll('#pagiItem') //get all element with id 'pagiItem'
    pagiItem.forEach(function () {
        $(pagiItem).remove() //remove all
    })
}

function renderPagination(){
    numPages = findNumPages();
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

function clean(data){
    // console.log("cleaning data...")
    var newData = [];

    jQuery(data).each(function (i, item) {
        // console.log(item.pk, item.fields.title, item.fields.price, item.fields.product_img)
        // var fields = item.fields;

        // console.log(typeof(fields))
        // console.log(fields)
        var aNewData = {"id":item.pk, "title":item.fields.title, "price":item.fields.price, 
            "product_img":item.fields.product_img, "description":item.fields.description, 
            "category":item.fields.category, "active": item.fields.active}
        // console.log("aNewData:"+aNewData)

        // aNewData = Object.assign({},aNewData)
        // data = new Map(Object.entries(fields))
        newData.push(aNewData)    
        // console.log("fields:"+fields)
        // console.log("aNewData:"+aNewData)
    })
    // pageData = Object.assign({},newData);
    pageData = newData;
    // console.log("pageData after cleaning: "+pageData)
}

function appendData(pk,title,price,product_img){
    $("#productList").append('<div class="col-12 col-md-6 col-lg-4" id="product">' +
                '<div class="clean-product-item">' +
                '<div class="image" style="height:25vh;"><a href="' + "/shopping/detail/" + pk + 
                '"><img class="img-fluid d-block mx-auto" style="margin: 0; position: relative; top: 50%; -ms-transform: translateY(-50%); transform: translateY(-50%);" src="/static/' + 
                product_img + '"></a></div>' +
                '<div class="product-name"><a href="' + "/shopping/detail/" + pk + '">' + title + '</a></div>' +
                '<div class="about">' +
                '<div class="rating"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star.svg"><img src="/static/assets/img/star-half-empty.svg"><img src="/static/assets/img/star-empty.svg"></div>' +
                '<div class="price">' +
                '<h3>' + Number(price).toFixed(1) + '$</h3>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>')
}

function renderData(){
    // console.log("type of data:"+typeof(pageData))
    // console.log(pageData)

    for(var i = (current_page-1) * records_per_page; (i <= current_page * records_per_page - 1)
    && i < pageData.length; i++){
        var item = pageData[i] 
        var pk,title,price,product_img;

        pk = item.id;
        title = item.title;
        price = item.price;
        product_img = item.product_img;

        // console.log(pk, title, price, product_img)
        appendData(pk,title,price,product_img)
    }
}

function loadPage(chosenPage){
    $('html, body').animate({ scrollTop: 0 }, 'fast');
    setTimeout(function(){
        //do what you need here
        
    var ele
    var eles = document.getElementById("pagi").getElementsByTagName('li');

    for(let i = 0; i < eles.length; i ++){
        if(eles[i].value == chosenPage) {
            ele = eles[i]
            console.log("find")
        }
    }

    console.log(ele)
    ele.className += " active"

    if (chosenPage != 1){
        $("#pagiItem[name='prev']").removeClass("disabled");
    }
    else{
        $("#pagiItem[name='prev']").addClass("disabled");
    }

    if (chosenPage < findNumPages()){
        $("#pagiItem[name='next']").removeClass("disabled");
    }
    else{
        $("#pagiItem[name='next']").addClass("disabled");
    }

    current_page = chosenPage;
    // console.log("current page: "+current_page);

    resetData("#product")
    
    for(var i = (current_page-1) * records_per_page; (i <= current_page * records_per_page - 1)
    && i < pageData.length; i++){
        var item = pageData[i] 
        var pk,title,price,product_img;
        
        pk = item.id;
        title = item.title;
        price = item.price;
        product_img = item.product_img;

        // console.log(pk, title, price, product_img)
        appendData(pk,title,price,product_img)
    }
    }, 1000);

}

function init(){
    //init
    var prep = document.getElementById('json-data').textContent;
    // console.log("prep from textContent: "+prep)

    var data = JSON.parse(prep);
    pageData = data;
    current_page = 1;
    // console.log("data from textContent:"+data)
    
    //reset products
    resetData('#product')
                    
    //reset pagination
    resetPagination()

    //render pagination
    renderPagination()

    //render new products
    renderData();
}

$(document).ready(function () {
    current_page = 1;

    $("#pagi").on('click', '#pagiItem', function(){
        // console.log("hehe")
        // console.log($(this).val()+" "+$(this).attr('name'))

        var page = Number($(this).val());
        var option = $(this).attr('name');

        //event here
        if(page != 0){
            if(page != current_page && page <= numPages){
                console.log("OK");

                //remove active before call addClass()
                $("#pagiItem.active").removeClass("active");
                // $(this).addClass("active")

                loadPage(page);
            }
        }
        else{
            if(option == 'prev' && current_page>1){
                // console.log("prev")                
                $("#pagiItem.active").removeClass("active");

                loadPage(current_page-1)
            }
            if(option == 'next' && current_page<numPages){
                // console.log("next")
                $("#pagiItem.active").removeClass("active");

                loadPage(current_page+1)
            }
        }
    })

    init()

    var csrfToken = $("input[name=csrfmiddlewaretoken]").val()

    $("#search").on('click', 'button', function () {
        var dataID = $(this).data('id') //dataID of the input
        // console.log(csrfToken)

        var searchQuery = $.trim($("#searchInfo").val())
        // console.log("search query: "+searchQuery)

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
                    // console.log(JSON.stringify(response));
                    var obj = jQuery.parseJSON(JSON.stringify(response)); //better JSON
                    // console.log(typeof obj)
                    // console.log(obj)
                    
                    var data = JSON.parse(obj);
                    console.log("prep from obj: "+obj)
                    // console.log("data from object:"+data)
                    
                    pageData = data;
                    clean(data);
                    current_page = 1;
                    // const productList = document.querySelectorAll('#productlist') //get all element with id 'productList'

                    //reset products
                    resetData('#product')
                    
                    //reset pagination
                    resetPagination()

                    //render pagination
                    renderPagination()

                    //render new products
                    renderData();

                    // const category_inputs = document.querySelectorAll('#category0') //get all element with above id
                    // category_inputs.forEach(function (category_input) {
                    //     // $(product).remove() //remove all
                    //     // console.log("hehe")
                    //     $(category_input).prop('checked', true) //set all #category 0 to 'checked'
                    // })

                    $('#category0').prop('checked', true)
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
                // console.log(JSON.stringify(response));
                var obj = jQuery.parseJSON(JSON.stringify(response)); //better JSON

                // console.log(typeof obj)
                // console.log(obj)

                var data = JSON.parse(obj);
                pageData = data;

                clean(data);
                current_page = 1;
                // const productList = document.querySelectorAll('#productlist') //get all element with id 'productList'

                //reset products
                resetData('#product')
                
                //reset pagination
                resetPagination()

                //render pagination
                renderPagination()

                //render new products
                renderData();

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
                // console.log(JSON.stringify(response));
                var obj = jQuery.parseJSON(JSON.stringify(response)); //better JSON

                // console.log(typeof obj)
                // console.log(obj)

                var data = JSON.parse(obj);
                pageData = data;
                
                clean(data);
                current_page = 1;
                // const productList = document.querySelectorAll('#productlist') //get all element with id 'productList'

                //reset products
                resetData('#product')
                
                //reset pagination
                resetPagination()

                //render pagination
                renderPagination()

                //render new products
                renderData();

                $("#searchInfo").val("")
            }
        })
    })
})