# RKSOK server

### About:
A new generation of data transfer protocol that will revolutionize the world and allow humanity to step into a new era.
Welcome to the future!

### Install:
1. At root of the project create virtual environment: `python -m venv env`
2. Activate virtual environment: `. env/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Create config.py file.
5. Run RKSOK server: `python server.py <server> <port>`

### Project structure:
* config.py: contains constants for various settings:
    * DEFAULT_RKSOK_SERVER_ADDRESS = "server_address"
    * DEFAULT_RKSOK_SERVER_PORT = server_port
    * VALIDATION_SERVER_ADDRESS = "validation_server_address"
    * VALIDATION_SERVER_PORT = validation_server_port
    * ENCODING = "UTF-8"
    * PROTOCOL = "РКСОК/1.0"
* files.py: contains functions for working with phonebook files.
* responses.py: contains functions for working with responses to client.
* server.py: contains functions for receiving and processing a request from a client.
* specs.py: the specification contains a description of request verbs and response statuses in RKSOK.
* utils.py: contains functions for checking requests and their content.