from zeep import Client

# URL của WSDL
wsdl = 'http://127.0.0.1:8000/soap/?wsdl'
client = Client(wsdl=wsdl)

print("1. Get student")
print("2. Create student")
print("3. Update student")
print("4. Delete student")
choice = int(input("Chọn chức năng: "))

if choice == 1:
    student_id = int(input("Nhập student_id: "))
    response = client.service.getStudentInfo(student_id)
    print(response)

elif choice == 2:
    sid = int(input("Nhập student_id: "))
    name = input("Nhập tên: ")
    avg = float(input("Nhập avgScore: "))
    disc = int(input("Nhập disciplineScore: "))
    response = client.service.createStudent(sid, name, avg, disc)
    print(response)

elif choice == 3:
    sid = int(input("Nhập student_id: "))
    name = input("Tên (để trống nếu không đổi): ") or None
    avg = input("avgScore (bỏ trống nếu không đổi): ")
    avg = float(avg) if avg else None
    disc = input("disciplineScore (bỏ trống nếu không đổi): ")
    disc = int(disc) if disc else None
    response = client.service.updateStudent(sid, name, avg, disc)
    print(response)

elif choice == 4:
    sid = int(input("Nhập student_id: "))
    response = client.service.deleteStudent(sid)
    print(response)

else:
    print("Lựa chọn không hợp lệ, vui lòng nhập 1-4.")
