/**
 * Created by maxxie on 16-1-24.
 */
var compan = false;
var bar_transparent = true;
var app_com_readmore = false;
var app_news_date_list = false;

var app_carousel_click = false;
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

$('#bar_search').click(function(){
    $('.search-container').css('display','block');
    $('.search-container').removeClass('animated fadeOutDown');
    $('.search-container').addClass('animated fadeInDown');
});

$('#search-remove').click(function(){
    $('.search-container').removeClass('animated fadeInDown');
    $('.search-container').addClass('animated fadeOutDown');
});