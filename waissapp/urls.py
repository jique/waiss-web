from django.urls import path
from . import views

app_name = 'waiss'

urlpatterns = [
     path('dashboard/', views.index, name='index'),
     path('login/', views.login, name='login'),
     path('signin/', views.register, name='register'),
     path('welcome/', views.load_page, name='load_page'),
     path('computation_option/', views.computation_option, name='simp_advanced'),
     path('about/', views.about, name='about'),
     path('about-the-calculations/', views.about_calc, name='about_calc'),
     
     #SYSTEMS
     path('calculate-basin-system/', views.basin_calc, name='sys_basin'),
     
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
     path('add_irrigation/', views.add_irrigation, name='add_irrigation'),
     path('edit_irrigation/<str:pk>/', views.edit_irrigation, name='edit_irrigation'),
     path('list_irrigation/', views.list_irrigation, name='list_irrigation'),
     path('delete_irrigation/<str:pk>/', views.delete_irrigation, name='delete_irrigation'),

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
]