# Setup Labeling Interface

The use of Docker is not required, but is recommended, as it gives you the same shared environment and makes it easier to work together.

If you do not want to use Docker, you can skip directly to the last step and start the rating interface via the console.

## Docker

Make sure you install Docker & Docker Compose ([Installation](https://docs.docker.com/compose/install/)).

Navigate into your local labeling interface folder and execute the following commands:
> docker build -t dis18_arts .
> 
> docker compose up

Now you can attach with your IDE (we would recommend VS Code) to the docker container ([Attaching with VS Code](https://code.visualstudio.com/docs/devcontainers/attach-container)).

## Rating interface

Run `streamlit run rating_interface.py` to start your local instance of the labeling interface server.
