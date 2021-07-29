$(document).ready(function () {
    // Set the date we're counting down to
    var countDownDate = new Date().getTime() + 10000;

    // Update the count down every 1 second
    var x = setInterval(function () {

        // Get today's date and time
        var now = new Date().getTime();

        // Find the distance between now and the count down date
        var distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        var seconds = Math.floor((distance) / 1000);

        // Output the result in an element with id="demo"
        document.getElementById("timer").innerHTML = seconds + "s ";

        // If the count down is over, write some text 
        if (seconds <= 0) {
            clearInterval(x);
            pageRedirect();
        }
    }, 1000);
});
    
function pageRedirect() {
        window.location.replace("https://waisset.pythonanywhere.com/mydashboard/");
}
