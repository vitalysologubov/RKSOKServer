import asyncio

from conifg import ENCODING, PROTOCOL


def create_response(verb: str, name: str = "", content: str = "", check_verb: str = "") -> str:
    """Creates a response intended for checking on validation server or for
    client.
    """

    if check_verb:
        if content:
            return f"{check_verb} {PROTOCOL}\r\n{verb} {name} {PROTOCOL}\r\n{content}\r\n\r\n"
        else:
            return f"{check_verb} {PROTOCOL}\r\n{verb} {name} {PROTOCOL}\r\n\r\n"
    else:
        if content:
            return f"{verb} {PROTOCOL}\r\n{content}\r\n\r\n"
        else:
            return f"{verb} {PROTOCOL}\r\n\r\n"


async def send_response(writer: asyncio.streams.StreamWriter, response: str) -> None:
    """Sends response to client in bytes."""

    writer.write(response.encode(ENCODING))
    await writer.drain()
    writer.close()
