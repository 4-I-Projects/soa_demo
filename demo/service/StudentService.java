package com.example.demo.service;

import com.example.demo.model.StudentRequest;
import com.example.demo.model.StudentResponse;
import org.springframework.stereotype.Service;

@Service
public class StudentService {

    public StudentResponse evaluate(StudentRequest req) {
        String gpaClass = classifyGPA(req.getGpa());
        String renluyenClass = classifyRenluyen(req.getRenluyen());
        return new StudentResponse(req.getStudent_id(), req.getGpa(),
                gpaClass, req.getRenluyen(), renluyenClass);
    }

    private String classifyGPA(double gpa) {
        if (gpa >= 3.6) return "Xuất sắc";
        if (gpa >= 3.2) return "Giỏi";
        if (gpa >= 2.5) return "Khá";
        if (gpa >= 2.0) return "Trung bình";
        return "Yếu";
    }

    private String classifyRenluyen(int score) {
        if (score >= 90) return "Xuất sắc";
        if (score >= 80) return "Tốt";
        if (score >= 65) return "Khá";
        if (score >= 50) return "Trung bình";
        if (score >= 35) return "Yếu";
        return "Kém";
    }
}
