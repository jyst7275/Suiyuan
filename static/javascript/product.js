/**
 * Created by maxxie on 16-2-7.
 */
$('.product-pic-list ul li').hover(function(){
    $('.product-detail-img > img').attr('src', $(this).children('img').first().attr('src'));
});

$('#box-add').click(function(){
    $('#number_box').val(Number($('#number_box').val()) + 1);
});
$('#box-minus').click(function(){
    var to = Number($('#number_box').val()) - 1;
    if(to < 0)
        to = 0;
    $('#number_box').val(to);
});