# Todo Application Requirements

## 1. Purpose and Scope

The application is a lightweight Django task manager. Users can view, search, create, edit, complete, cancel, and delete Todo items. The web interface uses English text, a white-and-blue color palette, and a responsive layout with a left sidebar containing a single Todo List menu item.

## 2. Technology and Project Structure

- Backend: Python and Django.
- Database: Django's default SQLite database at `db.sqlite3`.
- Frontend: Django templates, Bootstrap 5.3.8 via CDN, and app styles in `todo/static/todo/css/main.css`.
- Project configuration and URL routing: `core/`.
- Todo application code, templates, static assets, and migrations: `todo/`.
- Shared layout: `todo/templates/base.html`; app pages extend this template.
- The repository has no dependency manifest. Django and other Python dependencies are not pinned in the source tree.

## 3. Data Requirements

Each Todo item must contain:

- `title`: required text, up to 200 characters.
- `description`: optional text.
- `status`: one of `Pending`, `Completed`, or `Cancelled`; new items default to `Pending`.
- `created_at`: automatically assigned when the item is created and excluded from editable form fields.

Items are ordered newest first. The creation date is displayed on create and edit forms as a read-only date. The timestamp is stored by Django with timezone support enabled; the project timezone is UTC.

## 4. Functional Requirements

1. **List and search:** The main route (`/`) displays the task list, status, creation date/time, and available actions. Users can search title and description with a case-insensitive text query and filter by an exact creation date. Both filters may be used together. Users can clear active filters.
2. **Create:** `/todos/create/` displays a dedicated form for title, description, and status. A successful submission creates the task and returns to the list with a confirmation message.
3. **Edit:** `/todos/<id>/edit/` displays a dedicated edit form. The creation timestamp cannot be changed. A successful update returns to the list with a confirmation message.
4. **Complete and cancel:** POST actions at `/todos/<id>/complete/` and `/todos/<id>/cancel/` update the task status and return to the list with a confirmation message.
5. **Delete:** `/todos/<id>/delete/` displays a dedicated confirmation page. The item is removed only after the user submits the confirmation form; the action then returns to the list with a confirmation message.
6. **Admin:** Django admin at `/admin/` provides Todo search by title and description, and filtering/display by status and creation time.

## 5. Interface and Accessibility

- All visible interface copy and document language must be English.
- Use the shared `base.html` layout for the list, create, edit, and delete-confirmation pages.
- The main page focuses on “Your Tasks” and provides a New Task link, search controls, an empty state, and task actions.
- The layout must remain usable on narrow screens; forms, navigation, and the task table should adapt to smaller viewports.
- Forms and state-changing actions must include Django CSRF tokens. Destructive deletion must require a separate confirmation page.

## 6. Routing and Request Rules

The list route accepts GET requests. Create, edit, and delete-confirmation views accept GET and POST. Complete and cancel actions accept POST only. Missing task IDs return Django's not-found response.

## 7. Configuration and Operational Constraints

Use Django migrations to create and update the SQLite schema. The current settings enable `DEBUG`, use a development secret key, and leave `ALLOWED_HOSTS` empty; these settings are for local development. A deployment must use a private production secret, disable debug mode, and configure allowed hosts. Main task pages currently do not require authentication; the admin uses Django's normal authentication.

## 8. Verification Notes

`todo/tests.py` currently contains only the Django `TestCase` import and placeholder comment. No automated feature coverage or coverage threshold is defined in the repository.
