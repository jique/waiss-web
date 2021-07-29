var fx = document.getElementById("id_farm_lat"), //farm location holders
    fy = document.getElementById("id_farm_long"),
    fh = document.getElementById("fh"),
    sx = document.getElementById("id_station_lat"), //station location holders
    sy = document.getElementById("id_station_long"),
    sh = document.getElementById("sh");

$(document).ready(function (){
    /*--EVENT LISTENERS--*/
    $('body').on('change', ':input', function () {
        /*performs a recalculation everytime an input field is changed*/
        calcCumStage();
    });
    $('body').on('click', "#get-my-loc", function (){
        fx = document.getElementById("id_farm_lat"), //farm location holders
        fy = document.getElementById("id_farm_long"),
        fh = document.getElementById("fh"),
        getLocationforFarm();
    });
    $('body').on('click', "#sta-my-loc", function (){
        sx = document.getElementById("id_station_lat"), //station location holders
        sy = document.getElementById("id_station_long"),
        sh = document.getElementById("sh");
        getLocationforStation();
    });
});

/*--AJAX LOADED HTML DATA--*/
function fetch(){
    var form = $('form');
    var url = window.location.href;
    var section = $('.section');

    $.ajax({
        url: url,
        data: form.serialize(),
        success: function (response) {
            section.html(response);
        }
    }); 
}
/*--end of AJAX LOADED HTML DATA--*/

/*--HTML GEOLOCATION--*/
/*requet the user's current location and directly input
to the concerned field*/
function getLocationforFarm() {
    x = fx;
    y = fy;
    h = fh;
    getLocation();
}

function getLocationforStation() {
    x = sx;
    y = sy;
    h = sh;
    getLocation();
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    x.value = parseFloat(position.coords.latitude);
    x.focus();
    y.value = parseFloat(position.coords.longitude);
    y.focus();
    h.innerHTML = "";
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            h.innerHTML = "User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            h.innerHTML = "Location information is unavailable."
            break;
        case error.TIMEOUT:
            h.innerHTML = "The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            h.innerHTML = "An unknown error occurred."
            break;
    }
}
/*--end of HTML GEOLOCATION--*/

/*--Cumulative Stage Computation--*/
function calcCumStage() {
    stage_init = $('input[name="stage_init"]').val();
    stage_dev = $('input[name="stage_dev"]').val();
    stage_mid = $('input[name="stage_mid"]').val();
    stage_late = $('input[name="stage_late"]').val();
    crop_dtm = $('input[name="crop_dtm"]').val();

    if ((stage_init != "") && (stage_dev != "") && (stage_mid != "") && (stage_late != "")) {
        cs_init =stage_init;
        cs_dev = parseInt(stage_init) + parseInt(stage_dev);
        cs_mid = parseInt(stage_init) + parseInt(stage_dev) + parseInt(stage_mid);
        cs_late = parseInt(stage_init) + parseInt(stage_dev) + parseInt(stage_mid) + parseInt(stage_late);
        $('input[name="crop_dtm"]').val(cs_late);
    }
}