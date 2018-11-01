  $(document).ready(function () {
      var stickyHeaderTop = $('#accordion').offset().top;
      // var stickyHeaderTop = $('#nav').offset().bottom;
      console.log(stickyHeaderTop);
      $(window).scroll(function(){
              if( $(window).scrollTop() > stickyHeaderTop -47) {
                      $('#accordion').css({position: 'fixed', top: '40px'});
              } else {
                      $('#accordion').css({position: 'static', top: '0px'});
              }
      });
    });
