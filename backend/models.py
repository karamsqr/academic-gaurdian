from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    roll_number = Column(String, unique=True, nullable=False)

    attendances = relationship("Attendance", back_populates="student")
    marks = relationship("Mark", back_populates="student")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)

    attendances = relationship("Attendance", back_populates="course")
    assessments = relationship("Assessment", back_populates="course")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    date = Column(Date, nullable=False)
    present = Column(Boolean, default=False)

    student = relationship("Student", back_populates="attendances")
    course = relationship("Course", back_populates="attendances")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("courses.id"))

    name = Column(String, nullable=False)
    max_marks = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)

    course = relationship("Course", back_populates="assessments")
    marks = relationship("Mark", back_populates="assessment")


class Mark(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"))
    assessment_id = Column(Integer, ForeignKey("assessments.id"))

    score = Column(Float, nullable=False)

    student = relationship("Student", back_populates="marks")
    assessment = relationship("Assessment", back_populates="marks")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"))

    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)