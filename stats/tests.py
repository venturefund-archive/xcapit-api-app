from django.test import TestCase, tag
from users.models import User
from django.urls import reverse
from rest_framework import status
import json
from .serializers import LogsSerializer
from stats.models import LoginHistory, Logs
from django.utils import timezone

# Create your tests here.
log_data = {
    "description": '{"test":"jsontest"}',
    "button_id": 'ninguno',
    "component_id": 'ninguno',
}
log_serializer_data = {
    "valid": {
        "description": '{"test":"jsontest"}',
        "button_id": 'ninguno',
        "component_id": 'ninguno',
        "ip": '190.153.12.5',
        "user_id": 1
    },
    "invalid_1": {
        "ip": '190.153.12.5',
        "user_id": 1
    }
}
user_test_data = {
    'email': 'test1@test.com',
    'password': 'test'
}


@tag('stats_logs')
class LogsViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User(email="test1@test.com",
                         is_active=True)
        self.user.set_password('test')
        self.user.save()

        self.user2 = User(email="test2@test.com",
                          is_active=False)
        self.user2.set_password('test')
        self.user2.save()

    def test_logs_create(self):
        response = self.client.post(
            reverse('stats:logs'), json.dumps(log_data),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logs_get(self):
        response = self.client.get(
            reverse('stats:logs'),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@tag('stats_public_logs')
class PublicLogsViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User(email="test1@test.com",
                         is_active=True)
        self.user.set_password('test')
        self.user.save()

        self.user2 = User(email="test2@test.com",
                          is_active=False)
        self.user2.set_password('test')
        self.user2.save()

    def test_logs_create(self):
        response = self.client.post(
            reverse('stats:public-logs'), json.dumps(log_data),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LogsSerializerTestCase(TestCase):

    def test_valid_data_serializer(self):
        serializer = LogsSerializer(data=log_serializer_data['valid'])
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_serializer_1(self):
        serializer = LogsSerializer(data=log_serializer_data['invalid_1'])
        self.assertFalse(serializer.is_valid())


@tag('stats_count_users')
class UsersCountAPIViewTestCase(TestCase):
    def setUp(self) -> None:
        users = [
            {
                'email': 'test1@gmail.com',
                'is_active': True
            },
            {
                'email': 'test2@gmail.com',
                'is_active': True
            },
            {
                'email': 'test3@gmail.com',
                'is_active': True
            }
        ]
        user1 = User.objects.create(**users[0])
        user1.created_at = '2019-05-04T15:28:54.842295Z'
        user1.save()
        user2 = User.objects.create(**users[1])
        user2.created_at = '2019-06-04T15:28:54.842295Z'
        user2.save()
        user3 = User.objects.create(**users[2])
        user3.created_at = '2018-07-04T15:28:54.842295Z'
        user3.save()

    def test_count_users(self):
        response = self.client.get(
            reverse('stats:count-users'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['users'], 1)
        self.assertTrue('users' in response.data)
        self.assertTrue('active' in response.data)
        self.assertTrue('inactive' in response.data)

    def test_count_users_by_year(self):
        response1 = self.client.get(
            reverse('stats:count-users') + "?year=2018",
            content_type='application/json'
        )
        response2 = self.client.get(
            reverse('stats:count-users') + "?year=2019",
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 1)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 2)
        self.assertTrue('month' in response1.data[0])
        self.assertTrue('users' in response1.data[0])
        self.assertTrue('active' in response1.data[0])
        self.assertTrue('inactive' in response1.data[0])

    def test_count_users_by_year_month(self):
        response = self.client.get(
            reverse('stats:count-users') + "?year=2019&month=5",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('users' in response.data)
        self.assertEqual(response.data['users'], 1)
        self.assertTrue('active' in response.data)
        self.assertEqual(response.data['active'], 1)
        self.assertTrue('inactive' in response.data)
        self.assertEqual(response.data['inactive'], 0)


class LoginHistoryTestCase(TestCase):

    def setUp(self):
        self.history = LoginHistory.objects.create(email='test@test.com',
                                                   agent='test_agent',
                                                   ip='192.168.0.12',
                                                   logged=True)

    def test_string_representation(self):
        history = LoginHistory.objects.get(email='test@test.com')
        self.assertEqual(history.agent, self.history.agent)
        self.assertEqual(history.ip, self.history.ip)
        self.assertEqual(history.logged, self.history.logged)


@tag('stats_count_fund_summary')
class FundSummaryViewsAPIViewTestCase(TestCase):
    def setUp(self):
        Logs.objects.create(agent='test_agent',
                            ip='192.168.0.12',
                            description='desc',
                            button_id='btn_id',
                            component_id='FundSummaryPage',
                            user_id=1,
                            event_id='evt_id',
                            fired_at=timezone.now()
                            )

    def test_count_fund_summary(self):
        """ Test sin user_id """
        response = self.client.get(
            reverse('stats:count-fund-summary'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, int))
        self.assertEqual(response.data, 1)

    def test_count_fund_summary_user_id(self):
        """ Test con user_id """
        response = self.client.get(
            reverse('stats:count-fund-summary'), {'user_id': 1},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, int))
        self.assertEqual(response.data, 1)

    def test_count_fund_summary_user_id_empty_data(self):
        """ Test con user_id empty data """
        response = self.client.get(
            reverse('stats:count-fund-summary'), {'user_id': 3},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, int))
        self.assertEqual(response.data, 0)


@tag('stats_count_fund_balance')
class FundBalanceViewsAPIViewTestCase(TestCase):
    def setUp(self):
        Logs.objects.create(agent='test_agent',
                            ip='192.168.0.12',
                            description='desc',
                            button_id='btn_id',
                            component_id='FundBalancePage',
                            user_id=1,
                            event_id='evt_id',
                            fired_at=timezone.now()
                            )

    def test_count_fund_balance(self):
        """ Test sin user_id """
        response = self.client.get(
            reverse('stats:count-fund-balance'),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, int))
        self.assertEqual(response.data, 1)

    def test_count_fund_balance_user_id(self):
        """ Test con user_id """
        response = self.client.get(
            reverse('stats:count-fund-balance'), {'user_id': 1},
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, int))
        self.assertEqual(response.data, 1)

    def test_count_fund_balance_user_id_empty_data(self):
        """ Test con user_id empty data"""
        response = self.client.get(
            reverse('stats:count-fund-balance'), {'user_id': 3},
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, int))
        self.assertEqual(response.data, 0)


