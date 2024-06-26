from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("dashbord.urls")),
    path("api/",include("talvido_app.api.urls")),
    path("api/",include("mlm.api.urls")),
    path("api/payment/",include("payment.razorpay.urls")),
    path("api/",include("chat.api.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
