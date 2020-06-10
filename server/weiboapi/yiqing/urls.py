from django.conf.urls import url
from yiqing import views
urlpatterns = [
  url(r'^yiqing/$',views.yiqingReturn)
]

