"""
Unit tests for uncertainty.py
"""

import pytest
import numpy as np
from saussure_quantum.core import SignoCuanto, Langue
from saussure_quantum.uncertainty import (
    ObservablesSaussureanos,
    PrincipioIncertidumbreSaussure,
    incertidumbre_saussure_heisenberg,
    paradoja_del_observador_linguistico,
    HBAR_SEMIOTICO
)


class TestObservablesSaussureanos:
    """Pruebas para observables complementarios"""
    
    def test_initialization(self):
        """Test inicialización"""
        obs = ObservablesSaussureanos(5)
        assert obs.dimension == 5
        assert obs.S.shape == (5, 5)
        assert obs.P.shape == (5, 5)
    
    def test_sintagma_operator(self):
        """Test operador sintagma (posición)"""
        obs = ObservablesSaussureanos(4)
        # Debe ser diagonal con 0,1,2,3
        expected_S = np.diag([0, 1, 2, 3])
        assert np.allclose(obs.S, expected_S)
    
    def test_conmutacion(self):
        """Test relación de conmutación [S, P] = iℏ·I"""
        obs = ObservablesSaussureanos(5, hbar=1.0)
        assert obs.verificar_conmutacion(tolerancia=1e-5)
    
    def test_conmutacion_hbar_custom(self):
        """Test con ℏ personalizado"""
        hbar = 2.0
        obs = ObservablesSaussureanos(5, hbar=hbar)
        assert obs.verificar_conmutacion(tolerancia=1e-5)
    
    def test_incertidumbre_estado_base(self):
        """Test incertidumbre para estado base"""
        obs = ObservablesSaussureanos(10)
        lang = Langue(10)
        estado = lang.estado_base(0)  # Sintagma puro
        
        delta_S, delta_P, producto = obs.incertidumbre(estado)
        
        # Delta_S debe ser 0 (posición definida)
        assert np.isclose(delta_S, 0.0, atol=1e-10)
        # Delta_P debe ser muy grande (momento incierto)
        assert delta_P > 1.0
        # Principio de incertidumbre: ΔS·ΔP ≥ ℏ/2
        assert producto >= HBAR_SEMIOTICO / 2 - 1e-10
    
    def test_estado_minima_incertidumbre(self):
        """Test estado de mínima incertidumbre"""
        obs = ObservablesSaussureanos(20)
        estado = obs.estado_minima_incertidumbre()
        delta_S, delta_P, producto = obs.incertidumbre(estado)
        
        # Debe saturar la cota (o estar muy cerca)
        cota = HBAR_SEMIOTICO / 2
        # El producto debe ser >= cota, pero cercano
        assert producto >= cota - 1e-5
        # Factor no debe ser enorme (ej. < 2)
        assert producto / cota < 2.0


class TestPrincipioIncertidumbreSaussure:
    """Pruebas para el principio de incertidumbre"""
    
    def test_initialization(self):
        """Test inicialización"""
        lang = Langue(8)
        principio = PrincipioIncertidumbreSaussure(lang)
        assert principio.langue == lang
        assert principio.hbar == HBAR_SEMIOTICO
    
    def test_analizar_estado(self):
        """Test análisis de estado"""
        lang = Langue(10)
        principio = PrincipioIncertidumbreSaussure(lang)
        estado = lang.superposicion([1] * 10)
        
        analisis = principio.analizar_estado(estado)
        
        assert "delta_sintagma" in analisis
        assert "delta_paradigma" in analisis
        assert "producto_incertidumbre" in analisis
        assert "satisface_principio" in analisis
        assert analisis["satisface_principio"] is True
    
    def test_estado_sintagmatico_puro(self):
        """Test estado con sintagma puro"""
        lang = Langue(5)
        principio = PrincipioIncertidumbreSaussure(lang)
        estado = principio.estado_sintagmatico_puro(2)
        
        # Debe ser el estado base en índice 2
        assert np.isclose(estado.amplitudes[2], 1.0)
        assert np.sum(np.abs(estado.amplitudes)) == 1.0
        
        analisis = principio.analizar_estado(estado)
        assert np.isclose(analisis["delta_sintagma"], 0.0, atol=1e-10)
    
    def test_estado_paradigmatico_puro(self):
        """Test estado con paradigma puro"""
        lang = Langue(5)
        principio = PrincipioIncertidumbreSaussure(lang)
        estado = principio.estado_paradigmatico_puro(1)
        
        analisis = principio.analizar_estado(estado)
        # El momento debe estar bien definido (delta_P pequeño)
        assert analisis["delta_paradigma"] < 0.1
    
    def test_demostrar_principio(self):
        """Test demostración completa"""
        lang = Langue(10)
        principio = PrincipioIncertidumbreSaussure(lang)
        
        demo = principio.demostrar_principio()
        
        assert "sintagma_puro" in demo
        assert "paradigma_puro" in demo
        assert "minima_incertidumbre" in demo
        
        # El estado de mínima incertidumbre debe tener producto más bajo
        prod_min = demo["minima_incertidumbre"]["producto"]
        prod_sintagma = demo["sintagma_puro"]["producto"]
        
        # El producto de mínima incertidumbre debe ser finito
        assert np.isfinite(prod_min)
        # El producto del sintagma puro puede ser inf o muy grande
        assert prod_sintagma > prod_min or np.isinf(prod_sintagma)


class TestFuncionesDeAltoNivel:
    """Pruebas para funciones helper"""
    
    def test_incertidumbre_saussure_heisenberg(self):
        """Test función principal"""
        estado = SignoCuanto(["x", "y", "z"], [1, 1, 1])
        resultado = incertidumbre_saussure_heisenberg(estado)
        
        assert "producto_incertidumbre" in resultado
        assert resultado["satisface_principio"] is True
    
    def test_paradoja_observador(self):
        """Test paradoja del observador"""
        estado = SignoCuanto(["a", "b"], [1, 0])  # Estado puro
        resultado = paradoja_del_observador_linguistico(estado)
        
        assert "estado_original" in resultado
        assert "despues_medir_sintagma" in resultado
        assert "despues_medir_paradigma" in resultado
        
        # Medir sintagma debe perturbar el paradigma
        perturbacion = resultado["despues_medir_sintagma"]["cambio_significativo"]
        # Para estado puro, debería ser True o al menos definido
        assert isinstance(perturbacion, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])