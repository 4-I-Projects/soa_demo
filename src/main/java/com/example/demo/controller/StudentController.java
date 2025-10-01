package com.example.demo.controller;

import com.example.demo.model.StudentRequest;
import com.example.demo.model.StudentResponse;
import com.example.demo.service.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/students")
public class StudentController {

    @Autowired
    private StudentService studentService;

    // 1. Client-Server + 2. Stateless
    @PostMapping("/evaluation")
    public StudentResponse evaluateStudent(@RequestBody StudentRequest req) {
        return studentService.evaluate(req);
    }

    // 3. Cacheable
    @GetMapping("/hello")
    public ResponseEntity<String> hello() {
        return ResponseEntity.ok()
                .header("Cache-Control", "max-age=60") // cache 60 giây
                .body("Xin chào! Đây là dữ liệu cacheable.");
    }

    // 4. Uniform Interface (GET, PUT, DELETE)
    @GetMapping("/{id}")
    public StudentResponse getStudent(@PathVariable String id) {
        return new StudentResponse(id, 3.2, "Giỏi", 80, "Tốt");
    }

    @PutMapping("/{id}")
    public StudentResponse updateStudent(@PathVariable String id, @RequestBody StudentRequest req) {
        req.setStudent_id(id);
        return studentService.evaluate(req);
    }

    @DeleteMapping("/{id}")
    public String deleteStudent(@PathVariable String id) {
        return "Đã xóa sinh viên " + id;
    }

    // 6. Code on Demand
    @GetMapping("/script")
    public ResponseEntity<String> getScript() {
        String js = "alert('Xin chào từ RESTful Code on Demand!');";
        return ResponseEntity.ok()
                .header("Content-Type", "application/javascript")
                .body(js);
    }
}
