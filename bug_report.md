# 🐛 Reporte de Errores — Saussure-Quantum Fusion
**Versión analizada:** 0.1.0  
**Fecha:** Abril 2026  
**Estado general:** Funcional con issues menores

---

## ISSUE #1 — Bug crítico en `uncertainty.py`

**Archivo:** `saussure_quantum/uncertainty.py`  
**Método:** `PrincipioIncertidumbreSaussure.visualizar_espacio_fase()`  
**Severidad:** 🔴 Media (el método no se invoca en ningún lado aún, pero romperá en runtime si alguien lo llama)

### Descripción

El método referencia `self.dimension`, atributo que no existe en la clase `PrincipioIncertidumbreSaussure`. La dimensión correcta está en `self.langue.dimension`.

### Código actual (incorrecto)

```python
def visualizar_espacio_fase(self, estado: SignoCuanto) -> np.ndarray:
    psi = estado.amplitudes
    d = self.dimension        # ❌ AttributeError: 'PrincipioIncertidumbreSaussure' has no attribute 'dimension'
    W = np.zeros((d, d), dtype=float)
    ...
```

### Solución

```python
def visualizar_espacio_fase(self, estado: SignoCuanto) -> np.ndarray:
    psi = estado.amplitudes
    d = self.langue.dimension  # ✅ Correcto
    W = np.zeros((d, d), dtype=float)
    ...
```

---

## ISSUE #2 — Notebook `02_operador_diferencia.ipynb` con celdas de código rotas

**Archivo:** `notebooks/02_operador_diferencia.ipynb`  
**Severidad:** 🔴 Alta (las celdas de código desde la sección 5 en adelante no se ejecutan en Jupyter)

### Descripción

A partir de la sección 5 ("El operador D̂ como matriz"), el notebook tiene las celdas de código embebidas dentro de bloques `markdown` como texto plano con triple backtick. Jupyter las muestra como texto formateado, pero **no las ejecuta**. El notebook 01 y los demás están correctos; solo el 02 tiene este problema.

### Ejemplo del problema (en el JSON del notebook)

```json
{
  "cell_type": "markdown",   // ❌ Debería ser "code"
  "source": [
    "## 5. El operador D̂ como matriz\n",
    "```python\n",             // ❌ Código dentro de markdown
    "lang = Langue(4, 'demo')\n",
    "..."
  ]
}
```

### Solución

Separar cada bloque de código en su propia celda con `"cell_type": "code"`. El patrón correcto es:

```json
{
  "cell_type": "markdown",
  "source": ["## 5. El operador D̂ como matriz\n", "Descripción..."]
},
{
  "cell_type": "code",        // ✅ Celda de código separada
  "execution_count": null,
  "metadata": {},
  "outputs": [],
  "source": [
    "lang = Langue(4, 'demo')\n",
    "operador = OperadorDiferencia(lang)\n",
    "..."
  ]
}
```

**Celdas afectadas:** secciones 5, 6, 7, 8, 9 y 10 del notebook.

---

## ISSUE #3 — Test frágil en `test_uncertainty.py`

**Archivo:** `tests/test_uncertainty.py`  
**Método:** `TestObservablesSaussureanos.test_estado_minima_incertidumbre()`  
**Severidad:** 🟡 Baja (el test pasa la mayoría de las veces, pero puede fallar según la dimensión)

### Descripción

El test asume que el estado gaussiano generado por `estado_minima_incertidumbre()` produce un producto ΔS·ΔP menor que `2 * cota`. En espacios discretos pequeños, una gaussiana no satura bien la cota de Heisenberg y el factor puede superar 2x dependiendo de la dimensión usada (actualmente `dimension=20`).

### Código actual

```python
def test_estado_minima_incertidumbre(self):
    obs = ObservablesSaussureanos(20)
    estado = obs.estado_minima_incertidumbre()
    delta_S, delta_P, producto = obs.incertidumbre(estado)

    cota = HBAR_SEMIOTICO / 2
    assert producto >= cota - 1e-5
    assert producto / cota < 2.0   # ⚠️ Puede fallar para d pequeño o grande
```

### Solución

Relajar la cota superior o hacerla dependiente de la dimensión, y agregar un mensaje descriptivo:

```python
def test_estado_minima_incertidumbre(self):
    obs = ObservablesSaussureanos(20)
    estado = obs.estado_minima_incertidumbre()
    delta_S, delta_P, producto = obs.incertidumbre(estado)

    cota = HBAR_SEMIOTICO / 2
    # El principio de incertidumbre debe satisfacerse
    assert producto >= cota - 1e-5, f"Viola el principio: {producto} < {cota}"
    # En discreto, el estado coherente no satura perfectamente.
    # Se acepta hasta 5x la cota mínima como razonable.
    assert producto / cota < 5.0, f"Demasiado lejos de la cota: factor={producto/cota:.2f}"
```

---

## ISSUE #4 — Dependencia `qiskit` innecesaria en `requirements.txt`

**Archivo:** `requirements.txt`  
**Severidad:** 🟢 Cosmética (no rompe nada, pero confunde a quien instala el paquete)

### Descripción

`qiskit>=0.39.0` está listado como dependencia directa, pero no se importa ni se usa en ningún módulo del paquete. Es una dependencia pesada (~500MB con sus subdependencias). El README lo menciona como trabajo futuro en el roadmap.

### Código actual

```
# requirements.txt
qiskit>=0.39.0    # ⚠️ No se usa en ningún módulo
```

### Solución

Moverlo a un extra opcional en `setup.py` (donde ya existe correctamente) y eliminarlo de `requirements.txt`:

```
# requirements.txt — eliminar la línea de qiskit

# setup.py — ya está bien configurado aquí:
extras_require={
    "quantum": ["qiskit>=0.39.0"],   # ✅ Instalar con: pip install -e ".[quantum]"
}
```

---

## Resumen general

| # | Archivo | Problema | Severidad | Esfuerzo de fix |
|---|---------|----------|-----------|-----------------|
| 1 | `uncertainty.py` | `self.dimension` → `self.langue.dimension` | 🔴 Media | 1 línea |
| 2 | `02_operador_diferencia.ipynb` | Celdas de código dentro de markdown | 🔴 Alta | Reescribir el notebook |
| 3 | `test_uncertainty.py` | Cota superior demasiado estricta | 🟡 Baja | 2 líneas |
| 4 | `requirements.txt` | `qiskit` listado sin usarse | 🟢 Cosmética | Eliminar 1 línea |

**Total de archivos afectados:** 4 de 13  
**Ningún issue rompe el flujo principal del paquete.**  
El fix más urgente es el #2 (notebook) si el proyecto se usa pedagógicamente,  
y el #1 (bug) si se planea exponer `visualizar_espacio_fase()` al usuario.
