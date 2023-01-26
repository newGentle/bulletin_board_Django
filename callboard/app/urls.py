from django.urls import path, include
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, MyPostsList, response_accept, response_delete, subscribe, unsubscribe

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('createpost', PostCreate.as_view(), name='create_post'),
    path('<int:pk>/updatepost', PostUpdate.as_view(), name='update_post'),
    path('<int:pk>/deletepost', PostDelete.as_view(), name='delete_post'),
    path('myposts', MyPostsList.as_view(), name='myposts_list'),
    path('response_accept/<int:pk>', response_accept, name='response_accept'),
    path('response_delete/<int:pk>', response_delete, name='response_delete'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),

]
