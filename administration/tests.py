from django.test import TestCase, tag
from administration.serializer import UserAdminSerializer
from users.models import User
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, Mock
import json
from users.test_utils import get_credentials


class UserAdminSerializerTestCase(TestCase):

    def setUp(self):
        self.serializer_class = UserAdminSerializer
        self.user_attributes = {
            'email': 'test2@gmail.com', "is_active": True}
        self.serializer_data = {
            'id': 1,
            'email': 'test1@gmail.com',
            'is_active': True,
            'password': 'test',
            'created_at': '2019-07-04T15:28:54.842295Z',
            'updated_at': '2019-07-04T15:29:22.445290Z'
        }

        self.user = User.objects.create(**self.user_attributes)
        self.serializer = self.serializer_class(instance=self.user)

    def test_containt_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'email', 'is_active',
                                            'created_at', 'updated_at'])

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user_attributes['email'])

    def test_valid_data_serializer(self):
        serializer = self.serializer_class(data=self.serializer_data)
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_serializer(self):
        serializer = self.serializer_class(data=self.user_attributes)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer(self):
        serializer = self.serializer_class(data=self.serializer_data)
        serializer.is_valid()
        self.assertEqual(str(serializer.create(
            serializer.validated_data)), self.serializer_data['email'])


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.headers = get_credentials(
            self.client,
            email="test@test.com",
            password="test"
        )
        self.user = User.objects.get(email='test@test.com')
        self.user2 = User.objects.create(email='test2@test.com',
                                         is_active=False)

    def test_user_get(self):
        response = self.client.get(
            reverse('administration:users', kwargs={'pk': 1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['email'], self.user.email)
        self.assertEqual(response.json()['is_active'], self.user.is_active)
        self.assertEqual(response.json()['id'], self.user.id)

    def test_user_list_without_filters(self):
        response = self.client.get(
            reverse('administration:user-list'), {'ordering': '-created_at'},
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_active(self):
        response = self.client.get(
            reverse('administration:user-list'),
            {'is_active': 'True', 'ordering':
             '-created_at'},
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()['results']), 1)

    def test_user_list_inactive(self):
        response = self.client.get(
            reverse('administration:user-list'),
            {'is_active': 'False',
             'ordering': '-created_at'},
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], [
                         UserAdminSerializer(self.user2).data])

    def test_user_list_email(self):
        response = self.client.get(
            reverse('administration:user-list'),
            {'email': 'test@test',
             'ordering': '-created_at'},
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], [
                         UserAdminSerializer(self.user).data])

    def test_user_list_both_valid(self):
        response = self.client.get(
            reverse('administration:user-list'),
            {'email': 'test@test.com',
             'ordering': '-created_at',
             'is_active': 'True'},
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], [
                         UserAdminSerializer(self.user).data])

    def test_user_list_both_invalid(self):
        response = self.client.get(
            reverse('administration:user-list'),
            {'email': 'test@test.com',
             'ordering': '-created_at',
             'is_active': 'False'},
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], [])

    def test_user_update_valid_1(self):
        response = self.client.put(
            reverse('administration:users', kwargs={'pk': self.user.id}),
            json.dumps({'email': 'updated@test.com'}),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.id).email,

                         'updated@test.com')
        self.assertTrue(User.objects.get(
            pk=self.user.id).check_password('test'))

    def test_user_update_valid_2(self):
        response = self.client.put(
            reverse('administration:users', kwargs={'pk': self.user.id}),
            json.dumps({'email': 'updated@test.com', 'password': 'hello'}),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(
            pk=self.user.id).email, 'updated@test.com')
        self.assertTrue(User.objects.get(
            pk=self.user.id).check_password('hello'))

    def test_user_update_valid_3(self):
        response = self.client.put(
            reverse('administration:users', kwargs={'pk': self.user.id}),
            json.dumps({'password': 'hello'}),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(
            pk=self.user.id).email, 'test@test.com')
        self.assertTrue(User.objects.get(
            pk=self.user.id).check_password('hello'))

    def test_user_update_valid_4(self):
        response = self.client.put(
            reverse('administration:users', kwargs={'pk': self.user.id}),
            json.dumps({}),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(
            pk=self.user.id).email, 'test@test.com')
        self.assertTrue(User.objects.get(
            pk=self.user.id).check_password('test'))

    def test_user_update_valid_5(self):
        response = self.client.put(
            reverse('administration:users', kwargs={'pk': self.user.id}),
            json.dumps({'is_active': False}),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.id).is_active, False)
        self.assertTrue(User.objects.get(
            pk=self.user.id).check_password('test'))

