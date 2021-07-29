var url, soilId, container;
var all_soil_list=[], user_soil_list=[];
$(document).ready(function (){
    $('#user-soil').find('.user-soil').each(function(){
        user_soil_list.push($(this).val());
    });
    $('#all-soil').find('.all-soil').each(function(){
        all_soil_list.push($(this).val());
    });
    $('body').on('change', '#all-soil', function(){
        url = $('#soils').attr('data-soil-url');
        soilId = $('#all-soil').val();   

        if (soilId != 'Choose'){
            $.ajax({
                url:url,
                data:{
                    'soil':soilId,
                },
                success: function(data){
                    $('#data-holder').html(data);
                }
            });  
            $('#user-soil').val('Choose').trigger('change');
        }
    });
    $('body').on('change', '#user-soil', function(){
        url = $('#soils').attr('data-soil-url');
        soilId = $('#user-soil').val();   

        if (soilId != 'Choose'){
            $.ajax({
                url:url,
                data:{
                    'soil':soilId,
                },
                success: function(data){
                    $('#data-holder').html(data);
                }
            });  
            $('#all-soil').val('Choose').trigger('change');
        }
    });
    $("#data").on('click', "#btn-edit-this-soil", function () {
        url = window.location.href;
        soilId = $("#soil-container").attr("data-id");

        $.ajax({
            url: url,
            data: {
                'soil': soilId
            },
            success: function(data){
                $("#edit-soil-holder").html(data);
            }
        });
    });
    $("#data").on('click', "#btn-delete-this-soil", function () {
        url = window.location.href;
        soilId = $("#soil-container").attr("data-id");

        $.ajax({
            url: url,
            data: {
                'soil': soilId
            },
            success: function(data){
                $("#delete-soil-holder").html(data);
            }
        });
    });
});