from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
path("", views.homepage, name="home"),

path("<str:community>", views.communities, name="community"),
path("new_community/", views.new_community, name="new-community"),
path("<str:community>/edit", views.community_edit, name="community-edit"),
path("<str:community>/<str:author>/delete", views.community_delete, name="community-delete"),

path("<str:community>/<str:post>", views.post_details, name="post-details"),
path("<str:community>/new_post/", views.new_post, name="new-post"),
path("<str:community>/<str:post>/edit", views.post_edit, name="post-edit"),
path("<str:community>/<str:post>/<str:author>/delete", views.post_delete, name="post-delete"),

path("<str:category>/", views.category_filter, name="show-category"),


   
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)