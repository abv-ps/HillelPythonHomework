"""
This module demonstrates a producer-consumer pattern using asyncio and a queue.

The producer generates tasks and adds them to the queue with a delay.
Multiple consumers concurrently process the tasks from the queue.
Once all tasks are processed, the program completes.

The program consists of three main asynchronous functions:
    - producer(queue: asyncio.Queue) -> None: Simulates the production of tasks.
    - consumer(queue: asyncio.Queue, consumer_id: int) -> None: Simulates the consumption of tasks.
    - main() -> None: Coordinates the execution of the producer and multiple consumers.

Usage:
    1. The producer function creates five tasks and puts them into the queue.
    2. Three consumers concurrently process the tasks.
    3. Once all tasks are processed, the program terminates.

This module utilizes asyncio to manage concurrent execution and demonstrates the basic
concept of task scheduling and consumption using a queue.
"""

import asyncio
from logger_config import get_logger

logger = get_logger(__name__, "producer_consumer.log")

async def producer(queue: asyncio.Queue) -> None:
    """
    Produces tasks and adds them to the queue with a delay.

    Args:
        queue (asyncio.Queue): The queue to store tasks.

    Returns:
        None
    """
    for i in range(1, 6):
        await asyncio.sleep(0.5)  # Simulate delay in task creation
        task = f"Task-{i}"
        await queue.put(task)
        logger.info("Produced: %s, task", task)

    # Add completion markers for consumers
    for _ in range(3):  # 3 consumers will receive the termination signal
        await queue.put(None)


async def consumer(queue: asyncio.Queue, consumer_id: int) -> None:
    """
    Consumes tasks from the queue and processes them.

    Args:
        queue (asyncio.Queue): The queue with tasks to process.
        consumer_id (int): The identifier for the consumer.

    Returns:
        None
    """
    while True:
        task = await queue.get()
        if task is None:  # Received termination signal
            queue.task_done()
            break
        logger.info("Consumer-%s processing %s", consumer_id, task)
        await asyncio.sleep(2)  # Simulate task processing
        logger.info("Consumer-%s finished %s", consumer_id, task)
        queue.task_done()


async def main() -> None:
    """
    Runs the producer and multiple consumers concurrently.

    This function starts the producer and several consumers concurrently.
    It waits for all tasks to be processed before finishing.

    Returns:
        None
    """
    queue: asyncio.Queue = asyncio.Queue()

    # Start the producer and multiple consumers
    producer_task = asyncio.create_task(producer(queue))
    consumer_tasks = [asyncio.create_task(consumer(queue, i)) for i in range(3)]

    # Wait for all tasks to finish
    await asyncio.gather(producer_task, *consumer_tasks)
    await queue.join()  # Wait until all tasks are processed


if __name__ == "__main__":
    asyncio.run(main())
