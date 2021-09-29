# api-reflector

![CI](https://github.com/backwardspy/api-reflector/actions/workflows/main.yml/badge.svg)

A configurable API mocking service.

## Development

api-reflector uses [poetry](https://python-poetry.org) for dependency
management.

It is recommended that you use poetry 1.2+ along with
[poetry-dotenv-plugin](https://github.com/mpeteuil/poetry-dotenv-plugin) for
easier project configuration.

```shell
$ poetry install
$ poetry shell
$ api-reflector-migrate
$ flask run
```

All configuration is done via environment variables. If you are using
`poetry-dotenv-plugin` or another dotenv tool, you can use a `.env` file in the
project root to set configuration variables. `.env.example` is provided as an
example. If you use the example dotenv file, make sure you update `secret_key`.

## Azure auth

Azure SSO can be enabled by setting azure_auth_enabled to `true` in your environment.
If Azure SSO is enabled, three extra environment variables need to be provided:

```
azure_client_id
azure_client_secret
azure_tenant
```

Additionally, the `external_url` setting should be used to control the redirect back from the auth flow.

## Local Testing

By default, insecure redirect URLS will be rejected.
If you want to test locally, set OAUTHLIB_INSECURE_TRANSPORT=true in your environment.
