# Elasticsearch Quick Start Connector

This project allows you to create a simple connection to Elasticsearch that can be used with Cohere's API.

## Limitations

Currently this connector will perform full-text search, but only for a single index of your Elasticsearch cluster. Since Elasticsearch is essentially a key-value store, it will return the full document as-is to Cohere.

## Configuration

You will need to configure this connector with the credentials and path necessary to connect to your Elasticsearch instance.
This connector is currently only configured to search a single index of your ES cluster, you will need to point to it by specifying your `ELASTIC_CLOUD_ID`, `ELASTIC_URL`, and `ELASTIC_INDEX`.

Then, to authorize your connection you will either require an `ELASTIC_API_KEY` _or_ both `ELASTIC_USER` and `ELASTIC_PASS`.

## Development

(Optional) For local development, you can start Elasticsearch and fill it with data by running:

```bash
  $ docker-compose run data-loader
```

After running the command, your Elasticsearch instance will run in the background on the default localhost:9200. To start it again later, you can
run:

```bash
  $ docker-compose up
```

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Then start the server

```bash
  $ poetry run flask --app provider --debug run
```

Check with curl to see that everything is working

```bash
  $ curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "Weber charcoal"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
