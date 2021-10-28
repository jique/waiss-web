var map = L.map('tracemap');
var mapCenter = [14.16358, 121.25078];     
var markCenter = L.marker(mapCenter).addTo(map);  
    
function buildMap(){ 
    if (!isNaN($('input[name="farm_lat"]').val()) && $('input[name="farm_lat"]').val() != "" && !isNaN($('input[name="farm_long').val()) && $('input[name="farm_long').val() != ""){
        mapCenter = [parseFloat($('input[name="farm_lat"]').val()), parseFloat($('input[name="farm_long').val())];
    }
    markCenter.setLatLng(mapCenter).addTo(map);
    map.setView(mapCenter, 10);
        
    var mapboxUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZ3JtYiIsImEiOiJja3QyZTB1emEwbWpyMm5ueGNsM3p6ZWZxIn0.qosdXRuQF0PUAo2XT48_0g';

    L.tileLayer(mapboxUrl, {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 20,
        id: 'mapbox/satellite-streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiZ3JtYiIsImEiOiJja3QyZTB1emEwbWpyMm5ueGNsM3p6ZWZxIn0.qosdXRuQF0PUAo2XT48_0g'
    }).addTo(map);

    if ($('input[name="initial-farm_map"]').val() && $('input[name="initial-farm_map"]').val() != "" && $('input[name="initial-farm_map"]').val() != '{}'){
        var points = JSON.parse($('input[name="initial-farm_map"]').val())['points'];
        latlngs = [];
        for (i=0; i<points.length; i++){
            latlngs[i] = [points[i]['lat'], points[i]['lng']];
        }  
        coords = [latlngs];
        L.polygon(coords).addTo(map);
        map.fitBounds(latlngs);
    }

    L.control.measure({
        primaryLengthUnit: 'meters',
        secondaryLengthUnit: 'kilometers',
        primaryAreaUnit: 'sqmeters',
        secondaryAreaUnit: 'hectares',
        position: 'topleft'
    }).addTo(map);

    map.on('measurefinish', function(evt) {
        writeResults(evt);
    });

    function writeResults(results) {
        $('input[name="farm_area"]').val(parseFloat(results.area));
        document.getElementById('id_farm_map').value = JSON.stringify(
        {
            area: results.area,
            areaDisplay: results.areaDisplay,
            lastCoord: results.lastCoord,
            length: results.length,
            lengthDisplay: results.lengthDisplay,
            pointCount: results.pointCount,
            points: results.points
        },
        null,
        2
        );
        var center = L.polygon(results.points).getBounds().getCenter();
        $('input[name="farm_lat"]').val(parseFloat(center.lat));
        $('input[name="farm_long"]').val(parseFloat(center.lng));
    }

    map.on('click', function(e){
        var lat = e.latlng.lat;
        var lng = e.latlng.lng;
        $('input[name="farm_lat"]').val(lat);
        $('input[name="farm_long"]').val(lng);
    });

        
    $('body').on('change', 'input[name="farm_lat"]', function () {
        var x = $(this).val();
        var y = $('input[name="farm_long"]').val();
        if(x == ""){
            x = mapCenter[0];
        }
        if(y == ""){
            y = mapCenter[1];
        }
        map.panTo({lat:x, lng:y});
        markCenter.setLatLng({lat:x, lng:y});
    });
        
    $('body').on('change', 'input[name="farm_long"]', function () {
        var x = $('input[name="farm_lat"]').val();
        var y = $(this).val();
        if(x == ""){
            x = mapCenter[0];
        }
        if(y == ""){
            y = mapCenter[1];
        }
        map.panTo({lat:x, lng:y});
        markCenter.setLatLng({lat:x, lng:y});
    });     
    L.control.mousePosition().addTo(map);
}
buildMap();

/*--HTML GEOLOCATION--*/
/*requet the user's current location and directly input
to the concerned field*/

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

var fx = document.getElementById("id_farm_lat"), //farm location holders
fy = document.getElementById("id_farm_long"),
fh = document.getElementById("fh"),
sx = document.getElementById("id_station_lat"), //station location holders
sy = document.getElementById("id_station_long"),
sh = document.getElementById("sh");

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
    map.panTo({lat:position.coords.latitude, lng:position.coords.longitude});
    markCenter.setLatLng({lat:position.coords.latitude, lng:position.coords.longitude});
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
            map.remove();
            map = L.map('tracemap');
            buildMap();           
        }
    }); 
}
/*--end of AJAX LOADED HTML DATA--*/