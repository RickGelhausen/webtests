---
---

document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('.burger').addEventListener('click', function() {
        document.querySelector('.navbar ul').classList.toggle('nav-open');
    });
});