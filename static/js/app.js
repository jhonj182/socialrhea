(function($) {
    "use strict";

    /*-------------------------------------
        Validar Upload Multiple Images
    -------------------------------------*/
    const imginput = document.querySelector('.js-imginput')
    const form = document.querySelector('.js-post-form')

    // Esto define lo que sucede cuando el usuario intenta enviar los datos.
    if (imginput){
    imginput.addEventListener("change", function(e){
      let fileInput = imginput;
      let filePath = fileInput.value;
      console.log( fileInput.files);
      var allowedExtensions = /(.jpg|.jpeg|.png|.gif)$/i;
      if(!allowedExtensions.exec(filePath)){
          alert('Please upload file having extensions .jpeg/.jpg/.png/.gif only.');
          fileInput.value = '';
          return false;
      }else{
        let i = 0
        
          //Image preview
          if (fileInput.files) {
              var cadena = ""
              var filesAmount = fileInput.files.length;
              for (i = 0; i < filesAmount; i++) {
                var reader = new FileReader();
                reader.onload = function(e) {
                  var div = document.createElement("div");
                  div.classList.add('img-preview')
                  var img = document.createElement('img');
                  img.src = e.target.result
                  div.appendChild(img);
                  document.getElementById('imagePreview').appendChild(div);
                };
                reader.readAsDataURL(fileInput.files[i]);
              }
          }
      }
    })
    form.addEventListener("submit", function (event) {
      event.preventDefault()
      let check = imginput.value.length;
      if (check > 0){
        alert("paso");
        form.submit();
      }
      const test = email.value.length === 0 || emailRegExp.test(email.value);
      if (!test) {
        email.className = "invalid";
        error.innerHTML = "I expect an e-mail, darling!";
        error.className = "error active";

        // Algunos navegadores antiguos no son compatibles con el método event.preventDefault ()
        return false;
      } else {
        email.className = "valid";
        error.innerHTML = "";
        error.className = "error";
      }
    });
  }
    /*-------------------------------------
        Login Form initiating
    -------------------------------------*/
    const login = document.querySelector(".js-loginform");
    var mensajes = ""
    $('.js-loginform').on('submit', (e)=>{
        e.preventDefault();
        if ($('.js-user').val().length > 0 && $('.js-pass').val().length > 0){
          login.submit();
        }else{
          alert('Debe ingresar un usuario y contraseña validos')
        }
    });

    function mostrarError(mensaje) {
      const errores = document.querySelectorAll('.error');
      const mensajeError = document.createElement('p');
      mensajeError.textContent = mensaje;
      mensajeError.classList.add('border', 'border-red-500', 'background-red-100', 'text-red-500', 'p-3', 'mt-5', 'text-center', 'error');
      console.log(mensajeError)
      login.appendChild(mensajeError)
      console.log(errores);
      if (errores.length === 0) {
          login.appendChild(mensajeError)
      }
  }
    /*-------------------------------------
    On Scroll 
    -------------------------------------*/
    $(window).on('scroll', function() {

        // Back Top Button
        if ($(window).scrollTop() > 500) {
            $('.scrollup').addClass('back-top');
        } else {
            $('.scrollup').removeClass('back-top');
        }
        // Sticky Header
        if ($('body').hasClass('sticky-header')) {
            var stickyPlaceHolder = $("#rt-sticky-placeholder"),
                menu = $("#header-menu"),
                menuH = menu.outerHeight(),
                topHeaderH = $('#header-topbar').outerHeight() || 0,
                middleHeaderH = $('#header-middlebar').outerHeight() || 0,
                targrtScroll = topHeaderH + middleHeaderH;
            if ($(window).scrollTop() > targrtScroll) {
                menu.addClass('rt-sticky');
                stickyPlaceHolder.height(menuH);
            } else {
                menu.removeClass('rt-sticky');
                stickyPlaceHolder.height(0);
            }
        }
    });

    /*---------------------------------------
    On Click Section Switch
    --------------------------------------- */
    $('[data-type="section-switch"]').on('click', function () {
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
            var target = $(this.hash);
            if (target.length > 0) {

                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });

    /*-------------------------------------
      Sidebar Toggle Menu
    -------------------------------------*/
    $('.menu-content').on('click', '.header-nav-item .menu-link', function(e) {
        if ($(this).parents('body').hasClass('mobile-menu-wrapper')) {
            var animationSpeed = 0,
                subMenuSelector = '.sub-menu',
                $this = $(this),
                checkElement = $this.next();
            if (checkElement.is(subMenuSelector) && checkElement.is(':visible')) {
                checkElement.slideUp(animationSpeed, function() {
                    checkElement.removeClass('menu-open');
                });
                checkElement.parent(".header-nav-item").removeClass("active");
            } else if ((checkElement.is(subMenuSelector)) && (!checkElement.is(':visible'))) {
                var parent = $this.parents('ul').first();
                var ul = parent.find('ul:visible').slideUp(animationSpeed);
                ul.removeClass('menu-open');
                var parent_li = $this.parent("li");
                checkElement.slideDown(animationSpeed, function() {
                    checkElement.addClass('menu-open');
                    parent.find('.header-nav-item.active').removeClass('active');
                    parent_li.addClass('active');
                });
            }
            if (checkElement.is(subMenuSelector)) {
                e.preventDefault();
            }
        } else {
            if ($(this).attr('href') === "#") {
                e.preventDefault();
            }
        }
    });

    /*-------------------------------------
    Side menu class Add
    --------------------------------------*/
    $('#wrapper').on('click', '.toggler-open', function(event) {
        event.preventDefault();
        
        var $this = $(this),
            wrapp = $(this).parents('body').find('#wrapper'),
            wrapMask = $('<div / >').addClass('closeMask'),
            sideMenuSelect = ('.fixed-sidebar');

        if (!$this.parents(sideMenuSelect).hasClass('lg-menu-open')) {
            wrapp.addClass('open').append(wrapMask);
            $this.parents(sideMenuSelect).addClass('lg-menu-open');

        }else {
            removeSideMenu();
        }

        function removeSideMenu() {
           wrapp.removeClass('open').find('.closeMask').remove();
           $this.parents(sideMenuSelect).removeClass('lg-menu-open');
        }

        $('.toggler-close, .closeMask').on('click', function() {
            removeSideMenu();
        });

    });

    /*-------------------------------------
    Mobile Menu Class Add
    --------------------------------------*/
    $(".mobile-menu-toggle").on("click", function() {
        if ($("#wrapper").hasClass("mobile-menu-expand")) {
            $("#wrapper").removeClass("mobile-menu-expand");
        } else {
            $("#wrapper").addClass("mobile-menu-expand");
        }
    });

    function mobile_nav_class() {
        var mq = window.matchMedia("(max-width: 991px)");
        if (mq.matches) {
            $("body").addClass("mobile-menu-wrapper");
        } else {
            $("body").removeClass("mobile-menu-wrapper");
        }
    }

    $(window).resize(function() {
        mobile_nav_class();
    });
    mobile_nav_class();

    /*-------------------------------------
    Chat Conversation Box
    -------------------------------------*/

    $('#chat-head-toggle').on("click", function() {
        $(this).parents('.fixed-sidebar').toggleClass('chat-head-hide');
        
    });

    $('.chat-plus-icon').on("click", function() {
        $(this).siblings('.file-attach-icon').toggleClass('show');
    });

    $('.chat-shrink').on("click", function() {

        $(this).parents('#chat-box-modal').toggleClass('shrink');

    });

    $('.chat-open').on("click", function() {

        $('#chat-box-modal').toggleClass('modal-show');

        setTimeout(function() {
            $('#chat-box-modal').removeClass('shrink');
        }, 300);
    });
    

    $('.drop-btn').on('click', function() {
        var $this = $(this),
            elment = $('.drop-menu'),
            maskWrap = $('<div / >').addClass('closeMask');
        if (!elment.hasClass('show')) {
            $this.siblings(elment).addClass('show');
            $('#wrapper').addClass('open').append(maskWrap);
        }else {
            $this.siblings(elment).removeClass('show');
            $('#wrapper').find('.closeMask').remove();
        }
        $('.closeMask').on('click',  function() {
            $this.siblings(elment).removeClass('show');
            $('#wrapper').find('.closeMask').remove();
        });
    });

const btnDelete = document.querySelectorAll('.js-delete')
if (btnDelete) {
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if(!confirm('Esta acción no se puede deshacer!')) {
        e.preventDefault();
      }
    });
  });
}
    /*-------------------------------------
    Section background image
    -------------------------------------*/
    $("[data-bg-image]").each(function() {
        var img = $(this).data("bg-image");
        $(this).css({
            backgroundImage: "url(" + img + ")"
        });
    });

    /*--------------------------------------
    Isotope initialization
    --------------------------------------*/
    var $container = $(".isotope-wrap");
    if ($container.length > 0) {
        var $isotope;
        var blogGallerIso = $(".featuredContainer", $container).imagesLoaded(function() {
            $isotope = $(".featuredContainer", $container).isotope({
                filter: "*",
                transitionDuration: "1s",
                hiddenStyle: {
                    opacity: 0,
                    transform: "scale(0.001)"
                },
                visibleStyle: {
                    transform: "scale(1)",
                    opacity: 1
                }
            });
        });
        $container.find(".isotope-classes-tab").on("click", "a", function() {
            var $this = $(this);
            $this
                .parent(".isotope-classes-tab")
                .find("a")
                .removeClass("current");
            $this.addClass("current");
            var selector = $this.attr("data-filter");
            $isotope.isotope({
                filter: selector
            });
            return false;
        });
    }

    /*-------------------------------------
        Masonry
    -------------------------------------*/
    var galleryIsoContainer = $("#no-equal-gallery");
    if (galleryIsoContainer.length) {
        var blogGallerIso = galleryIsoContainer.imagesLoaded(function() {
            blogGallerIso.isotope({
                itemSelector: ".no-equal-item",
                masonry: {
                    columnWidth: ".no-equal-item",
                    horizontalOrder: true
                }
            });
        });
    }

    /*-------------------------------------
        Product View
    -------------------------------------*/
    $('.user-view-trigger').on('click', function(e) {
        var self = $(this),
            data = self.attr("data-type"),
            target = $("#user-view");
        self.parents('.user-view-switcher').find('li.active').removeClass('active');
        self.parent('li').addClass('active');
        target.children('.row').find('>div').animate({
            opacity: 0,
        }, 200, function() {
            if (data === "user-grid-view") {
                target.removeClass('user-list-view');
                target.addClass('user-grid-view');
            } else if (data === "user-list-view") {
                target.removeClass('user-grid-view');
                target.addClass('user-list-view');
            }
            target.children('.row').find('>div').animate({
                opacity: 1,
            }, 100);
        });
        e.preventDefault();
        return false;
    });

    /*-------------------------------------
     Quantity Holder
     -------------------------------------*/
    $('#quantity-holder').on('click', '.quantity-plus', function() {

        var $holder = $(this).parents('.quantity-holder');
        var $target = $holder.find('input.quantity-input');
        var $quantity = parseInt($target.val(), 10);
        if ($.isNumeric($quantity) && $quantity > 0) {
            $quantity = $quantity + 1;
            $target.val($quantity);
        } else {
            $target.val($quantity);
        }

    }).on('click', '.quantity-minus', function() {

        var $holder = $(this).parents('.quantity-holder');
        var $target = $holder.find('input.quantity-input');
        var $quantity = parseInt($target.val(), 10);
        if ($.isNumeric($quantity) && $quantity >= 2) {
            $quantity = $quantity - 1;
            $target.val($quantity);
        } else {
            $target.val(1);
        }
    });

    /*-------------------------------------
        ElevateZoom
    -------------------------------------*/

    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
        elevateZoom();
    });

    function elevateZoom() {
        if ($.fn.elevateZoom !== undefined) {
            $('.zoom_01').elevateZoom({
                zoomType: "inner",
                cursor: "crosshair",
                zoomWindowFadeIn: 500,
                zoomWindowFadeOut: 200
            });
        }
    }

    elevateZoom();

    /*-------------------------------------
        Tooltip
    -------------------------------------*/
    $('[data-toggle="tooltip"]').tooltip()

    /*-------------------------------------
        Slick Carousel
    -------------------------------------*/
    $(".slick-carousel").slick();

    /*-------------------------------------
        Select2 activation code
    -------------------------------------*/
    if ($('select.select2').length) {
        $('select.select2').select2({
            theme: 'classic',
            dropdownAutoWidth: true,
            width: '100%',
            minimumResultsForSearch: Infinity
        });
    }

    /*-------------------------------------
        Video Popup
    -------------------------------------*/
    var yPopup = $(".popup-youtube");
    if (yPopup.length) {
        yPopup.magnificPopup({
            disableOn: 700,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        });
    }

    /*-------------------------------------
     Gallery Popup
    -------------------------------------*/
    if ($('.zoom-gallery').length) {
        $('.zoom-gallery').each(function() {
            $(this).magnificPopup({
                delegate: 'a.popup-zoom',
                type: 'image',
                gallery: {
                    enabled: true
                }
            });
        });
    }

    /*-------------------------------------
        Google Map
    -------------------------------------*/
    if ($("#googleMap").length) {
        window.onload = function() {
            var styles = [{
                featureType: 'water',
                elementType: 'geometry.fill',
                stylers: [{
                    color: '#b7d0ea'
                }]
            }, {
                featureType: 'road',
                elementType: 'labels.text.fill',
                stylers: [{
                    visibility: 'off'
                }]
            }, {
                featureType: 'road',
                elementType: 'geometry.stroke',
                stylers: [{
                    visibility: 'off'
                }]
            }, {
                featureType: 'road.highway',
                elementType: 'geometry',
                stylers: [{
                    color: '#c2c2aa'
                }]
            }, {
                featureType: 'poi.park',
                elementType: 'geometry',
                stylers: [{
                    color: '#b6d1b0'
                }]
            }, {
                featureType: 'poi.park',
                elementType: 'labels.text.fill',
                stylers: [{
                    color: '#6b9a76'
                }]
            }];
            var options = {
                mapTypeControlOptions: {
                    mapTypeIds: ['Styled']
                },
                center: new google.maps.LatLng(-37.81618, 144.95692),
                zoom: 10,
                disableDefaultUI: true,
                mapTypeId: 'Styled'
            };
            var div = document.getElementById('googleMap');
            var map = new google.maps.Map(div, options);
            var styledMapType = new google.maps.StyledMapType(styles, {
                name: 'Styled'
            });
            map.mapTypes.set('Styled', styledMapType);

            var marker = new google.maps.Marker({
                position: map.getCenter(),
                animation: google.maps.Animation.BOUNCE,
                icon: 'media/map-marker.png',
                map: map
            });
        };
    }

    /*-------------------------------------
        Sal Init
    -------------------------------------*/
    sal({
        threshold: 0.05,
        once: true
    });

    if ($(window).outerWidth() < 1025) {
        var scrollAnimations = sal();
        scrollAnimations.disable();
    }

    /*-------------------------------------
    Jquery Serch Box
    -------------------------------------*/
    $('a[href="#header-search"]').on("click", function (event) {
        event.preventDefault();
        var target = $("#header-search");
        target.addClass("open");
        setTimeout(function () {
            target.find('input').focus();
        }, 600);
        return false;
    });

    $("#header-search, #header-search button.close").on("click keyup", function (event) {
        if (
            event.target === this ||
            event.target.className === "close" ||
            event.keyCode === 27
        ) {
            $(this).removeClass("open");
        }
    });

})(jQuery);