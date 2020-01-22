from django.urls import path
from . import views
urlpatterns = [
    # 조심
    path('article/insert', views.article_insert, name="article/insert"),
    path('chart/insert', views.chart_insert, name="chart/insert"),

    # 차트
    path('chart/list', views.chart_list, name="chart/list"),
    path('chart/barplt', views.chart_barplt, name="chart/barplt"),
    path('chart/total', views.chart_total, name="chart/total"),
    path('chart/big', views.chart_big, name="chart/big"),
    path('chart/small', views.chart_small, name="chart/small"),
    path('chart/favorite', views.chart_favorite, name="chart/favorite"),
    path('chart/unfavorite', views.chart_unfavorite, name="chart/unfavorite"),

    # 메인
    path('main/index', views.main_index, name= "index"),
    path('main/login', views.main_login, name = "login"),
    path('main/join', views.main_join, name = "join"),
    path('main/logout', views.main_logout, name = "logout"),
    path('main/mypage', views.main_mypage, name = "main_mypage"),

    # 기사
    path('article/main',views.article_main, name="article/main"),
    path('article/scrap',views.article_scrap1, name="article/scrap"),

]

