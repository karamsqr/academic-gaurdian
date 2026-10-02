# =====================================================
# RISK SERVICE
# =====================================================

def calculate_risk(attendance_percentage, average_marks):

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

    return {
        "level": risk_level,
        "reason": risk_reason
    }