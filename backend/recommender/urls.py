from django.conf.urls import url
from recommender import views

urlpatterns = [
    #url(r'^$',views.index, name="index"),
    url(r'^$',views.post_recommender, name="index"),
]