var seconds = 0;

function incrementSeconds() {
    seconds += 1;
    document.getElementById('nyan').innerText = "You have nyaned for " + seconds + " seconds!";
}


$(function() {
    $('.chat').before("<p class='admonition-title chat'><i class='fad fa-hat-santa'></i>&nbsp;Elf Chat</p>");
    $('.goal').before("<p class='admonition-title goal'><i class='fad fa-gift'></i>&nbsp;Goal</p>");
    $('.gamehint').before("<p class='admonition-title gamehint'><i class='fad fa-globe-snow'></i>&nbsp;Hints</p>");
    $('.trailhint').before("<p class='admonition-title trailhint'><i class='fad fa-deer-rudolph'></i>&nbsp;Trail Hint</p>");

    var nyan_update = setInterval(incrementSeconds, 1000);
});

