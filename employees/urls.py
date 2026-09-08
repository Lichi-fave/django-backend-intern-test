"""
URL routing for the employees app.

TODO (candidate): Wire up DepartmentViewSet and EmployeeViewSet here,
typically using a DRF DefaultRouter, so that the following endpoints exist:

    GET/POST         /api/departments/
    GET/PUT/DELETE   /api/departments/<id>/
    GET/POST         /api/employees/
    GET/PUT/DELETE   /api/employees/<id>/

Example pattern once your views are ready:

    from rest_framework.routers import DefaultRouter
    from .views import DepartmentViewSet, EmployeeViewSet

    router = DefaultRouter()
    router.register('departments', DepartmentViewSet)
    router.register('employees', EmployeeViewSet)

    urlpatterns = router.urls
"""


from  rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, EmployeeViewSet

router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('employees', EmployeeViewSet)

urlpatterns = router.urls
