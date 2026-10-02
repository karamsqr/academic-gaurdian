from pydantic import BaseModel
from typing import List


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    roll_number: str

    class Config:
        from_attributes = True


class AttendanceInfo(BaseModel):
    percentage: float
    present: int
    total: int
    status: str


class MarksInfo(BaseModel):
    average: float
    assessments_completed: int


class RiskInfo(BaseModel):
    level: str
    reason: str


class CourseInfo(BaseModel):
    id: int
    name: str
    code: str


class CourseDashboardInfo(BaseModel):
    course: CourseInfo
    attendance: AttendanceInfo
    marks: MarksInfo


class OverallDashboardInfo(BaseModel):
    attendance: AttendanceInfo
    marks: MarksInfo
    risk: RiskInfo
    alerts: List[str]


class DashboardResponse(BaseModel):
    student: StudentResponse
    overall: OverallDashboardInfo
    courses: List[CourseDashboardInfo]