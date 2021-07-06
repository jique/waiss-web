//FARM
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-farm').modal('show');
			},
			success: function(data){
				$('#modal-farm .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.farm-table tbody').html(data.list_farm);
					$('.modal').modal('hide');
				} else {
					$('#modal-farm .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$(".show-form").click(ShowForm);
$("#modal-farm").on("submit",".create-form",SaveForm);

//update
$('.farm-table').on("click",".show-form-update",ShowForm);
$('#modal-farm').on("submit",".update-form",SaveForm)

});
//FARM

//PERSONNEL
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-personnel').modal('show');
			},
			success: function(data){
				$('#modal-personnel .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.personnel-table tbody').html(data.list_personnel);
					$('.modal').modal('hide');
				} else {
					$('#modal-personnel .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$(".show-form").click(ShowForm);
$("#modal-personnel").on("submit",".create-form",SaveForm);

//update
$('.personnel-table').on("click",".show-form-update",ShowForm);
$('#modal-personnel').on("submit",".update-form",SaveForm)

});
//PERSONNEL

//CROP
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-crop').modal('show');
			},
			success: function(data){
				$('#modal-crop .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.crop-table tbody').html(data.list_crop);
					$('.modal').modal('hide');
				} else {
					$('#modal-crop .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$(".show-form").click(ShowForm);
$("#modal-crop").on("submit",".create-form",SaveForm);

//update
$('.crop-table').on("click",".show-form-update",ShowForm);
$('#modal-crop').on("submit",".update-form",SaveForm)

});
//CROP

//SOIL
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-soil').modal('show');
			},
			success: function(data){
				$('#modal-soil .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.soil-table tbody').html(data.list_soil);
					$('.modal').modal('hide');
				} else {
					$('#modal-soil .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$(".show-form").click(ShowForm);
$("#modal-soil").on("submit",".create-form",SaveForm);

//update
$('.soil-table').on("click",".show-form-update",ShowForm);
$('#modal-soil').on("submit",".update-form",SaveForm)

});
//SOIL

//CALIB
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-calib').modal('show');
			},
			success: function(data){
				$('#modal-calib .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.calib-table tbody').html(data.list_calib);
					$('.modal').modal('hide');
				} else {
					$('#modal-calib .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$(".show-form").click(ShowForm);
$("#modal-calib").on("submit",".create-form",SaveForm);

//update
$('.calib-table').on("click",".show-form-update",ShowForm);
$('#modal-calib').on("submit",".update-form",SaveForm)

});
//CALIB

//FIELDUNIT
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-fieldunit').modal('show');
			},
			success: function(data){
				$('#modal-fieldunit .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.fieldunit-table tbody').html(data.list_fieldunit);
					$('.modal').modal('hide');
				} else {
					$('#modal-fieldunit .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$(".show-form").click(ShowForm);
$("#modal-fieldunit").on("submit",".create-form",SaveForm);

//update
$('.fieldunit-table').on("click",".show-form-update",ShowForm);
$('#modal-fieldunit').on("submit",".update-form",SaveForm)

});
//FIELDUNIT

//SENSOR
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-sensor').modal('show');
			},
			success: function(data){
				$('#modal-sensor .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.sensor-table tbody').html(data.list_sensor);
					$('.modal').modal('hide');
				} else {
					$('#modal-sensor .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$(".show-form").click(ShowForm);
$("#modal-sensor").on("submit",".create-form",SaveForm);

//update
$('.sensor-table').on("click",".show-form-update",ShowForm);
$('#modal-sensor').on("submit",".update-form",SaveForm)

});
//SENSOR

//MC
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-mc').modal('show');
			},
			success: function(data){
				$('#modal-mc .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.mc-table tbody').html(data.list_mc);
					$('.modal').modal('hide');
				} else {
					$('#modal-mc .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$(".show-form").click(ShowForm);
$("#modal-mc").on("submit",".create-form",SaveForm);

//update
$('.mc-table').on("click",".show-form-update",ShowForm);
$('#modal-mc').on("submit",".update-form",SaveForm)

});
//MC

//BASIN
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-basin').modal('show');
			},
			success: function(data){
				$('#modal-basin .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.basin-table tbody').html(data.list_basin);
					$('.modal').modal('hide');
				} else {
					$('#modal-basin .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$(".show-form").click(ShowForm);
$("#modal-basin").on("submit",".create-form",SaveForm);

//update
$('.basin-table').on("click",".show-form-update",ShowForm);
$('#modal-basin').on("submit",".update-form",SaveForm)

});
//BASIN

