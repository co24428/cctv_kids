from django.urls import path
from . import views
urlpatterns = [
    # 조심
    path('article/insert', views.article_insert, name="article/insert"),
    path('chart/insert', views.chart_insert, name="chart/insert"),

    # 차트
    path('chart/list', views.chart_list, name="chart/list"),
    path('chart/barplt', views.chart_barplt, name="chart/barplt"),
    path('chart/circleplt', views.chart_circleplt, name="chart/circleplt"),
    path('chart/total', views.chart_total, name="chart/total"),
]

