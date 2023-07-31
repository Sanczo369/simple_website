const navBar = document.querySelector('.navbar');
const toTop = document.querySelector('.to-top');

window.addEventListener('scroll', () =>{
    if (window.scrollY>100){
        toTop.classList.add("active");
        navBar.classList.add("activeNav");
    }
    else{
        toTop.classList.remove("active");
        navBar.classList.remove("activeNav");
    }
})

const menuBtn = document.querySelector('.menu-btn');
let menuOpen = false
menuBtn.addEventListener('click', () => {
    if(!menuOpen) {
        menuBtn.classList.add('open');
        menuOpen = true;
    }else {
        menuBtn.classList.remove('open');
        menuOpen = false;
    }
});