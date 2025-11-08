from src.schemas.facilities import FacilitiesCottageAdd





async def test_get_all_facilitiec_cottage(db):
    await db.facilcott.get_all()

