import pytest
from datetime import datetime
from attendance.application.attendance_report_generator import AttendanceReportGenerator
from attendance.domain.student import Student
from attendance.domain.presence_record import PresenceRecord


class TestAttendanceReportGenerator:

    def test_generate_report_sorted_and_formatted(self):
        report_gen = AttendanceReportGenerator()

        student1 = Student("Marco")
        student1.register_presence(PresenceRecord(
            1, datetime.strptime("09:00", "%H:%M"), datetime.strptime("10:00", "%H:%M"), "R100"))
        student1.register_presence(PresenceRecord(
            2, datetime.strptime("11:00", "%H:%M"), datetime.strptime("12:10", "%H:%M"), "F101"))

        student2 = Student("David")
        student2.register_presence(PresenceRecord(
            3, datetime.strptime("08:00", "%H:%M"), datetime.strptime("08:30", "%H:%M"), "R200"))

        student3 = Student("Fran")  # No presences

        students = [student1, student2, student3]
        report = report_gen.generate(students)

        expected_lines = [
            "Marco: 130 minutes in 2 days",
            "David: 30 minutes in 1 day",
            "Fran: 0 minutes"
        ]

        for line in expected_lines:
            assert line in report