from django.urls import path
from .views import *

app_name = 'fowlist'

urlpatterns = [
    path('', index),
    path('login/', FowlistLoginView.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', fowlist_logout, name='logout'),
    path('change-email/', ChangeEmailUserView.as_view(), name='change-email'),
    path('password-change/', ChangePasswordView.as_view(), name='password-change'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register/done/', RegisterDoneView.as_view(), name='register-done'),
    path('register/activate/<str:sign>/', user_activate, name='register-activate'),
    path('profile/create-checklist', create_checklist, name='create-checklist'),
    path('profile/create-goal', create_goal, name='create-goal'),
    path('list/', all_lists, name='all_lists' ),
    path('profile/is_done', point_is_done, name='is_done'),
    path('list/add-checklist', add_checklist, name='add-checklist'),
    path('profile/delete_list', delete_list, name='delete_list'),
    path('profile/get_edit_list', get_edit_list, name='get_edit_list'),
    path('profile/edit_list', edit_list, name="edit_list")
]