$(function(){
	window.defaultStatus="Design + Programming by FEINHEIT kreativ studio · www.feinheit.ch";
    
    if(navigator.platform == 'iPad' || navigator.platform == 'iPhone' || navigator.platform == 'iPod'){
        $("footer").css("position", "static");
    };
});

// usage: log('inside coolFunc',this,arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console){
    console.log( Array.prototype.slice.call(arguments) );
  }
};

// Sliders
var el = document.getElementsByTagName('html')[0];
var supports = {
    hashchange: el.className.indexOf('no-hashchange') == -1,
    history: el.className.indexOf('no-history') == -1,
    transitions: el.className.indexOf('no-csstransitions') == -1
    };

// moodboard
$(document).ready(function(){
    if (supports.transitions) {
        $('.slides').moodboard({slide_time: 4000});
    } else {
        var $slides = $('.slides');
        $slides.moodboard({
            slide_time: 4000,
            _reveal: function($mb, data, newidx) {
                data.slides[data.current].css({'z-index': 100}).animate({opacity: 0}, 800);
                data.slides[newidx].css({'z-index': 101}).animate({opacity: 1}, 800, function() {
                    data.slides[newidx][0].style.removeAttribute('filter');
                });
                data.current = newidx;
            }
        });
    }

    if (!supports.transitions) {
        // move div behind img, so that missing cleartext support in IE CSS
        // filters does not produce ugly artifacts
        $('.flip div').show().css('z-index', 99);
        $('.flip img').css('position', 'absolute').show().css('z-index', 110);

        // hide image instead of revealing colored layer on mouseover
        $('.flip').hover(function() {
            $('img', this).stop(true, true).animate({opacity:0.1}, 'fast');
        }, function() {
            $('img', this).stop(true, true).animate({opacity:1});
        });
    }
});

// quotes
$(document).ready(function(){
    if (supports.transitions) {
        $('.quotes').moodboard({slide_time: 4000});
    } else {
        var $slides = $('.slides');
        $slides.moodboard({
            slide_time: 4000,
            _reveal: function($mb, data, newidx) {
                data.slides[data.current].css({'z-index': 100}).animate({opacity: 0}, 800);
                data.slides[newidx].css({'z-index': 101}).animate({opacity: 1}, 800, function() {
                    data.slides[newidx][0].style.removeAttribute('filter');
                });
                data.current = newidx;
            }
        });
    }

    if (!supports.transitions) {
        // move div behind img, so that missing cleartext support in IE CSS
        // filters does not produce ugly artifacts
        $('.flip div').show().css('z-index', 99);
        $('.flip img').css('position', 'absolute').show().css('z-index', 110);

        // hide image instead of revealing colored layer on mouseover
        $('.flip').hover(function() {
            $('img', this).stop(true, true).animate({opacity:0.1}, 'fast');
        }, function() {
            $('img', this).stop(true, true).animate({opacity:1});
        });
    }
});
