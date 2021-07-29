from django.urls import path
from . import views, computations

app_name = 'waiss'

urlpatterns = [
     path('dashboard/', computations.index, name='index'),
     path('accounts/register/', views.register, name='register'),
     path('accounts/profile', views.profile, name='profile'),
     path('about/', views.about, name='about'),
     path('about-the-calculations/', views.about_calc, name='about_calc'),
     path('', views.home, name='home_page'),
     path('waiss/', views.home_waiss, name='home_page_waiss'),
     
     #FIELDUNIT_PARAMETERS
     path('new_fieldunit/', views.new_fieldunit, name='new_fieldunit'),
     path('add_fieldunit/', views.add_fieldunit, name='add_fieldunit'),
     path('list_fieldunit/', views.list_fieldunit, name='list_fieldunit'),
     path('edit_fieldunit/<str:id>/update', views.edit_fieldunit, name='edit_fieldunit'),

     #SENSOR_PARAMETERS
     path('new_sensor/', views.new_sensor, name='new_sensor'),
     path('add_sensor/', views.add_sensor, name='add_sensor'),
     path('list_sensor/', views.list_sensor, name='list_sensor'),
     path('edit_sensor/<str:id>/update', views.edit_sensor, name='edit_sensor'),

     #CALIBRATION_PARAMETERS
     path('new_calib/', views.new_calib, name='new_calib'),
     path('add_calib/', views.add_calib, name='add_calib'),
     path('list_calib/', views.list_calib, name='list_calib'),
     path('edit_calib/<str:id>/update', views.edit_calib, name='edit_calib'),

     #FARM_PARAMETERS
     path('new_farm/', views.new_farm, name='new_farm'),
     path('add_farm/', views.add_farm, name='add_farm'),   
     path('list_farm/', views.list_farm, name='list_farm'),
     path('edit_farm/<str:id>/update', views.edit_farm, name='edit_farm'),

     #PERSONNEL_PARAMETERS
     path('new_personnel/', views.new_personnel, name='new_personnel'),
     path('add_personnel/',views.add_personnel, name='add_personnel'),
     path('list_personnel/', views.list_personnel, name='list_personnel'),
     path('edit_personnel/<str:id>/update', views.edit_personnel, name='edit_personnel'),

    
     #CROP_PARAMETERS
     path('new_crop/', views.new_crop, name='new_crop'),
     path('list_crop/', views.list_crop, name='list_crop'),
     path('add_crop/', views.add_crop, name='add_crop'),
     path('edit_crop/<str:id>/update', views.edit_crop, name='edit_crop'),

     #SOIL_PARAMETERS
     path('new_soil/', views.new_soil, name='new_soil'),
     path('add_soil/', views.add_soil, name='add_soil'),
     path('list_soil/', views.list_soil, name='list_soil'),
     path('edit_soil/<str:id>/update', views.edit_soil, name='edit_soil'),
     
     #IRRIGATION_PARAMETERS
     path('new_irrigation/', views.new_irrigation, name='new_irrigation'),
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
     path('edit_basin/<str:id>/update', views.edit_basin, name='edit_basin'),
     path('edit_border/<str:id>/update', views.edit_border, name='edit_border'),
     path('edit_furrow/<str:id>/update', views.edit_furrow, name='edit_furrow'),
     path('edit_drip/<str:id>/update', views.edit_drip, name='edit_drip'),
     path('edit_sprinkler/<str:id>/update', views.edit_sprinkler, name='edit_sprinkler'),

     #MESSAGES
     path('messages/', views.list_msgs, name='messages'),
     path('delete_msg/<str:pk>/', views.delete_msgs, name='messages_delete'),
     path('view-conversation/<str:number>/', views.view_msg, name='view-conversation'),

     #MC READINGS
     path('new_mc/', views.new_mc, name='new_mc'),
     path('add_mc/', views.add_mc, name='add_mc'),
     path('list_mc/<str:name>/', views.list_mc, name='list_mc'),
     path('edit_mc/<str:id>/update', views.edit_mc, name='edit_mc'),


     #WAISSystems
     path('new_system/', views.new_system, name='new_system'),
     path('add_system/', views.add_system, name='add_system'),
     path('edit_system/<str:id>/', views.edit_system, name='edit_system'),
     path('list_system/', views.list_system, name='list_system'),

     #Other Data
     path('add_shaded/', views.add_shaded, name='add_shaded'),
     path('edit_shaded/<str:id>/update', views.edit_shaded, name='edit_shaded'),
     path('list_shaded/', views.list_shaded, name='list_shaded'),

     path('add_gravi/', views.add_gravi, name='add_gravi'),
     path('edit_gravi/<str:id>/update', views.edit_gravi, name='edit_gravi'),
     path('list_gravi/', views.list_gravi, name='list_gravi'),

     path('add_rainfall/', views.add_rainfall, name='add_rainfall'),
     path('edit_rainfall/<str:id>/update', views.edit_rainfall, name='edit_rainfall'),
     path('list_rainfall/', views.list_rainfall, name='list_rainfall'),

     path('upload_csv/', views.upload_csv, name='upload_csv'),
     path('options/', views.options, name='simp_advanced'),
     path('sarai-header/', views.sarai_header, name='sarai_header')
]