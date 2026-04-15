# Simulación de Trayectorias Celulares — Células Sanas vs Infectadas

Simulación dinámica del movimiento de glóbulos rojos sanos e infectados bajo la acción del campo eléctrico generado por dos placas asimétricas, modelando el principio de **dielectroforesis** para la detección de malaria.

---

## Descripción

El script combina dos cálculos independientes sobre la misma geometría de placas de `Campos_Malaria`:

1. **Campo de fondo** (visualización): campo eléctrico y potencial en una malla de 1000×1000 puntos con `Nq = 500` cargas por placa, idéntico al de `Campos_Malaria`.
2. **Dinámica de partículas**: integración numérica (Euler explícito) de las ecuaciones de movimiento de 30 células bajo la fuerza de Coulomb del campo, usando `Nq_sim = 150` cargas por placa para reducir el coste computacional.

Las células se diferencian por su carga efectiva (`q_sana` vs `q_infectada`), lo que provoca trayectorias distintas y permite visualizar cómo el campo no uniforme separa ambas poblaciones.

---

## Ejemplo de salida

```
trayectorias_malaria.png
```

La imagen muestra el campo de fondo (potencial en escala `bone`, líneas equipotenciales blancas, líneas de campo verdes) con las trayectorias superpuestas: **verde** para células sanas, **rojo** para infectadas. Todas las células parten desde `y = 2.5` con velocidad inicial hacia abajo.

---

## Estructura del código

```
Simulacion_Malaria.py
│
├── Geometría (compartida)      # Mismas placas y Nq=500 que Campos_Malaria
├── Campo de fondo              # Ex, Ey, V en malla 1000×1000 (k=1, q=1)
├── Parámetros de simulación    # k_fis, q_fis, dt, m, max_steps, Nq_sim
├── Bucle de partículas         # 30 células, asignación aleatoria sana/infectada
│   ├── Fuerza de Coulomb       # Suma sobre Nq_sim cargas positivas y negativas
│   ├── Integrador Euler        # vx, vy → x, y en cada paso dt
│   └── Condición de salida     # Para si y < -2.5 o |x| > 3
└── Visualización               # contourf + streamplot + trayectorias coloreadas
```

---

## Parámetros configurables

### Geometría de las placas (idéntica a Campos_Malaria)

| Parámetro     | Valor | Descripción |
|---|---|---|
| `dx_placa`    | `-1.0` | Posición X de la placa positiva |
| `largo_roja`  | `4`    | Longitud de la placa positiva (m) |
| `largo_azul`  | `1`    | Longitud de la placa negativa (m) |
| `Nq`          | `500`  | Cargas por placa para el campo de fondo |

### Dinámica de partículas

| Parámetro      | Valor   | Descripción |
|---|---|---|
| `k_fis`        | `9e9`   | Constante de Coulomb real (N·m²/C²) |
| `q_fis`        | `1e-5`  | Carga de cada punto de la placa (C) |
| `Nq_sim`       | `150`   | Cargas por placa en la simulación dinámica |
| `N_particulas` | `30`    | Número de células simuladas |
| `dt`           | `0.02`  | Paso de tiempo del integrador (s) |
| `m`            | `1`     | Masa de cada célula (kg, adimensional) |
| `max_steps`    | `2000`  | Pasos máximos por trayectoria |
| `v_ini`        | `10`    | Velocidad inicial hacia abajo (m/s) |
| `q_sana`       | `0.8e-6` | Carga efectiva de célula sana (C) |
| `q_infectada`  | `1.4e-6` | Carga efectiva de célula infectada (C) |
| `ruido`        | `0.3e-6` | Desviación estándar del ruido en la carga (C) |

---

## Fundamento físico

### Fuerza de Coulomb sobre la célula

La fuerza que ejerce cada carga de la placa $q_i$ sobre una célula de carga $q_{cell}$ en la posición $\vec{r}$ es:

$$\vec{F}_i = k \, q_{cell} \, q_i \frac{\vec{r} - \vec{r}_i}{|\vec{r} - \vec{r}_i|^3}$$

La fuerza total se obtiene sumando sobre todas las cargas de ambas placas (superposición).

### Integración de movimiento (Euler explícito)

$$\vec{v}^{n+1} = \vec{v}^n + \frac{\vec{F}^n}{m} \, \Delta t$$
$$\vec{r}^{n+1} = \vec{r}^n + \vec{v}^{n+1} \, \Delta t$$

### Dielectroforesis (principio subyacente)

La dielectroforesis es la migración de partículas polarizables bajo un campo eléctrico **no uniforme**. La fuerza DEP es proporcional al gradiente del campo al cuadrado:

$$\vec{F}_{DEP} \propto \nabla |\vec{E}|^2$$

Los glóbulos rojos infectados con *Plasmodium falciparum* tienen una polarizabilidad eléctrica distinta a los sanos, lo que en este modelo se representa como una carga efectiva diferente. Esto hace que se desvíen de manera distinta al atravesar el campo no uniforme, permitiendo su separación y detección.

---

## Modelo físico

Las células se introducen desde `y = 2.5` con velocidad inicial uniforme hacia abajo (`vy = -v_ini`). Al entrar en la región de campo no uniforme entre las placas asimétricas, la fuerza de Coulomb actúa de forma diferente sobre células sanas e infectadas:

- **Células sanas** (carga menor, verde): experimentan menor fuerza lateral y tienden a atravesar la región con menor desviación.
- **Células infectadas** (carga mayor, rojo): experimentan mayor fuerza y se desvían más notoriamente hacia la placa positiva o negativa según su posición de entrada.

La variación aleatoria con `ruido` introduce dispersión realista entre células de la misma categoría.

---

## Dependencias

```bash
pip install numpy matplotlib
```

| Librería     | Versión mínima | Uso |
|---|---|---|
| `numpy`      | 1.20+          | Álgebra vectorial, mallas, integración |
| `matplotlib` | 3.3+           | Visualización 2D (contourf, streamplot, plot) |

---

## Ejecución

```bash
python Actividades/Celulas_Simuladas/Simulacion_Malaria.py
```

La imagen se guarda automáticamente en la carpeta del script:

```
Actividades/Celulas_Simuladas/trayectorias_malaria.png
```

No se abre ventana gráfica (usa el backend `Agg` de matplotlib).
