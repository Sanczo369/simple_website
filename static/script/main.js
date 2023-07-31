const toTop = document.querySelector('.navbar');
const navBar = document.querySelector('.to-top');

window.addEventListener('scroll', () =>{
    if (window.scrollY>100){
        toTop.classList.add("active");
        toTop.classList.add("activeNav");
    }
    else{
        toTop.classList.remove("active");
        toTop.classList.remove("activeNav");
    }
})