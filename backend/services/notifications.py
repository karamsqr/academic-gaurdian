# =====================================================
# NOTIFICATION SERVICE
# =====================================================

def generate_alerts(attendance_percentage, average_marks):

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

    return alerts