from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db

from models import (
    Student,
    Course,
    Attendance,
    Assessment,
    Mark
)

from schemas import (
    StudentResponse,
    DashboardResponse
)

from services.attendance import (
    calculate_attendance,
    predict_attendance,
    predict_attendance_if_attend_all,
    calculate_classes_needed
)

from services.marks import calculate_average_marks

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
    # -----------------------------------------
    # Find student
    # -----------------------------------------
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # -----------------------------------------
    # Overall attendance
    # -----------------------------------------
    attendance_records = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).all()

    attendance = calculate_attendance(attendance_records)

    attendance_percentage = attendance["percentage"]
    present_classes = attendance["present"]
    total_classes = attendance["total"]
    attendance_status = attendance["status"]

    # -----------------------------------------
    # Overall marks
    # -----------------------------------------
    marks = db.query(Mark).filter(
        Mark.student_id == student_id
    ).all()

    average_marks = calculate_average_marks(marks)

    # -----------------------------------------
    # Risk
    # -----------------------------------------
    risk = calculate_risk(
        attendance_percentage,
        average_marks
    )

    # -----------------------------------------
    # Alerts
    # -----------------------------------------
    alerts = generate_alerts(
        attendance_percentage,
        average_marks
    )

    # -----------------------------------------
    # Course-wise information
    # -----------------------------------------
    courses = db.query(Course).all()

    course_data = []

    for course in courses:

        # Course attendance
        course_attendance_records = db.query(
            Attendance
        ).filter(
            Attendance.student_id == student_id,
            Attendance.course_id == course.id
        ).all()

        course_attendance = calculate_attendance(
            course_attendance_records
        )

        # Course marks
        course_marks = (
            db.query(Mark)
            .join(Assessment)
            .filter(
                Mark.student_id == student_id,
                Assessment.course_id == course.id
            )
            .all()
        )

        course_average_marks = calculate_average_marks(
            course_marks
        )

        # Course information
        course_data.append({
            "course": {
                "id": course.id,
                "name": course.name,
                "code": course.code
            },

            "attendance": {
                "percentage": course_attendance["percentage"],
                "present": course_attendance["present"],
                "total": course_attendance["total"],
                "status": course_attendance["status"]
            },

            "marks": {
                "average": course_average_marks,
                "assessments_completed": len(course_marks)
            }
        })

    # -----------------------------------------
    # Final dashboard response
    # -----------------------------------------
    return {
        "student": student,

        "overall": {
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
                "level": risk["level"],
                "reason": risk["reason"]
            },

            "alerts": alerts
        },

        "courses": course_data
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
    predicted_if_attend_all = predict_attendance_if_attend_all(
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
        "predicted_at_current_rate": predicted_percentage,
        "predicted_if_attend_all": predicted_if_attend_all,
        "future_classes": future_classes,
        "classes_needed_for_75_percent": classes_needed
    }

    # your existing code...

    return {
        "student_id": student_id,
        "current_attendance": current_percentage,
        "predicted_at_current_rate": predicted_percentage,
        "predicted_if_attend_all": predicted_if_attend_all,
        "future_classes": future_classes,
        "classes_needed_for_75_percent": classes_needed
    }


# =====================================================
# COURSE-WISE STUDENT DATA
# =====================================================

@app.get("/students/{student_id}/courses")
def get_student_courses(
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
    # GET ALL COURSES
    # -------------------------------------------------

    courses = db.query(Course).all()

    course_data = []

    # -------------------------------------------------
    # PROCESS EACH COURSE
    # -------------------------------------------------

    for course in courses:

        # ---------------------------------------------
        # COURSE ATTENDANCE
        # ---------------------------------------------

        attendance_records = db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.course_id == course.id
        ).all()

        attendance = calculate_attendance(
            attendance_records
        )

        present_classes = attendance["present"]
        total_classes = attendance["total"]

        # ---------------------------------------------
        # COURSE ATTENDANCE PREDICTION
        # ---------------------------------------------

        predicted_percentage = predict_attendance(
            present_classes,
            total_classes,
            future_classes
        )

        predicted_if_attend_all = predict_attendance_if_attend_all(
            present_classes,
            total_classes,
            future_classes
        )

        classes_needed = calculate_classes_needed(
            present_classes,
            total_classes
        )

        # ---------------------------------------------
        # COURSE MARKS
        # ---------------------------------------------

        mark_records = (
            db.query(Mark)
            .join(Assessment)
            .filter(
                Mark.student_id == student_id,
                Assessment.course_id == course.id
            )
            .all()
        )

        average_marks = calculate_average_marks(
            mark_records
        )

        # ---------------------------------------------
        # ADD COURSE DATA
        # ---------------------------------------------

        course_data.append({

            "course": {

                "id": course.id,

                "name": course.name,

                "code": course.code
            },

            "attendance": {

                "percentage": attendance["percentage"],

                "present": attendance["present"],

                "total": attendance["total"],

                "status": attendance["status"],

                "predicted_at_current_rate": predicted_percentage,

                "predicted_if_attend_all": predicted_if_attend_all,

                "classes_needed_for_75_percent": classes_needed,

                "future_classes": future_classes
            },

            "marks": {

                "average": average_marks,

                "assessments_completed": len(mark_records)
            }
        })

    # -------------------------------------------------
    # RETURN COURSE DATA
    # -------------------------------------------------

    return course_data