class GameEventException(BaseException):
    """Exception raised for game-related events."""

    def __init__(self, event_type: str, details: dict) -> None:
        """
        Initialize GameEventException.

        Args:
            event_type: Type of the game event.
            details: Additional details related to the event.
        """
        super().__init__(f"Game Event Occurred: {event_type}")
        self.event_type = event_type
        self.details = details

    def __str__(self) -> str:
        return f"[{self.event_type}] Details: {self.details}"


def trigger_event(event_type: str, details: dict) -> None:
    """
    Trigger a game event by raising an exception.

    Args:
        event_type: Type of the event.
        details: Additional details of the event.
    Raises:
         GameEventException: Always raised with the provided details.
    """
    raise GameEventException(event_type, details)


def handle_death_event() -> None:
    """
    Handle death-related game events by triggering exceptions.
    """
    causes = [
        {"cause": "sword strike"},
        {"cause": "fall"},
        {"cause": "crossbow bolt"},
    ]

    for cause in causes:
        try:
            print(f"Triggering 'Death' event: {cause['cause']}")
            trigger_event("Death", cause)
        except GameEventException as e:
            print(f"Event caught: {e}")
            print(f"Message for user: 'Your character died due to {cause['cause']}.'")


def handle_level_up_event() -> None:
    """
    Handle level-up events by triggering exceptions.
    """
    level_up_reasons = [
        {"reason": "New character level", "details": "level 99 reached"},
        {"reason": "Experience points gained", "details": "+ 50 XP"},
        {"reason": "Increased stamina", "details": "your stamina increased by 7%"},
    ]

    for reason in level_up_reasons:
        try:
            print(f"Triggering 'LevelUp' event: {reason['reason']} - {reason['details']}")
            trigger_event("LevelUp", reason)
        except GameEventException as e:
            print(f"Event caught: {e}")
            print(f"Message for user: 'Level Up! {reason['reason']} ({reason['details']}).'")


if __name__ == "__main__":
    try:
        handle_death_event()
        print("_&_" * 27)
        handle_level_up_event()
    except GameEventException as e:
        print(f"General Event Handling: {e}")
        print("Event details have been logged.")
