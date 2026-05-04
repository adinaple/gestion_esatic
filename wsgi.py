import sys
import os
 
# Remplace 'tonusername' par ton vrai nom d'utilisateur PythonAnywhere
path = '/home/tonusername/Gestion_esatic'
if path not in sys.path:
    sys.path.insert(0, path)
 
from app import app as application
 