from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="this field cannot be empty")
    parser.add_argument("password", type=str, required=True, help="this field cannot be empty")

    def post(self):
        data=UserRegister.parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message":"user already exists"}
        user=UserModel(data["username"],data["password"])
        user.save_to_db()
        return {"message":"user was registered"}
