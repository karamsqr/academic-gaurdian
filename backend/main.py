from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db

from models import (
    Student,
    Attendance,
    Mark
)

from schemas import (
    StudentResponse,
    DashboardResponse
)

from services.attendance import (
    calculate_attendance,
    predict_attendance,
    calculate_classes_needed
)
from services.risk import calculate_risk

from services.notifications import generate_alerts

app = FastAPI(
    title="Academic Guardian API",
    description="Intelligent Student Academic Monitoring and Support System",
    version="1.0"
)


# =====================================================
# CREATE DATABASE TABLES
# =====================================================

Base.metadata.create_all(bind=engine)


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():
    return {
        "message": "Academic Guardian API is running!"
    }


# =====================================================
# GET ALL STUDENTS
# =====================================================

@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    db: Session = Depends(get_db)
):

    students = db.query(Student).all()

    return students


# =====================================================
# GET ONE STUDENT
# =====================================================

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# =====================================================
# STUDENT DASHBOARD
# =====================================================

@app.get(
    "/students/{student_id}/dashboard",
    response_model=DashboardResponse
)
def get_student_dashboard(
    student_id: int,
    db: Session = Depends(get_db)
):

    # -------------------------------------------------
    # FIND STUDENT
    # -------------------------------------------------

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # -------------------------------------------------
    # ATTENDANCE
    # -------------------------------------------------

    attendance_records = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).all()

    attendance = calculate_attendance(
        attendance_records
    )

    attendance_percentage = attendance["percentage"]
    present_classes = attendance["present"]
    total_classes = attendance["total"]
    attendance_status = attendance["status"]

    # -------------------------------------------------
    # MARKS
    # -------------------------------------------------

    marks = db.query(Mark).filter(
        Mark.student_id == student_id
    ).all()

    percentages = []

    for mark in marks:

        assessment = mark.assessment

        if assessment and assessment.max_marks > 0:

            percentage = (
                mark.score /
                assessment.max_marks
            ) * 100

            percentages.append(percentage)


    if percentages:

        average_marks = sum(percentages) / len(percentages)

    else:

        average_marks = 0


    average_marks = round(
        average_marks,
        2
    )

    # -------------------------------------------------
    # RISK CALCULATION
    # -------------------------------------------------

    risk = calculate_risk(
        attendance_percentage,
        average_marks
    )

    risk_level = risk["level"]
    risk_reason = risk["reason"]

    # -------------------------------------------------
    # ALERTS
    # -------------------------------------------------

    alerts = generate_alerts(
        attendance_percentage,
        average_marks
    )

    # -------------------------------------------------
    # RETURN DASHBOARD
    # -------------------------------------------------

    return {

        "student": student,

        "attendance": {

            "percentage": attendance_percentage,

            "present": present_classes,

            "total": total_classes,

            "status": attendance_status
        },

        "marks": {

            "average": average_marks,

            "assessments_completed": len(marks)
        },

        "risk": {

            "level": risk_level,

            "reason": risk_reason
        },

        "alerts": alerts
    }

# =====================================================
# ATTENDANCE PREDICTION
# =====================================================

@app.get(
    "/students/{student_id}/attendance-prediction"
)
def get_attendance_prediction(
    student_id: int,
    future_classes: int = 3,
    db: Session = Depends(get_db)
):
    # -------------------------------------------------
    # FIND STUDENT
    # -------------------------------------------------

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # -------------------------------------------------
    # GET ATTENDANCE RECORDS
    # -------------------------------------------------

    attendance_records = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).all()

    # -------------------------------------------------
    # CALCULATE CURRENT ATTENDANCE
    # -------------------------------------------------

    attendance = calculate_attendance(
        attendance_records
    )

    present_classes = attendance["present"]
    total_classes = attendance["total"]
    current_percentage = attendance["percentage"]

    # -------------------------------------------------
    # PREDICT FUTURE ATTENDANCE
    # -------------------------------------------------


    predicted_percentage = predict_attendance(
        present_classes,
        total_classes,
        future_classes
    )
    classes_needed = calculate_classes_needed(
        present_classes,
        total_classes
    )

    # -------------------------------------------------
    # RETURN RESULT
    # -------------------------------------------------

    return {
        "student_id": student_id,
        "current_attendance": current_percentage,
        "predicted_attendance": predicted_percentage,
        "future_classes": future_classes,
        "classes_needed_for_75_percent": classes_needed
    }