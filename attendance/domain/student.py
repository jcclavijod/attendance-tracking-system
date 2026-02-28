from typing import List, Set
from .presence_record import PresenceRecord
from attendance.settings import MIN_PRESENCE_DURATION


class Student:
    """
    Domain Entity: Student

    Purpose:
        Represents a university student and encapsulates
        attendance-related business logic.

    Responsibilities:
        - Register valid presence records.
        - Compute total attendance minutes.
        - Compute total distinct attendance days.

    Business Rules:
        - Presence records shorter than MIN_DURATION minutes are ignored.
    """
    
    MIN_DURATION = MIN_PRESENCE_DURATION

    def __init__(self, name: str):
        """
        Initializes a new student with a given name.

        Args:
            name (str): The student's full name.
        """
        self.name = name
        self._presences: List[PresenceRecord] = []

    def register_presence(self, record: PresenceRecord) -> None:
        """
        Registers a presence record if it meets the minimum duration.

        Args:
            record (PresenceRecord): A presence record to add.
        """
        if record.duration_minutes() >= self.MIN_DURATION:
            self._presences.append(record)

    def total_minutes(self) -> int:
        """
        Calculates the total attendance minutes for the student.

        Returns:
            int: Sum of all valid presence durations.
        """
        return sum(p.duration_minutes() for p in self._presences)

    def total_days(self) -> int:
        """
        Counts the number of distinct days the student attended.

        Returns:
            int: Number of unique days with valid presence records.
        """
        return len({p.day for p in self._presences})