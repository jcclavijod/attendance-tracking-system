from typing import Dict
from attendance.domain.student import Student
from attendance.domain.presence_record import PresenceRecord
from attendance.infrastructure.logging_config import logger


class AttendanceService:
    """
    Application Service: AttendanceService

    Purpose:
        Coordinates student registration and presence recording.

    Responsibilities: 
        - Manage student instances.
        - Delegate attendance logic to domain entities.
        - Provide access to registered students.
    """

    def __init__(self):
        """
        Initializes the service with an empty student registry.
        """
        self._students: Dict[str, Student] = {}

    def register_student(self, name: str) -> None:
        """
        Registers a new student if not already present.

        Args:
            name (str): Name of the student to register.
        """
        if not name:
            logger.warning("Attempted to register student with empty name")
            return
        if name not in self._students:
            self._students[name] = Student(name)
            logger.info(f"Student registered: {name}")

    def register_presence(
        self,
        name: str,
        day: int,
        start,
        end,
        room: str
    ) -> None:
        """
        Registers a presence record for an existing student.
        
        Notes:
            - If the student is not registered, the method does nothing.
            - PresenceRecord handles duration calculation and business rules.
        """

        if name not in self._students:
            logger.warning("Presence ignored for unregistered student '%s'", name)
            return

        try:
            record = PresenceRecord(day, start, end, room)
            self._students[name].register_presence(record)
        except Exception as e:
            logger.error(f"Error registering presence for {name}: {e}")

    def students(self):
        """
        Retrieves all registered students.

        Returns:
            List[Student]: List of Student instances.
        """
        return list(self._students.values())