from django.conf.urls import url
from rscipin import views
urlpatterns = [
  url(r'^rscipin/$',views.rscipinReturn)
]

