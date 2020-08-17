from django.urls import path
from . import views

app_name = 'waiss'

urlpatterns = [
     path('', views.index, name='index'),
     path('input-calibration-constants/', views.calib, name='calib'),
     path('about/', views.about, name='about'),
     path('charts/', views.charts, name='charts'),
     path('add-farm/', views.farm_account, name='farmaccount'),    
     path('add-sensor/', views.add_sensor, name='addsensor'),
     path('add-fieldunit/', views.add_fieldunit, name='addfieldunit'),
     path('add-intakefamily/', views.add_intake, name='intakefamily'),
     path('add-advisorysettings/',views.add_personnel, name='advisorysettings'),
     
     path('add-fieldunit-settings/', views.field_unit_settings, name='fieldunitsettings'),
     path('select-irrig-type/', views.choose_irrig, name='irriginfo'),
     path('select-irrig-type-database/', views.choose_irrig_database, name='choose-irrigation-system-type'),
     path('show-irrig-calculations/', views.irrig_calculations, name='irrig-calculations'),
     path('show-farm-summary/', views.farm_summaries, name='farmsummaries'),
     
     
     path('show-calib-equations-database/',views.select_eqn, name='select_eqn'),
     path('show_intakefamily/-database', views.select_intakefamily, name='select_intakefamily'),
     path('show-fieldunit-database/', views.fieldunit_list_view, name='fieldunitslist'),
     path('show-farm-database/', views.farm_list_view, name='farmlist'),
     path('show-sensor-database/', views.sensor_list_view, name='sensorlist'),
     path('show-personnel-database/', views.personnel_list_view, name='personnellist'),
    
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
]