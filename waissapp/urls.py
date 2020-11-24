from django.urls import path
from . import views

app_name = 'waiss'

urlpatterns = [
     path('dashboard/', views.index, name='index'),
     path('', views.login, name='login'),
     path('register/', views.register, name='register'),

     path('welcome/', views.load_page, name='load_page'),
     path('computation_option/', views.computation_option, name='simp_advanced'),
     path('choose-irrigation/', views.irrig_type, name='irrig_type'),

     #NEW_DATA
     path('newpersonnel/', views.newpersonnel, name='new_personnel'),
     path('newfieldunit/', views.newfieldunit, name='new_fieldunit'),
     path('newsensor/', views.newsensor, name='new_sensor'),
     path('newcrop/', views.newcrop, name='new_crop'),
     path('newsoil/', views.newsoil, name='new_soil'),
     path('newcalibrationequation/', views.newcalib, name='new_calib'),
     path('newbasin/', views.newbasin, name='new_basin'),
     path('newborder/', views.newborder, name='new_border'),
     path('newfurrow/', views.newfurrow, name='new_furrow'),
     path('newdrip/', views.newdrip, name='new_drip'),
     path('newsprinkler/', views.newsprinkler, name='new_sprinkler'),
     path('newsysbasin/', views.newsysbasin, name='new_sysbasin'),
     path('newsysborder/', views.newsysborder, name='new_sysborder'),
     path('newsysfurrow/', views.newsysfurrow, name='new_sysfurrow'),
     path('newsysdrip/', views.newsysdrip, name='new_sysdrip'),
     path('newsyssprinkler/', views.newsyssprinkler, name='new_syssprinkler'),
     path('newintakefamily/', views.newintakefamily, name='new_intakefamily'),

     path('about/', views.about, name='about'),
     path('charts/', views.charts, name='charts'), 
     path('show-irrig-calculations/', views.irrig_calculations, name='irrig-calculations'),
     
     #SYSTEMS
     path('calculate-basin-system/', views.basin_calc, name='sys_basin'),
     path('calculate-border-system/', views.border_calc, name='sys_border'),
     path('calculate-furrow-system/', views.furrow_calc, name='sys_furrow'),
     path('calculate-drip-system/', views.drip_calc, name='sys_drip'),
     path('calculate-sprinkler-system/', views.sprinkler_calc, name='sys_sprinkler'),
     
     #FIELDUNIT_PARAMETERS
     path('show-fieldunit-database/', views.fieldunit_list_view, name='list_fieldunit'),
     path('add-fieldunit/', views.add_fieldunit, name='add_fieldunit'),
     path('edit_fieldunit/<str:pk>/', views.editFieldUnit, name='edit_fieldunit'),
     path('delete_fieldunit/<str:pk>/', views.deleteFieldUnit, name='delete_fieldunit'),

     #SENSOR_PARAMETERS
     path('add-sensor/', views.add_sensor, name='add_sensor'),
     path('show-sensor-database/', views.sensor_list_view, name='list_sensor'),
     path('edit_sensor/<str:pk>/', views.editSensor, name='edit_sensor'),
     path('delete_sensor/<str:pk>/', views.deleteSensor, name='delete_sensor'),

     #CALIBRATION_PARAMETERS
     path('add-calib/', views.add_calib, name='add_calib'),
     path('show-calib-database/', views.list_calib, name='list_calib'),
     path('edit_calib/<str:pk>/', views.editCalib, name='edit_calib'),
     path('delete_calib/<str:pk>/', views.deleteCalib, name='delete_calib'),

     #FARM_PARAMETERS
     path('add-farm/', views.farm_account, name='add_farm'),   
     path('show-farm-database/', views.farm_list_view, name='list_farm'),
     path('edit_farm/<str:pk>/', views.editFarm, name='edit_farm'),
     path('delete_farm/<str:pk>/', views.deleteFarm, name='delete_farm'),

     #PERSONNEL_PARAMETERS
     path('add-farm-manager/',views.add_personnel, name='add_personnel'),
     path('show-personnel-database/', views.personnel_list_view, name='list_personnel'),
     path('edit_personnel/<str:pk>/', views.editPersonnel, name='edit_personnel'),
     path('delete_personnel/<str:pk>/', views.deletePersonnel, name='delete_personnel'),
    
     #CROP_PARAMETERS
     path('show-crop-database/', views.list_crop, name='list_crop'),
     path('add-crop-parameters/', views.add_crop, name='add_crop'),
     path('edit_crop/<str:pk>/', views.editCrop, name='edit_crop'),
     path('delete_crop/<str:pk>/', views.deleteCrop, name='delete_crop'),

     #SOIL_PARAMETERS
     path('add-soil-parameters/', views.add_soil, name='addsoil'),
     path('show-soil-database/', views.list_soil, name='list_soil'),
     path('edit_soil/<str:pk>/', views.editSoil, name='edit_soil'),
     path('delete_soil/<str:pk>/', views.deleteSoil, name='delete_soil'),
     
     #INTAKE_FAMILY_PARAMETERS
     path('add-intakefamily/', views.add_intakefamily, name='add_intakefamily'),
     path('show-intakefamily-database/', views.list_intakefamily, name='list_intakefamily'),
     path('edit_intakefamily/<str:pk>/', views.editIntakeFamily, name='edit_intakefamily'),
     path('delete_intakefamily/<str:pk>/', views.deleteIntakeFamily, name='delete_intakefamily'),

     #DRIP_PARAMETERS
     path('edit_drip/<str:pk>/', views.editDrip, name='edit_drip'),
     path('delete_drip/<str:pk>/', views.deleteDrip, name='delete_drip'),
     path('add-drip-system/', views.add_drip, name='adddrip'),
     path('show-drip-database/', views.drip_list, name='listdrip'),
     
     #SPRINKLER_PARAMETERS
     path('edit_sprinkler/<str:pk>/', views.editSprinkler, name='edit_sprinkler'),
     path('delete_sprinkler/<str:pk>/', views.deleteSprinkler, name='delete_sprinkler'),
     path('add-sprinkler-system/', views.add_sprinkler, name='addsprinkler'),
     path('show-sprinkler-database/', views.sprinkler_list, name='listsprinkler'),
     
     #BORDER_PARAMETERS
     path('edit_border/<str:pk>/', views.editBorder, name='edit_border'),
     path('delete_border/<str:pk>/', views.deleteBorder, name='delete_border'),
     path('add-border-system/', views.add_border, name='addborder'),
     path('show-border-database/', views.border_list, name='listborder'),
     
     #FURROW_PARAMETERS
     path('edit_furrow/<str:pk>/', views.editFurrow, name='edit_furrow'),
     path('delete_furrow/<str:pk>/', views.deleteFurrow, name='delete_furrow'),
     path('add-furrow-system/', views.add_furrow, name='addfurrow'),
     path('show-furrow-database/', views.furrow_list, name='listfurrow'),
     
     #BASIN_PARAMETERS
     path('edit_basin/<str:pk>/', views.editBasin, name='edit_basin'),
     path('delete_basin/<str:pk>/', views.deleteBasin, name='delete_basin'),
     path('add-basin-system/', views.add_basin, name='addbasin'),
     path('show-basin-database/', views.basin_list, name='listbasin'),

     path('send-message/', views.send_message, name='send-message'), #Send a message
     path('delete_msg/<str:pk>/', views.delete_msgs, name='messages_delete'),
     path('messages/', views.list_msgs, name='messages'),
     path('view-conversation/', views.view_msg, name='view-conversation'),
]