function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('('  + prefix + '.\\d+-)');
    var replacement = prefix + '-' + ndx + '-';
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
    replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (formCount < 1000) {
        var row = $(".item:last").clone(false).get(0);
        $(row).removeAttr('id').hide().insertAfter(".item:last").slideDown(300);
        $(".errorlist", row).remove();
        $(row).children().removeClass("error")
        $(row).find('.formset-field').each(function(){
            updateElementIndex(this, prefix, formCount);
            $(this).val('');
            $(this).removeAttr('value');
            $(this).prop('checked', false);
        });

        $(row).find(".delete").click(function () {
            return deleteForm(this, prefix);
        });
        $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);
    }
    return false;
}

function deleteForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (formCount >1) {
        var goto_id = $(btn).find('input').val();
        if( goto_id){
            $.ajax({
                url: "/" + window.location.pathname.split("/")[1] + "/formset-data-delete/" + goto_id,
                error: function (){
                    console.log("error");
                },
                success: function(data){
                    $(btn).parents('.item').remove();
                },
                type: 'GET'
            });
        }else(
            $(btn).parents('.item').remove());
        }

        var forms = $('.item');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        var i=0;
        for (formCount = forms.length; 1 < formCount; i++) {
            $(forms.get(i)).find('.formset-field').each(function () {
                updateElementIndex(this, prefix, i);
            });
        }
        return false;
    }
    $("body").on('click', '.remove-form-row', function () {
    deleteForm($(this), String($('.add-form-row').attr('id')));
    
    });
    
    $("body").on('click', '.add-form-row', function () {
   addForm($(this), String($('.add-form-row').attr('id')));
    
    });
}