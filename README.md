# CodeAlpha E-Commerce Store

This repository contains the CodeAlpha E-Commerce Django project nested in the
`CodeAlpha_E-Commerce Store/` folder.

Quickstart
```bash
git clone https://github.com/eMMANUEL849/codealpha_tasks.git
cd codealpha_tasks/CodeAlpha_E-Commerce\ Store
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Project structure (important paths)
- `CodeAlpha_E-Commerce Store/`
  - `products/` — product images and assets
  - `store/` — Django app
  - `storeproject/` — Django project settings
  - `manage.py`, `requirements.txt`

Notes
- `venv/` and `db.sqlite3` are ignored via `.gitignore`.
- If you want the project at repository root instead of the nested folder, let me know.
