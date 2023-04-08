from administration import views
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = "administration"

urlpatterns = [
    path('', views.index, name='index'),
    path('services', views.ServiceListCreateView.as_view(), name='service-list'),
    path('services/<int:pk>', views.ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/delete', views.ServiceDeleteView.as_view(), name='service-delete'),
    path('documents', views.DocumentListCreateView.as_view(), name='document-list'),
    path('documents/<int:pk>', views.DocumentUpdateView.as_view(), name='document-update'),
    path('documents/<int:pk>/delete', views.DocumentDeleteView.as_view(), name='document-delete'),
    path('companies', views.CompanyListCreateView.as_view(), name='company-list'),
    path('companies/<int:pk>', views.CompanyUpdateView.as_view(), name='company-update'),
    path('companies/<int:pk>/delete', views.CompanyDeleteView.as_view(), name='company-delete'),
    path('posts', views.PostListView.as_view(), name='post-list'),
    path('posts/create', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('users', views.UserListView.as_view(), name='user-list'),
    path('users/create', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/update', views.UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete', views.UserDeleteView.as_view(), name='user-delete'),
    path('auth/login', views.LoginView.as_view(), name='auth-login'),
    path('auth/profile', views.profile, name='auth-profile'),
    path('auth/logout', views.LogoutView.as_view(), name='auth-logout'),
    path('auth/password-change', views.PasswordChangeView.as_view(), name='auth-password-change'),
]
