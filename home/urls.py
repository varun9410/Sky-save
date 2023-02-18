from home import views
from django.urls.conf import path
urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('drive',views.drive,name='drive'),
    path('logout',views.logout,name='logout'),
    path('upload',views.upload,name='upload'),
    path('table',views.table,name='table'),
    path('download/<str:file_url>',views.download,name='download'),
    path('delete/<int:id>',views.delete,name='delete')
]