# TODO: Hacer cuando retomemos app admin
# @tag('admin_funds_list')
# class FundsListAPIViewTestCase(TestCase):
#     def setUp(self):
#         self.headers = get_credentials(
#             self.client,
#             email="test@test.com",
#             password="test"
#         )
#         self.user = User.objects.get(email='test@test.com')
#         self.user2 = User.objects.create(email='test2@test.com',
#                                          is_active=False)

#     def test_list_funds_no_superuser(self):
#         response = self.client.get(
#             reverse('admin-funds-list'), 
#             content_type='application/json', 
#             **self.headers)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     @patch('requests.get')
#     def test_list_funds(self, mock_get):
#         fake_responses_get = [Mock(), Mock()]
#         fake_responses_get[0].json.return_value = [
#             {'nombre_bot': 'test', 'id_corrida': 1, 'status': {}}]
#         fake_responses_get[1].status_code = 200
#         fake_responses_get[1].json.return_value = []
#         mock_get.side_effect = fake_responses_get
#         headers = get_credentials(self.client, True)
#         response = self.client.get(
#             reverse('admin-funds-list'), content_type='application/json', **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# @tag('admin_fund_status')
# class FundStatusAdminAPIViewTestCase(TestCase):
#     def setUp(self):
#         self.fund = {'nombre_bot': 'test', 'id_corrida': 1}

#     def test_get_fund_status_unauth(self):
#         response = self.client.get(
#             reverse('admin-fund-status', kwargs={'fund_name': 'test'}),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_get_fund_status_no_superuser(self):
#         headers = get_credentials(self.client, False)
#         response = self.client.get(
#             reverse('admin-fund-status', kwargs={'fund_name': 'test'}),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     @patch('requests.get')
#     def test_get_fund_status_no_active_runs(self, mock_get):
#         fake_responses = [Mock()]
#         fake_responses[0].json.return_value = []
#         mock_get.side_effect = fake_responses
#         headers = get_credentials(self.client, True)
#         response = self.client.get(
#             reverse('admin-fund-status', kwargs={'fund_name': 'test'}), content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(response.data, {})

#     @patch('requests.get')
#     def test_get_fund_status_runs_without_state(self, mock_get):
#         fake_responses = [Mock(), Mock()]
#         fake_responses[0].json.return_value = [self.fund]
#         fake_responses[1].json.return_value = []
#         mock_get.side_effect = fake_responses
#         headers = get_credentials(self.client, True)
#         response = self.client.get(
#             reverse('admin-fund-status', kwargs={'fund_name': 'test'}),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'fund': self.fund, 'status': None})


# @tag('admin_fund_balance')
# class FundBalanceAdminAPIViewTestCase(TestCase):
#     def setUp(self):
#         self.fund = {'nombre_bot': 'test', 'id_corrida': 1}

#     def test_get_fund_balance_unauth(self):
#         response = self.client.get(
#             reverse('admin-fund-balance', kwargs={'fund_name': 'test'}),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_get_fund_balance_no_superuser(self):
#         headers = get_credentials(self.client, False)
#         response = self.client.get(
#             reverse('admin-fund-balance', kwargs={'fund_name': 'test'}),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     @patch('requests.get')
#     def test_get_fund_balance_without_states(self, mock_get):
#         fake_responses = [Mock(), Mock()]
#         fake_responses[0].status_code = 200
#         fake_responses[0].json.return_value = [self.fund]
#         fake_responses[1].json.return_value = []
#         mock_get.side_effect = fake_responses
#         headers = get_credentials(self.client, True)
#         response = self.client.get(
#             reverse('admin-fund-balance', kwargs={'fund_name': 'test'}),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'fund': self.fund, 'balance': None})


