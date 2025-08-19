import json
from django.test import TestCase
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Task
from django.urls import reverse

# Create your tests here.
class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('home'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpass'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
        self.assertFalse(response.context['user'].is_authenticated)  # Verify user is not logged in

    def test_logout(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass',
            'confirm_password': 'newpass'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('register'), {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpass',
        'confirm_password': 'wrongpass'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')
        self.assertFalse(response.context['user'].is_authenticated)  # Verify user is not registered/logged in

    def test_register_short_password(self):
        response = self.client.post(reverse('register'), {
            'username': 'shortpass',
            'email': 'short@example.com',
            'password': '12',
            'confirm_password': '12'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password must be at least 3 characters')
        self.assertFalse(User.objects.filter(username='shortpass').exists())

    def test_register_duplicate_username(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'dup@example.com',
            'password': 'testpass',
            'confirm_password': 'testpass'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Error, username already exists, User another.')

    def test_register_duplicate_email(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser2',
            'email': 'test@example.com',
            'password': 'testpass',
            'confirm_password': 'testpass'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email already in use.')

class TaskTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.client.login(username='testuser', password='testpass')
        self.task = Task.objects.create(user=self.user, text='My Task', status='todo', date='2025-08-17')

    def test_create_task(self):
        response = self.client.post(reverse('create-task'), data={
            'text': 'Test Task',
            'status': 'todo',
            'date': '2025-08-17'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(text='Test Task').exists())

    def test_get_task_list(self):
        response = self.client.get(
            reverse('get-tasks'), 
            {'date': '2025-08-17'}  # Pass the date matching the created task
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)  # Parse JSON response
        self.assertIn('tasks', data)
        self.assertEqual(len(data['tasks']), 1)
        self.assertEqual(data['tasks'][0]['text'], 'My Task')
        self.assertEqual(data['tasks'][0]['status'], 'todo')
        self.assertEqual(data['tasks'][0]['date'], '2025-08-17')

    def test_update_task(self):
        response = self.client.put(reverse('update-task', args=[self.task.id]), data={
            'text': 'My Task',
            'status': 'inprogress',
            'date': '2025-08-17'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'inprogress')


    def test_delete_task(self):
        response = self.client.delete(reverse('delete-task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_permission_cannot_edit_others_task(self):
        other_task = Task.objects.create(user=self.other_user, text='Other Task', status='todo', date='2025-08-17')
        response = self.client.put(reverse('update-task', args=[other_task.id]), data={
            'text': 'Hack Task',
            'status': 'done',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 404)  # Forbidden
        other_task.refresh_from_db()
        self.assertEqual(other_task.text, 'Other Task')  # unchanged

    def test_unauthorized_access_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('get-tasks'), follow=True)
        self.assertRedirects(response, '/login/?next=/api/tasks/')

class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_password_reset_request_valid_email(self):
        response = self.client.post(reverse('password_reset'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)  # redirect to done page

    def test_password_reset_request_invalid_email(self):
        response = self.client.post(reverse('password_reset'), {'email': 'wrong@example.com'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No account found with this email.")

    # EXTRA: resend password reset email
    def test_resend_password_reset_email(self):
        session = self.client.session
        session['reset_email'] = 'test@example.com'
        session.save()
        response = self.client.post(reverse('password_reset_resend'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password reset email resent.")
    
    # EXTRA: full reset flow (simplified)
    def test_full_password_reset_flow(self):
        # Step 1: request reset
        response = self.client.post(reverse('password_reset'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)

        # Step 2: get user and set new password manually (simulate confirm step)
        self.user.set_password('newpass123')
        self.user.save()

        # Step 3: login with new password
        login_success = self.client.login(username='testuser', password='newpass123')
        self.assertTrue(login_success)