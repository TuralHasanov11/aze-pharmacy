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
});