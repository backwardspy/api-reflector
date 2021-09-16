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
$ flask run
```

All configuration is done via environment variables. If you are using
`poetry-dotenv-plugin` or another dotenv tool, you can use a `.env` file in the
project root to set configuration variables. `.env.example` is provided as an
example. If you use the example dotenv file, make sure you update `secret_key`.

## Azure auth

Azure authorization can be disabled by setting the env variable azure_auth_enabled to 0,
or re-enabled, by setting azure_auth_enabled to 1. 
If Azure authentication is enabled, three extra variables need to be provided in the env file:
```
azure_client_id
azure_client_secret
azure_tenant
```
Otherwise, the service will not run.

## Local Testing

If Azure auth is enabled, it is important to either export, or set
```
OAUTHLIB_INSECURE_TRANSPORT=1
```
in the .env file.