@tag('stats_count_logins')
class LoginsCountAPIViewTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='test1@test.com')
        self.user = User.objects.create_user(**{
            'email': 'test_login_count@test.com',
            'password': 'test'
        })
        LoginHistory.objects.create(email='test_login_count@test.com',
                                    agent='test_agent',
                                    ip='192.168.0.12',
                                    logged=True)
        LoginHistory.objects.create(email='test_login_count@test.com',
                                    agent='test_agent',
                                    ip='192.168.0.12',
                                    logged=False)

    def test_count_logins(self):
        """ Test sin user_id """

        response = self.client.get(
            reverse('stats:count-logins'),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('success' in response.data)
        self.assertTrue('failed' in response.data)
        self.assertEqual(response.data['success'], 1)
        self.assertEqual(response.data['failed'], 1)

    def test_count_logins_user_id(self):
        """ Test con user_id """

        response = self.client.get(
            reverse('stats:count-logins'), {'user_id': self.user.id},
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('success' in response.data)
        self.assertTrue('failed' in response.data)
        self.assertEqual(response.data['success'], 1)
        self.assertEqual(response.data['failed'], 1)


@tag('stats_count_open')
class OpenCountAPIViewTestCase(TestCase):
    def setUp(self):
        Logs.objects.create(agent='test_agent',
                            ip='192.168.0.12',
                            description='desc',
                            button_id='btn_id',
                            component_id='cmp_id',
                            user_id=1,
                            event_id='load',
                            fired_at=timezone.now()
                            )

    def test_open_count(self):
        """ Test sin user_id """

        response = self.client.get(
            reverse('stats:count-opens'),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, int))
        self.assertEqual(response.data, 1)

    def test_open_count_user_id(self):
        """ Test con user_id """

        response = self.client.get(
            reverse('stats:count-opens'), {'user_id': 1},
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, int))
        self.assertEqual(response.data, 1)

    def test_open_count_user_id_empty_data(self):
        """ Test con user_id empty data"""

        response = self.client.get(
            reverse('stats:count-opens'), {'user_id': 3},
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, int))
        self.assertEqual(response.data, 0)


@tag('stats_count_actions')
class FundActionsCountAPIViewTestCase(TestCase):
    def setUp(self):
        Logs.objects.create(agent='test_agent',
                            ip='192.168.0.12',
                            description='desc',
                            button_id='Pause Fund',
                            component_id='cmp_id',
                            user_id=1,
                            event_id='click',
                            fired_at=timezone.now()
                            )
        Logs.objects.create(agent='test_agent',
                            ip='192.168.0.12',
                            description='desc',
                            button_id='Resume Fund',
                            component_id='cmp_id',
                            user_id=1,
                            event_id='click',
                            fired_at=timezone.now()
                            )
        Logs.objects.create(agent='test_agent',
                            ip='192.168.0.12',
                            description='desc',
                            button_id='Finalize Fund',
                            component_id='cmp_id',
                            user_id=1,
                            event_id='click',
                            fired_at=timezone.now()
                            )
        Logs.objects.create(agent='test_agent',
                            ip='192.168.0.12',
                            description='desc',
                            button_id='Renew Fund',
                            component_id='cmp_id',
                            user_id=1,
                            event_id='click',
                            fired_at=timezone.now()
                            )

    def test_actions_count(self):
        """ Test sin user_id """

        response = self.client.get(
            reverse('stats:count-fund-actions'),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['pause_fund'], 1)
        self.assertEqual(response.data['resume_fund'], 1)
        self.assertEqual(response.data['finalize_fund'], 1)
        self.assertEqual(response.data['renew_fund'], 1)

    def test_actions_count_user_id(self):
        """ Test con user_id """

        response = self.client.get(
            reverse('stats:count-fund-actions'), {'user_id': 1},
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['pause_fund'], 1)
        self.assertEqual(response.data['resume_fund'], 1)
        self.assertEqual(response.data['finalize_fund'], 1)
        self.assertEqual(response.data['renew_fund'], 1)

    def test_actions_count_user_id_empty_data(self):
        """ Test con user_id empty data """

        response = self.client.get(
            reverse('stats:count-fund-actions'), {'user_id': 3},
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['pause_fund'], 0)
        self.assertEqual(response.data['resume_fund'], 0)
        self.assertEqual(response.data['finalize_fund'], 0)
        self.assertEqual(response.data['renew_fund'], 0)
