from src.schemas.facilities import FacilitiesCottageAdd


async def test_add_facilitie_cottage(db):
    data = ["Барбекю", "Гриль", "Лес"]

    [await db.facilcott.insert_to_database(FacilitiesCottageAdd(title = f)) for f in data]
    await db.commit()


async def test_get_all_facilitiec_cottage(db):
    await db.facilcott.get_all()

