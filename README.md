# Installation and Running - development:
### Creating a Python virtual environment
python -m venv .venv

### Activating the virtual environment on different operating systems
source .venv/bin/activate # Linux  
source .venv\bin\activate # Windows CMD  
.\venv\Scripts\activate.bat # Windows PowerShell  

### Installing required dependencies
pip install -r requirements.txt  

### Migrating the database
python manage.py makemigrations  
python manage.py migrate  

### Running the application
python manage.py runserver  

### Admin page URL
[localhost:8000/bym_admin](localhost:8000/bym_admin)

-------------------------------------------------------------------

# Instalacija i pokretanje - development:
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

### URL administratorske stranice
[localhost:8000/bym_admin](localhost:8000/bym_admin)
