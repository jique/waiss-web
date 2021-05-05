from django.urls import path
from . import views


app_name = 'waiss'

urlpatterns = [
     path('', views.index, name='index'),
     path('register/', views.register, name='register'),
     path('accounts/profile', views.profile, name='profile'),
     path('about/', views.about, name='about'),
     path('about-the-calculations/', views.about_calc, name='about_calc'),
     
     #FIELDUNIT_PARAMETERS
     path('new_fieldunit/', views.new_fieldunit, name='new_fieldunit'),
     path('add_fieldunit/', views.add_fieldunit, name='add_fieldunit'),
     path('list_fieldunit/', views.list_fieldunit, name='list_fieldunit'),
     path('edit_fieldunit/<str:pk>/', views.edit_fieldunit, name='edit_fieldunit'),
     path('delete_fieldunit/<str:pk>/', views.delete_fieldunit, name='delete_fieldunit'),

     #SENSOR_PARAMETERS
     path('new_sensor/', views.new_sensor, name='new_sensor'),
     path('add_sensor/', views.add_sensor, name='add_sensor'),
     path('list_sensor/', views.list_sensor, name='list_sensor'),
     path('edit_sensor/<str:pk>/', views.edit_sensor, name='edit_sensor'),
     path('delete_sensor/<str:pk>/', views.delete_sensor, name='delete_sensor'),

     #CALIBRATION_PARAMETERS
     path('new_calib/', views.new_calib, name='new_calib'),
     path('add_calib/', views.add_calib, name='add_calib'),
     path('list_calib/', views.list_calib, name='list_calib'),
     path('edit_calib/<str:pk>/', views.edit_calib, name='edit_calib'),
     path('delete_calib/<str:pk>/', views.delete_calib, name='delete_calib'),

     #FARM_PARAMETERS
     path('new_farm/', views.new_farm, name='new_farm'),
     path('add_farm/', views.add_farm, name='add_farm'),   
     path('list_farm/', views.list_farm, name='list_farm'),
     path('edit_farm/<str:pk>/', views.edit_farm, name='edit_farm'),
     path('delete_farm/<str:pk>/', views.delete_farm, name='delete_farm'),

     #PERSONNEL_PARAMETERS
     path('new_personnel/', views.new_personnel, name='new_personnel'),
     path('add_personnel/',views.add_personnel, name='add_personnel'),
     path('list_personnel/', views.list_personnel, name='list_personnel'),
     path('edit_personnel/<str:pk>/', views.edit_personnel, name='edit_personnel'),
     path('delete_personnel/<str:pk>/', views.delete_personnel, name='delete_personnel'),
    
     #CROP_PARAMETERS
     path('new_crop/', views.new_crop, name='new_crop'),
     path('list_crop/', views.list_crop, name='list_crop'),
     path('add_crop/', views.add_crop, name='add_crop'),
     path('edit_crop/<str:pk>/', views.edit_crop, name='edit_crop'),
     path('delete_crop/<str:pk>/', views.delete_crop, name='delete_crop'),

     #SOIL_PARAMETERS
     path('new_soil/', views.new_soil, name='new_soil'),
     path('add_soil/', views.add_soil, name='add_soil'),
     path('list_soil/', views.list_soil, name='list_soil'),
     path('edit_soil/<str:pk>/', views.edit_soil, name='edit_soil'),
     path('delete_soil/<str:pk>/', views.delete_soil, name='delete_soil'),
     
     #IRRIGATION_PARAMETERS
     path('new_irrigation/', views.new_irrigation, name='new_irrigation'),
     path('new_basin/', views.new_basin, name='new_basin'),
     path('new_border/', views.new_border, name='new_border'),
     path('new_furrow/', views.new_furrow, name='new_furrow'),
     path('new_drip/', views.new_drip, name='new_drip'),
     path('new_sprinkler/', views.new_sprinkler, name='new_sprinkler'),
     path('add_basin/', views.add_basin, name='add_basin'),
     path('add_border/', views.add_border, name='add_border'),
     path('add_drip/', views.add_drip, name='add_drip'),
     path('add_furrow/', views.add_furrow, name='add_furrow'),
     path('add_sprinkler/', views.add_sprinkler, name='add_sprinkler'),
     path('list_basin/', views.list_basin, name='list_basin'),
     path('list_border/', views.list_border, name='list_border'),
     path('list_furrow/', views.list_furrow, name='list_furrow'),
     path('list_sprinkler/', views.list_sprinkler, name='list_sprinkler'),
     path('list_drip/', views.list_drip, name='list_drip'),
     path('edit_basin/<str:pk>/', views.edit_basin, name='edit_basin'),
     path('edit_border/<str:pk>/', views.edit_border, name='edit_border'),
     path('edit_furrow/<str:pk>/', views.edit_furrow, name='edit_furrow'),
     path('edit_sprinkler/<str:pk>/', views.edit_sprinkler, name='edit_sprinkler'),
     path('edit_drip/<str:pk>/', views.edit_drip, name='edit_drip'),
     path('delete_basin/<str:pk>/', views.delete_basin, name='delete_basin'),
     path('delete_border/<str:pk>/', views.delete_border, name='delete_border'),
     path('delete_furrow/<str:pk>/', views.delete_furrow, name='delete_furrow'),
     path('delete_sprinkler/<str:pk>/', views.delete_sprinkler, name='delete_sprinkler'),
     path('delete_drip/<str:pk>/', views.delete_drip, name='delete_drip'),

     #MESSAGES
     path('messages/', views.list_msgs, name='messages'),
     path('delete_msg/<str:pk>/', views.delete_msgs, name='messages_delete'),
     path('view-conversation/<str:number>/', views.view_msg, name='view-conversation'),

     #MC READINGS
     path('new_mc/', views.new_mc, name='new_mc'),
     path('add_mc/', views.add_mc, name='add_mc'),
     path('list_mc/<str:name>/', views.list_mc, name='list_mc'),
     path('edit_mc/<str:name>/', views.edit_mc, name='edit_mc'),
     path('delete_mc/<str:pk>/', views.delete_mc, name='delete_mc'),

     #WAISSystems
     path('new_system/', views.new_system, name='new_system'),
     path('add_system/', views.add_system, name='add_system'),
     path('edit_system/<str:pk>/', views.edit_system, name='edit_system'),
     path('list_system/', views.list_system, name='list_system'),
     path('delete_system/<str:pk>/', views.delete_system, name='delete_system'),

     #Other Data
     path('add_percent_shaded/', views.add_shaded, name='add_shaded'),
     path('edit_percent_shaded/<str:pk>/', views.edit_shaded, name='edit_shaded'),
     path('delete_percent_shaded/<str:pk>/', views.delete_shaded, name='delete_shaded'),

     path('add_gravimetric/', views.add_gravimetric, name='add_gravimetric'),
     path('edit_gravimetric/<str:pk>/', views.edit_gravimetric, name='edit_gravimetric'),
     path('delete_gravimetric/<str:pk>/', views.delete_gravimetric, name='delete_gravimetric'),

     path('add_rainfall/', views.add_rainfall, name='add_rainfall'),
     path('edit_rainfall/<str:pk>/', views.edit_rainfall, name='edit_rainfall'),
     path('delete_rainfall/<str:pk>/', views.delete_rainfall, name='delete_rainfall'),

     path('upload_csv/', views.upload_csv, name='upload_csv')
]