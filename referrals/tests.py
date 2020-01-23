from django.test import TestCase, tag
from users.test_utils import get_credentials, create_user
from django.urls import reverse
from rest_framework import status
from .models import Referral

test_data = {
    "referral_email1": 'referr@ls1.com',
    "referral_email2": 'referr@ls2.com',
    "referral_email3": 'referr@ls3.com'
}

test_referals = [
    {
        "email": "test1@gmail.com",
        "created_at": "2019-10-02T12:54:24.807939Z",
        "accepted_at": "2019-10-02T12:54:24.808043Z",
        "accepted": False,
        "referral_id": ''
    },
    {
        "email": "test2@gmail.com",
        "created_at": "2019-10-02T12:54:24.816117Z",
        "accepted_at": "2019-10-02T12:54:24.816170Z",
        "accepted": True,
        "referral_id": ''
    },
    {
        "email": "test3@hotmail.com",
        "created_at": "2019-10-02T12:54:24.822652Z",
        "accepted_at": "2019-10-02T12:54:24.822709Z",
        "accepted": True,
        "referral_id": ''
    }]


@tag('referrals')
class ReferralsViewSetTestCase(TestCase):

    def setUp(self):
        self.user_data = {
            "email": "referr@ls.com",
            "password": "referrals1T"
        }
        self.user = create_user(**self.user_data, is_superuser=False)

    def test_post_referrals(self):
        response = self.client.post(
            reverse('referrals:referrals',
                    kwargs={'user_id': self.user.id}),
            data={'email': test_data.get('referral_email1')},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_other_referrals(self):
        response1 = self.client.post(
            reverse('referrals:referrals',
                    kwargs={'user_id': self.user.id}),
            data={'email': test_data.get('referral_email2')}
        )
        response2 = self.client.post(
            reverse('referrals:referrals',
                    kwargs={'user_id': self.user.id}),
            data={'email': test_data.get('referral_email3')},
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_post_referrals_already_exists(self):
        response1 = self.client.post(
            reverse('referrals:referrals',
                    kwargs={'user_id': self.user.id}),
            data={'email': test_data.get('referral_email3')},
        )
        response2 = self.client.post(
            reverse('referrals:referrals',
                    kwargs={'user_id': self.user.id}),
            data={'email': test_data.get('referral_email3')},
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_referrals_is_an_user(self):
        response = self.client.post(
            reverse('referrals:referrals',
                    kwargs={'user_id': self.user.id}),
            data={'email': self.user_data["email"]},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@tag('get_referrals')
class UserReferralsViewSetTestCase(TestCase):

    def setUp(self) -> None:
        self.user = create_user('referr@ls.com', 'referrals1T', False)
        self.user.referral_id = 'ref123'
        self.user.save()
        self.credentials = get_credentials(
            self.client,
            email='referr@ls.com',
            password='referrals1T',
            new_user=False
        )
        test_referals[0]['referral_id'] = self.user.referral_id
        test_referals[1]['referral_id'] = self.user.referral_id
        test_referals[2]['referral_id'] = self.user.referral_id
        objs = [Referral(**referral) for referral in test_referals]
        Referral.objects.bulk_create(objs)

    def test_user_referrals(self):
        response = self.client.get(
            reverse('referrals:user-referrals',
                    kwargs={'user_id': self.user.id}),
            {'cursor': '',
             'ordering': '-accepted,email,created_at'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),
                         Referral.objects.filter(
                             referral_id=self.user.referral_id).count()
                         )
        self.assertTrue('cursors' in response.data)
        self.assertTrue('links' in response.data)
        self.assertTrue('results' in response.data)
