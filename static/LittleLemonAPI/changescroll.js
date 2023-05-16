function changeBg(){
    var navbar = document.getElementById('config');
    var scrollValue = window.scrollY;
    console.log(scrollValue)
    if(scrollValue < 150){
        navbar.style.backgroundColor = "transparent";
    }
    else {
        navbar.style.backgroundColor = "rgba(60, 245, 119, .5)";
    }
    if(scrollValue >= 1314 && scrollValue < 1971){
        navbar.style.backgroundColor = "rgba(17, 210, 200, 0.5)"
    }
}
window.addEventListener('scroll', changeBg)