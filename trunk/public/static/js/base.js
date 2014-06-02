$(function() {
    $(window).scroll(function() {
        if ($("header").height() < $(window).scrollTop()) {
            $("nav").addClass("fixed");
        } else {
            $("nav").removeClass("fixed");
        }
    }).scroll();
});

