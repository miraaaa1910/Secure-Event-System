from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView 
from django.conf import settings
from django.conf.urls.static import static
from events.views import SignUpView
from events import views as event_views

urlpatterns = [
    # Auth & Admin
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # Built-in Login/Logout
    path('accounts/signup/', SignUpView.as_view(), name='signup'),

    path('', TemplateView.as_view(template_name='home.html'), name='home'), # Landing page

    #Event CRUD
    path('events/', event_views.event_list, name='event_list'),
    path('events/new/', event_views.event_create, name='event_create'),
    path('events/<int:pk>/', event_views.event_detail, name='event_detail'),
    path('events/edit/<int:pk>/', event_views.event_update, name='event_update'),
    path('events/delete/<int:pk>/', event_views.event_delete, name='event_delete'),
    path('audit-log/', event_views.AuditLogListView.as_view(), name='audit_log'),
    path('profile/', event_views.profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 