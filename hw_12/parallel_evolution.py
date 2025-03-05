"""
This module simulates the evolution of a population of organisms over multiple generations.
Each organism goes through a life cycle, including eating, aging, reproducing,
and possibly getting sick or recovering.
The simulation runs concurrently using multiprocessing for performance optimization.

Classes:
    Organism: Represents an organism with attributes such as health, food,
              reproduction capability, and disease status.
        - health (int): Current health level of the organism.
        - food (int): Amount of food available to the organism.
        - reproduction_chance (float): Probability of reproducing in each cycle.
        - disease_chance (float): Probability of catching a disease.
        - is_sick (bool): Indicates whether the organism is sick.

Functions:
    simulate_organism_life(organism: Organism) -> tuple:
        Simulates the life cycle of a single organism, including eating,
        reproducing, catching disease, and aging.
        This function is executed in a separate process for each organism.

    evolve_population(population_size: int, generations: int, num_processes: int) -> list:
        Simulates the evolution of a population of organisms over multiple generations.
        Uses multiprocessing to simulate organisms' life cycles in parallel.
        Returns the final population after all generations.
"""
import random
import multiprocessing


class Organism:
    """
    Represents an organism with health, food, reproduction capability, and disease status.

    Attributes:
        health (int): Current health level of the organism.
        food (int): Amount of food available to the organism.
        reproduction_chance (float): Probability of reproducing in each cycle.
        disease_chance (float): Probability of catching a disease.
        is_sick (bool): Indicates whether the organism is sick.
    """

    def __init__(self, health: int, food: int, reproduction_chance: float,
                 disease_chance: float) -> None:
        """
        Initializes an organism with health, food, reproduction chance, and disease chance.

        Args:
            health (int): The initial health of the organism.
            food (int): The amount of food the organism starts with.
            reproduction_chance (float): The probability that the organism will reproduce.
            disease_chance (float): The probability that the organism will get sick.

        Returns:
            None
        """
        self.health = health
        self.food = food
        self.reproduction_chance = reproduction_chance
        self.disease_chance = disease_chance
        self.is_sick = False  # Organism disease status

    def eat(self) -> None:
        """
        Consumes food to improve health or loses health if no food is available.

        Returns:
            None
        """
        if self.food > 0:
            self.health += 1
            self.food -= 1
        else:
            self.health -= 1  # Lose health if no food

    def reproduce(self) -> "Organism | None":
        """
        Attempts to reproduce based on the reproduction chance.

        Returns:
            Organism | None: A new organism if reproduction is successful, otherwise None.
        """
        if random.random() < self.reproduction_chance:
            return Organism(
                health=random.randint(5, 15),
                food=random.randint(3, 10),
                reproduction_chance=self.reproduction_chance,
                disease_chance=self.disease_chance,
            )
        return None

    def catch_disease(self) -> None:
        """Determines if the organism catches a disease."""
        if not self.is_sick and random.random() < self.disease_chance:
            self.is_sick = True
            self.health -= 2

    def heal(self) -> None:
        """Gives the organism a chance to recover from illness."""
        if self.is_sick and random.random() < 0.3:
            self.is_sick = False
            self.health += 3  # Healing improves health by 3

    def age(self) -> None:
        """Reduces health over time and applies additional penalty if sick."""
        self.health -= 2  # Natural aging
        if self.is_sick:
            self.health -= 2  # Additional health loss due to illness

    def live(self) -> tuple[list, list]:
        """
        Simulates a single step of the organism's life cycle.
        - Eats food
        - Ages
        - Tries to reproduce
        - May get sick or recover

        Returns:
            tuple: A tuple containing two lists:
                - The first list contains the current organism if it is still alive,
                  otherwise it's empty.
                - The second list contains the offspring if reproduction occurred,
                  otherwise it's empty.
        """
        self.catch_disease()
        self.eat()
        self.age()
        self.heal()
        offspring = self.reproduce()

        return [self] if self.health > 0 else [], [offspring] if offspring else []


def simulate_organism_life(organism: Organism) -> tuple:
    """
    Simulate the life cycle of a single organism, including eating, reproducing,
    catching disease, and aging.
    This function is executed in a separate process for each organism.

    Args:
        organism (Organism): The organism to simulate life for.

    Returns:
        tuple: A tuple containing the current organism and a newly reproduced organism (if any).
               If the organism does not survive, both values in the tuple will be None.
    """
    return organism.live()


def evolve_population(population_size: int, generations: int, num_processes: int):
    """
    Simulates evolution over multiple generations.

    Args:
        population_size (int): Initial number of organisms.
        generations (int): Number of generations to simulate.
        num_processes (int): Number of parallel processes.

    Returns:
        list: Final population after all generations.
    """
    population = [
        Organism(
            health=random.randint(5, 15),
            food=random.randint(3, 10),
            reproduction_chance=random.uniform(0.3, 0.7),
            disease_chance=random.uniform(0.1, 0.3)
        ) for _ in range(population_size)
    ]

    for generation in range(generations):
        print(f"Generation {generation + 1}...")

        # Use multiprocessing to simulate the life of each organism concurrently
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.map(simulate_organism_life, population)

        # Rebuild the population by adding surviving and newly reproduced organisms.
        population = []
        for old_organisms, new_organisms in results:
            population.extend(old_organisms)
            population.extend(new_organisms)

        print(f"Population size: {len(population)}")

    return population


if __name__ == "__main__":
    final_population = evolve_population(population_size=77, generations=15, num_processes=4)
    print(f"Final population size: {len(final_population)}")
