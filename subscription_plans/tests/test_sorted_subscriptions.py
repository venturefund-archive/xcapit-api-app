from subscription_plans.sorted_subscriptions import SortedSubscriptions


def test_sorted_subscriptions():
    assert SortedSubscriptions([], lambda x: x)


def test_sorted_subscriptions_last():
    sorted_subscriptions = SortedSubscriptions(
        [
            {'id': 1, 'date_created': '2021-07-21T14:38:41.948-04:00'},
            {'id': 2, 'date_created': '2021-07-21T14:44:48.541-04:00'},
            {'id': 3, 'date_created': '2021-07-21T14:09:48.909-04:00'},
        ],
        lambda subscription: subscription.get('date_created')
    )
    assert sorted_subscriptions.last()[0].get('id') == 2
