---
---

document.addEventListener("DOMContentLoaded", function() {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.navbar ul');
    if (burger && nav) {
        burger.addEventListener('click', function() {
            nav.classList.toggle('nav-open');
        });
    } else {
        console.warn('burger or nav elements not found!');
    }
});