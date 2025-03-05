import asyncio
import aiohttp
import logging

print("simulate_requests.py started")

async def simulate_requests() -> None:
    """
    Simulates multiple requests to the server with both fast and slow responses.
    """
    logging.info("Starting to simulate multiple client requests.")

    async with aiohttp.ClientSession() as session:
        tasks = [
            session.get('http://127.0.0.1:7777/'),
            session.get('http://127.0.0.1:7777/slow'),
            session.get('http://127.0.0.1:7777/'),
            session.get('http://127.0.0.1:7777/slow'),
            session.get('http://127.0.0.1:7777/'),
            session.get('http://127.0.0.1:7777/slow'),
            session.get('http://127.0.0.1:7777/')
        ]

        responses = await asyncio.gather(*tasks)

        for response in responses:
            content = await response.text()
            logging.info(f"Received response: {content}...")

    logging.info("Finished all simulated requests.")

if __name__ == "__main__":
    asyncio.run(simulate_requests())
