//new_farm
//modal_add_edit_farm
$(document).ready(function () {
  repeat();
  $('#modal-farm').on('shown.bs.modal', function (e) {
    repeat();
  });
  repeat1();
  $('#modal-crop').on('shown.bs.modal', function (e) {
    repeat1();
  });
  repeat2();
  $('#modal-soil').on('shown.bs.modal', function (e) {
    repeat2();
  });
  repeat3();
  $('#modal-calib').on('shown.bs.modal', function (e) {
    repeat3();
  });
  repeat5();
  $('#modal-drip').on('shown.bs.modal', function (e) {
    repeat5();
  });
  showHide7();
  $("#id_bln_irrigation").change(function () {
    showHide7();
  });
  showHide8();
  $("#id_select_irrigation").change(function () {
    showHide8();
  });
});
function repeat() {
  showHide();
  $("#id_select_coordinates").change(function () {
    showHide();
  });
}
function showHide() {
  var checkedValue = $("#id_select_coordinates").val();
  if (checkedValue == "yes") {
    $("#collapseOne").collapse('show');
    $("#id_lat").prop('required',true);
    $("#id_long").prop('required',true);
  } else if (checkedValue == "no") {
    $("#collapseOne").collapse('hide');
    $("#id_lat").prop('required',false);
    $("#id_long").prop('required',false);
  }
}
//new_crop
function repeat1() {
  showHide2();
  showHide3();
  showHide4();
  $("#id_eqnform").change(function () {            
    showHide2();
  });
  $("#id_root_growth_model").change(function () {
    showHide3();
  });
  $("#id_select_drip").change(function () {
    showHide4();
  });
}
function showHide2() {
  var checkedValue = $("#id_eqnform").val();
  if (checkedValue == "linear") {
    $("#panel1").collapse('show');
    $("#panel2").collapse('hide');
    $("#id_root_a").prop('required',true);
    $("#id_root_b").prop('required',true);
    $("#id_root_c").prop('required',false);
    $("#id_kc_ini").prop('required',false);
    $("#id_kc_mid").prop('required',false);
    $("#id_kc_end").prop('required',false);
    $("#id_kc_cc_1").prop('required',false);
    $("#id_kc_cc_2").prop('required',false);
    $("#id_kc_cc_3").prop('required',false);
  } else if (checkedValue == "quadratic") {
    $("#panel1").collapse('hide');
    $("#panel2").collapse('show');
    $("#id_root_a").prop('required',true);
    $("#id_root_b").prop('required',true);
    $("#id_root_c").prop('required',true);
    $("#id_kc_ini").prop('required',false);
    $("#id_kc_mid").prop('required',false);
    $("#id_kc_end").prop('required',false);
    $("#id_kc_cc_1").prop('required',false);
    $("#id_kc_cc_2").prop('required',false);
    $("#id_kc_cc_3").prop('required',false);
  }
}
function showHide3() {
  var checkedValue = $("#id_root_growth_model").val();
  if (checkedValue == "Borg-Grimes Model") {
    $("#collapse1").collapse('show');
    $("#collapse2").collapse('hide');
    $("#collapse3").collapse('hide');
    $("#id_eqnform").prop('required',false);
    $("#id_kc_ini").prop('required',false);
    $("#id_kc_mid").prop('required',false);
    $("#id_kc_end").prop('required',false);
    $("#id_kc_cc_1").prop('required',false);
    $("#id_kc_cc_2").prop('required',false);
    $("#id_kc_cc_3").prop('required',false);
    $("#id_root_a").prop('required',false);
    $("#id_root_b").prop('required',false);
    $("#id_root_c").prop('required',false);
  } else if (checkedValue == "Inverse Kc") {
    $("#collapse1").collapse('hide');
    $("#collapse2").collapse('show');
    $("#collapse3").collapse('hide');
    $("#id_kc_ini").prop('required',true);
    $("#id_kc_mid").prop('required',true);
    $("#id_kc_end").prop('required',true);
    $("#id_kc_cc_1").prop('required',true);
    $("#id_kc_cc_2").prop('required',true);
    $("#id_kc_cc_3").prop('required',true);
    $("#id_eqnform").prop('required',false);
    $("#id_root_a").prop('required',false);
    $("#id_root_b").prop('required',false);
    $("#id_root_c").prop('required',false);
  } else if (checkedValue == "User-Defined") {
    $("#collapse1").collapse('hide');
    $("#collapse2").collapse('hide');
    $("#collapse3").collapse('show');
    $("#id_eqnform").prop('required',true);
    $("#id_kc_ini").prop('required',false);
    $("#id_kc_mid").prop('required',false);
    $("#id_kc_end").prop('required',false);
    $("#id_kc_cc_1").prop('required',false);
    $("#id_kc_cc_2").prop('required',false);
    $("#id_kc_cc_3").prop('required',false);
  }
}
function showHide4() {
  var checkedValue = $("#id_select_drip").val();
  if (checkedValue == "yes") {
    $("#collapseOne").collapse('show');
    $("#id_peak_Etcrop").prop('required',true);
    $("#id_transpiration_ratio").prop('required',true);
  } else if (checkedValue == "no") {
    $("#collapseOne").collapse('hide');
    $("#id_peak_Etcrop").prop('required',false);
    $("#id_transpiration_ratio").prop('required',false);
  }
}
//new_soil
function repeat2() {
  showHide5();
  $("#id_bln_surface_irrigation").change(function () {
    showHide5();
  });
}
function showHide5() {
  var checkedValue = $("#id_bln_surface_irrigation").val();
  if (checkedValue == "yes") {
    $("#collapse4").collapse('show');
    $("#id_intake_family").prop('required',true);
  } else if (checkedValue == "no") {
    $("#collapse4").collapse('hide');
    $("#id_intake_family").prop('required',false);
  }
}
//new_calib
function repeat3() {
  showHide6();
  $("#id_calib_equation").change(function () {
    showHide6();
  });
}
function showHide6() {
  var checkedValue = $("#id_calib_equation").val();
  if (checkedValue == "quadratic") {
    $("#id_coeff_c").prop('required',true);
  } else if (checkedValue == "symmetrical sigmoidal") {
    $("#id_coeff_c").prop('required',true);
    $("#id_coeff_d").prop('required',true);
  } else if (checkedValue == "asymmetrical sigmoidal") {
    $("#id_coeff_c").prop('required',true);
    $("#id_coeff_d").prop('required',true);
    $("#id_coeff_m").prop('required',true);
  }
}
//add_drip
function repeat5() {
  showHide10();
  $("#id_bln_ii").change(function () {
    showHide10();
  });
}
function showHide10() {
  var checkedValue = $("#id_bln_ii").val();
  if (checkedValue == "yes") {
    $("#collapse_irrig_II").collapse('show');
    $('#id_irrigation_interval').prop('required',true);
  } else if (checkedValue == "no") {
    $("#collapse_irrig_II").collapse('hide');
    $('#id_irrigation_interval').prop('required', false);
  }
}
//new_irrigation
function showHide7() {
  var checkedValue = $("#id_bln_irrigation").val();
  if (checkedValue == "False") {
    $("#collapse_irrig_One").collapse('show');
    $("#collapse_irrig_Two").collapse('hide');
    $("#collapse_irrig_1").collapse('hide');
    $("#collapse_irrig_2").collapse('hide');
    $("#collapse_irrig_3").collapse('hide');
    $("#collapse_irrig_4").collapse('hide');
    $("#collapse_irrig_5").collapse('hide');
  } else if (checkedValue == "True") {
    $("#collapse_irrig_One").collapse('hide');
    $("#collapse_irrig_Two").collapse('show');
  }
}
function showHide8() {
  var checkedValue = $("#id_select_irrigation").val();
  if (checkedValue == "basin") {
    $("#collapse_irrig_1").collapse('show');
    $("#collapse_irrig_2").collapse('hide');
    $("#collapse_irrig_3").collapse('hide');
    $("#collapse_irrig_4").collapse('hide');
    $("#collapse_irrig_5").collapse('hide');
  } else if (checkedValue == "border") {
    $("#collapse_irrig_1").collapse('hide');
    $("#collapse_irrig_2").collapse('show');
    $("#collapse_irrig_3").collapse('hide');
    $("#collapse_irrig_4").collapse('hide');
    $("#collapse_irrig_5").collapse('hide');
  } else if (checkedValue == "furrow") {
    $("#collapse_irrig_1").collapse('hide');
    $("#collapse_irrig_2").collapse('hide');
    $("#collapse_irrig_3").collapse('show');
    $("#collapse_irrig_4").collapse('hide');
    $("#collapse_irrig_5").collapse('hide');
  } else if (checkedValue == "sprinkler") {
    $("#collapse_irrig_1").collapse('hide');
    $("#collapse_irrig_2").collapse('hide');
    $("#collapse_irrig_3").collapse('hide');
    $("#collapse_irrig_4").collapse('show');
    $("#collapse_irrig_5").collapse('hide');
  } else if (checkedValue == "drip") {
    $("#collapse_irrig_1").collapse('hide');
    $("#collapse_irrig_2").collapse('hide');
    $("#collapse_irrig_3").collapse('hide');
    $("#collapse_irrig_4").collapse('hide');
    $("#collapse_irrig_5").collapse('show');  
  }
}