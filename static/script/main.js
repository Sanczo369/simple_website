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
const ulList = document.querySelector('.hamburgerNav');
let menuOpen = false
menuBtn.addEventListener('click', () => {
    if(!menuOpen) {
        menuBtn.classList.add('open');
        ulList.classList.add('see');
        menuOpen = true;
    }else {
        menuBtn.classList.remove('open');
        ulList.classList.remove('see');
        menuOpen = false;
    }
});

let valueDisplays = document.querySelectorAll(".num");
let interval = 4000;
valueDisplays.forEach((valueDisplay) => {
    let startValue = 0;
    let endValue = parseInt(valueDisplay.getAttribute("data-val"));
    let duration = Math.floor(interval / endValue);
    let counter = setInterval(function () {
        if (window.scrollY>=1410){
            startValue += 1;
            valueDisplay.textContent = startValue;
            if (startValue >= endValue){
                clearInterval(counter);
            }
        }
    }, duration)
});

let counter = 1;
let sliderFlage = false
setInterval(function(){
    document.getElementById('radio' + counter).checked = true;
    if(!sliderFlage){
        counter++;
        if(counter>=4){
            sliderFlage = true;
        }
    }else {
        counter--;
        if(counter<=1){
            sliderFlage = false;
        }
    }
}, 5000);

function closeNewsletterPopup() {
    var newsletterPopup = document.getElementById('newsletterPopup');
    newsletterPopup.style.display = 'none';
}

// Wyświetlenie alert boxa po załadowaniu strony
window.onload = function() {
    var newsletterPopup = document.getElementById('newsletterPopup');
    newsletterPopup.style.display = 'block';
};
