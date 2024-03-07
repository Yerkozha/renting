
from rest_framework import routers

from .views import HireViewSet

router = routers.DefaultRouter()
router.register(r'', HireViewSet)

urlpatterns = router.get_urls()