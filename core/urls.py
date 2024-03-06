
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('super-server/',include('server_app.urls',namespace='super_app')),
    path('',include('customer.urls',namespace='customer')),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)