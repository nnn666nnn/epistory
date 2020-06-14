from django.conf.urls import url
from wbcipin import views
urlpatterns = [
    url(r'^wbcipin/$',views.wbcipinReturn)
]
