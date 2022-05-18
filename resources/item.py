from flask_restful import Resource, reqparse
from models.item import ItemModel
from flask_jwt import jwt_required

class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="this filed cannot be empty")
    parser.add_argument("store_id", type=float, required=True, help="every item must have a store id")

    @jwt_required()
    def get(self, name):
        item=ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"item not found"}

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message":"item already exists"}
        data=Item.parser.parse_args()
        item=ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message":"an error occurred during data saving"}
        return item.json()

    def delete(self, name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message":"item was deleted"}
        return {"message": "item not found"}

    def put(self, name):
        data=Item.parser.parse_args()
        item=ItemModel.find_by_name(name)
        if item:
            item.price=data["price"]
        else:
            item=ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "an error occurred during data saving"}
        return item.json()

class ItemList(Resource):
    def get(self):
        return {"items":list(map(lambda x: x.json(), ItemModel.query.all()))}