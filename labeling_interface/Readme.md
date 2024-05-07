# Setup Labeling Interface

Make sure you install Docker & Docker Compose [Installation](https://docs.docker.com/compose/install/).

Navigate into your local labeling interface folder and execute the following commands:
> docker build -t dis18_arts .
> 
> docker compose up

Now you can attach with your IDE (we would recommend VS Code) to the container ([Attaching with VS Code](https://code.visualstudio.com/docs/devcontainers/attach-container)).

Run `streamlit run labeling_interface` to start your local instance of the labeling interface server.
