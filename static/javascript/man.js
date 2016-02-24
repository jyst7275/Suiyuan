/**
 * Created by maxxie on 16-1-24.
 */
var compan = false;
var bar_transparent = true;
var app_com_readmore = false;
var app_news_date_list = false;
var last_scroll_top = document.body.scrollTop|document.documentElement.scrollTop;
var bar_show = true;
var app_carousel_click = false;
var countdown = 0;
$('#app-com-btn').click(function(){
    if(compan) {
        $('#app-com-panel').fadeOut(100);
        compan = false;
    }
    else {
        $('#app-com-panel').fadeIn(100);
        compan = true;
    }
});

$('.app-about-com-con a').click(function(){
    if(app_com_readmore) {
        $('.app-com-readmore').slideUp(500);
        $('.app-about-com-con a i').attr('class','fa fa-plus');
        $('.app-about-com-con a span').html('展开');
        app_com_readmore = false;
    }
    else{
        $('.app-com-readmore').slideDown(500);
        $('.app-about-com-con a i').attr('class','fa fa-minus');
        $('.app-about-com-con a span').html('');
        app_com_readmore = true;
    }
});

$('.app-news-list-bar').click(function(){
    if(app_news_date_list){
        app_news_date_list = false;
        $('.app-news-bar-list').slideUp(500);
        $('.app-news-list-bar-icon i').attr('class','fa fa-plus');
    }
    else{
        app_news_date_list = true;
        $('.app-news-bar-list').slideDown(500);
        $('.app-news-list-bar-icon i').attr('class','fa fa-minus');
    }
});

setInterval(function(){
    if(app_carousel_click){
        app_carousel_click = false;
        return;
    }
    var thisElem = $('.app-carousel-list').children('.app-active');
    var thisIndi = $('.app-carousel-indicator-list').children('.app-active');
    var nextElem = thisElem.next();
    var nextIndi = thisIndi.next();
    if(nextElem.length==0)
        nextElem = $('.app-carousel-list').children().first();
    if(nextIndi.length == 0)
        nextIndi = $('.app-carousel-indicator-list').children().first();
    thisElem.removeClass('app-active animated fadeIn');
    thisIndi.removeClass('app-active');
    nextElem.addClass('app-active animated fadeIn');
    nextIndi.addClass('app-active');
    $('.app-product-head').css('background',nextElem.attr('data-bg-color'));
},8000);

setInterval(function(){
    var thisElem = $('.app-news-flow ul').children('.app-active');
    var nextElem = thisElem.next();
    if(nextElem.length==0)
        nextElem = $('.app-news-flow ul').children().first();
    thisElem.removeClass('app-active animated fadeIn');
    nextElem.addClass('app-active animated fadeIn');
},4000);

$('.app-carousel-indicator-point').click(function(){
    var nowElem = $('.app-carousel-list').children('.app-active');
    var nowIndi = $('.app-carousel-indicator-list').children('.app-active');
    var nextElem = $('.app-carousel-list').children().eq($(this).attr('data-slide-to'));
    nowElem.removeClass('app-active animated fadeIn');
    nowIndi.removeClass('app-active');
    nextElem.addClass('app-active animated fadeIn');
    $(this).addClass('app-active');
    app_carousel_click = true;
    $('.app-product-head').css('background',nextElem.attr('data-bg-color'));
});

$('.app-product-type-list li').hover(function(){
    var elem = $(this).children('.app-product-type-sidebar');
    elem.css('display','block');
},function(){
    var elem = $(this).children('.app-product-type-sidebar')
    elem.css('display','none');
});

$('.bar_search').click(function(){
    $('.search-container').css('display','block');
    $('.search-container').removeClass('animated fadeOutDown');
    $('.search-container').addClass('animated fadeInDown');
});

$('#search-remove').click(function(){
    $('.search-container').removeClass('animated fadeInDown');
    $('.search-container').addClass('animated fadeOutDown');
});

$(document).scroll(function(){
    var hi = document.body.scrollTop|document.documentElement.scrollTop;
    if(hi > last_scroll_top && hi >80 && bar_show) {
        $('.app-nav').removeClass('animation-move-down');
        $('.app-nav').addClass('animation-move-up');
    }
    else{
        $('.app-nav').removeClass('animation-move-up');
        $('.app-nav').addClass('animation-move-down');
    }
    last_scroll_top = hi;

});

function setPage(type, page){
    $.get('/v1/passage/'+ type + '/' + '?page='+page, function(data){
        $('.app-news-list-container').empty();
        if(data.count > 0) {
            for (var i = 0; i < data.count; i++) {
                if(data.results[i].img_url != "")
                $('.app-news-list-container').append('<li class="app-news-container"> \
                <img src=' + data.results[i].img_url + ' alt=""> \
                <div class="app-news-text"> \
                <h4>' + data.results[i].pass_title + '</h4> \
                    <div class="app-news-date">' + data.results[i].pub_date + '</div> \
                <div>' + data.results[i].pass_summery + '</div> \
                <hr style="border-top: solid 1px #5596e6"> \
                    <i class="fa fa-book fa-lg" style="color: #337ab7"></i><a class="app-news-text-more" href=' + data.results[i].pass_url + '>阅读新闻</a>\
                    </div></li>');
                else
                $('.app-news-list-container').append('<li class="app-news-container"> \
                <div class="app-news-text"> \
                <h4>' + data.results[i].pass_title + '</h4> \
                    <div class="app-news-date">' + data.results[i].pub_date + '</div> \
                <div>' + data.results[i].pass_summery + '</div> \
                <hr style="border-top: solid 1px #5596e6"> \
                    <i class="fa fa-book fa-lg" style="color: #337ab7"></i><a class="app-news-text-more" href=' + data.results[i].pass_url + '>阅读新闻</a>\
                    </div></li>');
            }
            $('.app-news-pageguide').attr('data-page', page);
        }
        else{
            $('.app-news-list-container').append('<p>没有相关信息</p>')
        }
    });
}

