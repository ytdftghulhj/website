"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from blog.views import *

router = routers.DefaultRouter()
router.register(r'user', CustomUserViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'article', ArticleViewSet)
router.register(r'subscription', SubscriptionsViewSet)
router.register(r'comment', CommentsViewSet)
router.register(r'notification', NotificationViewSet)

blog_urls = [
    path('api/', include(router.urls))
]

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(blog_urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', AuthUserView.as_view(), name='login'),
    path('registr/', RegistrUserView.as_view(), name='registr'),
    path('users/<int:pk>/', RegistrUserView.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

