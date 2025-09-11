from rest_framework.routers import DefaultRouter
from .views import ClassTypeViewSet, InstructorViewSet, ClassSessionViewSet

router = DefaultRouter()
router.register(r'classtypes', ClassTypeViewSet)
router.register(r'instructors', InstructorViewSet)
router.register(r'classsessions', ClassSessionViewSet)

urlpatterns = router.urls
