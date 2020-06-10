from django.conf.urls import url
from resou import views
urlpatterns = [
  url(r'^resou/$',views.resouReturn)
]

