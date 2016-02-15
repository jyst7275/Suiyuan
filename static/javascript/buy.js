/**
 *
 * Created by maxxie on 16-2-13.
 */
var all_selected = true;
get_cart();

$.extend({
    StandardPost:function(url,args){
    //        var temp = document.createElement("form");
    //temp.action = url;
    //temp.method = "post";
    //temp.style.display = "none";
    //for (var x in params) {
    //    var opt = document.createElement("input");
    //    opt.name = x;
    //    opt.value = params[x];
    //    temp.appendChild(opt);
    //}
    //    var cs = document.createElement("input");
    //    cs.name = "csrfmiddlewaretoken";
    //    cs.value = Cookies.get('csrftoken');
    //    temp.appendChild(cs);
    //document.body.appendChild(temp);
    ////temp.submit();
    //return temp;
        var form = $("<form id='request-form' method='post'></form>"),
            input;
        form.attr({"action":url});
        $.each(args,function(key,value){
            input = $("<input type='hidden'>");
            input.attr({"name":key});
            input.val(value);
            form.append(input);
        });
        input = $("<input type='hidden'>");
        input.attr({"name":'csrfmiddlewaretoken'});
        input.val(Cookies.get('csrftoken'));
        form.append(input);
        $('body').append(form);
        document.getElementById('request-form').submit();
    }
});
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
    }
});

function get_cart(){
    var cart_now = Cookies.getJSON('cart');
    if(!cart_now) {
        Cookies.set('cart', {}, {expires:30});
        cart_now = {}
    }
    return cart_now;
}
function add_to_cart(product_index, number){
    var cart_now = get_cart();

    if(cart_now.hasOwnProperty(product_index)) {
        if(!cart_now[product_index])
            cart_now[product_index] = number;
        else
            cart_now[product_index] = number + cart_now[product_index];
    }
    else{
        cart_now[product_index] = number;
    }
    Cookies.set('cart',cart_now);
}
function remove_cart(product_index){
    var cart_now = get_cart();
    delete cart_now[product_index];
    Cookies.set('cart',cart_now);
}

$('.buy-product').click(function(){
    var code = $(this).attr('data-buy');
    var number = Number($('#number-box').val());
    add_to_cart(code,number);
    $('#after-buy').reveal({
        animation:'fadeAndPop',
        animationspeed:300,
        closeonbackgroundclick:true,
        dismissmodalclass:'close-reveal-model'
    });
});
$('.buy-product-one').click(function(){
    var code = $(this).attr('data-buy');
    add_to_cart(code,1);
    $('#after-buy').reveal({
        animation:'fadeAndPop',
        animationspeed:300,
        closeonbackgroundclick:true,
        dismissmodalclass:'close-reveal-model'
    });
});

function refreshSingle(product_index){
    var change_elem = $('#cart-list').children('[data-id='+product_index +']').children('.cart-product-detail');
    var price = Number(change_elem.children('.cart-bar-price').text());
    var number = Number(change_elem.children('.cart-bar-number').children('input').val());
    change_elem.children('.cart-bar-price-total').text((price*number).toFixed(1));
}

function refreshTotal(){
    var child = $('#cart-list').children().first();
    var total = 0;
    var total_number = 0;
    while(child.length != 0){
        var elem = child.children('.cart-product-detail');
        var selected = child.attr('data-check');
        child = child.next();
        if(selected == "false")
            continue;
        total += Number(elem.children('.cart-bar-price-total').text());
        total_number += Number(elem.children('.cart-bar-number').children('input').val());

    }
    $('#cart-total-price').children('span').text('￥' + total.toFixed(1));
    $('#cart-total-count').children('span').text(total_number);
}

function selectOne(elem, to){
    elem.attr('data-check',to);
    if(!to)
        elem.children('.cart-product-detail').children('.cart-bar-all').children('span').children('input').removeAttr('checked');
    else
        elem.children('.cart-product-detail').children('.cart-bar-all').children('span').children('input').prop('checked',true);
}
function setTwo(to){
    if(!to)
        $('.cart-select-all').children('span').children('input').removeAttr('checked');
    else
        $('.cart-select-all').children('span').children('input').prop('checked',true);
    all_selected = to;
}
function getAllSelect(){
    var return_var = true;
    $('#cart-list').children().each(function(){
        if($(this).attr('data-check') == "false") {
            return_var = false;
            return false;
        }
    });
    return return_var;
}
$('.cart-select-all').click(function(){
    var to = true;
    if(all_selected)
        to = false;
    var child = $('#cart-list').children().first();
    while(child.length!=0){
        selectOne(child,to);
        child = child.next();
    }
    setTwo(to);
    refreshTotal();
});

$('.product-select-box').click(function(){
    var pr_id = $(this).attr('data-target');
    var now = $('#cart-list').children('[data-id=' + pr_id + ']').attr('data-check');
    if(now == "true") {
        $('#cart-list').children('[data-id=' + pr_id + ']').attr('data-check', false);
        setTwo(false);
    }
    else {
        $('#cart-list').children('[data-id=' + pr_id + ']').attr('data-check', true);
        setTwo(getAllSelect());
    }
    refreshTotal();
});

$('.cart-footer-delete').click(function(){
    $('#cart-list').children().each(function(){
        var selected = $(this).attr('data-check');
        if(selected == "true") {
            $(this).remove();
            remove_cart($(this).attr('data-id'));
        }
    });
    refreshTotal();
    setTwo(getAllSelect());
});

