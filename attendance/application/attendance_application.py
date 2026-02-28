from datetime import datetime
from attendance.infrastructure.logging_config import logger

class AttendanceApplication:
    """
    Application Orchestrator: AttendanceApplication

    Purpose:
        Orchestrates the complete attendance processing workflow.

    Workflow:
        1. Receive parsed input events.
        2. Delegate operations to AttendanceService.
        3. Generate the final formatted report.
    """

    def __init__(self, service, report_generator):
        """
        Initializes the orchestrator with required application services.
        """
        self.service = service
        self.report_generator = report_generator

    def run(self, events):
        """
        Executes the attendance processing workflow.

        Workflow:
            - Registers students.
            - Converts presence event times to datetime objects.
            - Registers presences in AttendanceService.
            - Delegates report generation to AttendanceReportGenerator.
        """
        for i, event in enumerate(events, start=1):
            try:
                if event["type"] == "student":
                    self.service.register_student(event["name"])

                elif event["type"] == "presence":
                    # Parse start and end times into datetime objects
                    start = datetime.strptime(event["start"], "%H:%M")
                    end = datetime.strptime(event["end"], "%H:%M")

                    self.service.register_presence(
                        name=event["name"],
                        day=event["day"],
                        start=start,
                        end=end,
                        room=event["room"]
                    )
                else:
                    logger.warning(f"Unknown event at position {i}: {event}")
            except Exception as e:
                logger.error(f"Error processing event {i}: {event}, {e}")
        # Generate final report
        try:
            return self.report_generator.generate(self.service.students())
        except Exception as e:
            logger.error(f"Error generating final report: {e}")
            return ""