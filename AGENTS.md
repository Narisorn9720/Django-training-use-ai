# Repository Guidelines

## Project Structure

This repository is a small Django project. `manage.py` is the command-line entry point. `core/` contains project settings, root URL routing, and ASGI/WSGI entry points. `todo/` is the application package, with models, views, admin registration, app configuration, and schema migrations under `todo/migrations/`. Add app-specific templates or static files within `todo/` as the project grows. Tests belong in `todo/tests.py` or in a `todo/tests/` package.

## Development Commands

Run commands from the repository root with Django installed in the active Python environment:

- `python manage.py runserver` starts the local development server.
- `python manage.py check` runs Django's project configuration checks.
- `python manage.py test` discovers and runs the Django test suite.
- `python manage.py makemigrations` creates migration files after model changes; review them before committing.
- `python manage.py migrate` applies migrations to the local SQLite database (`db.sqlite3`).

No dependency or packaging manifest is currently present; record any new runtime dependencies in a requirements file if one is introduced.

## Style and Naming

Use standard Python style with four-space indentation and clear, descriptive names. Follow Django conventions: model and class names use `CapWords`, functions and modules use `snake_case`, URL names are lowercase, and migrations are generated with `makemigrations` rather than named manually. Keep views focused and put database behavior in models or dedicated app logic where appropriate. No formatter or linter is configured currently.

## Testing

Use Django's built-in `TestCase` and place tests near the app code in `todo/tests.py` (or a `tests/` package for a larger suite). Name test files `test_*.py` and test methods `test_*`. Cover model behavior, URL responses, and view behavior; run `python manage.py test` before submitting changes. The current test module contains no substantive tests, and no coverage threshold is configured.

## Commits and Pull Requests

Git history is unavailable in this checkout, so no existing commit convention could be confirmed. Use short imperative commit subjects, for example `Add todo item model`. Pull requests should explain the change and validation performed, link any related issue, and include screenshots when changing user-facing pages.

## Security and Configuration

`core/settings.py` currently contains a development secret key and enables `DEBUG`. Keep local development settings out of production; load secrets from environment configuration and disable debug mode before deployment.
