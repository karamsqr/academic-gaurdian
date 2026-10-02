# =====================================================
# MARKS SERVICE
# =====================================================

def calculate_average_marks(mark_records):

    if not mark_records:
        return 0

    total_percentage = 0

    for mark in mark_records:

        if mark.assessment.max_marks > 0:

            percentage = (
                mark.score
                / mark.assessment.max_marks
            ) * 100

            total_percentage += percentage

    average_marks = (
        total_percentage / len(mark_records)
    )

    return round(average_marks, 2)