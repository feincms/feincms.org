$(function(){
    if(navigator.platform == 'iPad' || navigator.platform == 'iPhone' || navigator.platform == 'iPod'){
        $("footer").css("position", "static");
    };
});

// moodboard
$(document).ready(function(){
        $('.slides').moodboard({slide_time: 4000});
});

// quotes
$(document).ready(function(){
        $('.quotes').moodboard({
            slide_time: 4000,
            _init_controls: function($mb, data) {
                var $controls = $('<div id="quote-navigation" />').appendTo($mb);

                $('<a class="button-previous" />').appendTo($controls).bind('click', function() {
                    $mb.moodboard('previous'); });
                $('<a class="button-next" />').appendTo($controls).bind('click', function() {
                    $mb.moodboard('next'); });
            }
        });
});
