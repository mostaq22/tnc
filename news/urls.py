from django.urls import path
from .views import homepage, fact_detail, post_detail, category
urlpatterns = [
    path('', homepage),
    path('fact/<int:id>/', fact_detail),
    path('post/<int:id>/', post_detail),
    path('category/<int:id>/', category),
]