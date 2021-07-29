var url, stationId, container;
var all_station_list=[], user_station_list=[];
$(document).ready(function (){
    $('#user-station').find('.user-station').each(function(){
        user_station_list.push($(this).val());
    });
    $('#all-station').find('.all-station').each(function(){
        all_station_list.push($(this).val());
    });
    $('body').on('change', '#all-station', function(){
        url = $('#stations').attr('data-station-url');
        stationId = $('#all-station').val();   

        if (stationId != 'Choose'){
            $.ajax({
                url:url,
                data:{
                    'station':stationId,
                },
                success: function(data){
                    $('#data-holder').html(data);
                }
            });  
            $('#user-station').val('Choose').trigger('change');
        }
    });
    $('body').on('change', '#user-station', function(){
        url = $('#stations').attr('data-station-url');
        stationId = $('#user-station').val();
        
        if (stationId != 'Choose'){
            $.ajax({
                url:url,
                data:{
                    'station':stationId,
                },
                success: function(data){
                    $('#data-holder').html(data);
                }
            });     
            $('#all-station').val('Choose').trigger('change');
        }
    });
    $("#data").on('click', ".btn-edit-this-data", function () {
        url = window.location.href;
        container = $(this).closest('tr').find('td.data-entry');
        dataId = container.attr("data-id");

        $.ajax({
            url: url,
            data: {
                'data_item': dataId
            },
            success: function (data) {
                $("#edit-data-holder").html(data);
            }
        });
    });
    $("#data").on('click', ".btn-delete-this-data", function () {
        url = window.location.href;
        container = $(this).closest('tr').find('td.data-entry');
        dataId = container.attr("data-id");

        $.ajax({
            url: url,
            data: {
                'data_item': dataId
            },
            success: function(data){
                $("#delete-data-holder").html(data);
            }
        });
    });
    $("#data").on('click', "#btn-edit-this-station", function () {
        url = window.location.href;
        stationId = $("#station-container").attr("data-id");

        $.ajax({
            url: url,
            data: {
                'station': stationId
            },
            success: function(data){
                $("#edit-station-holder").html(data);
            }
        });
    });
    $("#data").on('click', "#btn-delete-this-station", function () {
        url = window.location.href;
        stationId = $("#station-container").attr("data-id");

        $.ajax({
            url: url,
            data: {
                'station': stationId
            },
            success: function(data){
                $("#delete-station-holder").html(data);
            }
        });
    });
});