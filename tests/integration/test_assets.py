from app.models.asset import Asset


def test_list_assets_route(client, db_session, fake_user_payload, fake_auth_payload):
    create_response = client.post("users/", json=fake_user_payload)
    assert create_response.status_code == 200

    auth_response = client.post("auth/login", json=fake_auth_payload)
    assert auth_response.status_code == 200
    auth_response_data = auth_response.json()

    asset = Asset(name="Bitcoin", symbol="BTC-USD", code="BTC")
    db_session.add(asset)
    db_session.commit()
    db_session.refresh(asset)

    response = client.get(
        "assets/",
        headers={"Authorization": f"Bearer {auth_response_data['access_token']}"},
    )
    assert response.status_code == 200

    assets = response.json()
    assert isinstance(assets, list)
    assert len(assets) > 0

    found_asset = next((item for item in assets if item["id"] == str(asset.id)), None)

    assert found_asset is not None
    assert found_asset["name"] == asset.name
    assert found_asset["symbol"] == asset.symbol
    assert found_asset["code"] == asset.code
