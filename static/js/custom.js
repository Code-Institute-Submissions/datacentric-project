/* Dropdown side menu */
/* Login & register tabs */
/* Accordion */

$(document).ready(function(){
    $(".dropdown-trigger").dropdown();
    $(".sidenav").sidenav();
    $('select').formSelect();
    $('.tabs').tabs();
    $('.collapsible').collapsible();
});

/* Home page slide show */

var slideIndex = 0;
carousel();
    function carousel() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none"; 
    }
    slideIndex++;
    if (slideIndex > x.length) {slideIndex = 1} 
    x[slideIndex-1].style.display = "block"; 
    setTimeout(carousel, 5000);
}