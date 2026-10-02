# =====================================================
# ATTENDANCE SERVICE
# =====================================================

def calculate_attendance(attendance_records):

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

    return {
        "percentage": attendance_percentage,
        "present": present_classes,
        "total": total_classes,
        "status": attendance_status
    }