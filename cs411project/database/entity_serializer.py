class EntitySerializer:
   
    @classmethod
    def db_entities_to_python(cls, entities, field_names):
        """
            Args: 
                entities -> generator containing the resulting entities of a DB call
                field_names -> Ordered list of strings containing the field names for the corresponding column of a DB entity
                                This list must have the same length as the number of columns returned by the DB query


            Returns a dictionary of each entity, with keys defined in field_names
        """
        return [cls._db_entity_to_dict(entity, field_names) for entity in entities]

    @classmethod
    def _db_entity_to_dict(cls, db_entity, field_names):
        entity_dict = {}
        for idx in range(len(field_names)):
            entity_dict[field_names[idx]] = db_entity[idx]

        return entity_dict

