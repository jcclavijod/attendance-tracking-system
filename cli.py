import sys

from attendance.infrastructure.input_parser import InputParser
from attendance.application.attendance_service import AttendanceService
from attendance.application.attendance_report_generator import AttendanceReportGenerator
from attendance.application.attendance_application import AttendanceApplication


def main():

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    parser = InputParser()
    service = AttendanceService()
    report_generator = AttendanceReportGenerator()

    app = AttendanceApplication(service, report_generator)

    events = parser.parse(lines)
    result = app.run(events)

    print(result)


if __name__ == "__main__":
    main()