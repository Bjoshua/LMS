const menu_btn = document.querySelector('.hamburger');
const mobile_menu = document.querySelector('.mobile-nav');
menu_btn.addEventListener('click', function () {
    menu_btn.classList.toggle('is-active');
    mobile_menu.classList.toggle('is-active');
});
// let sections = document.getElementsByTagName('div');
// for (let i =0; i < sections.length; i++){
//     sections[i].classList.add('fade-in');
// }
// function debounce(func, wait=20, immediate=true){
//     var timeout;
//     return function(){
//         var context = this, args= arguments;
//         var later = function(){
//             timeout = null;
//             if (!immediate) func.apply(context, args);
//         };
//         var callNow = immediate && !timeout;
//         clearTimeout(timeout);
//         timeout = setTimeout(later, wait);
//         if (callNow) func.apply(context, args);
//     };
// }
// const fadeIns = document.querySelectorAll('.fade-in');

// function checkFadeIns(){
//     fadeIns.forEach(fadeIn =>{
//         const fadeInPosition = fadeIn.getBoundingClientRect().top;
//         const screenPosition = window.innerHeight / 1.6;
//         if (fadeInPosition < screenPosition){
//             fadeIn.classList.add('is-visible');
//         } else {
//             fadeIn.classList.remove('is-visible')
//         }
//     })
// }
// window.addEventListener('scroll', debounce(checkFadeIns));
// checkFadeIns();




// let sections = document.getElementsByTagName('section');
// for (let i =0; i < sections.length; i++){
//     sections[i].classList.add('fade-in');
// }
// const faders = document.querySelectorAll('.fade-in')
// const appearOptions = {
//     treshold:0,
//     rootMargin: "0px 0px -250px 0px"
// };
// const appearOnScroll = new IntersectionObserver(function(
//     entries,
//     appearOnScroll
// ){
//     entries.forEach(entry =>{
//         if (!entry.isIntersecting){
//             return;
//         }else{
//             entry.target.classList.add("appear");
//             appearOnScroll.unobserve(entry.target);
//         }
//     });
// },
//     appearOptions);
//     faders.forEach(fader =>{
//         appearOnScroll.observe(fader);
// });

// let cursor= document.querySelector(".cursor")
// let cursor2 = document.querySelector(".cursor2")

// document.addEventListener("mousemove", e =>{
//     cursor.style.cssText = cursor2.style.cssText = "left: "+ e.clientX + "px; top: " + e.clientY + "px;";
// });
