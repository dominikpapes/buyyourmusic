# Instalacija i pokretanje:
### Stvaranje Python virtualnog okruženja
python -m venv .venv

### Pokretanje virtualnog okruženja na različitim operacijskim sustavima
source .venv/bin/activate # Linux  
source .venv\bin\activate # Windows CMD  
.\venv\Scripts\activate.bat # Windows PowerShell  

### Instaliranje potrebnih ovisnosti
pip install -r requirements.txt  

### Migriranje baze podataka
python manage.py makemigrations  
python manage.py migrate  

### Pokretanje aplikacije
python manage.py runserver  
