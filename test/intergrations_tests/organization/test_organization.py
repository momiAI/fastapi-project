async def test_not_booked(ac):
    response = await ac.get(
        "/organization/booked",
        params={"date_start": "2025-11-07", "date_end": "2025-11-08"},
    )
    assert response.status_code == 200


async def test_update_organization(db, ac):
    id_org = (await db.organization.get_all())[0].id
    response = await ac.patch(
        f"/organization/update/{id_org}",
        json={"name": "Белая роща", "description": "Ну очень большое описание"},
    )
    assert response.status_code == 200


async def test_delete_organization(ac, db):
    id_org = (await db.organization.get_all())[0].id
    response = await ac.delete(f"/organization/delete/{id_org}")
    assert response.status_code == 200
