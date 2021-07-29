/*This contains the scripts and functions for farms.html*/
var url,farmId, container;
$(document).ready(function () {
    //for farm details update in farms html
    $(".btn-show-farm").on('click', function () {
        url = $("#farms").attr("data-farm-url");
        farm = $(this).closest('div .farm-id');
        farmId = farm.attr("data-id");
        cropping = $(this).closest('div .cropping-season');
        croppingId = cropping.attr("data-id");

        $.ajax({
            url: url,
            data: {
                'farm': farmId,
                'cropping': croppingId
            },
            success: function(data){
                $("#data-holder").html(data);
            }
        });
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
    $("#data").on('click', "#btn-edit-this-farm", function () {
        url = window.location.href;
        farmId = $("#farm-container").attr("data-id");

        $.ajax({
            url: url,
            data: {
                'farm': farmId,
            },
            success: function(data){
                $("#edit-farm-holder").html(data);
            }
        });
    });
    $("#data").on('click', "#btn-delete-this-farm", function () {
        url = window.location.href;
        farmId = $("#farm-container").attr("data-id");

        $.ajax({
            url: url,
            data: {
                'farm': farmId,
            },
            success: function(data){
                $("#delete-farm-holder").html(data);
            }
        });
    });
    $("#data").on('click', "#btn-edit-this-cropping", function () {
        url = window.location.href;
        croppingId = $("#cropping-container").attr("data-id");

        $.ajax({
            url: url,
            data: {
                'cropping': croppingId
            },
            success: function(data){
                $("#edit-cropping-holder").html(data);
            }
        });
    });
    $("#data").on('click', "#btn-delete-this-cropping", function () {
        url = window.location.href;
        croppingId = $("#cropping-container").attr("data-id");

        $.ajax({
            url: url,
            data: {
                'cropping': croppingId
            },
            success: function(data){
                $("#delete-cropping-holder").html(data);
            }
        });
    });
});