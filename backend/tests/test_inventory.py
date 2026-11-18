def auth(client):
    response = client.post("/api/auth/login", json={"username": "admin", "password": "test-password"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}

def test_product_and_stock_movement_flow(client):
    headers = auth(client)
    created = client.post("/api/products", headers=headers, json={
        "code": "AR001", "name": "Arroz Tipo 1", "category": "Alimentos",
        "quantity": 30, "minimum_stock": 10
    })
    assert created.status_code == 201
    product = created.json()

    movement = client.post("/api/movements", headers=headers, json={
        "product_id": product["id"], "type": "SAIDA", "quantity": 5, "note": "Teste"
    })
    assert movement.status_code == 201

    products = client.get("/api/products", headers=headers).json()
    assert products[0]["quantity"] == 25

    history = client.get(f"/api/products/{product['id']}/movements", headers=headers)
    assert history.status_code == 200
    assert len(history.json()) == 1

def test_prevents_stock_below_zero(client):
    headers = auth(client)
    product = client.post("/api/products", headers=headers, json={
        "code": "CF001", "name": "Café", "quantity": 2, "minimum_stock": 1
    }).json()
    response = client.post("/api/movements", headers=headers, json={
        "product_id": product["id"], "type": "SAIDA", "quantity": 3
    })
    assert response.status_code == 422
    assert "Estoque insuficiente" in response.json()["detail"]

def test_protected_route_requires_authentication(client):
    response = client.get("/api/products")
    assert response.status_code == 401
