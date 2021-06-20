import asyncio

from loguru import logger

from config import RKSOK_SERVER_ADDRESS, RKSOK_SERVER_PORT
from files import get_data, remove_data, write_data
from responses import create_response, send_response
from specs import RequestVerb, ResponseStatus, ValidationStatus
from utils import get_validation_response, is_request_completed, is_request_ends_correctly


async def run_rksok_server() -> None:
    """Runs async RKSOK server."""

    server = await asyncio.start_server(process_request_body, RKSOK_SERVER_ADDRESS, RKSOK_SERVER_PORT)

    async with server:
        await server.serve_forever()


async def process_request_body(reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter) -> None:
    """Processes request body from client. Request is checked for presence of
    characters \r\n\r\n at end of line and for completeness of content. If
    check fails, a response about an incorrect request is returned. If
    successful - request is checked on validation server. If validation server
    does not allow processing request, then client will receive a response
    from this server. If it does - request is processed."""

    data = await reader.read(1024)
    request_from_client = data.decode()
    logger.info(f"Get request from client: {request_from_client!r}")

    if is_request_ends_correctly(request_from_client):
        result_of_checking_request = is_request_completed(request_from_client)

        if result_of_checking_request:
            verb, name, content = result_of_checking_request
            validation_result = await get_validation_result(verb=verb, name=name, content=content)
            response_to_client = await process_allowed_request(
                validation_result=validation_result, verb=verb, name=name, content=content)
        else:
            response_to_client = create_response(verb=ResponseStatus.INCORRECT)
    else:
        response_to_client = create_response(verb=ResponseStatus.INCORRECT)

    await send_response(writer, response_to_client)
    logger.info(f"Response to client: {response_to_client!r}")


async def get_validation_result(verb: str, name: str, content: str) -> str:
    """Checks request received from client on validation server and returns a response."""
                
    response_for_validation = create_response(verb=verb, name=name, content=content, check_verb=ValidationStatus.CHECK)
    logger.info(f"Response for validation: {response_for_validation!r}")
    
    validation_result = await get_validation_response(response_for_validation)
    logger.info(f"Validation result: {validation_result!r}")

    return validation_result


async def process_allowed_request(validation_result: str, verb: str, name: str, content: str) -> str:
    """Processes an allowed client request and returns a response."""

    if validation_result.split()[0] == ValidationStatus.ACCEPT:
        if verb == RequestVerb.GET:
            content = await get_data(name)

            if content:
                response_to_client = create_response(verb=ResponseStatus.OK, content=content)
            else:
                response_to_client = create_response(verb=ResponseStatus.NOT_FOUND)
        elif verb == RequestVerb.WRITE:
            await write_data(name, content)
            response_to_client = create_response(verb=ResponseStatus.OK)
        elif verb == RequestVerb.DELETE:
            result = await remove_data(name=name)

            if result:
                response_to_client = create_response(verb=ResponseStatus.OK)
            else:
                response_to_client = create_response(verb=ResponseStatus.NOT_FOUND)
    elif validation_result.split()[0] == ValidationStatus.REJECT:
        response_to_client = validation_result

    return response_to_client


if __name__ == "__main__":
    asyncio.run(run_rksok_server()) # Запуск асинхронного РКСОК сервера
