from datetime import date, timedelta

from database import SessionLocal
from models import Student, Course, Attendance, Assessment, Mark


def seed_database():

    db = SessionLocal()

    # Prevent duplicate data if seed is run again
    if db.query(Student).first():
        print("Database already contains data.")
        db.close()
        return

    # =====================================================
    # STUDENTS
    # =====================================================

    john = Student(
        name="John Smith",
        email="john@example.com",
        roll_number="IT001"
    )

    david = Student(
        name="David Brown",
        email="david@example.com",
        roll_number="IT002"
    )

    # Two students with similar names for our
    # voice/name-matching test
    alex1 = Student(
        name="Alex John",
        email="alex1@example.com",
        roll_number="IT003"
    )

    alex2 = Student(
        name="Alex Brown",
        email="alex2@example.com",
        roll_number="IT004"
    )

    mike = Student(
        name="Mike Wilson",
        email="mike@example.com",
        roll_number="IT005"
    )

    db.add_all([
        john,
        david,
        alex1,
        alex2,
        mike
    ])

    db.commit()

    # =====================================================
    # COURSES
    # =====================================================

    dbms = Course(
        name="Database Management Systems",
        code="DBMS"
    )

    java = Course(
        name="Java Programming",
        code="JAVA"
    )

    maths = Course(
        name="Engineering Mathematics",
        code="MATHS"
    )

    db.add_all([
        dbms,
        java,
        maths
    ])

    db.commit()

    # =====================================================
    # ATTENDANCE
    # =====================================================

    today = date.today()

    # -----------------------------------------------------
    # John Smith
    # Good attendance
    # -----------------------------------------------------

    for i in range(30):
        attendance = Attendance(
            student_id=john.id,
            course_id=dbms.id,
            date=today - timedelta(days=i),
            present=(i % 10 != 0)
        )

        db.add(attendance)

    # -----------------------------------------------------
    # David Brown
    # Poor attendance - HIGH RISK
    # -----------------------------------------------------

    for i in range(25):
        attendance = Attendance(
            student_id=david.id,
            course_id=dbms.id,
            date=today - timedelta(days=i),
            present=(i % 3 != 0)
        )

        db.add(attendance)

    # -----------------------------------------------------
    # Alex John
    # Good attendance
    # -----------------------------------------------------

    for i in range(30):
        attendance = Attendance(
            student_id=alex1.id,
            course_id=dbms.id,
            date=today - timedelta(days=i),
            present=(i % 10 != 0)
        )

        db.add(attendance)

    # -----------------------------------------------------
    # Alex Brown
    # Average attendance
    # -----------------------------------------------------

    for i in range(30):
        attendance = Attendance(
            student_id=alex2.id,
            course_id=dbms.id,
            date=today - timedelta(days=i),
            present=(i % 4 != 0)
        )

        db.add(attendance)

    # -----------------------------------------------------
    # Mike Wilson
    # Good attendance
    # -----------------------------------------------------

    for i in range(30):
        attendance = Attendance(
            student_id=mike.id,
            course_id=dbms.id,
            date=today - timedelta(days=i),
            present=(i % 8 != 0)
        )

        db.add(attendance)

    db.commit()

    # =====================================================
    # ASSESSMENTS
    # =====================================================

    quiz1 = Assessment(
        course_id=dbms.id,
        name="Quiz 1",
        max_marks=25,
        weight=20
    )

    quiz2 = Assessment(
        course_id=dbms.id,
        name="Quiz 2",
        max_marks=25,
        weight=20
    )

    assignment1 = Assessment(
        course_id=dbms.id,
        name="Assignment 1",
        max_marks=10,
        weight=10
    )

    db.add_all([
        quiz1,
        quiz2,
        assignment1
    ])

    db.commit()

    # =====================================================
    # MARKS
    # =====================================================

    db.add_all([

        # -------------------------------------------------
        # John Smith - GOOD
        # -------------------------------------------------

        Mark(
            student_id=john.id,
            assessment_id=quiz1.id,
            score=22
        ),

        Mark(
            student_id=john.id,
            assessment_id=quiz2.id,
            score=21
        ),

        Mark(
            student_id=john.id,
            assessment_id=assignment1.id,
            score=9
        ),

        # -------------------------------------------------
        # David Brown - POOR / HIGH RISK
        # -------------------------------------------------

        Mark(
            student_id=david.id,
            assessment_id=quiz1.id,
            score=10
        ),

        Mark(
            student_id=david.id,
            assessment_id=quiz2.id,
            score=8
        ),

        Mark(
            student_id=david.id,
            assessment_id=assignment1.id,
            score=4
        ),

        # -------------------------------------------------
        # Alex John - GOOD
        # -------------------------------------------------

        Mark(
            student_id=alex1.id,
            assessment_id=quiz1.id,
            score=23
        ),

        Mark(
            student_id=alex1.id,
            assessment_id=quiz2.id,
            score=21
        ),

        Mark(
            student_id=alex1.id,
            assessment_id=assignment1.id,
            score=9
        ),

        # -------------------------------------------------
        # Alex Brown - AVERAGE
        # -------------------------------------------------

        Mark(
            student_id=alex2.id,
            assessment_id=quiz1.id,
            score=16
        ),

        Mark(
            student_id=alex2.id,
            assessment_id=quiz2.id,
            score=15
        ),

        Mark(
            student_id=alex2.id,
            assessment_id=assignment1.id,
            score=7
        ),

        # -------------------------------------------------
        # Mike Wilson - GOOD
        # -------------------------------------------------

        Mark(
            student_id=mike.id,
            assessment_id=quiz1.id,
            score=20
        ),

        Mark(
            student_id=mike.id,
            assessment_id=quiz2.id,
            score=22
        ),

        Mark(
            student_id=mike.id,
            assessment_id=assignment1.id,
            score=9
        )
    ])

    db.commit()

    # =====================================================
    # DONE
    # =====================================================

    print()
    print("======================================")
    print(" DATABASE SEEDED SUCCESSFULLY!")
    print("======================================")
    print()
    print("Students created:")
    print("1 - John Smith   (IT001)")
    print("2 - David Brown  (IT002)")
    print("3 - Alex John    (IT003)")
    print("4 - Alex Brown   (IT004)")
    print("5 - Mike Wilson  (IT005)")
    print()
    print("Courses created:")
    print("1 - Database Management Systems (DBMS)")
    print("2 - Java Programming (JAVA)")
    print("3 - Engineering Mathematics (MATHS)")
    print()
    print("Voice ambiguity test:")
    print("There are TWO students named Alex.")
    print("The system should ask for confirmation")
    print("instead of guessing the student.")
    print()

    db.close()


if __name__ == "__main__":
    seed_database()