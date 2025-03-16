from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),        # Landing page as the root
    path('projects/', include('projects.urls')),  # Projects page
]
