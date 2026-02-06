### when init environment
- uv init blog
- uv venv
- source .venv/bin/activate
- uv add Django django-ckeditor djangorestframework uwsgi PyMySQL PyYAML django-haystack whoosh jieba
- uv pip freeze > requirements.txt
- django-admin startproject pb
- python manage.py startapp blog
- GRANT SELECT, INSERT, UPDATE, REFERENCES, DELETE, CREATE, DROP, ALTER, INDEX, TRIGGER, CREATE VIEW, SHOW VIEW, EXECUTE, ALTER ROUTINE, CREATE ROUTINE, CREATE TEMPORARY TABLES, LOCK TABLES, EVENT ON `db_name`.* TO 'user'@'localhost';
