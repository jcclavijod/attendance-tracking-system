from typing import TypedDict, Union, List
from attendance.infrastructure.logging_config import logger

# -----------------------------
# TypedDicts for strong typing
# -----------------------------
class StudentEvent(TypedDict):
    type: str
    name: str


class PresenceEvent(TypedDict):
    type: str
    name: str
    day: int
    start: str
    end: str
    room: str


Event = Union[StudentEvent, PresenceEvent]


class InputParser:
    """
    Infrastructure Component: InputParser

    Purpose:
        Parses raw input lines into structured event dictionaries.

    Notes:
        - This component isolates input format concerns
          from the domain and application layers.
        - It performs no business validation.
    """

    def parse(self, lines: List[str]) -> List[Event]:
        """
        Parses raw input lines into a list of structured Event dictionaries.

        Args:
            lines (List[str]): Raw input lines from file or stdin.

        Returns:
            List[Event]: Parsed events as StudentEvent or PresenceEvent dictionaries.
        """
        events: List[Event] = []

        for i, line in enumerate(lines, start=1):
            parts = line.strip().split()

            if not parts:
                continue  # Skip empty lines
            try:
                # Parse based on command type
                if parts[0] == "Student":
                    events.append(self._parse_student(parts))
                elif parts[0] == "Presence":
                    events.append(self._parse_presence(parts))
                else:
                    logger.warning(f"Line {i}: unknown command '{parts[0]}', ignored")
            except IndexError:
                logger.error(f"Line {i}: Missing information in line: '{line.strip()}'")
            except ValueError as e:
                logger.error(f"Line {i}: value error in '{line.strip()}': {e}")

        return events
    

# -----------------------------
# Private parsing methods
# -----------------------------
    def _parse_student(self, parts: List[str]) -> StudentEvent:
        """
        Parses a 'Student' line into a StudentEvent dictionary.
        """
        if len(parts) < 2:
            raise IndexError("Student name is missing")
        return {"type": "student", "name": parts[1]}

    def _parse_presence(self, parts: List[str]) -> PresenceEvent:
        """
        Parses a 'Presence' line into a PresenceEvent dictionary.
        """
        if len(parts) < 6:
            raise IndexError("Incomplete presence record")
        try:
            day = int(parts[2])
        except ValueError:
            raise ValueError("Day must be an integer 1-7")
        return {
            "type": "presence",
            "name": parts[1],
            "day": int(parts[2]),
            "start": parts[3],
            "end": parts[4],
            "room": parts[5]
        }