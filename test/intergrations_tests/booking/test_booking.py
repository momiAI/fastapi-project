import pytest


@pytest.fixture(scope="module")
async def delete_bookings(db_):
    await db_.booking.delete_from_test()
    await db_.commit()


async def test_get_all(test_auth_user_ac):
    response = await test_auth_user_ac.get("/booking/all")
    assert response.status_code == 200


async def test_book_me(test_auth_user_ac):
    response = await test_auth_user_ac.get("/booking/me")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "cottage_id,date_start ,date_end , status_code",
    [(1, "2025-11-07", "2025-11-08", 200), (1, "2025-11-07", "2025-11-08", 401)],
)
async def test_book_cottage(
    cottage_id, date_start, date_end, status_code, test_auth_user_ac
):
    response = await test_auth_user_ac.post(
        "/booking/add",
        json={"cottage_id": cottage_id, "date_start": date_start, "date_end": date_end},
    )
    assert response.status_code == status_code


async def test_booked_cottage(test_auth_user_ac):
    response = await test_auth_user_ac.get(
        "/booking/booked", params={"date_start": "2025-11-07", "date_end": "2025-11-08"}
    )

    assert response.status_code == 200


@pytest.mark.parametrize(
    "cottage_id, date_start, date_end, count, status_code",
    [
        (1, "2025-11-07", "2025-11-08", 1, 200),
        (1, "2025-11-07", "2025-11-08", 1, 401),
        (1, "2025-11-09", "2025-11-10", 2, 200),
    ],
)
async def test_booked_and_me_routes(
    test_auth_user_ac,
    delete_bookings,
    cottage_id,
    date_start,
    date_end,
    status_code,
    count,
):
    response_post = await test_auth_user_ac.post(
        "/booking/add",
        json={"cottage_id": cottage_id, "date_start": date_start, "date_end": date_end},
    )
    assert response_post.status_code == status_code
    response = await test_auth_user_ac.get("/booking/me")
    res = response.json()
    assert len(res) == count
