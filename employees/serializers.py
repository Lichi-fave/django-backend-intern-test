# TODO (candidate): Define DepartmentSerializer and EmployeeSerializer here
# using rest_framework.serializers.ModelSerializer, once the Department and
# Employee models exist in models.py.
#
# Remember the API must reject:
#   - duplicate employee email
#   - invalid email format
#   - negative salary
#   - a department id that doesn't exist
#
# Model-level constraints (unique=True, MinValueValidator, EmailField) are
# inherited automatically by ModelSerializer in most cases, but confirm this
# with your own tests.

from rest_framework import serializers
from .models import Department, Employee

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'department', 'job_title', 'salary', 'date_joined', 'is_active', 'created_at']
        read_only_fields = ['id', 'date_joined', 'created_at']


 # EmailField(unique=True) on the model gives the duplicate-email and invalid-format validation through 
 # ModelSerializer's auto generated UniqueValidator + EmailField. MinValueValidator(0) on `salary`
 # already rejects negative values. A non-exisent `dpartment`id is rejected automatically because department
 # is a PrimaryKeyRelatedField by default, which checks for existence of the referenced row.  
