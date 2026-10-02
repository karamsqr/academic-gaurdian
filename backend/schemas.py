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


class DashboardResponse(BaseModel):
    student: StudentResponse
    attendance: AttendanceInfo
    marks: MarksInfo
    risk: RiskInfo
    alerts: List[str]