from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from .views import index, result

urlpatterns = [
    path('', index, name='index'),
    path('result/<int:shift_id>', result, name='result'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)