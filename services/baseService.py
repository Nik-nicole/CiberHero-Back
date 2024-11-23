from extensions import db

class BaseService:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.query.all()

    def get_by_id(self, record_id):
        return self.model.query.get(record_id)

    def create(self, **kwargs):
        record = self.model(**kwargs)
        db.session.add(record)
        db.session.commit()
        return record

    def update(self, record_id, **kwargs):
        record = self.get_by_id(record_id)
        if not record:
            return None
        for key, value in kwargs.items():
            setattr(record, key, value)
        db.session.commit()
        return record

    def delete(self, record_id):
        record = self.get_by_id(record_id)
        if not record:
            return False
        db.session.delete(record)
        db.session.commit()
        return True