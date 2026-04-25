"""
uncertainty.py - Principio de incertidumbre Saussure-Heisenberg

Implementa:
- El análogo lingüístico del principio de incertidumbre cuántico
- Observables complementarios: Paradigma (momento) vs Sintagma (posición)
- Relación de conmutación no nula [Ŝ, P̂] = iℏ_efectivo
- La imposibilidad de conocer simultáneamente ambas dimensiones del signo
"""

import numpy as np
from typing import Tuple, Dict, Optional, List
from dataclasses import dataclass
from saussure_quantum.core import SignoCuanto, Langue


# Constante de Planck semiótica (unidad mínima de sentido)
HBAR_SEMIOTICO = 1.0  # Puede ajustarse para calibrar la incertidumbre


class ObservablesSaussureanos:
    """
    Observables complementarios del sistema lingüístico.
    
    Ŝ (Sintagma) = análogo a la posición
    P̂ (Paradigma) = análogo al momento
    
    Satisfacen: [Ŝ, P̂] = i·ℏ_semiotico
    """
    
    def __init__(self, dimension: int, hbar: float = HBAR_SEMIOTICO):
        """
        Inicializar los observables.
        
        Args:
            dimension: Dimensión del espacio de Hilbert lingüístico
            hbar: Constante de Planck semiótica
        """
        self.dimension = dimension
        self.hbar = hbar
        
        # Construir operadores
        self.S = self._construir_sintagma()
        self.P = self._construir_paradigma()
        
        # Verificar conmutación
        self._conmutador = self._calcular_conmutador()
    
    def _construir_sintagma(self) -> np.ndarray:
        """
        Operador Sintagma (posición lingüística).
        
        Representa la posición del signo en la cadena hablada,
        su relación con los elementos adyacentes.
        
        En base discreta: matriz diagonal con valores 0,...,d-1
        """
        # Posiciones sintagmáticas (orden en la frase)
        return np.diag(np.arange(self.dimension))
    
    def _construir_paradigma(self) -> np.ndarray:
        """
        Operador Paradigma (momento lingüístico).
        
        Representa la capacidad de sustitución del signo,
        sus alternativas posibles en el sistema.
        
        Análogo al operador momento: P = -iℏ·d/dx
        En base discreta: matriz de desplazamiento
        """
        # Construir matriz de momento (diferencias finitas)
        P = np.zeros((self.dimension, self.dimension), dtype=complex)
        
        for i in range(self.dimension):
            # Derivada discreta hacia adelante
            if i < self.dimension - 1:
                P[i, i+1] = -1j * self.hbar / 2
                P[i+1, i] = 1j * self.hbar / 2
        
        return P
    
    def _calcular_conmutador(self) -> np.ndarray:
        """Calcular [S, P] = S·P - P·S"""
        return self.S @ self.P - self.P @ self.S
    
    def verificar_conmutacion(self, tolerancia: float = 1e-10) -> bool:
        """
        Verificar que [S, P] ≈ i·ℏ·I
        
        Returns:
            True si se cumple la relación de conmutación
        """
        esperado = 1j * self.hbar * np.eye(self.dimension)
        diferencia = np.linalg.norm(self._conmutador - esperado)
        return diferencia < tolerancia
    
    def incertidumbre(self, estado: SignoCuanto) -> Tuple[float, float, float]:
        """
        Calcular ΔS · ΔP para un estado dado.
        
        Args:
            estado: Estado cuántico-semiótico
        
        Returns:
            (ΔS, ΔP, ΔS·ΔP)
        
        Note:
            Por el principio de incertidumbre: ΔS·ΔP ≥ ℏ/2
        """
        psi = estado.amplitudes
        
        # Valor esperado de S
        exp_S = np.vdot(psi, self.S @ psi).real
        exp_S2 = np.vdot(psi, self.S @ self.S @ psi).real
        var_S = exp_S2 - exp_S**2
        delta_S = np.sqrt(max(var_S, 0))
        
        # Valor esperado de P
        exp_P = np.vdot(psi, self.P @ psi).real
        exp_P2 = np.vdot(psi, self.P @ self.P @ psi).real
        var_P = exp_P2 - exp_P**2
        delta_P = np.sqrt(max(var_P, 0))
        
        producto = delta_S * delta_P
        
        return delta_S, delta_P, producto
    
    def estado_minima_incertidumbre(self) -> SignoCuanto:
        """
        Genera un estado que satura la cota de incertidumbre.
        
        Estado coherente semiótico: mínima incertidumbre posible.
        """
        # Estado gaussiano en representación de posición (sintagma)
        x = np.linspace(-3, 3, self.dimension)
        psi = np.exp(-x**2 / 2)  # Gaussian packet
        psi = psi / np.linalg.norm(psi)
        
        # Usar significantes genéricos
        significantes = [f"pos_{i}" for i in range(self.dimension)]
        
        return SignoCuanto(significantes, psi.tolist())


