python -m venv .venv

source .venv/bin/activate # Linux

source .venv\bin\activate # Windows CMD

.\venv\Scripts\activate.bat # Windows PowerShell

pip install -r requirements.txt
python manage.py runserver
