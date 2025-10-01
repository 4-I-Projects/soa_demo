from zeep import Client

# URL của WSDL
wsdl = 'http://127.0.0.1:8000/soap/?wsdl'
client = Client(wsdl=wsdl)

# gọi request 
student_id = 105
response = client.service.getStudentInfo(student_id)

# in ra kết quả

print(response)