function closeWindow(){
    $('.reveal-modal-bg').trigger('click');
}

function add_address(){
    $('#add-address').reveal({
        animation:'fadeAndPop',
        animationspeed:300,
        closeonbackgroundclick:true,
        dismissmodalclass:'close-reveal-model'
    });
}

$('body').on('click', '.address-remove-btn', function(){
    var id = $(this).parent().parent().attr('data-id');
    var father = $(this).parent().parent();
    $.ajax({
        url:'/v1/user/address/' + id + '/',
        type:'DELETE',
        data:{},
        success:function(){
            alert('a');
            father.remove();
        }
    });
});

$('#add-address-submit').click(function(){
    $.ajax({
        url:'/v1/user/address/',
        type:'POST',
        data:{
            name:$('#add-address input[name=address-username]').val(),
            province:$('#add-address input[name=address-province]').val(),
            city:$('#add-address input[name=address-city]').val(),
            country:$('#add-address input[name=address-country]').val(),
            detail:$('#add-address textarea[name=address-detail]').val(),
            cellphone:$('#add-address input[name=address-cellphone]').val()
        },
        success:function(return_data){
            var data = $.parseJSON(return_data);
            $('#address-list').append('<li data-id=' + data.address_id +'>\
                <div class="address-edit">\
                    <a class="address-edit-btn" href="javascript:void(0)">编辑</a>\
                    <a class="address-remove-btn" href="javascript:void(0)">删除</a>\
                </div>\
                <div class="address-short address-selected">'+ data.short +'</div>\
                <div class="address-name">' + data.name + '</div>\
                <div class="address-long">' + data.long + '</div>\
                <div class="address-cellphone">' + data.cellphone + '</div>\
            </li>');
        }
    });
    $('.reveal-modal-bg').trigger('click');
});

$('#edit-address-submit').click(function(){
    var id = $('#edit-address').attr('data-id');
        $.ajax({
        url:'/v1/user/address/' + id + '/',
        type:'PUT',
        data:{
            name:$('#edit-address input[name=address-username]').val(),
            province:$('#edit-address input[name=address-province]').val(),
            city:$('#edit-address input[name=address-city]').val(),
            country:$('#edit-address input[name=address-country]').val(),
            detail:$('#edit-address textarea[name=address-detail]').val(),
            cellphone:$('#edit-address input[name=address-cellphone]').val()
        },
        success:function(return_data){
            var data = $.parseJSON(return_data);
            $('#address-list > li[data-id=' + id + ']').replaceWith('<li data-id=' + data.address_id +'>\
                <div class="address-edit">\
                    <a class="address-edit-btn" href="javascript:void(0)">编辑</a>\
                    <a class="address-remove-btn" href="javascript:void(0)">删除</a>\
                </div>\
                <div class="address-short address-selected">'+ data.short +'</div>\
                <div class="address-name">' + data.name + '</div>\
                <div class="address-long">' + data.long + '</div>\
                <div class="address-cellphone">' + data.cellphone + '</div>\
            </li>');
        }
    });
    $('.reveal-modal-bg').trigger('click');
});

$('#order-confirm-btn').click(function(){
    var id_list = [];
    var count_list = [];
    if(!check_address())
        return;
    $('#order-list').children().each(function(){
        id_list.push($(this).attr('data-id'));
        count_list.push($(this).attr('data-count'));
    });
    $.StandardPost('/order/request/',{
        id:id_list,
        count:count_list,
        address:$('#address-list').attr('data-selected')
    });
});

$('body').on('click', '.address-short',function(){
        var parent = $(this).parent().parent();
    var id = $(this).parent().attr('data-id');
    parent.children('.address-selected').removeClass('address-selected');
    parent.children('[data-id=' + id + ']').addClass('address-selected');
    parent.attr('data-selected',id);
    check_address();
});

function request_order(){
    var id_list = [];
    var count_list = [];
    $('#cart-list').children().each(function(){
        if($(this).attr('data-check') == 'true') {
            id_list.push($(this).attr('data-id'));
            count_list.push($(this).find('.cart-number-box').val());
        }
    });
    $.StandardPost('/order/confirm/',{
        id:id_list,
        count:count_list
    });
}

function check_address(){
    var bool = true;
    if($('#address-list').attr('data-selected') == "" || ! $('#address-list').attr('data-selected'))
        bool = false;
    if(!bool)
        $('#address-no-reminder').fadeIn(500);
    else
        $('#address-no-reminder').fadeOut(500);
    return bool;
}

$('.window-cancel').click(closeWindow);

$('body').on('click','.address-edit-btn', function(){
    var id = $(this).parent().parent().attr('data-id');
    $.ajax({
        url:'/v1/user/address/' + id + '/',
        type:'GET',
        success:function(data){
            var data_json = $.parseJSON(data);
            $('#edit-address input[name=address-username]').val(data_json.name);
            $('#edit-address input[name=address-province]').val(data_json.province);
            $('#edit-address input[name=address-city]').val(data_json.city);
            $('#edit-address input[name=address-country]').val(data_json.country);
            $('#edit-address textarea[name=address-detail]').val(data_json.detail);
            $('#edit-address input[name=address-cellphone]').val(data_json.cellphone);
            $('#edit-address').attr('data-id',id);
        }
    });
   $('#edit-address').reveal({
        animation:'fadeAndPop',
        animationspeed:300,
        closeonbackgroundclick:true,
        dismissmodalclass:'close-reveal-model'
    });
});