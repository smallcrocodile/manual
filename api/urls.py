from django.conf.urls import url,include
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls.static import static
from manual import settings

router = DefaultRouter()
router.register(r'companys', views.CompanyViewSet)
router.register(r'manuals',views.ManualViewSet)
router.register(r'docimages',views.DocImageViewSet)



urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^docs/', include_docs_urls(title='Manual API')),
    url(r'^token/', obtain_jwt_token),
    url(r'^search/',views.search),
    url(r'^getuser/',views.getuser),
    url(r'^getqrcode/',views.getqrcode),
    url(r'^upload/',views.upload),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)