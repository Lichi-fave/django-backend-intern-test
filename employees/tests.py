from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Department, Employee



class SetupSanityTests(APITestCase):
    """
    Confirms the project boots and `python manage.py test` runs cleanly
    before you've written any code. Feel free to delete this once you
    have real tests below.
    """

    def test_environment_is_configured(self):
        self.assertTrue(True)


# TODO (candidate): Add your own tests below. At minimum, cover:
#   - Department creation
#   - Employee creation
#   - Employee listing
#   - Employee retrieval
#   - Duplicate email validation (should be rejected)
#   - Negative salary validation (should be rejected)
#   - Department filtering (e.g. ?department=<id>)
#   - Authentication restrictions (writes require login, reads don't)
#
# Tip: rest_framework.test.APITestCase is generally a better fit than
# django.test.TestCase for exercising the API endpoints themselves.

class DepartmentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_anyone_can_list_departments(self):
        Department.objects.create(name='Sales')
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_create_department(self):
        response = self.client.post('/api/departments/', {'name': 'Engineering'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_authenticated_user_can_create_department(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/departments/', {'name': 'Engineering'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 1)

class EmployeeAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.dept = Department.objects.create(name='Sales')
        self.other_dept = Department.objects.create(name='Marketing')

    def _auth(self):
        self.client.force_authenticate(user=self.user)

    def test_create_employee(self):
        self._auth()
        payload = {
            'first_name': 'Deborah',
            'last_name': 'Samuels',
            'email': 'deborah.samuels@gmail.com',
            'department': self.dept.id,
            'salary': '50000.00',
        }
        response = self.client.post('/api/employees/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)

    def test_list_employees(self):
        Employee.objects.create(first_name='Lara', last_name='George', email='lara.george@gmail.com', department=self.dept, salary='40000')
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_employee(self):
        emp = Employee.objects.create(first_name='Lara', last_name='George', email='lara.george@gmail.com', department=self.dept, salary='40000')
        response = self.client.get(f'/api/employees/{emp.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'lara.george@gmail.com')

    def test_duplicate_email_rejected(self):
        self._auth()
        Employee.objects.create(first_name='Lara', last_name='George', email='lara.george@gmail.com', department=self.dept, salary='40000')
        payload = {
            'first_name': 'Deborah',
            'last_name': 'Samuels',
            'email': 'lara.george@gmail.com',  
            'department': self.dept.id,
            'salary': '50000.00',
        }
        response = self.client.post('/api/employees/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


    def test_invalid_email_format_rejected(self):
        self._auth()
        payload = {
            'first_name': 'Deborah',
            'last_name': 'Samuels',
            'email': 'not-an-email',
            'department': self.dept.id,
            'salary': '50000.00',
        }
        response = self.client.post('/api/employees/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_negative_salary_rejected(self):
        self._auth()
        payload = {
            'first_name': 'Lara',
            'last_name': 'George',
            'email': 'lara.george@gmail.com',
            'department': self.dept.id,
            'salary': '-50000.00',
        }
        response = self.client.post('/api/employees/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('salary', response.data)

    def test_nonexistent_department_rejected(self):
        self._auth()
        payload = {
            'first_name': 'Lara',
            'last_name': 'George',
            'email': 'lara.george@gmail.com',
            'department': 999,  # Non-existent department ID
            'salary': '50000.00',
        }
        response = self.client.post('/api/employees/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('department', response.data)

    def test_filter_by_department(self):
        Employee.objects.create(first_name='Deborah', last_name='Samuels', email='deborah.samuels@gmail.com', department=self.dept, salary='40000')
        Employee.objects.create(first_name='Samantha', last_name='Parker', email='samantha.parker@gmail.com', department=self.other_dept, salary='45000')
        response = self.client.get(f'/api/employees/?department={self.dept.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['email'], 'deborah.samuels@gmail.com')

    def test_filter_by_is_active(self):
        Employee.objects.create(first_name='Deborah', last_name='Samuels', email='deborah.samuels@gmail.com', department=self.dept, salary='40000', is_active=False)
        Employee.objects.create(first_name='Samantha', last_name='Parker', email='samantha.parker@gmail.com', department=self.dept, salary='45000', is_active=True)
        response = self.client.get(f'/api/employees/?is_active=true')
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['email'], 'samantha.parker@gmail.com')

    def test_search_employees(self):
        Employee.objects.create(first_name='Pierre', last_name='Dupont', email='pierre.dupont@gmail.com', department=self.dept, salary='40000')
        Employee.objects.create(first_name='Samantha', last_name='Parker', email='samantha.parker@gmail.com', department=self.dept, salary='45000')
        response = self.client.get(f'/api/employees/?search=pierre')
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['first_name'], 'Pierre')

    def test_unauthenticated_cannot_write(self):
        payload = {
            'first_name': 'Deborah',
            'last_name': 'Samuels',
            'email': 'deborah.samuels@gmail.com',
            'department': self.dept.id,
            'salary': '50000.00',
        }
        response = self.client.post('/api/employees/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_delete(self):
        emp = Employee.objects.create(first_name='Lara', last_name='George', email='lara.george@gmail.com', department=self.dept, salary='40000')
        response = self.client.delete(f'/api/employees/{emp.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)