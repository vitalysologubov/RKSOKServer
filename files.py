import aiofiles

from typing import Union

from aiofiles import os
from loguru import logger


async def write_data(name: str, content: str) -> None:
    """Writes data from a request to a file."""

    async with aiofiles.open(f"phone_book_data/{name}", "w") as file:
        await file.write(content)
        logger.info(f'File "phone_book_data/{name}" saved.')


async def get_data(name: str) -> Union[bool, str]:
    """Takes data from a file to respond to client. If file is found, then
    content is returned. If not - False."""

    try:
        async with aiofiles.open(f"phone_book_data/{name}", "r") as file:
            content = await file.read()
    except FileNotFoundError:
        logger.info(f'File "phone_book_data/{name}" not found.')
        return False

    return content


async def remove_data(name: str) -> bool:
    """Deletes file by given name. If file is found and deleted, then True is
    returned. If not - False."""

    try:
        await os.remove(f"phone_book_data/{name}")
        logger.info(f'File "phone_book_data/{name}" removed.')
    except FileNotFoundError:
        logger.info(f'File "phone_book_data/{name}" not found.')
        return False

    return True
