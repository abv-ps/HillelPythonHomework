class InsufficientResourcesException(Exception):
    """
    Exception raised when there are not enough resources to perform an action.
    """

    def __init__(self, required_resource: str, required_amount: int, current_amount: int):
        """
        Initialize the exception.

        Args:
            required_resource: Resource that is lacking (e.g., "gold", "mana").
            required_amount: Required amount of the resource.
            current_amount: Current amount of the resource available to the player.
        """
        super().__init__(
            f"Not enough {required_resource}. Needed {required_amount}, but you have {current_amount}."
        )
        self.required_resource = required_resource
        self.required_amount = required_amount
        self.current_amount = current_amount

    def get_missing_amount(self) -> int:
        """
        Returns the amount of resource missing to perform the action.
        """
        return self.required_amount - self.current_amount


class Player:
    def __init__(self, name: str, resources: dict):
        """
        Initialize the player.

        Args:
            name: Player's name.
            resources: Dictionary containing resources and their amounts (e.g., {"gold": 100, "mana": 50}).
        """
        self.name = name
        self.resources = resources

    def some_action(self, action: str, required_resource: str, required_amount: int):
        """
        Performs an action, checking for sufficient resources.

        Args:
            action: Description of the action (e.g., "attack", "cast spell").
            required_resource: Resource required for the action.
            required_amount: Amount of the resource needed for the action.
        """
        current_amount = self.resources.get(required_resource, 0)

        if current_amount < required_amount:
            raise InsufficientResourcesException(required_resource, required_amount, current_amount)

        self.resources[required_resource] = max(0, current_amount - required_amount)
        current_amount = self.resources[required_resource]
        print(f"{self.name} successfully {action} with {required_amount} {required_resource}, "
              f"remain {required_resource}: {current_amount}.")


if __name__ == "__main__":
    try:
        player = Player("Arthas", {"gold": 80, "mana": 100})
        player.some_action("buy Ziggurat", "gold", 47)
    except InsufficientResourcesException as e:
        print(f"Error: {e}")

    try:
        player.some_action("cast spell", "mana", 33)
    except InsufficientResourcesException as e:
        print(f"Error: {e}")
