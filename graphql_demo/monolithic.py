from flask import Flask
from flask_graphql import GraphQLView
import graphene


# ===== Helper functions =====
def classify_gpa(gpa: float) -> str:
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


def classify_discipline(score: int) -> str:
    if score >= 90:
        return "Xuất sắc"
    elif score >= 80:
        return "Tốt"
    elif score >= 65:
        return "Khá"
    elif score >= 50:
        return "Trung bình"
    elif score >= 35:
        return "Yếu"
    else:
        return "Kém"


# ===== GraphQL Schema =====
class StudentResult(graphene.ObjectType):
    gpa = graphene.Float()
    discipline_score = graphene.Int()
    gpa_eval = graphene.String()
    discipline_eval = graphene.String()


class Query(graphene.ObjectType):
    student_result = graphene.Field(
        StudentResult,
        gpa=graphene.Float(required=True),
        discipline_score=graphene.Int(required=True)
    )

    def resolve_student_result(self, info, gpa, discipline_score):
        return StudentResult(
            gpa=gpa,
            discipline_score=discipline_score,
            gpa_eval=classify_gpa(gpa),
            discipline_eval=classify_discipline(discipline_score)
        )


schema = graphene.Schema(query=Query)

# ===== Flask app =====
app = Flask(__name__)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema, graphiql=True  # graphiql=True để mở UI
    ),
)

if __name__ == "__main__":
    app.run(debug=True)
