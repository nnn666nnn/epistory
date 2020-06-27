from django.conf.urls import url
from qingxu import views
urlpatterns = [
        url(r'^qingxu/$',views.qingxuReturn)
        ]
