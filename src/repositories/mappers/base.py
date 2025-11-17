class DataMapper:
    db_model = None
    db_schema = None

    @classmethod
    def map_to_domain(cls, data):
        return cls.db_schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistont_entety(cls, data):
        return cls.db_schema(**data.model_dump(exclude_unset=True))
