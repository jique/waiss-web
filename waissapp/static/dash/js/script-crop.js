var url, cropId, container;
var all_crop_list=[], user_crop_list=[];
$(document).ready(function (){
    $('#user-crop').find('.user-crop').each(function(){
        user_crop_list.push($(this).val());
    });
    $('#all-crop').find('.all-crop').each(function(){
        all_crop_list.push($(this).val());
    });
    $('body').on('change', '#all-crop', function(){
        url = $('#crops').attr('data-crop-url');
        cropId = $('#all-crop').val();   

        if (cropId != 'Choose'){
            $.ajax({
                url:url,
                data:{
                    'crop':cropId,
                },
                success: function(data){
                    $('#data-holder').html(data);
                }
            });  
            $('#user-crop').val('Choose').trigger('change');
        }
    });
    $('body').on('change', '#user-crop', function(){
        url = $('#crops').attr('data-crop-url');
        cropId = $('#user-crop').val();   

        if (cropId != 'Choose'){
            $.ajax({
                url:url,
                data:{
                    'crop':cropId,
                },
                success: function(data){
                    $('#data-holder').html(data);
                }
            });  
            $('#all-crop').val('Choose').trigger('change');
        }
    });
    $("#data").on('click', "#btn-edit-this-crop", function () {
        url = window.location.href;
        cropId = $("#crop-container").attr("data-id");

        $.ajax({
            url: url,
            data: {
                'crop': cropId
            },
            success: function(data){
                $("#edit-crop-holder").html(data);
                computeCumStage('#modalEditCrop');
            }
        });
    });
    $("#data").on('click', "#btn-delete-this-crop", function () {
        url = window.location.href;
        cropId = $("#crop-container").attr("data-id");

        $.ajax({
            url: url,
            data: {
                'crop': cropId
            },
            success: function(data){
                $("#delete-crop-holder").html(data);
                computeCumStage('#modalDeleteCrop');
            }
        });
    });
    $("#modalAddCrop").on('change', ':input', function(){
        computeCumStage('#modalAddCrop');
    });
    $("#modalEditCrop").on('change', ':input', function(){
        computeCumStage('#modalEditCrop');
    });
    $("#modalDeleteCrop").on('change', ':input', function(){
        computeCumStage('#modalDeleteCrop');
    });
});


//--compute Cumulative Stage in Crop Information----//
function computeCumStage(modal) {
    stage_init = $(modal).find('input[name="stage_init"]').val();
    stage_dev = $(modal).find('input[name="stage_dev"]').val();
    stage_mid = $(modal).find('input[name="stage_mid"]').val();
    stage_late = $(modal).find('input[name="stage_late"]').val();
    crop_dtm = $(modal).find('input[name="crop_dtm"]').val();

    if ((stage_init != "") && (stage_dev != "") && (stage_mid != "") && (stage_late != "")) {
        cs_init =stage_init;
        cs_dev = parseInt(stage_init) + parseInt(stage_dev);
        cs_mid = parseInt(stage_init) + parseInt(stage_dev) + parseInt(stage_mid);
        cs_late = parseInt(stage_init) + parseInt(stage_dev) + parseInt(stage_mid) + parseInt(stage_late);
        $(modal).find('input[name="cs-init"]').val(cs_init);
        $(modal).find('input[name="cs-dev"]').val(cs_dev);
        $(modal).find('input[name="cs-mid"]').val(cs_mid);
        $(modal).find('input[name="cs-late"]').val(cs_late);
        $(modal).find('input[name="crop_dtm"]').val(cs_late);
    }
}
//-----end of cumulative growth stage computation-------//