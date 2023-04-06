from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app1 import views

urlpatterns =[
    path('admin',admin.site.urls),
    path('',views.index,name="index"),
    path('videos',views.videos,name = "videos"),
    path('videos2',views.videos2,name = "videos2"),
    path('dashboard_filter',views.dashboard,name = "dashboard_filter"),

    path('kpi_dashboard',views.kpi_dashboard,name = "kpi_dashboard"),
    path('operation',views.operation,name = "operation"),
    path('customer_service',views.customer_service,name = "customer_service"),
    path('primer_customer',views.primer_customer,name = "primer_customer"),
    path('security',views.security,name = "security"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  