"use strict"

$(document).ready(function () {
    /* height 100% as window height */
    $('.vh-100').css("min-height", $(window).height());
    /* height 100% as window height */
    $('.vhf-100').css("min-height", $(window).height() - $('.footer').outerHeight() );
});
/* Scroll content add class */
$(window).on("scroll", function () {
    var scroll = $(window).scrollTop();
    if (scroll >= 150) {
        $(".header").addClass("active")
    } else {
        $(".header").removeClass("active")
    }
});
