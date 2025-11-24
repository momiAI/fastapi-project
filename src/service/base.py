from src.utis.db_manager import DbManager

class BaseService:
    db : DbManager | None

    def __init__(self,db : DbManager | None = None):
        self.db = db
        