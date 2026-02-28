import pytest
from attendance.infrastructure.input_parser import InputParser


@pytest.fixture
def parser():
    return InputParser()


class TestInputParser:

    def test_parse_students_and_presences(self, parser):
        lines = [
            "Student Marco",
            "Presence Marco 1 09:00 10:00 R100",
            "Presence Marco 2 11:00 11:03 F101",  # under 5 minutes
            "Student David",
            "Presence David 3 08:00 08:30 R200"
        ]

        events = parser.parse(lines)

        # 2 students + 3 presences
        assert len(events) == 5
        assert events[0]["type"] == "student"
        assert events[0]["name"] == "Marco"
        assert events[2]["type"] == "presence"
        assert events[4]["name"] == "David"

    def test_parse_invalid_lines_logs_error(self, parser, caplog):
        lines = [
            "Student",          # Missing name
            "Presence Marco"    # Missing fields
        ]

        with caplog.at_level("ERROR"):
            events = parser.parse(lines)
        assert len(events) == 0
        assert any("Missing information in line" in m for m in caplog.messages)