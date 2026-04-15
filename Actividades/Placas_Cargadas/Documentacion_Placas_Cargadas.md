# Simulación de Campo Eléctrico — Dos Placas Cargadas (3D)

Visualización 3D del campo eléctrico generado por dos placas conductoras paralelas (positiva y negativa) modeladas como distribuciones discretas de cargas puntuales, usando el principio de superposición.

---

## Descripción

El script extiende el modelo del dipolo a un arreglo de `Nq` cargas por placa distribuidas a lo largo del eje vertical. Cada placa se representa geométricamente como un prisma rectangular 3D. El campo eléctrico se calcula en un plano 2D (z = 0) y se visualiza con flechas 3D (`quiver3`).

El resultado se guarda como imagen PNG con la escena 3D completa.

---

## Ejemplo de salida

```
campo_placas_paralelas.png
```

La imagen muestra la vista en perspectiva 3D con la placa roja (+) a la izquierda y la azul (−) a la derecha, marcadores amarillos sobre cada carga y flechas verdes indicando la dirección del campo eléctrico en el plano z = 0.

---

## Estructura del código

```
Placas_Cargadas.py
│
├── Parámetros físicos          # Constante k, carga q, número de cargas Nq
├── Geometría de las placas     # Posiciones x, largos, ancho visual
├── Posiciones de las cargas    # linspace a lo largo del largo de cada placa
├── Malla de cálculo 2D         # meshgrid 30×30 en z=0 sobre [-3, 3]²
├── Bucle de superposición      # Acumula Ex, Ey, Ez por cada carga +/−
├── Normalización               # quiver de dirección (magnitud uniforme)
├── prisma_vertices()           # Genera vértices y caras de cada placa 3D
└── Visualización 3D            # Poly3DCollection + scatter + quiver3
```

---

## Parámetros configurables

| Parámetro    | Valor por defecto | Descripción |
|---|---|---|
| `k`          | `1`               | Constante de Coulomb (simplificada) |
| `q`          | `1`               | Magnitud de la carga elemental |
| `Nq`         | `3`               | Cargas por placa (resolución de la distribución) |
| `v`          | `0.5`             | Semialtura de las placas en y, z |
| `dx_placa`   | `-1.0`            | Posición X de la placa positiva |
| `largo_roja` | `3`               | Longitud de la placa positiva (m) |
| `largo_azul` | `3`               | Longitud de la placa negativa (m) |
| `ancho`      | `-0.2`            | Grosor visual de las placas |

La placa positiva se sitúa en `x = dx_placa` y la negativa en `x = dx_placa + 2`.

---

## Fundamento físico

### Campo eléctrico por superposición

Para `Nq` cargas por placa, el campo total en el punto $\vec{r}$ es:

$$\vec{E}(\vec{r}) = k \sum_{i=1}^{N_q} q_i \frac{\vec{r} - \vec{r}_i}{|\vec{r} - \vec{r}_i|^3}$$

donde las $q_i > 0$ corresponden a la placa roja y las $q_i < 0$ a la placa azul.

### Singularidades numéricas

Para evitar divisiones por cero o valores extremos, cualquier distancia menor a `0.15 m` se reemplaza por `NaN`, lo que excluye esos puntos de la visualización.

### Normalización

Los vectores se normalizan para mostrar solo dirección:

$$\hat{E} = \frac{\vec{E}}{|\vec{E}|}$$

Los puntos donde $|\vec{E}| = 0$ o no es finito se asignan a cero para no interrumpir el graficado.

---

## Modelo físico

Con `Nq` pequeño (ej. 3), se observan los aportes individuales de cada carga. Al aumentar `Nq`, la distribución se aproxima a una placa continua y el campo entre las placas tiende a ser más uniforme en la región central. Como ambas placas tienen el mismo largo en esta actividad, el campo es más simétrico que en el caso de `Campos_Malaria`, donde las placas son asimétricas para crear el gradiente necesario para la dielectroforesis.

---

## Dependencias

```bash
pip install numpy matplotlib
```

| Librería     | Versión mínima | Uso |
|---|---|---|
| `numpy`      | 1.20+          | Álgebra vectorial, mallas numéricas |
| `matplotlib` | 3.3+           | Visualización 3D (Poly3DCollection, quiver3) |

---

## Ejecución

```bash
python Actividades/Placas_Cargadas/Placas_Cargadas.py
```

La imagen se guarda automáticamente en la carpeta del script:

```
Actividades/Placas_Cargadas/campo_placas_paralelas.png
```

Se abre además una ventana interactiva de matplotlib (backend por defecto).
