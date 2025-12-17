# proyecto_integracion/urls.py
from django.contrib import admin
from django.urls import path
from Barberia import views

# 👇 Sólo para desarrollo (sirve con runserver)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from Barberia import views
from Barberia.forms import MyLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas
    path('', views.mostrarindex,name='index'),
    path('Consulta/',views.consultas, name='consultas' ),
    path('Sobre/',views.mostrarSobreMI  , name='sobre' ),
    path('Agendamiento/', views.mostrarAgendamiento, name='agendar'),
    path('Agendamiento/ListadoHora', views.mostrarlistadoHora),
    path('RegistrarAgendamiento', views.RegistrarHorario),
    path('AgendarCita', views.AgendarCita),

    # APIs
    path('api/horas-disponibles/<int:dia_id>/', views.obtener_horas_disponibles, name='horas_disponibles'),
    path('api/slots', views.api_slots, name='api_slots'),  # 👉 añade esta si usas el calendario nuevo

    # PDF
    path('comprobante/<int:horario_id>/', views.generar_comprobante, name='generar_comprobante'),
    
    # auth
    path('login/',  auth_views.LoginView.as_view(
            template_name='auth/login.html',
            authentication_form=MyLoginForm
        ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('panel/', views.panel_horarios, name='panel'),
    path('panel/', views.panel_horarios, name='panel_horarios'),
    path('panel/export/', views.panel_export, name='panel_export'),
    path('panel/estado/<int:pk>/', views.panel_set_estado, name='panel_set_estado'),
    path("panel/calendario/", views.panel_calendario, name="panel_calendario"),
    path("panel/api/events/", views.panel_api_events, name="panel_api_events"),
    path("panel/export-rango/", views.panel_export_rango, name="panel_export_rango"),
    path("panel/exportar-excel/", views.panel_export_rango_excel, name="panel_export_rango_excel"),
    path("panel/api/stats/", views.panel_api_stats, name="panel_api_stats"),
    path("panel/api/canceladas/", views.panel_api_canceladas, name="panel_api_canceladas"),
    path("api/ocupadas", views.api_ocupadas, name="api_ocupadas")






]

# ❌ NUNCA declares rutas manuales a /static/... en urls
#    Esa línea tuya `path('static/css/style.cs/', ...)` rompía el CSS.
#    Debe ir este helper sólo en desarrollo:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
