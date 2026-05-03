def test_get_account_overview_route(
    client,
    fake_auth_payload,
    fake_user_payload,
    fake_plan_payload,
    fake_subscription_payload,
):
    user_response = client.post("users/", json=fake_user_payload)
    assert user_response.status_code == 200
    user = user_response.json()

    auth_response = client.post("auth/login", json=fake_auth_payload)
    assert auth_response.status_code == 200
    auth_response_data = auth_response.json()

    plan_response = client.post(
        "plans/",
        headers={"Authorization": f"Bearer {auth_response_data['access_token']}"},
        json=fake_plan_payload,
    )
    assert plan_response.status_code == 200
    plan = plan_response.json()

    subscription_payload = fake_subscription_payload(
        plan_id=plan["id"], user_id=user["id"]
    )

    subscription_response = client.post(
        "subscriptions/",
        headers={"Authorization": f"Bearer {auth_response_data['access_token']}"},
        json=subscription_payload,
    )
    assert subscription_response.status_code == 200
    subscription = subscription_response.json()

    overview_response = client.get(
        "account/overview",
        headers={"Authorization": f"Bearer {auth_response_data['access_token']}"},
    )
    assert overview_response.status_code == 200

    overview = overview_response.json()
    assert overview["id"] == subscription["id"]
    assert overview["user_id"] == user["id"]
    assert overview["plan_id"] == plan["id"]
    assert overview["active"] == subscription_payload["active"]
    assert overview["call_today"] == 0
