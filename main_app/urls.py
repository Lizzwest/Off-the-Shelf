from django.urls import path, re_path
from . import views
# from django.conf.urls import handler404

# handler404 = views.handler404

urlpatterns = [
    path('', views.index, name='index'),
    path('search_results/', views.search_results, name='search_results'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<username>/', views.profile, name='profile'),
    path('book_show/<int:id>/', views.book_show, name="book_show"),
    path('comments/<int:pk>/update/', views.CommentUpdate.as_view(), name="comments_update"),
    re_path(r'^(?P<path>.*)/$',views.handler404),
    # path('comment/create/<int:book_id>', views.CommentCreate.as_view(), name='comment_create'),
    # path('user/<username>/delete/', views.CatDelete.as_view(), name='cats_delete'),
]
