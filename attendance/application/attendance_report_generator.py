class AttendanceReportGenerator:
    """
    Application Service: AttendanceReportGenerator

    Purpose:
        Generates a formatted attendance report sorted
        by total attendance minutes in descending order.

    Responsibilities:
        - Sort students by total minutes.
        - Format output according to specification.
    """

    def generate(self, students) -> str:
        """
        Generates an attendance report.

        Example:
            Marco: 142 minutes in 2 days
            David: 104 minutes in 1 day
            Fran: 0 minutes
        """
        # Sort students by total minutes (descending)
        sorted_students = sorted(
            students,
            key=lambda s: s.total_minutes(),
            reverse=True
        )

        lines = []

        for student in sorted_students:
            minutes = student.total_minutes()
            days = student.total_days()

            if minutes == 0:
                # Special case: student without attendance
                lines.append(f"{student.name}: 0 minutes")
            else:
                day_label = "day" if days == 1 else "days"

                lines.append(
                    f"{student.name}: {minutes} minutes in {days} {day_label}"
                )

        return "\n".join(lines)