# api-reflector

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