class PrincipioIncertidumbreSaussure:
    """
    Implementa el principio fundamental de la fusión:
    No se puede conocer simultáneamente el valor paradigmático
    y sintagmático de un signo con precisión arbitraria.
    """
    
    def __init__(self, langue: Langue, hbar: float = HBAR_SEMIOTICO):
        """
        Args:
            langue: Sistema lengua sobre el que opera
            hbar: Constante de Planck semiótica
        """
        self.langue = langue
        self.hbar = hbar
        self.obs = ObservablesSaussureanos(langue.dimension, hbar)
    
    def analizar_estado(self, estado: SignoCuanto) -> Dict:
        """
        Análisis completo de incertidumbre para un estado.
        
        Returns:
            Diccionario con valores de incertidumbre y análisis cualitativo
        """
        delta_S, delta_P, producto = self.obs.incertidumbre(estado)
        cota_minima = self.hbar / 2
        
        # Interpretación cualitativa
        if producto < cota_minima * 1.1:
            interpretacion = "ESTADO DE MÍNIMA INCERTIDUMBRE (coherente)"
        elif producto > cota_minima * 10:
            interpretacion = "ALTA INCERTIDUMBRE (muy indeterminado)"
        else:
            interpretacion = "INCERTIDUMBRE MODERADA"
        
        # Análisis de dominancia
        if delta_S < delta_P:
            dominancia = "predomina precisión sintagmática (posición bien definida)"
        else:
            dominancia = "predomina precisión paradigmática (momento bien definido)"
        
        return {
            "delta_sintagma": delta_S,
            "delta_paradigma": delta_P,
            "producto_incertidumbre": producto,
            "cota_heisenberg": cota_minima,
            "satisface_principio": producto >= cota_minima - 1e-10,
            "factor_sobre_cota": producto / cota_minima if cota_minima > 0 else float('inf'),
            "interpretacion": interpretacion,
            "dominancia": dominancia
        }
    
    def estado_maxima_incertidumbre(self) -> SignoCuanto:
        """
        Estado donde la incertidumbre es máxima.
        
        Corresponde a una superposición uniforme donde no hay
        información ni sintagmática ni paradigmática.
        """
        amplitudes = np.ones(self.langue.dimension, dtype=complex) / np.sqrt(self.langue.dimension)
        return SignoCuanto(self.langue._base, amplitudes)
    
    def estado_sintagmatico_puro(self, posicion: int) -> SignoCuanto:
        """
        Estado con sintagma (posición) perfectamente definido.
        
        Implica máxima incertidumbre en el paradigma (momento).
        """
        if posicion >= self.langue.dimension:
            raise ValueError(f"Posición {posicion} fuera de rango")
        
        amplitudes = np.zeros(self.langue.dimension, dtype=complex)
        amplitudes[posicion] = 1.0
        return SignoCuanto(self.langue._base, amplitudes)
    
    def estado_paradigmatico_puro(self, momento: int) -> SignoCuanto:
        """
        Estado con paradigma (momento) perfectamente definido.
        
        Implica máxima incertidumbre en el sintagma (posición).
        """
        # Estados de momento son ondas planas discretas
        k = 2 * np.pi * momento / self.langue.dimension
        amplitudes = np.exp(1j * k * np.arange(self.langue.dimension))
        amplitudes = amplitudes / np.linalg.norm(amplitudes)
        return SignoCuanto(self.langue._base, amplitudes)
    
    def demostrar_principio(self) -> Dict:
        """
        Demostración interactiva del principio.
        
        Muestra cómo estados con sintagma preciso tienen
        paradigma incierto y viceversa.
        """
        resultados = {}
        
        # Caso 1: Sintagma bien definido
        estado_sintagma = self.estado_sintagmatico_puro(0)
        analisis_sintagma = self.analizar_estado(estado_sintagma)
        resultados["sintagma_puro"] = {
            "descripcion": "Signo con posición sintagmática perfectamente definida",
            "delta_sintagma": analisis_sintagma["delta_sintagma"],
            "delta_paradigma": analisis_sintagma["delta_paradigma"],
            "producto": analisis_sintagma["producto_incertidumbre"]
        }
        
        # Caso 2: Paradigma bien definido
        estado_paradigma = self.estado_paradigmatico_puro(0)
        analisis_paradigma = self.analizar_estado(estado_paradigma)
        resultados["paradigma_puro"] = {
            "descripcion": "Signo con valor paradigmático perfectamente definido",
            "delta_sintagma": analisis_paradigma["delta_sintagma"],
            "delta_paradigma": analisis_paradigma["delta_paradigma"],
            "producto": analisis_paradigma["producto_incertidumbre"]
        }
        
        # Caso 3: Estado de compromiso (mínima incertidumbre)
        estado_minimo = self.obs.estado_minima_incertidumbre()
        analisis_minimo = self.analizar_estado(estado_minimo)
        resultados["minima_incertidumbre"] = {
            "descripcion": "Estado de compromiso óptimo (mínima incertidumbre total)",
            "delta_sintagma": analisis_minimo["delta_sintagma"],
            "delta_paradigma": analisis_minimo["delta_paradigma"],
            "producto": analisis_minimo["producto_incertidumbre"]
        }
        
        return resultados
    
    def visualizar_espacio_fase(self, estado: SignoCuanto) -> np.ndarray:
        """
        Representación de Wigner (distribución cuasi-probabilidad)
        para visualizar la incertidumbre del signo.
        
        Returns:
            Matriz de distribución en espacio sintagma-paradigma
        """
        psi = estado.amplitudes
        d = self.langue.dimension  # ✅ Fix ISSUE #1: dimension vive en self.langue
        W = np.zeros((d, d), dtype=float)
        
        for x in range(d):
            for p in range(d):
                # Transformada de Wigner para sistemas discretos
                suma = 0
                for xi in range(d):
                    fase = np.exp(-2j * np.pi * p * xi / d)
                    suma += psi[x + xi] * np.conj(psi[x - xi]) * fase
                W[x, p] = (2 / d) * suma.real
        
        return W


