import sys
from typing import Union, Tuple

from config import DEFAULT_RKSOK_SERVER_ADDRESS, DEFAULT_RKSOK_SERVER_PORT, PROTOCOL
from specs import RequestVerb


def get_server_address_and_port() -> Tuple[str, int]:
    """Returns server address and port from command-line arguments."""

    try:
        return sys.argv[1], int(sys.argv[2])
    except (IndexError, ValueError):
        return DEFAULT_RKSOK_SERVER_ADDRESS, DEFAULT_RKSOK_SERVER_PORT


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


def is_request_completed(request: str) -> Union[Tuple[str, str, str], bool]:
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
