var fx = document.getElementById("id_farm_lat"), //farm location holders
    fy = document.getElementById("id_farm_long"),
    fh = document.getElementById("fh"),
    sx = document.getElementById("id_station_lat"), //station location holders
    sy = document.getElementById("id_station_long"),
    sh = document.getElementById("sh");

$(document).ready(function (){
    $('body').on('click', '#btnEnterData', function () {//resets Enter Single Data modal on click event of button
        document.getElementById('enterData').reset();
        $.ajax({
            url: window.location.href,
            data: {
                'valid_2': true
            },
            success: function(data){
                $("#enter-data-holder").html(data);
            }
        });
    });
    $('body').on('click', '#btnUploadData', function () {//resets Upload Data modal on click event of button
        document.getElementById('uploadData').reset();
        $.ajax({
            url: window.location.href,
            data: {
                'valid': true
            },
            success: function(data){
                $("#upload-data-holder").html(data);
            }
        });
    });
    $('body').on('click', '#btnAddStation', function () {//resets Add Station modal on click event of button
        document.getElementById('addStation').reset();
    });
    $('body').on('click', '#btnAddCrop', function () {//resets Add Crop modal on click event of button
        document.getElementById('addCrop').reset();
    });
    $('body').on('click', '#btnAddSoil', function () {//resets Add Soil modal on click event of button
        document.getElementById('addSoil').reset();
    });
    $('body').on('click', "#get-my-loc", function (){
        form = $(this).closest('form');
        fx = form.find('#id_farm_lat').get(0);
        fy = form.find('#id_farm_long').get(0);
        fh = form.find('#fh').get(0);
        getLocationforFarm();
    });
    $('body').on('click', "#sta-my-loc", function (){
        form = $(this).closest('form');
        sx = form.find('#id_station_lat').get(0);
        sy = form.find('#id_station_long').get(0);
        sh = form.find('#sh').get(0);
        getLocationforStation();
    });
    // Add remove loading class on body element based on Ajax request status
    $(document).on({
        ajaxStart: function(){
            $("body").addClass("loading"); 
        },
        ajaxStop: function(){ 
            $("body").removeClass("loading"); 
        }    
    });
});

//-----------HTML GEOLOCATION------------//
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
//---------end of HTML GEOLOCATION----------//