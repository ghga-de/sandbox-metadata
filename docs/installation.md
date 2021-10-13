# Setup and Installation

## Setting up the dev environment

A `Dockerfile` (and `docker-compose.yaml`) for a container corresponding to a development environment has been configured and made available in the `.devcontainer` folder.

You can use the configurations in `.devcontainer` to run VS Code in a Docker container via the [Remote Container extension for VS Code](https://code.visualstudio.com/docs/remote/containers-tutorial).

Alternatively, you can also run the container directly from your command line as follows:

```sh
# build the image first
docker build -t sandbox-metadata:dev -f .devcontainer/Dockerfile .

# run the container
docker run --rm -it -u vscode -v "${PWD}:/workspace" sandbox-metadata:dev bash
```


## Running the application

You can run the application in two ways,

```sh
metadata-service
```

or,

```sh
uvicorn metadata_service.main:app --reload
```

You can visit the API by navigating to [http://localhost:8000/docs]()


## Bootstrapping the metadata store

The metadata-store is a MongoDB instance that holds GHGA metadata records.

Each type of metadata record (Dataset, Study, etc.) is stored as a separate collection in the metadata-store.

To pre-load metadata records into a fresh instance of MongoDB:

```sh
# load GHGA metadata records
python scripts/populate_metadata_store.py --base-url http://localhost:8000 --directory examples

# load GHGA metadata records translated from EGA
python scripts/populate_metadata_store.py --base-url http://localhost:8000 --directory ega-examples/transformed
```
