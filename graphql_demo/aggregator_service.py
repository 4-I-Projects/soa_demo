from flask import Flask
from flask_graphql import GraphQLView
import graphene
import requests

# --------- Helper functions ----------
def evaluate_gpa(gpa: float) -> str:
    if gpa >= 3.6:
        return "Xuất sắc"
    elif gpa >= 3.2:
        return "Giỏi"
    elif gpa >= 2.5:
        return "Khá"
    elif gpa >= 2.0:
        return "Trung bình"
    else:
        return "Yếu"

def evaluate_conduct(score: int) -> str:
    if 90 <= score <= 100:
        return "Xuất sắc"
    elif 80 <= score <= 89:
        return "Tốt"
    elif 65 <= score <= 79:
        return "Khá"
    elif 50 <= score <= 64:
        return "Trung bình"
    elif 35 <= score <= 49:
        return "Yếu"
    else:
        return "Kém"

# --------- GraphQL Schema ----------
class StudentType(graphene.ObjectType):
    student_id = graphene.String()
    gpa = graphene.Float()
    gpa_eval = graphene.String()
    conduct = graphene.Int()
    conduct_eval = graphene.String()

class Query(graphene.ObjectType):
    student = graphene.Field(StudentType, student_id=graphene.String(required=True))

    def resolve_student(self, info, student_id):
        gpa_resp = requests.get(f"http://localhost:5001/gpa/{student_id}")
        conduct_resp = requests.get(f"http://localhost:5002/conduct/{student_id}")

        if gpa_resp.status_code != 200 or conduct_resp.status_code != 200:
            return None

        gpa = gpa_resp.json()["gpa"]
        conduct = conduct_resp.json()["conduct"]

        return StudentType(
            student_id=student_id,
            gpa=gpa,
            gpa_eval=evaluate_gpa(gpa),
            conduct=conduct,
            conduct_eval=evaluate_conduct(conduct)
        )

# --------- Mutations ----------
class UpdateGPA(graphene.Mutation):
    class Arguments:
        student_id = graphene.String(required=True)
        gpa = graphene.Float(required=True)

    student = graphene.Field(StudentType)

    def mutate(self, info, student_id, gpa):
        resp = requests.post(
            f"http://localhost:5001/gpa/{student_id}", json={"gpa": gpa}
        )
        if resp.status_code != 200:
            raise Exception("Failed to update GPA")

        return Query.resolve_student(self, info, student_id)

class UpdateConduct(graphene.Mutation):
    class Arguments:
        student_id = graphene.String(required=True)
        conduct = graphene.Int(required=True)

    student = graphene.Field(StudentType)

    def mutate(self, info, student_id, conduct):
        resp = requests.post(
            f"http://localhost:5002/conduct/{student_id}", json={"conduct": conduct}
        )
        if resp.status_code != 200:
            raise Exception("Failed to update Conduct")

        return Query.resolve_student(self, info, student_id)

class Mutation(graphene.ObjectType):
    update_gpa = UpdateGPA.Field()
    update_conduct = UpdateConduct.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

app = Flask(__name__)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
