//Update clock
function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    var ampm = h >= 12 ? 'PM' : 'AM';
    m = checkTime(m);
    s = checkTime(s);
    h = h % 12;
    h = h ? h : 12; // the hour '0' should be '12'

    document.getElementById('time').innerHTML = h + ":" + m + ":" + s + ' ' + ampm;

    var month = today.getMonth() + 1;
    var day = today.getDate();
    var year = today.getFullYear();

    document.getElementById('date').innerHTML = month + '/' + day + '/' + year;

    var t = setTimeout(startTime, 500);
    }
    console.log(startTime(new Date));
    function checkTime(i) {
      if (i < 10) { i = "0" + i };  // add zero in front of numbers < 10
      return i;
    }