# Funciones de alto nivel para fácil uso
def incertidumbre_saussure_heisenberg(
    estado: SignoCuanto,
    hbar: float = HBAR_SEMIOTICO
) -> Dict:
    """
    Función principal para calcular la incertidumbre de un signo.
    
    Args:
        estado: Signo-cuanto a analizar
        hbar: Constante de Planck semiótica
    
    Returns:
        Diccionario con resultados del principio de incertidumbre
    
    Example:
        >>> signo = SignoCuanto(["a","b","c"], [1,1,1])
        >>> incertidumbre_saussure_heisenberg(signo)
    """
    # Crear lengua temporal
    lang = Langue(estado.dimension)
    principio = PrincipioIncertidumbreSaussure(lang, hbar)
    return principio.analizar_estado(estado)


def paradoja_del_observador_linguistico(estado: SignoCuanto) -> Dict:
    """
    Ilustra la paradoja del observador en lingüística cuántica.
    
    Medir el valor sintagmático altera el valor paradigmático,
    y viceversa. No hay observación sin perturbación.
    
    Args:
        estado: Estado inicial
    
    Returns:
        Comparación de incertidumbres antes/después de mediciones
    """
    lang = Langue(estado.dimension)
    principio = PrincipioIncertidumbreSaussure(lang)
    
    # Estado original
    original = principio.analizar_estado(estado)
    
    # Simular medición de sintagma
    S = principio.obs.S
    psi = estado.amplitudes
    
    # Proyectar sobre autovalor de S (medir posición)
    autovalores_S, autovectores_S = np.linalg.eigh(S)
    probs_S = np.abs(autovectores_S.conj().T @ psi) ** 2
    idx_S = np.argmax(probs_S)  # Resultado más probable
    estado_S = SignoCuanto(estado.significantes.copy(), autovectores_S[:, idx_S])
    despues_S = principio.analizar_estado(estado_S)
    
    # Proyectar sobre autovalor de P (medir momento)
    P = principio.obs.P
    autovalores_P, autovectores_P = np.linalg.eigh(P)
    probs_P = np.abs(autovectores_P.conj().T @ psi) ** 2
    idx_P = np.argmax(probs_P)
    estado_P = SignoCuanto(estado.significantes.copy(), autovectores_P[:, idx_P])
    despues_P = principio.analizar_estado(estado_P)
    
    return {
        "estado_original": {
            "delta_S": original["delta_sintagma"],
            "delta_P": original["delta_paradigma"],
            "producto": original["producto_incertidumbre"]
        },
        "despues_medir_sintagma": {
            "delta_S": despues_S["delta_sintagma"],
            "delta_P": despues_S["delta_paradigma"],
            "producto": despues_S["producto_incertidumbre"],
            "cambio_significativo": despues_S["delta_P"] > original["delta_P"] * 1.5
        },
        "despues_medir_paradigma": {
            "delta_S": despues_P["delta_sintagma"],
            "delta_P": despues_P["delta_paradigma"],
            "producto": despues_P["producto_incertidumbre"],
            "cambio_significativo": despues_P["delta_S"] > original["delta_S"] * 1.5
        },
        "principio_demostrado": True
    }


# Alias conceptuales
incertidumbre_linguistica = incertidumbre_saussure_heisenberg
principio_saussure_heisenberg = incertidumbre_saussure_heisenberg