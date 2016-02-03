/**
 * Created by maxxie on 16-1-28.
 */
$(window).scroll(function(){
　　var scrollTop = $(this).scrollTop();
　　var scrollHeight = $(document).height();
　　var windowHeight = $(this).height();
　　if(scrollTop + windowHeight == scrollHeight){
      $('.app-detail-bar').css('visibility','visible');
　　  $('.app-detail-bar').removeClass('animated slideOutRight');
　　  $('.app-detail-bar').addClass('animated slideInRight');
　　}else{
        $('.app-detail-bar').addClass('visibility','hidden');
      $('.app-detail-bar').removeClass('animated slideInRight');
      $('.app-detail-bar').addClass('animated slideOutRight');
  }

});