function setPageBar(page_now){
    var page_max = $('.app-news-pageguide').attr('data-max');
    if(page_now <= 1)
        $('#app-news-page-prev').css('display', 'none');
    else
        $('#app-news-page-prev').css('display', 'block');
    if(page_now >= page_max)
        $('#app-news-page-next').css('display', 'none');
    else
        $('#app-news-page-next').css('display', 'block');
    $('.app-news-pageguide').attr('data-page', page_now);
}

function refreshPageBar(page_max){
    $('.app-news-pageguide .pagination').empty();
    if(page_max >= 1)
    $('.app-news-pageguide .pagination').append('<li><a style="display: none;" id="app-news-page-prev" href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>');
    for(var i = 0;i < page_max;i ++){
        $('.app-news-pageguide .pagination').append('<li class="app-news-page-btn" data-target=' + (i+1) + '><a href="javascript:void(0)">' + (i+1) + '</a></li>');
    }
    if(page_max > 1)
    $('.app-news-pageguide .pagination').append('<li><a id="app-news-page-next" href="javascript:void(0)" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>');
}

$('.app-new-bar-li').click(function(){
   var type = $(this).attr('data-type');
    setPage(type, 1);
    $('.app-new-bar-list').children('.app-active').removeClass("app-active");
    $(this).addClass('app-active');
        $.get('/v1/passage/' + type + '/' + "?max_page", function(data){
        refreshPageBar(data);
    });
    $('html,body').animate({scrollTop:$('#app-news-bar').offset().top}, 800);
    $('.app-news-type-'+$('.app-news-list-head').children('.app-active').attr('data-type')).removeClass("app-active");
    $('.app-news-type-'+$(this).attr('data-type')).addClass('app-active');
});

$('.app-news-list-head li').click(function(){
    var type = $(this).attr('data-type');
    setPage(type, 1);
    $('.app-news-type-'+$('.app-news-list-head').children('.app-active').attr('data-type')).removeClass("app-active");
    $('.app-news-type-'+$(this).attr('data-type')).addClass('app-active');

    //change bar
    $.get('/v1/passage/' + type + '/' + "?max_page", function(data){
        refreshPageBar(data);
    });
});

$('.preload-image').click(function(){
   document.getElementById('suiyuan-video').play();
    $('.preload-image').css('display','none');
});
$('#say-more').click(function(){
   $('#app-say-2').fadeIn(800);
    $(this).css('display','none');
    $('#say-more-arrow i').attr('class','fa fa-angle-double-up fa-2x app-icon-down app-icon-moving-down');
});
$('body').on('click', function(){
    var page = $(this).attr('data-target');
    var type = $('.app-news-list-head').attr('data-type');
    setPage(type, page);
    setPageBar(page);
});

$('#app-news-page-next').click(function(){
    var page = $('.app-news-pageguide').attr('data-page');
    var type = $('.app-news-list-head').attr('data-type');
    setPage(type, Number(page) + 1);
    setPageBar(Number(page) + 1)
});

$('#app-news-page-prev').click(function(){
    var page = $('.app-news-pageguide').attr('data-page');
    var type = $('.app-news-list-head').attr('data-type');
    setPage(type, Number(page) - 1);
    setPageBar(Number(page) - 1);
});

function set_countdown(){
    if(countdown == 0){
        $('#checkcode-btn').removeClass('checked');
        $('#checkcode-btn').text('点击获取验证码');
    }
    else{
        countdown -= 1;
        $('#checkcode-btn').text(countdown + 's 后重新获取');
        setTimeout(function(){
            set_countdown();
        },1000);
    }
}

function get_check_code(){
    if(countdown == 0) {
        var cellphone_input = $('#login-form input[name=cellphone]').val();
        var cellphone_rep = /^0?1[3|4|5|8][0-9]\d{8}$/;
        if(!cellphone_rep.test(cellphone_input)){
            alert('号码错误！');
            return;
        }
        $.ajax({
            url: '/v1/user/sendcode/' + cellphone_input + '/',
            type: 'POST',
            success: function (data) {
                var data_json = $.parseJSON(data);
            },
            error:function(a, b,c){
                alert("号码错误或请求间隔小于60s");
            }
        });
        $('#checkcode-btn').addClass('checked');
        countdown = 60;
        set_countdown()
    }
}




$('#checkcode-btn').click(get_check_code);

$('.myorder-detail-address').hover(function(){
   $(this).next().css('display','block');
}, function(){
    $(this).next().css('display','none');
});

$('.search-btn').click(function(){
   var search = $(this).parent().children('.search-class').val();
    location.href='/search?search=' + search;
});