# @tag('admin_subscriptions_list')
# class SubscriptionsListAPIViewTestCase(TestCase):

#     def test_get_fund_balance_unauth(self):
#         response = self.client.get(
#             reverse('admin-subscriptions-list', kwargs={'fund_name': 'test'}),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_get_fund_balance_no_superuser(self):
#         headers = get_credentials(self.client, False)
#         response = self.client.get(
#             reverse('admin-subscriptions-list', kwargs={'fund_name': 'test'}),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     @patch('requests.get')
#     def test_get_fund_balance_without_states(self, mock_get):
#         fake_responses = [Mock()]
#         fake_responses[0].status_code = 200
#         fake_responses[0].json.return_value = [{}]
#         mock_get.side_effect = fake_responses
#         headers = get_credentials(self.client, True)
#         response = self.client.get(
#             reverse('admin-subscriptions-list', kwargs={'fund_name': 'test'}),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)


# @tag('admin_fund_runs')
# class FundRunsAdminAPIViewTestCase(TestCase):

#     def test_fund_runs_unauth(self):
#         params = {'status': 'all', 'fund_name': 'test'}
#         response = self.client.get(
#             reverse('admin-fund-runs', kwargs=params),
#             content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_fund_runs_no_superuser(self):
#         params = {'status': 'all', 'fund_name': 'test'}
#         headers = get_credentials(self.client, False)
#         response = self.client.get(
#             reverse('admin-fund-runs', kwargs=params),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     @patch('requests.get')
#     def test_fund_runs(self, mock_get):
#         fake_responses_get = [Mock(), Mock()]
#         fake_responses_get[0].json.return_value = []
#         fake_responses_get[0].status_code = 200
#         fake_responses_get[1].json.return_value = []
#         fake_responses_get[1].status_code = 200
#         mock_get.side_effect = fake_responses_get
#         params = {'status': 'all', 'fund_name': 'test'}
#         headers = get_credentials(self.client, True)
#         response = self.client.get(
#             reverse('admin-fund-runs', kwargs=params),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# @tag('admin_status_by_run_id')
# class StausByRunIdAdminAPIViewTestCase(TestCase):
#     def setUp(self):
#         self.fund = {'nombre_bot': 'test', 'id_corrida': 1}

#     def test_status_by_run_id_unauth(self):
#         response = self.client.get(
#             reverse('admin-status-by-run-id', kwargs={'pk': 1}),
#             content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_status_by_run_id_no_superuser(self):
#         headers = get_credentials(self.client, False)
#         response = self.client.get(
#             reverse('admin-status-by-run-id', kwargs={'pk': 1}),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     @patch('requests.get')
#     def test_status_by_run_id_no_active_runs(self, mock_get):
#         fake_responses = [Mock()]
#         fake_responses[0].json.return_value = {}
#         fake_responses[0].status_code = 200
#         mock_get.side_effect = fake_responses
#         headers = get_credentials(self.client, True)
#         response = self.client.get(
#             reverse('admin-status-by-run-id', kwargs={'pk': 1}),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     @patch('requests.get')
#     def test_status_by_run_id_runs_without_state(self, mock_get):
#         fake_responses = [Mock(), Mock()]
#         fake_responses[0].json.return_value = {
#             'id_corrida': 1, 'nombre_bot': 'test'}
#         fake_responses[0].status_code = 200
#         fake_responses[1].json.return_value = []
#         fake_responses[1].status_code = 200
#         mock_get.side_effect = fake_responses
#         headers = get_credentials(self.client, True)
#         response = self.client.get(
#             reverse('admin-status-by-run-id', kwargs={'pk': 1}),
#             content_type='application/json',
#             **headers
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'fund': self.fund, 'status': None})
