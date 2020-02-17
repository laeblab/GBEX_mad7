from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from GBEX_app.drf import GBEX_API_ViewSets

router = routers.DefaultRouter()
for name, viewset in GBEX_API_ViewSets:
	router.register(name, viewset)


urlpatterns = [
	path('resumable_upload', include('GBEX_bigfiles.urls')),
	path('admin/', admin.site.urls),
	path('api/', include(router.urls)),
	path('', include('GBEX_app.urls')),
]


