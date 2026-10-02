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

    total_classes = len(attendance_records)

    present_classes = sum(
        1 for record in attendance_records
        if record.present
    )

    if total_classes > 0:

        attendance_percentage = (
            present_classes / total_classes
        ) * 100

    else:

        attendance_percentage = 0


    attendance_percentage = round(
        attendance_percentage,
        2
    )


    # Attendance status

    if attendance_percentage < 75:

        attendance_status = "DANGER"

    elif attendance_percentage < 80:

        attendance_status = "WARNING"

    else:

        attendance_status = "GOOD"


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

    if (
        attendance_percentage < 75
        and average_marks < 50
    ):

        risk_level = "HIGH"

        risk_reason = (
            "Low attendance and low academic performance"
        )

    elif (
        attendance_percentage < 75
        or average_marks < 50
    ):

        risk_level = "MEDIUM"

        if attendance_percentage < 75:

            risk_reason = (
                "Attendance is below the required level"
            )

        else:

            risk_reason = (
                "Academic performance is below the expected level"
            )

    else:

        risk_level = "LOW"

        risk_reason = (
            "Attendance and academic performance are healthy"
        )


    # -------------------------------------------------
    # ALERTS
    # -------------------------------------------------

    alerts = []


    if attendance_percentage < 75:

        alerts.append(
            "Attendance is below 75%"
        )


    if attendance_percentage >= 75 and attendance_percentage < 80:

        alerts.append(
            "Attendance is approaching the warning level"
        )


    if average_marks < 50:

        alerts.append(
            "Academic performance is low"
        )


    if not alerts:

        alerts.append(
            "No major academic alerts"
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