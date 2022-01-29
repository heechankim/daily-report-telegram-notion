"""Main module."""

import asyncio


async def nested():
    return 42


async def main():
    nested()

    print(await nested())


if __name__ == "__main__":
    asyncio.run(main())
