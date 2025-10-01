package com.example.demo.service;

import org.springframework.stereotype.Service;
import com.example.demo.model.StudentRequest;
import com.example.demo.model.StudentResponse;

import java.util.HashMap;
import java.util.Map;

@Service
public class StudentService {
    private final Map<String, StudentResponse> students = new HashMap<>();

    public StudentService() {
        // Danh sách mẫu
        students.put("1", new StudentResponse("1", 3.6, "Xuất sắc", 90, "Xuất sắc"));
        students.put("2", new StudentResponse("2", 2.8, "Khá", 70, "Khá"));
        students.put("3", new StudentResponse("3", 2.1, "Trung bình", 55, "Trung bình"));
        students.put("4", new StudentResponse("4", 1.5, "Yếu", 40, "Yếu"));
    }

    // Lấy toàn bộ sinh viên
    public Map<String, StudentResponse> getAllStudents() {
        return students;
    }

    // Lấy theo ID
    public StudentResponse getStudentById(String id) {
        return students.get(id);
    }

    // Thêm mới
    public StudentResponse addStudent(StudentRequest req) {
        String gpaClass = classifyGPA(req.getGpa());
        String renluyenClass = classifyRenluyen(req.getRenluyen());

        StudentResponse resp = new StudentResponse(
                req.getStudent_id(),
                req.getGpa(),
                gpaClass,
                req.getRenluyen(),
                renluyenClass
        );
        students.put(req.getStudent_id(), resp);
        return resp;
    }

    // Sửa thông tin
    public StudentResponse updateStudent(String id, StudentRequest req) {
        if (!students.containsKey(id)) return null;

        String gpaClass = classifyGPA(req.getGpa());
        String renluyenClass = classifyRenluyen(req.getRenluyen());

        StudentResponse resp = new StudentResponse(
                id,
                req.getGpa(),
                gpaClass,
                req.getRenluyen(),
                renluyenClass
        );
        students.put(id, resp);
        return resp;
    }

    // Xóa
    public boolean deleteStudent(String id) {
        return students.remove(id) != null;
    }

    // --- Hàm phân loại ---
    private String classifyGPA(double gpa) {
        if (gpa >= 3.6) return "Xuất sắc";
        if (gpa >= 3.2) return "Giỏi";
        if (gpa >= 2.5) return "Khá";
        if (gpa >= 2.0) return "Trung bình";
        return "Yếu";
    }

    private String classifyRenluyen(int r) {
        if (r >= 90) return "Xuất sắc";
        if (r >= 80) return "Tốt";
        if (r >= 65) return "Khá";
        if (r >= 50) return "Trung bình";
        return "Yếu";
    }
}
