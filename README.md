# Secure Event System

A Django-based event management application with secure user authentication, profile editing, image upload, event CRUD, and admin audit logging.

## Features

- User signup, login, and logout
- User profile editing with profile image upload
- Create, view, edit, and delete events
- Event detail page for each event
- Admin audit log view for staff users
- Secure event ownership checks so users only see and modify their own events

## Requirements

- Python 3.14+
- Django 6.0.5
- Pillow

## Setup

1. Clone the repository:

```bash
git clone https://github.com/<USER>/<REPO>.git
cd secure_event_system
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create environment variables:

Create a `.env` file in the project root and add:

```text
SECRET_KEY=your_secret_key_here
DEBUG=True
```

5. Run database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

7. Start the development server:

```bash
python manage.py runserver
```

## Usage

- Visit `http://127.0.0.1:8000/`
- Sign up or log in
- Manage your profile and upload a profile picture
- Create, view, edit, and delete events
- Admin users can access the audit log page

## Notes

- Media uploads are served in development via `MEDIA_URL` and `MEDIA_ROOT`
- Do not commit `db.sqlite3`, `venv/`, or `.env` to source control
- If you add a profile image, it will be saved under the `media/profile_images/` folder

## License

This project is provided as-is for learning and development purposes.