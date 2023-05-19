(function ($) {
	"use strict";


/*=============================================
	=          Windows OnLoad               =
=============================================*/
$(window).on('load', function () {
	preloader();
	mainSlider();
});


/*=============================================
	=    		 Preloader			      =
=============================================*/
function preloader() {
	$('#preloader').delay(0).fadeOut();
};


/*=============================================
	=          One page Menu               =
=============================================*/
$('.navigation a[href*="#"]:not([href="#"])').on("click", function() {
	if (location.pathname.replace(/^\//, "") == this.pathname.replace(/^\//, "") && location.hostname == this.hostname) {
		var target = $(this.hash);
		target = target.length ? target : $('[name=" + this.hash.slice(1) + "]');
		if (target.length) {
			if ($(window).width() < 768) {
				$("html, body").animate({
					scrollTop: target.offset().top - 70
				}, 1000, "easeInOutExpo");
			} else {
				$("html, body").animate({
					scrollTop: target.offset().top - 80
				}, 1000, "easeInOutExpo");
			}
			return false;
		}
	}
});

/*=============================================
	=    		Mobile Menu			      =
=============================================*/
//SubMenu Dropdown Toggle
if ($('.menu-area li.menu-item-has-children ul').length) {

	$('.menu-area .navigation li.menu-item-has-children').append('<div class="dropdown-btn"><span class="fas fa-angle-down"></span></div>');

}

//Mobile Nav Hide Show
if ($('.mobile-menu').length) {

	//Dropdown Button
	$('.mobile-menu li.menu-item-has-children .dropdown-btn').on('click', function () {
		$(this).toggleClass('open');
		$(this).prev('ul').slideToggle(500);
	});
	//Menu Toggle Btn
	$('.mobile-nav-toggler').on('click', function () {
		$('body').addClass('mobile-menu-visible');
	});

	//Menu Toggle Btn
	$('.menu-backdrop, .mobile-menu .close-btn, .mobile-menu .navigation li a').on('click', function () {
		$('body').removeClass('mobile-menu-visible');
	});
}


/*=============================================
	=          Data Background               =
=============================================*/
$("[data-background]").each(function () {
	$(this).css("background-image", "url(" + $(this).attr("data-background") + ")")
})

/*=============================================
	=           Data Color             =
=============================================*/
$("[data-bg-color]").each(function () {
	$(this).css("background-color", $(this).attr("data-bg-color"));
});


/*=============================================
	=            Header Search            =
=============================================*/
$(".header-search > a").on('click', function () {
	$(".search-popup-wrap").slideToggle();
	$('body').addClass('search-visible');
	return false;
});

$(".search-backdrop").on('click', function () {
	$(".search-popup-wrap").slideUp(500);
	$('body').removeClass('search-visible');
});


/*=============================================
	=     Menu sticky & Scroll to top      =
=============================================*/
$(window).on('scroll', function () {
	var scroll = $(window).scrollTop();
	if (scroll < 245) {
		$("#sticky-header").removeClass("sticky-menu");
		$('.scroll-to-target').removeClass('open');
		$("#header-top-fixed").removeClass("header-fixed-position");

	} else {
		$("#sticky-header").addClass("sticky-menu");
		$('.scroll-to-target').addClass('open');
		$("#header-top-fixed").addClass("header-fixed-position");
	}
});


/*=============================================
	=    		 Scroll Up  	         =
=============================================*/
if ($('.scroll-to-target').length) {
  $(".scroll-to-target").on('click', function () {
    var target = $(this).attr('data-target');
    // animate
    $('html, body').animate({
      scrollTop: $(target).offset().top
    }, 1000);

  });
}


/*=============================================
	=          OffCanvas Active            =
=============================================*/
$('.navSidebar-button').on('click', function () {
	$('body').addClass('offcanvas-menu-visible');
	return false;
});

$('.offCanvas-overlay, .offCanvas-toggle').on('click', function () {
	$('body').removeClass('offcanvas-menu-visible');
});


/*=============================================
	=    		 Main Slider		      =
=============================================*/
function mainSlider() {
	var BasicSlider = $('.slider-active');
	BasicSlider.on('init', function (e, slick) {
		var $firstAnimatingElements = $('.single-slider:first-child').find('[data-animation]');
		doAnimations($firstAnimatingElements);
	});
	BasicSlider.on('beforeChange', function (e, slick, currentSlide, nextSlide) {
		var $animatingElements = $('.single-slider[data-slick-index="' + nextSlide + '"]').find('[data-animation]');
		doAnimations($animatingElements);
	});
	BasicSlider.slick({
		autoplay: false,
		autoplaySpeed: 10000,
		dots: false,
		fade: true,
		arrows: false,
		responsive: [
			{ breakpoint: 767, settings: { dots: false, arrows: false } }
		]
	});

	function doAnimations(elements) {
		var animationEndEvents = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
		elements.each(function () {
			var $this = $(this);
			var $animationDelay = $this.data('delay');
			var $animationType = 'animated ' + $this.data('animation');
			$this.css({
				'animation-delay': $animationDelay,
				'-webkit-animation-delay': $animationDelay
			});
			$this.addClass($animationType).one(animationEndEvents, function () {
				$this.removeClass($animationType);
			});
		});
	}
}


/*=============================================
	=            Blog Active               =
=============================================*/
$('.blog-thumb-active').slick({
	dots: false,
	infinite: true,
	arrows: true,
	speed: 1500,
	slidesToShow: 1,
	slidesToScroll: 1,
	fade: true,
	prevArrow: '<button type="button" class="slick-prev"><i class="fas fa-arrow-left"></i></button>',
	nextArrow: '<button type="button" class="slick-next"><i class="fas fa-arrow-right"></i></button>',
});

/*=============================================
	=    		Isotope	Active  	      =
=============================================*/
$('.grid').imagesLoaded(function () {
	// init Isotope
	var $grid = $('.grid').isotope({
		itemSelector: '.grid-item',
		percentPosition: true,
		masonry: {
			columnWidth: '.grid-item',
		}
	});

});


})(jQuery);

jQuery(document).ready(function ($) {
  $('.home-shop-active').slick({
    dots: true,
    infinite: true,
    speed: 1000,
    autoplay: true,
    arrows: true,
    slidesToShow: 4,
    prevArrow: '<button type="button" class="slick-prev"><i class="flaticon-left-arrow"></i></button>',
    nextArrow: '<button type="button" class="slick-next"><i class="flaticon-right-arrow"></i></button>',
    slidesToScroll: 1,
    responsive: [
      {
      breakpoint: 1500,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: true,
        }
      },
      {
      breakpoint: 1200,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: true,
        }
      },
      {
      breakpoint: 992,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1
        }
      },
      {
      breakpoint: 767,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          arrows: true,
        }
      },
      {
      breakpoint: 575,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          arrows: false,
        }
      },
    ]
  });
  
    $(".brand-active").slick({
        dots: false,
        infinite: true,
        speed: 1000,
        autoplay: true,
        arrows: false,
        slidesToShow: 6,
        slidesToScroll: 2,
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 5,
                    slidesToScroll: 1,
                    infinite: true,
                },
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 1,
                },
            },
            {
                breakpoint: 767,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    arrows: false,
                },
            },
            {
                breakpoint: 575,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    arrows: false,
                },
            },
        ],
    });

    $("[data-background]").each(function () {
        $(this).css(
            "background-image",
            "url(" + $(this).attr("data-background") + ")"
        );
    });

    $("[data-bg-color]").each(function () {
        $(this).css("background-color", $(this).attr("data-bg-color"));
      });
    
      function easyPieChart() {
        $(".category-item").on("inview", function (event, isInView) {
          if (isInView) {
            $(".chart").easyPieChart({
              scaleLength: 0,
              lineWidth: 6,
              trackWidth: 6,
              size: 70,
              lineCap: "round",
              rotate: 360,
              trackColor: "#F4F4F4",
              barColor: "#FAA432",
            });
          }
        });
      }
      easyPieChart();

      $(function () {
        $(".accordion-collapse").on("show.bs.collapse", function () {
          $(this).parent().addClass("active-item");
          $(this).parent().prev().addClass("prev-item");
        });
  
        $(".accordion-collapse").on("hide.bs.collapse", function () {
          $(this).parent().removeClass("active-item");
          $(this).parent().prev().removeClass("prev-item");
        });
      });

      $('input').each(function (){
        $(this).on('input', function(){
          if(!this.checkValidity()){
            this.setCustomValidity($(this).attr('title'))
          }else{
            this.setCustomValidity("");
          }
        })
      })

      $('select').each(function (){
        $(this).on('change', function(){
          if(!this.checkValidity()){
            this.setCustomValidity($(this).attr('title'))
      
          }else{
            this.setCustomValidity("");
          }
        })       
      })

      $('textarea').each(function (){
        $(this).on('input', function(){
          if(!this.checkValidity()){
            this.setCustomValidity($(this).attr('title'))
      
          }else{
            this.setCustomValidity("");
          }
        }) 
      })


      $('.phone-input').on('input', (e)=>{
        if(!validatePhoneNumber($(e.currentTarget).val())){
          $(e.currentTarget).addClass('is-invalid')
          e.currentTarget.setCustomValidity($(e.currentTarget).attr('title'));
          $('.phone-help-text').addClass('text-danger')
        }else{
          $(e.currentTarget).removeClass('is-invalid')
          e.currentTarget.setCustomValidity("");
          $('.phone-help-text').removeClass('text-danger')
        }
      })
    
      function validatePhoneNumber(input_str) {
        return /^\+?1?\d{9,15}$/.test(input_str);
      }
});