//BORDER
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-border').modal('show');
			},
			success: function(data){
				$('#modal-border .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.border-table tbody').html(data.list_border);
					$('.modal').modal('hide');
				} else {
					$('#modal-border .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$('.show-form').click(ShowForm);
$("#modal-border").on("submit",".create-form",SaveForm);

//update
$('.border-table').on("click",".show-form-update",ShowForm);
$('#modal-border').on("submit",".update-form",SaveForm)

});
//BORDER
//FURROW
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-furrow').modal('show');
			},
			success: function(data){
				$('#modal-furrow .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.furrow-table tbody').html(data.list_furrow);
					$('.modal').modal('hide');
				} else {
					$('#modal-furrow .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$('.show-form').click(ShowForm);
$("#modal-furrow").on("submit",".create-form",SaveForm);

//update
$('.furrow-table').on("click",".show-form-update",ShowForm);
$('#modal-furrow').on("submit",".update-form",SaveForm)

});
//FURROW
//SPRINKLER
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-sprinkler').modal('show');
			},
			success: function(data){
				$('#modal-sprinkler .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.sprinkler-table tbody').html(data.list_sprinkler);
					$('.modal').modal('hide');
				} else {
					$('#modal-sprinkler .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$('.show-form').click(ShowForm);
$("#modal-sprinkler").on("submit",".create-form",SaveForm);

//update
$('.sprinkler-table').on("click",".show-form-update",ShowForm);
$('#modal-sprinkler').on("submit",".update-form",SaveForm)

});
//sprinkler
//drip
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-drip').modal('show');
			},
			success: function(data){
				$('#modal-drip .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.drip-table tbody').html(data.list_drip);
					$('.modal').modal('hide');
				} else {
					$('#modal-drip .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$('.show-form').click(ShowForm);
$("#modal-drip").on("submit",".create-form",SaveForm);

//update
$('.drip-table').on("click",".show-form-update",ShowForm);
$('#modal-drip').on("submit",".update-form",SaveForm)

});
//DRIP

//GRAVIMETRIC
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-gravi').modal('show');
			},
			success: function(data){
				$('#modal-gravi .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.gravi-table tbody').html(data.list_gravi);
					$('.modal').modal('hide');
				} else {
					$('#modal-gravi .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$('.show-form').click(ShowForm);
$("#modal-gravi").on("submit",".create-form",SaveForm);

//update
$('.gravi-table').on("click",".show-form-update",ShowForm);
$('#modal-gravi').on("submit",".update-form",SaveForm)

});
//GRAVIMETRIC

//RAINFALL
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-rainfall').modal('show');
			},
			success: function(data){
				$('#modal-rainfall .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.rainfall-table tbody').html(data.list_rainfall);
					$('.modal').modal('hide');
				} else {
					$('#modal-rainfall .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$('.show-form').click(ShowForm);
$("#modal-rainfall").on("submit",".create-form",SaveForm);

//update
$('.rainfall-table').on("click",".show-form-update",ShowForm);
$('#modal-rainfall').on("submit",".update-form",SaveForm)

});
//RAINFALL

//SHADED
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-shaded').modal('show');
			},
			success: function(data){
				$('#modal-shaded .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.shaded-table tbody').html(data.list_shaded);
					$('.modal').modal('hide');
				} else {
					$('#modal-shaded .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$('.show-form').click(ShowForm);
$("#modal-shaded").on("submit",".create-form",SaveForm);

//update
$('.shaded-table').on("click",".show-form-update",ShowForm);
$('#modal-shaded').on("submit",".update-form",SaveForm)

});
//SHADED

//WAISS
$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-system').modal('show');
			},
			success: function(data){
				$('#modal-system .modal-content').html(data.html_form);

			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('.system-table tbody').html(data.list_system);
					$('.modal').modal('hide');
				} else {
					$('#modal-system .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

// create 
$('.show-form').click(ShowForm);
$("#modal-system").on("submit",".create-form",SaveForm);

//update
$('.system-table').on("click",".show-form-update",ShowForm);
$('#modal-system').on("submit",".update-form",SaveForm)

});
//WAISS