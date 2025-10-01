package com.example.demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.example.demo.model.StudentRequest;
import com.example.demo.model.StudentResponse;
import com.example.demo.service.StudentService;

import java.util.Map;

@RestController
@RequestMapping("/students")
public class StudentController {

    @Autowired
    private StudentService studentService;

    // Lấy tất cả sinh viên
    @GetMapping
    public Map<String, StudentResponse> getAllStudents() {
        return studentService.getAllStudents();
    }

    // Lấy theo ID
    @GetMapping("/{id}")
    public StudentResponse getStudentById(@PathVariable String id) {
        return studentService.getStudentById(id);
    }

    // Thêm mới
    @PostMapping
    public StudentResponse addStudent(@RequestBody StudentRequest req) {
        return studentService.addStudent(req);
    }

    // Sửa
    @PutMapping("/{id}")
    public StudentResponse updateStudent(@PathVariable String id, @RequestBody StudentRequest req) {
        return studentService.updateStudent(id, req);
    }

    // Xóa
    @DeleteMapping("/{id}")
    public String deleteStudent(@PathVariable String id) {
        boolean deleted = studentService.deleteStudent(id);
        return deleted ? "Đã xóa sinh viên " + id : "Không tìm thấy sinh viên " + id;
    }
}
