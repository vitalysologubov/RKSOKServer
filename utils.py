import asyncio

from typing import Union

from conifg import ENCODING, PROTOCOL, VALIDATION_SERVER_ADDRESS, VALIDATION_SERVER_PORT
from specs import RequestVerb


def is_request_ends_correctly(request: str) -> bool:
    """Checks request from client. Request is considered correct if it ends to
    \r\n\r\n. In this case True is returned, otherwise - False.
    """

    return request.endswith("\r\n\r\n")


def is_verb_correct(verb: str) -> bool:
    """Checks verb. If verb value contains "ОТДОВАЙ", "УДОЛИ" or "ЗОПИШИ",
    then True is returned, otherwise - False.
    """

    return any([verb == RequestVerb.GET, verb == RequestVerb.WRITE, verb == RequestVerb.DELETE])


def is_name_correct(name: str) -> bool:
    """Checks name. If name is less than or equal to 30 characters, then True
    is returned, otherwise - False.
    """
    
    return len(name) <= 30


def is_protocol_correct(protocol: str) -> bool:
    """Checks protocol. If protocol value contains "РКСОК/1.0" then True is
    returned, otherwise - False.
    """

    return protocol == PROTOCOL


def is_request_completed(request: str) -> Union[bool, str]:
    """Checks request from client for completeness of content. If request
    contains verb, name and protocol values, then these values are returned,
    otherwise - False will be returned.
    """

    request = request.splitlines()

    if request:
        command = request[0].split()

        if len(command) >= 3:
            verb = command[0]
            name = " ".join(command[1:-1])
            protocol = command[-1]
            content = "".join([content + "\r\n" for content in request[1:-1]])[:-2]

            if all([is_verb_correct(verb), is_name_correct(name), is_protocol_correct(protocol)]):
                return verb, name, content

    return False


async def get_validation_response(request: str) -> str:
    """Sends a request from client to validation server and receives a
    response with permission to process request.
    """

    reader, writer = await asyncio.open_connection(VALIDATION_SERVER_ADDRESS, VALIDATION_SERVER_PORT)

    writer.write(request.encode(ENCODING))
    await writer.drain()
    
    data = await reader.read(1024)
    answer = data.decode()
    
    writer.close()
    await writer.wait_closed()

    return answer
