
STUDENTS = {
        101: {
        "name": "Nguyen Van A",
        "avgScore": 3.2,
        "disciplineScore": 85
    },
    102: {
        "name": "Tran Thi B",
        "avgScore": 2.4,
        "disciplineScore": 75
    },
    103: {
        "name": "Le Van C",
        "avgScore": 3.7,
        "disciplineScore": 90
    }
}

def get_student(student_id: int):
    data = STUDENTS.get(student_id)
    if not data:
        return None
    
    name = data["name"]
    avg = data["avgScore"]
    disclipline = data["disciplineScore"]
    if avg >= 3.6:
        avg_evaluation = "Xuất sắc"
    elif avg >= 3.2:
        avg_evaluation = "Giỏi"
    elif avg >= 2.5:
        avg_evaluation = "Khá"
    elif avg >= 2.0:
        avg_evaluation = "Trung bình"
    else:
        avg_evaluation = "Yếu"
    
    if disclipline >= 90:
        disclipline_evaluation = "Xuất sắc"
    elif disclipline >= 80:
        disclipline_evaluation = "Tốt"
    elif disclipline >= 65:
        disclipline_evaluation = "Khá"
    elif disclipline >= 50:
        disclipline_evaluation = "Trung bình"
    elif disclipline >= 35:
        disclipline_evaluation = "Yếu"
    else:
        disclipline_evaluation = "Kém"
    
    return {
        "id": student_id,
        "name": name,
        "avgScore": avg,
        "avgEvaluation": avg_evaluation,
        "disciplineScore": disclipline,
        "disciplineEvaluation": disclipline_evaluation

    }
