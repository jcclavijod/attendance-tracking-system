import pytest
from datetime import datetime
from attendance.application.attendance_service import AttendanceService
from attendance.domain.student import Student
from attendance.domain.presence_record import PresenceRecord


@pytest.fixture
def service():
    return AttendanceService()


class TestAttendanceService:

    def test_register_student_and_presence(self, service):
        service.register_student("Marco")
        service.register_presence(
            name="Marco",
            day=1,
            start=datetime.strptime("09:00", "%H:%M"),
            end=datetime.strptime("10:00", "%H:%M"),
            room="R100"
        )

        students = service.students()
        assert len(students) == 1
        student = students[0]
        assert student.name == "Marco"
        assert student.total_minutes() == 60
        assert student.total_days() == 1

    def test_ignore_short_presences(self, service):
        service.register_student("Marco")
        service.register_presence(
            name="Marco",
            day=1,
            start=datetime.strptime("09:00", "%H:%M"),
            end=datetime.strptime("09:03", "%H:%M"),  # 3 minutes < MIN_DURATION
            room="R100"
        )
        student = service.students()[0]
        assert student.total_minutes() == 0
        assert student.total_days() == 0

    def test_logs_warning_for_unregistered_student(self, service, caplog):
        with caplog.at_level("WARNING"):
            service.register_presence(
                name="Unknown",
                day=1,
                start=datetime.strptime("09:00", "%H:%M"),
                end=datetime.strptime("10:00", "%H:%M"),
                room="R100"
            )
        assert any("Presence ignored for unregistered student 'Unknown'" in m for m in caplog.messages)