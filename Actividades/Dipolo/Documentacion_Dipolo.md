# Simulación de Campo Eléctrico — Dipolo de Cargas Puntuales

Visualización del campo eléctrico vectorial 2D generado por dos cargas puntuales de signo opuesto (+q, −q), usando el principio de superposición de la Ley de Coulomb.

---

## Descripción

El script modela un **dipolo eléctrico**: una carga positiva y una negativa separadas una distancia `2d` sobre el eje x. El campo eléctrico resultante en cada punto del plano se obtiene sumando vectorialmente la contribución de cada carga.

El resultado se representa con flechas normalizadas (`quiver`) que muestran la **dirección** del campo en toda la región de interés, y se guarda como imagen PNG.

---

## Ejemplo de salida

```
campo_electrico_dipolo.png
```

La imagen muestra el plano XY con las dos cargas marcadas (rojo = +q, azul = −q) y una malla de flechas azules indicando la dirección del campo eléctrico.

---

## Estructura del código

```
Dipolo_Electrico.py
│
├── Parámetros físicos          # Constante k, carga q, separación d
├── Posiciones de las cargas    # q1_pos = (-d, 0),  q2_pos = (+d, 0)
├── Malla de cálculo 2D         # meshgrid sobre [-3, 3] × [-3, 3]  (paso 0.1)
├── Campo por superposición     # E1 (+q) + E2 (−q)
├── Normalización               # quiver de dirección (magnitud uniforme)
└── Visualización 2D            # quiver + marcadores de carga + leyenda
```

---

## Parámetros configurables

| Parámetro | Valor por defecto | Descripción |
|---|---|---|
| `k` | `9e9` | Constante de Coulomb (N·m²/C²) |
| `q` | `1` | Magnitud de la carga (C) |
| `d` | `0.5` | Semiseparación entre cargas (m) |

La carga positiva se ubica en `(-d, 0)` y la negativa en `(+d, 0)`.

---

## Fundamento físico

### Campo eléctrico de una carga puntual (Ley de Coulomb)

Para una carga $q_i$ en la posición $\vec{r}_i$, el campo en el punto $\vec{r}$ es:

$$\vec{E}_i(\vec{r}) = k \, q_i \frac{\vec{r} - \vec{r}_i}{|\vec{r} - \vec{r}_i|^3}$$

### Superposición

El campo total del dipolo es la suma vectorial de los campos individuales:

$$\vec{E}(\vec{r}) = \vec{E}_+(\vec{r}) + \vec{E}_-(\vec{r})$$

### Normalización para visualización

Para mostrar solo la dirección (independientemente de la magnitud), cada vector se divide entre su módulo:

$$\hat{E} = \frac{\vec{E}}{|\vec{E}|}$$

Esto es equivalente al escalado automático de MATLAB (`quiver` sin escala absoluta).

---

## Modelo físico

El campo de un dipolo eléctrico parte de la placa positiva y termina en la negativa. Cerca de cada carga el campo es radial e intenso; lejos del dipolo, las contribuciones de las dos cargas se cancelan parcialmente y el campo decae rápidamente. Esta geometría es la base conceptual para entender campos más complejos como el generado por los electrodos del dispositivo de detección de malaria.

---

## Dependencias

```bash
pip install numpy matplotlib
```

| Librería     | Versión mínima | Uso |
|---|---|---|
| `numpy`      | 1.20+          | Álgebra vectorial, mallas numéricas |
| `matplotlib` | 3.3+           | Visualización 2D (quiver, patches) |

---

## Ejecución

```bash
python Actividades/Dipolo/Dipolo_Electrico.py
```

La imagen se guarda automáticamente en la misma carpeta del script:

```
Actividades/Dipolo/campo_electrico_dipolo.png
```

Se abre además una ventana interactiva de matplotlib (backend por defecto).
