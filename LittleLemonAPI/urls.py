from django.urls import path
from . import views
from django.urls import re_path as url
from django.urls import include
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LoginView, LogoutView
from .views import signup, ViewPerfil, profile_view
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
urlpatterns = [
    path('', views.ViewsHome, name='home'),
    #path('menu-items/', views.menu_items, name='Add_Menu'),
    #path('menu-items', views.MenuItemsView.as_view()),
    #path('menu-items/<int:id>', views.single_item),
    #path('category/<int:pk>', views.category_detail, name='category-detail'),
    #-------------filter options---------------------
    #path('menuitems', views.MenuItemsViewSet.as_view({'get':'list'})),
    #path('menuitems/<int:pk>', views.MenuItemsViewSet.as_view({'get':'retrieve'})),

    #path('secret/', views.secret),
    #path('api-token-auth/', obtain_auth_token),
    #path('me/', views.me),
    #path('manager-view/', views.manager_view),
    #path('throttle-check/', views.throttle_check),
    #path('throttle-check-auth/', views.throttle_check_auth),
    #path('groups/manager/users/', views.managers),
    path('login/', LoginView.as_view(template_name='LittleLemonAPI/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='LittleLemonAPI/logout.html'), name='logout'),
    path('signup/', signup, name='Sign_Up'),
    path('profile/<str:username>/', profile_view, name='Profile'),
    path('change_avatar/', views.change_avatar, name='change_avatar'),
    path('add_menu/', views.WriteMenu.as_view(), name='Add_Menu'),
    path('add_category/', views.CreateCategory.as_view(), name='Add_Category'),
    path('menu/', views.viewmenu, name='Menu'),
    path('menu/<int:page_number>/', RedirectView.as_view(url='/menu/')),
    path('update_item/', views.updateitem, name='update_item'),
    path('cart/', views.cart, name='Cart'),
    path('search/', views.search, name='Search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)