from django.urls import path
from . import views
from .views import IndicatorForm
# from django.conf.urls import patterns, url, include


urlpatterns = [
    path('', views.home, name='homepage'),
    path('update', views.update_request, name='update_request'),
    path('delete', views.delete_database, name='dalete'),
    path('stocks', views.stocks_table, name='show_stocks'),
    path('stocks/<id>/', views.records_table, name='show_records'),
    path('indicators', views.indicators_table, name='show_indicators'),
    path('indicators/<name>/', views.boughts_table, name='show_indicator'),
    path('indicators/<name>/delete', views.delete_indicator, name='delete_indicator'),
    path('indicators/<name>/update', views.update_indicator, name='update_indicator'),
    path('add_indicator/', views.add_indicator, name='add_indicator'),
    # url(r'^email/send/$', views.sendmail),

]