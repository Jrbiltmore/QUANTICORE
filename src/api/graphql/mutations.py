import graphene
from .models import db, User as UserModel
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_jwt_extended import create_access_token
from marshmallow import Schema, fields, ValidationError

class UserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    age = graphene.Int(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)

class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserModel)
    token = graphene.String()

    def mutate(self, info, input):
        user = UserModel(
            name=input.name,
            age=input.age,
            email=input.email,
        )
        user.set_password(input.password)
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.id)
        return CreateUser(user=user, ok=True, token=token)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserModel)

    def mutate(self, info, id, input):
        user = UserModel.query.get(id)
        if user:
            user.name = input.name if input.name else user.name
            user.age = input.age if input.age else user.age
            if input.password:
                user.set_password(input.password)
            db.session.commit()
            return UpdateUser(user=user, ok=True)
        return UpdateUser(user=None, ok=False)

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        user = UserModel.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return DeleteUser(ok=True)
        return DeleteUser(ok=False)
