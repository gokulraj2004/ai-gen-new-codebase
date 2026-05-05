import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, test_user, auth_headers):
    """Test creating an item."""
    response = await client.post(
        "/api/v1/items",
        json={
            "title": "Test Item",
            "description": "A test item description",
            "tag_names": ["test", "example"],
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "A test item description"
    assert len(data["tags"]) == 2


@pytest.mark.asyncio
async def test_create_item_unauthorized(client: AsyncClient):
    """Test creating an item without auth."""
    response = await client.post(
        "/api/v1/items",
        json={
            "title": "Test Item",
            "description": "A test item description",
            "tag_names": [],
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient, test_user, auth_headers):
    """Test listing items."""
    # Create an item first
    await client.post(
        "/api/v1/items",
        json={
            "title": "Test Item",
            "description": "A test item description",
            "tag_names": [],
        },
        headers=auth_headers,
    )

    response = await client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient, test_user, auth_headers):
    """Test getting a single item."""
    # Create an item first
    create_response = await client.post(
        "/api/v1/items",
        json={
            "title": "Test Item",
            "description": "A test item description",
            "tag_names": [],
        },
        headers=auth_headers,
    )
    item_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient, test_user, auth_headers):
    """Test updating an item."""
    # Create an item first
    create_response = await client.post(
        "/api/v1/items",
        json={
            "title": "Test Item",
            "description": "Original description",
            "tag_names": [],
        },
        headers=auth_headers,
    )
    item_id = create_response.json()["id"]

    response = await client.put(
        f"/api/v1/items/{item_id}",
        json={"title": "Updated Item", "description": "Updated description"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Item"


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient, test_user, auth_headers):
    """Test deleting an item."""
    # Create an item first
    create_response = await client.post(
        "/api/v1/items",
        json={
            "title": "Test Item",
            "description": "To be deleted",
            "tag_names": [],
        },
        headers=auth_headers,
    )
    item_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/items/{item_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = await client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_list_tags(client: AsyncClient):
    """Test listing tags."""
    response = await client.get("/api/v1/tags")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_create_tag(client: AsyncClient, test_user, auth_headers):
    """Test creating a tag."""
    response = await client.post(
        "/api/v1/tags",
        json={"name": "newtag"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "newtag"


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"