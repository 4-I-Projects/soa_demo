from spyne import Application, rpc, ServiceBase, Integer, Unicode, ComplexModel, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from soap_backend import get_student


# định nghĩa kiểu dữ liệu trả về
class StudentResponse(ComplexModel):
    id = Integer
    name = Unicode
    avgScore = Float
    disciplineScore = Integer
    avg_Evaluation = Unicode
    discipline_Evaluation = Unicode

# định nghĩa SOAP Service
class StudentService(ServiceBase):
    @rpc(Integer, _returns=StudentResponse)
    def getStudentInfo(ctx, student_id):
        data = get_student(student_id)
        if not data:
            return None
        return StudentResponse(
            id=data["id"],
            name=data["name"],
            avgScore=data["avgScore"],
            disciplineScore=data["disciplineScore"],
            avg_Evaluation=data["avgEvaluation"],
            discipline_Evaluation=data["disciplineEvaluation"]
        )
    
# tạo ứng dụng SOAP
application = Application(
    [StudentService], #service nào 
    tns='spyne.examples.student', # target namespace
    in_protocol=Soap11(validator='lxml'), # soap input
    out_protocol=Soap11() # soap output
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('localhost', 8000, wsgi_app)
    print("SOAP server chạy tại http://127.0.0.1:8000/soap")
    print("WSDL có tại http://127.0.0.1:8000/soap/?wsdl")
    server.serve_forever()