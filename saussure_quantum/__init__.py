"""
Saussure-Quantum Fusion Package
================================

Implementación computacional de la fusión entre semiótica saussureana 
y mecánica cuántica.

Módulos principales:
- core: Clases base (SignoCuanto, Langue)
- operators: Operadores cuántico-semióticos
- collapse: Mecanismos de medición/parole
- uncertainty: Principio de incertidumbre
"""

# Versión del paquete
__version__ = "0.1.0"

# Importar clases principales para acceso directo
from saussure_quantum.core import SignoCuanto, Langue
from saussure_quantum.operators import operador_diferencia
from saussure_quantum.collapse import colapso_parole
from saussure_quantum.uncertainty import incertidumbre_saussure_heisenberg

# Definir qué se importa con "from package import *"
__all__ = [
    "SignoCuanto",
    "Langue", 
    "operador_diferencia",
    "colapso_parole",
    "incertidumbre_saussure_heisenberg",
]