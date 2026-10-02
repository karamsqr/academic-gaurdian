from datetime import date, timedelta

from database import SessionLocal
from models import Student, Course, Attendance, Assessment, Mark


def seed_database():

    # Create database tables
    from database import Base, engine
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

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
    # JOHN SMITH - GOOD
    # -----------------------------------------------------

    for course in [dbms, java, maths]:

        for i in range(20):

            db.add(
                Attendance(
                    student_id=john.id,
                    course_id=course.id,
                    date=today - timedelta(days=i),
                    present=(i % 10 != 0)
                )
            )

    # -----------------------------------------------------
    # DAVID BROWN
    # -----------------------------------------------------
    # DBMS  -> 64%  HIGH RISK
    # JAVA  -> 75%  WARNING
    # MATHS -> 90%  GOOD
    # -----------------------------------------------------

    # DBMS: 16 / 25 = 64%

    for i in range(25):

        db.add(
            Attendance(
                student_id=david.id,
                course_id=dbms.id,
                date=today - timedelta(days=i),
                present=(i % 3 != 0)
            )
        )

    # JAVA: 15 / 20 = 75%

    for i in range(20):

        db.add(
            Attendance(
                student_id=david.id,
                course_id=java.id,
                date=today - timedelta(days=i),
                present=(i % 4 != 0)
            )
        )

    # MATHS: 18 / 20 = 90%

    for i in range(20):

        db.add(
            Attendance(
                student_id=david.id,
                course_id=maths.id,
                date=today - timedelta(days=i),
                present=(i % 10 != 0)
            )
        )

    # -----------------------------------------------------
    # ALEX JOHN - GOOD
    # -----------------------------------------------------

    for course in [dbms, java, maths]:

        for i in range(20):

            db.add(
                Attendance(
                    student_id=alex1.id,
                    course_id=course.id,
                    date=today - timedelta(days=i),
                    present=(i % 10 != 0)
                )
            )

    # -----------------------------------------------------
    # ALEX BROWN - AVERAGE
    # -----------------------------------------------------

    for course in [dbms, java, maths]:

        for i in range(20):

            db.add(
                Attendance(
                    student_id=alex2.id,
                    course_id=course.id,
                    date=today - timedelta(days=i),
                    present=(i % 4 != 0)
                )
            )

    # -----------------------------------------------------
    # MIKE WILSON - GOOD
    # -----------------------------------------------------

    for course in [dbms, java, maths]:

        for i in range(20):

            db.add(
                Attendance(
                    student_id=mike.id,
                    course_id=course.id,
                    date=today - timedelta(days=i),
                    present=(i % 8 != 0)
                )
            )

    db.commit()

    # =====================================================
    # ASSESSMENTS
    # =====================================================

    assessments = {}

    for course in [dbms, java, maths]:

        quiz1 = Assessment(
            course_id=course.id,
            name="Quiz 1",
            max_marks=25,
            weight=20
        )

        quiz2 = Assessment(
            course_id=course.id,
            name="Quiz 2",
            max_marks=25,
            weight=20
        )

        assignment1 = Assessment(
            course_id=course.id,
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

        assessments[course.code] = {
            "quiz1": quiz1,
            "quiz2": quiz2,
            "assignment1": assignment1
        }

    # =====================================================
    # MARKS
    # =====================================================

    # -----------------------------------------------------
    # JOHN SMITH - GOOD
    # -----------------------------------------------------

    for course in [dbms, java, maths]:

        a = assessments[course.code]

        db.add_all([
            Mark(
                student_id=john.id,
                assessment_id=a["quiz1"].id,
                score=22
            ),
            Mark(
                student_id=john.id,
                assessment_id=a["quiz2"].id,
                score=21
            ),
            Mark(
                student_id=john.id,
                assessment_id=a["assignment1"].id,
                score=9
            )
        ])

    # -----------------------------------------------------
    # DAVID BROWN
    # -----------------------------------------------------
    # DBMS -> LOW
    # JAVA -> AVERAGE
    # MATHS -> GOOD
    # -----------------------------------------------------

    dbms_a = assessments["DBMS"]
    java_a = assessments["JAVA"]
    maths_a = assessments["MATHS"]

    # DBMS - average = 37.33%

    db.add_all([
        Mark(
            student_id=david.id,
            assessment_id=dbms_a["quiz1"].id,
            score=10
        ),
        Mark(
            student_id=david.id,
            assessment_id=dbms_a["quiz2"].id,
            score=8
        ),
        Mark(
            student_id=david.id,
            assessment_id=dbms_a["assignment1"].id,
            score=4
        )
    ])

    # JAVA - average = 64%

    db.add_all([
        Mark(
            student_id=david.id,
            assessment_id=java_a["quiz1"].id,
            score=16
        ),
        Mark(
            student_id=david.id,
            assessment_id=java_a["quiz2"].id,
            score=15
        ),
        Mark(
            student_id=david.id,
            assessment_id=java_a["assignment1"].id,
            score=6
        )
    ])

    # MATHS - average = 88%

    db.add_all([
        Mark(
            student_id=david.id,
            assessment_id=maths_a["quiz1"].id,
            score=22
        ),
        Mark(
            student_id=david.id,
            assessment_id=maths_a["quiz2"].id,
            score=22
        ),
        Mark(
            student_id=david.id,
            assessment_id=maths_a["assignment1"].id,
            score=9
        )
    ])

    # -----------------------------------------------------
    # ALEX JOHN - GOOD
    # -----------------------------------------------------

    for course in [dbms, java, maths]:

        a = assessments[course.code]

        db.add_all([
            Mark(
                student_id=alex1.id,
                assessment_id=a["quiz1"].id,
                score=23
            ),
            Mark(
                student_id=alex1.id,
                assessment_id=a["quiz2"].id,
                score=21
            ),
            Mark(
                student_id=alex1.id,
                assessment_id=a["assignment1"].id,
                score=9
            )
        ])

    # -----------------------------------------------------
    # ALEX BROWN - AVERAGE
    # -----------------------------------------------------

    for course in [dbms, java, maths]:

        a = assessments[course.code]

        db.add_all([
            Mark(
                student_id=alex2.id,
                assessment_id=a["quiz1"].id,
                score=16
            ),
            Mark(
                student_id=alex2.id,
                assessment_id=a["quiz2"].id,
                score=15
            ),
            Mark(
                student_id=alex2.id,
                assessment_id=a["assignment1"].id,
                score=7
            )
        ])

    # -----------------------------------------------------
    # MIKE WILSON - GOOD
    # -----------------------------------------------------

    for course in [dbms, java, maths]:

        a = assessments[course.code]

        db.add_all([
            Mark(
                student_id=mike.id,
                assessment_id=a["quiz1"].id,
                score=20
            ),
            Mark(
                student_id=mike.id,
                assessment_id=a["quiz2"].id,
                score=22
            ),
            Mark(
                student_id=mike.id,
                assessment_id=a["assignment1"].id,
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
    print("David Brown demo profile:")
    print("DBMS  -> Low attendance + Low marks")
    print("JAVA  -> Warning attendance + Average marks")
    print("MATHS -> Good attendance + Good marks")
    print()
    print("Voice ambiguity test:")
    print("There are TWO students named Alex.")
    print("The system should ask for confirmation")
    print("instead of guessing the student.")
    print()

    db.close()


if __name__ == "__main__":
    seed_database()