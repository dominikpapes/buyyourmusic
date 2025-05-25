Instalacija i pokretanje:
# stvaranje Python virtualnog okruženja
python -m venv .venv

# pokretanje virtualnog okruženja na različitim operacijskim sustavima
source .venv/bin/activate # Linux
source .venv\bin\activate # Windows CMD
.\venv\Scripts\activate.bat # Windows PowerShell

# instaliranje potrebnih ovisnosti
pip install -r requirements.txt

# migriranje baze podataka
python manage.py makemigrations
python manage.py migrate

# pokretanje aplikacije
python manage.py runserver
