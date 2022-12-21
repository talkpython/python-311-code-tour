import asyncio
import random

from asyncio import TaskGroup
from typing import Any


# region Async methods for logging

async def record_action_to_db():
    print("Logging to DB...")
    # noinspection PyTypeChecker
    outcomes: list[Any] = [None] * 3 + [DbException] * 2 + [SocketException]

    if error := random.choice(outcomes):
        raise error("No can DB!")

    print("Logged to DB successfully.")


async def record_action_to_external_api():
    print("Logging to API...")
    # noinspection PyTypeChecker
    outcomes: list[Any] = [None] * 2 + [HttpException] * 3

    if error := random.choice(outcomes):
        raise error("No can API!")

    print("Logged to API successfully.")


async def record_action_to_log():
    print("Logging to File...")
    # noinspection PyTypeChecker
    outcomes: list[Any] = [None] * 3 + [FileException] * 2

    if error := random.choice(outcomes):
        raise error("No can File!")

    print("Logged to File successfully.")


# endregion

# region Local exception types
class DbException(Exception):
    ...


class HttpException(Exception):
    ...


class SocketException(Exception):
    ...


class FileException(Exception):
    ...


# endregion


def main():
    # asyncio.run(record_action())

    try:
        asyncio.run(record_action())
    except* DbException as db:
        for e in db.exceptions:
            print(f"DbException: Error with DB: {e}")
    except* HttpException:
        print("HttpException: Error with API")
    except* FileException:
        print("FileException: Error with file!")
    except* Exception as x:
        print(f"{len(x.exceptions)} additional errors:")
        for e in x.exceptions:
            print(f"Error: {e}")


# def main():
#     # asyncio.run(record_action())
#
#     try:
#         asyncio.run(record_action())
#     except Exception as x:
#         print("Error:")
#         print(type(x).__name__, x)


async def record_action():
    async with TaskGroup() as tg:
        tg.create_task(record_action_to_external_api())
        tg.create_task(record_action_to_log())
        tg.create_task(record_action_to_db())


if __name__ == '__main__':
    main()
