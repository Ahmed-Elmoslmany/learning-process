import models
import services.utils.exceptions as exc
import sqlalchemy.exc as alchemyExc

class CurdOperator:
    def __init__(self, model, session=None):
        self.model = model
        self.session = session or models.model.db.session
        
    def get_all(self, **filters):
        try:    
            return self.session.query(self.model).filter_by(**filters).all()    
        except exc.SqlAlchemyError as e:
            raise exc.CrudOperatorError('error fetching all records', 'get_all')
        
    def get_by_id(self, id):
        try:
            record = self.session.query(self.model).get(id)
            if not record:
                raise exc.RecordNotFound(f'record with id: {id} not found')
            return record
        except exc.SqlAlchemyError as e:
            raise exc.CrudOperatorError('error fetching record', 'get_by_ids')     
    
    def get_one(self, **filters):
        try:
            record = self.session.query(self.model).filter_by(**filters).first()
            return record
        except exc.SqlAlchemyError as e:
            raise exc.CrudOperatorError('error fetching record', 'get_one')    
    
    def create(self, json_body):
        try:
            new_record = self.model(**json_body)
            self.session.add(new_record)
            self.session.commit()
            return new_record
        except alchemyExc.SQLAlchemyError as e:
            raise exc.CrudOperatorError('error add record', 'create')        
    
    def update(self, id, json_body):
        try:
            record = self.session.query(self.model).get(id)
            if not record:
                raise exc.RecordNotFound(f'record with id: {id} not found')
            for key, value in json_body.items():
                setattr(record, key, value)
            self.session.commit()
            return record
        except exc.SqlAlchemyError as e:
            raise exc.CrudOperatorError('error update record', 'update')
    
    def delete(self, id):
        try:
            record = self.session.query(self.model).get(id)
            if not record:
                return False
            self.session.delete(record)
            self.session.commit()
            return True
        except exc.SqlAlchemyError as e:
            raise exc.CrudOperatorError('error delete record', 'delete')
