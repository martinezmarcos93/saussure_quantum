"""
Unit tests for core.py
"""

import pytest
import numpy as np
from saussure_quantum.core import SignoCuanto, Langue


class TestSignoCuanto:
    """Pruebas para la clase SignoCuanto"""
    
    def test_initialization(self):
        """Test inicialización básica"""
        s = SignoCuanto(["a", "b", "c"], [1, 1, 1])
        assert s.dimension == 3
        assert len(s.significantes) == 3
        assert np.isclose(np.linalg.norm(s.amplitudes), 1.0)
    
    def test_initialization_uniform(self):
        """Test inicialización uniforme (sin amplitudes)"""
        s = SignoCuanto(["x", "y"])
        assert np.isclose(s.amplitudes[0], 1/np.sqrt(2))
        assert np.isclose(s.amplitudes[1], 1/np.sqrt(2))
    
    def test_normalization(self):
        """Test normalización automática"""
        s = SignoCuanto(["a", "b"], [3, 4])  # Norma = 5
        expected = np.array([3/5, 4/5])
        assert np.allclose(s.amplitudes, expected)
    
    def test_probability_by_string(self):
        """Test cálculo de probabilidad por nombre"""
        s = SignoCuanto(["gato", "perro"], [1, 0])
        assert s.probabilidad("gato") == 1.0
        assert s.probabilidad("perro") == 0.0
    
    def test_probability_by_index(self):
        """Test cálculo de probabilidad por índice"""
        s = SignoCuanto(["rojo", "azul"], [0.6, 0.8])
        assert np.isclose(s.probabilidad(0), 0.36)  # 0.6^2
        assert np.isclose(s.probabilidad(1), 0.64)  # 0.8^2
    
    def test_probability_invalid(self):
        """Test error con significante inexistente"""
        s = SignoCuanto(["a", "b"], [1, 1])
        with pytest.raises(ValueError):
            s.probabilidad("c")
    
    def test_collapse(self):
        """Test colapso del estado"""
        s = SignoCuanto(["A", "B"], [1, 0])  # 100% A
        sig, estado_colapsado = s.colapsar()
        assert sig == "A"
        assert estado_colapsado.amplitudes[0] == 1.0
        assert estado_colapsado.amplitudes[1] == 0.0

    def test_collapse_forced(self):
        """Test colapso con índice forzado"""
        s = SignoCuanto(["uno", "dos"], [0.5, 0.5])
        sig, estado_colapsado = s.colapsar(idx=1)
        assert sig == "dos"
        assert estado_colapsado.amplitudes[0] == 0.0
        assert estado_colapsado.amplitudes[1] == 1.0
    
    def test_density_matrix(self):
        """Test matriz densidad"""
        s = SignoCuanto(["a", "b"], [1, 0])
        rho = s.densidad()
        assert rho.shape == (2, 2)
        assert np.isclose(rho[0, 0], 1.0)
        assert np.isclose(rho[1, 1], 0.0)
    
    def test_phase_relative(self):
        """Test fase relativa"""
        s = SignoCuanto(["a", "b"], [1, 1j])
        fase = s.fase_relativa(0, 1)
        assert np.isclose(fase, -np.pi/2)  # arg(1 / 1j) = arg(-i) = -π/2


class TestLangue:
    """Pruebas para la clase Langue"""
    
    def test_initialization(self):
        """Test inicialización"""
        l = Langue(5, "Test")
        assert l.dimension == 5
        assert l.nombre == "Test"
        assert len(l._base) == 5
    
    def test_estado_base(self):
        """Test creación de estado base"""
        l = Langue(3)
        estado = l.estado_base(1)
        assert np.isclose(estado.amplitudes[1], 1.0)
        assert np.isclose(estado.amplitudes[0], 0.0)
        assert estado.dimension == 3
    
    def test_superposicion(self):
        """Test creación de superposición"""
        l = Langue(3)
        estado = l.superposicion([1, 0.5j, 0.3])
        assert estado.dimension == 3
        assert np.isclose(np.linalg.norm(estado.amplitudes), 1.0)
    
    def test_superposicion_wrong_dimension(self):
        """Test error con dimensiones incorrectas"""
        l = Langue(3)
        with pytest.raises(ValueError):
            l.superposicion([1, 1])  # Solo 2 coeficientes para dimensión 3
    
    def test_base_canonica(self):
        """Test generación de base canónica"""
        l = Langue(4)
        base = l.base_canonica()
        assert len(base) == 4
        for i, b in enumerate(base):
            assert np.isclose(b.amplitudes[i], 1.0)
    
    def test_producto_interno(self):
        """Test producto interno"""
        l = Langue(2)
        psi = l.superposicion([1, 0])
        phi = l.superposicion([0, 1])
        prod = l.producto_interno(psi, phi)
        assert np.isclose(prod, 0.0)  # Ortogonales
    
    def test_producto_interno_mismatch(self):
        """Test error con dimensiones incompatibles"""
        l1 = Langue(2)
        l2 = Langue(3)
        psi = l1.superposicion([1, 0])
        phi = l2.superposicion([0, 1, 0])
        with pytest.raises(ValueError):
            l1.producto_interno(psi, phi)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
    