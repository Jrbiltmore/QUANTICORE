from flask import Flask, request
from flask_graphql import GraphQLView
import graphene
from graphene import ObjectType, String, Int, List, Field, Mutation, Boolean

# Sample in-memory data storage
users = [
    {"id": 1, "name": "John Doe", "age": 28},
    {"id": 2, "name": "Jane Smith", "age": 34},
]

# Define a User type
class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()

# Define the Query class
class Query(ObjectType):
    users = List(UserType)
    user = Field(UserType, id=Int(required=True))

    def resolve_users(root, info):
        return users

    def resolve_user(root, info, id):
        for user in users:
            if user['id'] == id:
                return user
        return None

# Define the CreateUser mutation
class CreateUser(Mutation):
    class Arguments:
        name = String(required=True)
        age = Int(required=True)

    ok = Boolean()
    user = Field(lambda: UserType)

    def mutate(root, info, name, age):
        new_id = max(user['id'] for user in users) + 1
        new_user = {"id": new_id, "name": name, "age": age}
        users.append(new_user)
        return CreateUser(ok=True, user=new_user)

# Define the UpdateUser mutation
class UpdateUser(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        age = Int()

    ok = Boolean()
    user = Field(lambda: UserType)

    def mutate(root, info, id, name=None, age=None):
        user = next((user for user in users if user["id"] == id), None)
        if user is None:
            return UpdateUser(ok=False, user=None)
        
        if name:
            user['name'] = name
        if age:
            user['age'] = age
        
        return UpdateUser(ok=True, user=user)

# Define the DeleteUser mutation
class DeleteUser(Mutation):
    class Arguments:
        id = Int(required=True)

    ok = Boolean()

    def mutate(root, info, id):
        global users
        users = [user for user in users if user["id"] != id]
        return DeleteUser(ok=True)

# Define the Mutation class
class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

# Define the schema
schema = graphene.Schema(query=Query, mutation=Mutation)

# Set up the Flask application
app = Flask(__name__)

# Add the GraphQL view to the Flask app
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable the GraphiQL interface
    )
)

# Basic route for health check
@app.route('/')
def index():
    return "Welcome to the GraphQL API. Visit /graphql to use the GraphiQL interface."

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
