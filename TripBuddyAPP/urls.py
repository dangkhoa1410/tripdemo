from django.urls import path


from . import views	# the . indicates that the views file can be found in the same directory as this file
                    
urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('travels', views.success),
    path('logout', views.logout),
    path('addtrip', views.create),
    path('view/<int:tripID>', views.tripinfo),
    path('newtrip', views.new),
    path('join/<int:tripID>',views.join),
    path('cancel/<int:tripID>',views.cancel),
    path('delete/<int:tripID>',views.delete),
]
