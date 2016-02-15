/**
 * Created by maxxie on 16-2-7.
 */
$('.product-pic-list ul li').hover(function(){
    $('.product-detail-img > img').attr('src', $(this).children('img').first().attr('src'));
});

$('.box-add').click(function(){
    var target = $('#' + $(this).attr('data-target'));
    target.val(Number(target.val()) + 1);
});
$('.box-minus').click(function(){
    var target = $('#' + $(this).attr('data-target'));
    var to = Number(target.val()) - 1;
    if(to <= 1)
        to = 1;
    target.val(to);
});
function check_set_cart(pr_id, number){
    var cart_now = get_cart();
    if(number <= 0)
        delete cart_now[pr_id];
    else
        cart_now[pr_id] = Number(number);
    Cookies.set('cart',cart_now);
    refreshSingle(pr_id);
    refreshTotal();
}
$('.cook-change').click(function(){
    var pr_id = $(this).attr('data-target');
    var target = $('#' + pr_id);
    var number = target.val();
    check_set_cart(pr_id,number);
});

$('.cart-product-delete').click(function(){
    var pr_id = $(this).attr('data-target');
    $('#cart-list').children('[data-id=' + pr_id + ']').remove();
    remove_cart(pr_id);
    refreshTotal();
    setTwo(getAllSelect());
});

$("body").on("propertychange input", ".cart-number-box", function () {
    var pr_id = $(this).attr('id');
    var num = Number($(this).val().replace(/\D/g,''));
    if(!(num > 0))
        num = 1;
    else if(num > 100)
        num = 99;
    $(this).val(num);
    check_set_cart(pr_id,num);
});