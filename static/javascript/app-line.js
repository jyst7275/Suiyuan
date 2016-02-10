/**
 * Created by maxxie on 16-2-10.
 */

var now = 0;
$('.line-section').waypoint(function(direction){
    if(direction == 'down') {
        $('#line-section-' + now + ' .line-frame').removeClass('app-fixed');
        $('#line-section-' + now + ' .line-frame').addClass('bottom-zero');
    }
    else {
        $('#line-section-' + now + ' .line-frame').addClass('app-fixed');
         $('#line-section-' + now + ' .line-frame').removeClass('bottom-zero');
    }
},{
    offset:'100%'
});

$('#line-section-1').waypoint(function(direction){
        if(direction == "down") {
            now = 1;
            $('#line-section-1 .line-frame').addClass('app-fixed');
        }
        else{
            $('#line-section-1 .line-frame').removeClass('app-fixed');
            now = 0;
        }

});
$('#line-section-2').waypoint(function(direction){
        if(direction == "down") {
            now = 2;
            $('#line-section-2 .line-frame').addClass('app-fixed');
        }
        else{
            $('#line-section-2 .line-frame').removeClass('app-fixed');
            now = 1;
        }

});
$('#line-section-3').waypoint(function(direction){
        if(direction == "down") {
            now = 3;
            $('#line-section-3 .line-frame').addClass('app-fixed');
        }
        else{
            $('#line-section-3 .line-frame').removeClass('app-fixed');
            now = 2;
        }

});
$('#line-section-4').waypoint(function(direction){
        if(direction == "down") {
            now = 4;
            $('#line-section-4 .line-frame').addClass('app-fixed');
        }
        else{
            $('#line-section-4 .line-frame').removeClass('app-fixed');
            now = 3;
        }

});
$('.line-frame').css('height', window.innerHeight);
$('.line-frame').css('width', window.innerWidth);

