/* script.js */

document.addEventListener("DOMContentLoaded", function() {
    const timer = document.getElementById('displaytimer');
    const inputTag = document.getElementById('timer');
    let t = 0;

    setInterval(() => {
        t += 1;
        timer.innerHTML = "<b>Timer: " + t + " seconds</b>";
        inputTag.value = t;
    }, 1000);
});
