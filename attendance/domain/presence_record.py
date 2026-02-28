from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PresenceRecord:
    """
    Domain Value Object: PresenceRecord

    Purpose:
        Represents a student's presence in a specific room and day.

    Characteristics:
        - Immutable.
        - Provides duration calculation in minutes.
    """

    day: int        # Day of the week (1-7)
    start: datetime # Start time of presence
    end: datetime   # End time of presence
    room: str       # Room code where presence was detected
    
    def duration_minutes(self) -> int:
        """
        Calculates the duration of the presence in minutes.

        Returns:
            int: Duration in minutes between start and end time.
        """
        delta = self.end - self.start
        return int(delta.total_seconds() / 60)