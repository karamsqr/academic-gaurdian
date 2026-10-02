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

# =====================================================
# ATTENDANCE PREDICTION
# =====================================================

def predict_attendance(
    present_classes,
    total_classes,
    future_classes=3
):
    """
    Predict attendance if the student maintains
    their current attendance pattern.
    """

    if total_classes == 0:
        return 0.0

    current_percentage = (
        present_classes / total_classes
    ) * 100

    # Estimate future attendance using
    # the student's current attendance rate.
    predicted_present = (
        present_classes
        + (current_percentage / 100) * future_classes
    )

    predicted_total = (
        total_classes + future_classes
    )

    predicted_percentage = (
        predicted_present / predicted_total
    ) * 100

    return round(predicted_percentage, 2)

# =====================================================
# ATTENDANCE PREDICTION IF ALL FUTURE CLASSES ARE ATTENDED
# =====================================================

def predict_attendance_if_attend_all(
    present_classes,
    total_classes,
    future_classes
):
    """
    Predict attendance if the student attends
    all upcoming classes.
    """

    if total_classes == 0:
        return 0.0

    predicted_present = (
        present_classes + future_classes
    )

    predicted_total = (
        total_classes + future_classes
    )

    predicted_percentage = (
        predicted_present / predicted_total
    ) * 100

    return round(predicted_percentage, 2)

# =====================================================
# ATTENDANCE RECOVERY CALCULATION
# =====================================================

def calculate_classes_needed(
    present_classes,
    total_classes,
    target_percentage=75
):
    """
    Calculate the minimum number of consecutive
    classes a student must attend to reach the
    target attendance percentage.
    """

    if total_classes == 0:
        return 0

    current_percentage = (
        present_classes / total_classes
    ) * 100

    # Already at or above target
    if current_percentage >= target_percentage:
        return 0

    classes_needed = 0

    while True:

        future_present = present_classes + classes_needed
        future_total = total_classes + classes_needed

        future_percentage = (
            future_present / future_total
        ) * 100

        if future_percentage >= target_percentage:
            return classes_needed

        classes_needed += 1
        