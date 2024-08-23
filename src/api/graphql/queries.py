import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .schema import User
from .models import User as UserModel

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(User.connection)
    user = graphene.Field(User, id=graphene.Int())

    def resolve_user(self, info, id):
        query = User.get_query(info)
        return query.filter(UserModel.id == id).first()
