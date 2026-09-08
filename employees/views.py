# TODO (candidate): Define DepartmentViewSet and EmployeeViewSet here using
# rest_framework.viewsets.ModelViewSet, once your models and serializers
# exist.
#
# Requirements to implement on the views:
#   - Unauthenticated users may GET (list/retrieve) employees and departments.
#   - Only authenticated users may POST/PUT/DELETE.
#   - Employee list must support filtering by `department` and `is_active`,
#     e.g. GET /api/employees/?department=1&is_active=true
#   - Employee list must support search across first_name, last_name, email,
#     and job_title, e.g. GET /api/employees/?search=john
#
# See the README for the full endpoint and permission spec.

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    GET (list/retrieve) for unauthenticated users, 
    POST/PUT/DELETE for authenticated users.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    GET (list/retrieve) for unauthenticated users, 
    POST/PUT/DELETE for authenticated users.
    Supports filtering by `department` and `is_active`, and search across
    first_name, last_name, email, and job_title.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'job_title']
