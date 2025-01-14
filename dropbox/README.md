# Dropbox Quick Start Connector

This package is a utility for connecting Cohere to Dropbox, featuring a simple local development setup.

## Limitations

The Dropbox connector currently searches for all active files within your Dropbox instance. Note that new files added will require a couple minutes of indexing time to be searchable. Dropbox usually takes less than 5 minutes.

**Please note, currently, the contents of individual files is not decoded.**

## Configuration

To use the Dropbox connector, first create an app in the [Developer App Console](https://www.dropbox.com/developers/apps). Select Scoped Access, and give it the access type it needs. Note that `App folder` access will give your app access to a folder specifically created for your app, while `Full Dropbox` access will give your app access to all files and folders currently in your Dropbox instance.

Once you have created a Dropbox app, head over to the Permissions tab of your app and enable `files.metadata.read` and `files.content.read`. Then go to the Settings tab and retrieve your App key and App secret and place them into a `.env` file (see `.env-template` for reference):

```
DROPBOX_APP_KEY=xxxx
DROPBOX_APP_SECRET=xxxx
```

Optionally, you can configure the `DROPBOX_PATH` to modify the subdirectory to search in, or the `DROPBOX_SEARCH_LIMIT` to affect the max number of results returned.

## Authentication

#### Testing

To test the connection, you can generate a temporary access token from your App's settings page. Use this for the `DROPBOX_ACCESS_TOKEN` environ variable.

#### `DROPBOX_CONNECTOR_API_KEY`

The `DROPBOX_CONNECTOR_API_KEY` should contain an API key for the connector. This value must be present in the `Authorization` header for all requests to the connector.

#### OAuth

When using OAuth for authentication, the connector does not require any additional environment variables. Instead, the OAuth flow should occur outside of the Connector and Cohere's API will forward the user's access token to this connector through the `Authorization` header.

With OAuth the connector will be able to search any Dropbox folders and files that the user has access to.

To configure OAuth, follow the same steps in the Configuration section to create a Dropbox App. You will also need to register a redirect URI on that app to `https://api.cohere.com/v1/connectors/oauth/token`.

You can then register the connector with Cohere's API using the following configuration:
Note: Your App key and App secret values correspond to `client_id` and `client_secret` respectively.

```bash
curl  -X POST \
  'https://api.cohere.ai/v1/connectors' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {COHERE-API-KEY}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "name": "Dropbox with OAuth",
  "url": "{YOUR_CONNECTOR-URL}",
  "oauth": {
    "client_id": "{DROPBOX-OAUTH-CLIENT-ID}",
    "client_secret": "{DROPBOX-OAUTH-CLIENT-SECRET}",
    "authorize_url": "https://www.dropbox.com/oauth2/authorize",
    "token_url": "https://www.dropbox.com/oauth2/token"
  }
}'
```

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  poetry config virtualenvs.in-project true
  poetry install --no-root
```

To run the Flask server in development mode, please run:

```bash
  poetry run flask --app provider --debug run
```

The Flask API will be bound to :code:`localhost:5000`.

```bash
  curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "charcoal"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
