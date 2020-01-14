from django.test import TestCase, tag
from users.test_utils import get_credentials, create_user
from django.urls import reverse
from rest_framework import status
import json


@tag('terms_and_conditions')
class TermsAndConditionsViewSetTestCase(TestCase):

    def setUp(self) -> None:
        self.user = create_user('terms@cond.com', 'termsandconditions', False)
        self.credentials = get_credentials(
            self.client,
            email='terms@cond.com',
            password='termsandconditions',
            new_user=False
        )
        self.client.post(
            reverse('terms_and_conditions:terms-and-conditions'),
            QUERY_STRING=f'user_id={self.user.id}',
            data={'accepted': True}
        )

    def test_post_terms_and_conditions(self):
        response = self.client.post(
            reverse('terms_and_conditions:terms-and-conditions'),
            QUERY_STRING=f'user_id={self.user.id}',
            data={'accepted': True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_terms_and_conditions(self):
        response = self.client.get(
            reverse('terms_and_conditions:terms-and-conditions'),
            QUERY_STRING=f'user_id={self.user.id}',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_terms_and_conditions(self):
        response = self.client.get(
            reverse('terms_and_conditions:terms-and-conditions'),
            QUERY_STRING=f'user_id={self.user.id}'
        )
        data = response.data
        data['accepted'] = False
        response = self.client.put(
            reverse('terms_and_conditions:terms-and-conditions-update',
                    kwargs={'pk': data.get('id')}),
            QUERY_STRING=f'user_id={self.user.id}',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_terms_and_conditions_when_they_dont_exist(self):
        user2 = create_user('terms2@cond.com', 'termsandconditions', False)
        response = self.client.get(
            reverse('terms_and_conditions:terms-and-conditions'),
            QUERY_STRING=f'user_id={user2.id}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

    # def test_get_terms_and_conditions_when_user_doesnt_exist(self):
    #     response = self.client.get(
    #         reverse('terms_and_conditions:terms-and-conditions'),
    #         QUERY_STRING=f'user_id=32'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data['error_code'],
    #                      'terms_and_conditions.retrieve.userDoesNotExist')
