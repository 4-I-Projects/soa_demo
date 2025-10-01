package com.example.demo.model;

public class StudentResponse {
    private String student_id;
    private double gpa;
    private String gpa_classification;
    private int renluyen;
    private String renluyen_classification;

    public StudentResponse(String student_id, double gpa, String gpa_classification,
                           int renluyen, String renluyen_classification) {
        this.student_id = student_id;
        this.gpa = gpa;
        this.gpa_classification = gpa_classification;
        this.renluyen = renluyen;
        this.renluyen_classification = renluyen_classification;
    }

    public String getStudent_id() { return student_id; }
    public double getGpa() { return gpa; }
    public String getGpa_classification() { return gpa_classification; }
    public int getRenluyen() { return renluyen; }
    public String getRenluyen_classification() { return renluyen_classification; }
}