$(document).scroll(function(){
    var scroll_now = document.body.scrollTop;
    if(now == 1) {
        var off = scroll_now - $('#line-section-1').offset().top;
        if (off <= 50) {
            $('.dry-rake').css('left', '800px');
            $('.dirt-shadow').css('width', '540px');
        }
        else if (off <= 100) {
            $('.dry-rake').css('left', '700px');
            $('.dirt-shadow').css('width', '440px');
        }
        else if (off <= 150) {
            $('.dry-rake').css('left', '600px');
            $('.dirt-shadow').css('width', '340px');
        }
        else if (off <= 200) {
            $('.dry-rake').css('left', '500px');
            $('.dirt-shadow').css('width', '240px');
        }
        else if (off <= 250){
            $('.dry-rake').css('left', '400px');
            $('.dirt-shadow').css('width', '140px');
        }

        if(off <= 250){
            $('#line-section-1 .show-text').css('opacity','0');
            $('#line-section-1 .show-text').css('top','250px');
        }
        else if(off <= 300){
            $('#line-section-1 .show-text').css('opacity','0.3');
            $('#line-section-1 .show-text').css('top','230px');
        }
        else if(off <= 350){
            $('#line-section-1 .show-text').css('opacity','0.8');
            $('#line-section-1 .show-text').css('top','200px');
        }
        else if(off <= 400){
            $('#line-section-1 .show-text').css('opacity','1');
            $('#line-section-1 .show-text').css('top','170px');
        }
    }
    else if(now == 2){
        var off = scroll_now - $('#line-section-2').offset().top;


        if(off <= 200) {
            $('#dirt-plant-1').css('margin-top', '-460px');
            $('#dirt-plant-root-1').css('margin-top', '-350px');
        }
        else if(off <= 250) {
            $('#dirt-plant-1').css('margin-top', '-410px');
            $('#dirt-plant-root-1').css('margin-top', '-300px');
        }
        else if(off <= 300) {
            $('#dirt-plant-1').css('margin-top', '-310px');
            $('#dirt-plant-root-1').css('margin-top', '-200px');
        }
        else if(off > 300 && off <= 350) {
            $('#dirt-plant-1').css('margin-top', '-210px');
            $('#dirt-plant-root-1').css('margin-top', '-98px');
        }


        if(off <=500) {
            $('.dirt-hole').css('display','block');
            $('.dirt-hole-besides').css('display','block');
            $('.dirt-hole-besides-on').css('display', 'none');
        }
        else {
            $('#dirt-hole-2').css('display','none');
            $('#dirt-hole-3').css('display','none');
            $('#dirt-hole-besides-2').css('display','none');
            $('#dirt-hole-besides-3').css('display','none');
            if (off <= 600) {
                $('.dirt-plant').css('display', 'block');
                $('.dirt-plant-2').css('display', 'none');
            }
            else if (off <= 900) {
                $('.dirt-plant-2').css('display', 'block');
                $('#dirt-plant-2').css('display', 'none');
                $('#dirt-plant-3').css('display', 'none');
            }
        }
        if(off <= 900 && off > 600) {
            $('#dirt-plant-2-3').css('display', 'block');
            $('.dirt-plant-3').css('display', 'none');
        }
        else if(off > 900){
            $('#dirt-plant-2-3').css('display', 'none');
            $('.dirt-plant-3').css('display', 'block');
        }

        if(off <= 500)
            $('.sky-container .show-text').css('opacity', '0');
        else if(off <= 600)
            $('.sky-container .show-text').css('opacity', '0.3');
        else if(off <= 700)
            $('.sky-container .show-text').css('opacity', '0.6');
        else if(off <= 800)
            $('.sky-container .show-text').css('opacity', '0.8');
        else
            $('.sky-container .show-text').css('opacity', '1');

    }
    else if(now == 3){
        var off = scroll_now - $('#line-section-3').offset().top;

        if(off <= 50 ){
            $('.rice-prev').css('top', '80px')
        }
        else if(off <= 100 ){
            $('.rice-prev').css('top', '160px')
        }
        else if(off <= 150 ){
            $('.rice-prev').css('top', '240px')
        }
        else{
            $('.rice-prev').css('top', '350px')
        }

        if(off <= 300) {
            $('.machine-middle').css('display', 'block');
            $('.machine-middle-animated').css('display', 'none');
        }
        else {
            $('.machine-middle').css('display', 'none');
            $('.machine-middle-animated').css('display', 'block');
        }

        if(off <= 600){
            $('#line-section-3 .show-text .text-container').css('opacity','0');
        }
        else if(off <= 700){
            $('#line-section-3 .show-text .text-container').css('opacity','0.3');
        }
        else if(off <= 800){
            $('#line-section-3 .show-text .text-container').css('opacity','0.7');
        }
        else{
            $('#line-section-3 .show-text .text-container').css('opacity','1');
        }

        if(off <= 1500){
            $('.rice-next').css('margin-top', '-300px');
        }
        else if(off <=1600)
            $('.rice-next').css('margin-top', '-195px');
        else if(off <=1700)
            $('.rice-next').css('margin-top', '-90px');
        else if(off <=1800)
            $('.rice-next').css('margin-top', '15px');
        else
            $('.rice-next').css('margin-top', '120px');

        if(off > 1800)
            $('.rice-next').css('display', 'none');
        else
            $('.rice-next').css('display', 'block');
    }
    else if(now == 4){
        var off = scroll_now - $('#line-section-4').offset().top;
        if(off <= 100){
            $('.suiyuan-bag').css('transform','scale(1,1)');
            $('.suiyuan-bag').css('top','200px');
        }
        else if(off <= 200){
            $('.suiyuan-bag').css('transform','scale(0.9,0.9)');
            $('.suiyuan-bag').css('top','250px');
        }
        else if(off <= 300){
            $('.suiyuan-bag').css('transform','scale(0.8,0.8)');
            $('.suiyuan-bag').css('top','300px');
        }
        else{
            $('.suiyuan-bag').css('transform','scale(0.7,0.7)');
            $('.suiyuan-bag').css('top','350px');
        }

        if(off <= 400){
            $('#line-section-4 .show-text').css('opacity','0');
            $('#line-section-4 .show-text').css('top','130px');
        }
        else if(off <= 500){
            $('#line-section-4 .show-text').css('opacity','0.3');
            $('#line-section-4 .show-text').css('top','150px');
        }
        else if(off <= 600){
            $('#line-section-4 .show-text').css('opacity','0.8');
            $('#line-section-4 .show-text').css('top','170px');
        }
        else{
            $('#line-section-4 .show-text').css('opacity','1');
            $('#line-section-4 .show-text').css('top','190px');
        }

        if(off <= 600){
            $('.suiyuan-bag-ba').css('opacity',0);
            $('.suiyuan-bag-ba').removeClass('animated fadeIn');
        }
        else{
            $('.suiyuan-bag-ba').addClass('animated fadeIn');
        }

    }
});

$('#click-to-start').click(function(){
    $('html,body').animate({scrollTop:$('#line-section-1').offset().top}, 800);
});