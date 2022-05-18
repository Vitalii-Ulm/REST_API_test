from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message":"store not found"}

    def post(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            return {"message":"store with such name already exists"}
        store=StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message":"an error occurred during saving data"}
        return store.json()

    def delete(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message":"store was deleted"}
        return {"message": "store not found"}

class StoreList(Resource):
    def get(self):
        return {"stores":list(map(lambda x: x.json(), StoreModel.query.all()))}