"""
Generador Poético Cuántico

Un poeta cuántico-saussureano que genera versos a partir de
superposiciones de palabras y colapsos probabilísticos.
"""

import random
import copy
import numpy as np
from saussure_quantum import SignoCuanto, Langue
from saussure_quantum.collapse import colapso_parole, ContextoEnunciativo
from saussure_quantum.operators import operador_diferencia


class PoetaCuantico:
    """
    Poeta que escribe versos usando colapsos cuánticos.
    
    Cada palabra comienza en superposición y colapsa
    al ser "dicha" (escrita).
    """
    
    def __init__(self, nombre: str = "Quantum Poet"):
        self.nombre = nombre
        self.historial = []
        
        # Diccionario cuántico: cada entrada es un SignoCuanto
        self.diccionario = {
            "sustantivos": SignoCuanto(
                ["amor", "caos", "luz", "sombra", "infinito", "vacío"],
                [1, 1.2, 0.8, 0.9, 1.1, 0.7]
            ),
            "verbos": SignoCuanto(
                ["nace", "muere", "sueña", "vuela", "cae", "asciende"],
                [1, 0.9, 1.3, 0.8, 0.6, 1.1]
            ),
            "adjetivos": SignoCuanto(
                ["eterno", "fugaz", "profundo", "ligero", "oscuro", "brillante"],
                [1.2, 0.8, 0.7, 1.1, 0.9, 1.3]
            ),
            "conectores": SignoCuanto(
                ["y", "o", "pero", "cuando", "donde", "como"],
                [1.5, 0.5, 0.8, 1.2, 0.6, 0.9]
            )
        }
    
    def palabra_aleatoria(self, categoria: str, humor: float = 1.0) -> str:
        """
        Genera una palabra colapsando una categoría.

        Args:
            categoria: "sustantivos", "verbos", "adjetivos", "conectores"
            humor: Temperatura semántica (1.0 = normal, >1 = más caótico)
        """
        if categoria not in self.diccionario:
            return "?"

        # deepcopy para que cualquier mutación del SignoCuanto (ej. llamada directa
        # a .colapsar()) no corrompa el estado del diccionario compartido entre poemas.
        signo = copy.deepcopy(self.diccionario[categoria])
        contexto = ContextoEnunciativo(temperatura_semantica=humor)

        palabra, _, info = colapso_parole(signo, contexto)
        return palabra
    
    def generar_verso(self, estructura: list, humor: float = 1.0) -> str:
        """
        Genera un verso con una estructura dada.
        
        Args:
            estructura: Lista de categorías, ej: ["sustantivos", "verbos", "adjetivos"]
            humor: Temperatura semántica
        
        Returns:
            Verso generado
        """
        palabras = []
        for cat in estructura:
            palabra = self.palabra_aleatoria(cat, humor)
            palabras.append(palabra)
        
        verso = " ".join(palabras)
        verso = verso[0].upper() + verso[1:]  # Capitalizar
        self.historial.append(verso)
        return verso
    
    def generar_poema(self, num_versos: int = 4, humor_inicial: float = 1.0) -> str:
        """
        Genera un poema completo.
        
        El humor puede variar a lo largo del poema.
        """
        poema = []
        
        for i in range(num_versos):
            # Variación de humor (cada verso puede ser diferente)
            humor = humor_inicial * (0.8 + 0.4 * np.sin(i))
            
            # Estructuras alternativas para variedad
            estructuras = [
                ["sustantivos", "verbos", "adjetivos"],
                ["adjetivos", "sustantivos", "verbos"],
                ["verbos", "sustantivos"],
                ["conectores", "adjetivos", "sustantivos", "verbos"]
            ]
            
            estructura = random.choice(estructuras)
            verso = self.generar_verso(estructura, humor)
            poema.append(verso)
        
        return "\n".join(poema)
    
    def estado_poetico(self) -> dict:
        """
        Analiza el estado cuántico del poeta.
        
        Returns:
            Estadísticas de los poemas generados
        """
        if not self.historial:
            return {"poemas_generados": 0}
        
        # Frecuencia de palabras usadas
        palabras = []
        for verso in self.historial:
            palabras.extend(verso.lower().split())
        
        frecuencias = {}
        for p in palabras:
            frecuencias[p] = frecuencias.get(p, 0) + 1
        
        return {
            "poemas_generados": len(self.historial),
            "palabras_totales": len(palabras),
            "vocabulario_unico": len(frecuencias),
            "palabra_mas_usada": max(frecuencias, key=frecuencias.get) if frecuencias else None
        }


def ejemplo_principio_diferencia():
    """
    Ejemplo del principio de diferencia aplicado a poesía.
    """
    print("\n" + "="*60)
    print("PRINCIPIO DE DIFERENCIA EN POESÍA")
    print("="*60)
    
    # Una palabra aislada (sin contexto)
    palabra_aislada = SignoCuanto(["amor", "odio", "indiferencia"], [1, 0, 0])
    
    # La misma palabra en oposición con otras
    amor = SignoCuanto(["amor", "odio", "indiferencia"], [1, 0, 0])
    odio = SignoCuanto(["amor", "odio", "indiferencia"], [0, 1, 0])
    indiferencia = SignoCuanto(["amor", "odio", "indiferencia"], [0, 0, 1])
    
    diferencia = operador_diferencia([amor, odio, indiferencia])
    
    print("\n📖 Una palabra aislada (no tiene sentido):")
    print(amor)
    
    print("\n📖 La misma palabra en el sistema de diferencias:")
    print(diferencia)
    print("\n'El amor ES porque NO ES odio ni indiferencia'")
    print("   → Saussure demostrado cuánticamente")


def main():
    """Función principal de demostración"""
    
    print("="*60)
    print("🎭 BIENVENIDO AL POETA CUÁNTICO-SAUSSUREANO 🎭")
    print("="*60)
    
    # Demostración del principio de diferencia
    ejemplo_principio_diferencia()
    
    # Crear poeta
    poeta = PoetaCuantico("Neurona Cuántica")
    
    # Generar poemas con diferentes humores
    print("\n" + "="*60)
    print("POEMA 1: HUMOR NORMAL (ℏ = 1.0)")
    print("="*60)
    print(poeta.generar_poema(num_versos=4, humor_inicial=1.0))
    
    print("\n" + "="*60)
    print("POEMA 2: HUMOR ALTO (Caos semántico)")
    print("="*60)
    print(poeta.generar_poema(num_versos=4, humor_inicial=2.5))
    
    print("\n" + "="*60)
    print("ESTADÍSTICAS DEL POETA")
    print("="*60)
    stats = poeta.estado_poetico()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("✨ CONCEPTO FINAL ✨")
    print("="*60)
    print("Cada palabra nace de una superposición cuántica")
    print("y colapsa en el acto de ser dicha.")
    print("La poesía es la huella de esos colapsos.")
    print("\n   — Fusión Saussure × Quantum —")


if __name__ == "__main__":
    main()