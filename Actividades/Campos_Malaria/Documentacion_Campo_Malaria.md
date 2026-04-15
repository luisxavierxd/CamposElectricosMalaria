# Simulación de Campo Eléctrico — Dos Placas Conductoras

Simulación numérica del campo eléctrico y potencial electrostático generado por dos placas conductoras paralelas de distinto tamaño y carga, usando el principio de superposición de cargas puntuales discretas.

```
---
Simulación de campos eléctricos semi-continuos para un campo no uniforme


Descripción general
Esta parte del proyecto construye gráficamente un campo eléctrico generado por dos placas con una distribución de 500 cargas de signos opuestos para cada una. Se forma un campo eléctrico no uniforme útil para la detección de células de malaria que se comportarán distintos sobre el campo a comparación con células sanas.

Modelo Físico
Este es un sistema físico formado por dos placas cargadas eléctricamente. La placa roja está cargada positivamente y la placa azul está cargada negativamente, ambas almacenan 500 partículas. Como son placas de distintos signos, se genera un campo eléctrico entre ellas, para la que cada punto en el espacio será la suma vectorial del efecto de cada una de ellas. Esto sigue la Ley de Coulomb, que dice que el campo depende de la carga y disminuye con la distancia. 
El campo eléctrico de la placa positiva sale y se dirige hacia la placa negativa. Este campo no es uniforme, ya que depende de la distancia y el tamaño de las placas. 
	Comportamiento entre placas: si las placas fueran infinitas y del  mismo tamaño, el campo entre ellas sería uniforme, es decir, con la misma intensidad y dirección en toda la región. Pero en este caso, como las placas tienen tamaños distintos

Explicación física de la gráfica 
El Potencial (V) son las líneas curvas blancas que forman campos de relieve. Cerca de una carga puntual, podemos unir los puntos entre las posiciones que tienen el mismo potencial, creando curvas equipotenciales (escalar).
El Campo eléctrico (E): región del espacio modificada por la presencia de las 1,000 cargas, donde las células experimentarán fuerzas de atracción y repulsión (vectorial).
```

## Descripción

El script modela dos placas conductoras:

- Placa positiva (roja): cargada con `+q`, de mayor longitud
- Placa negativa (azul): cargada con `-q`, de menor longitud

Cada placa se discretiza en `Nq = 500` cargas puntuales distribuidas uniformemente a lo largo de su eje vertical. El campo eléctrico y el potencial en cada punto del espacio se calculan por superposición, aplicando la Ley de Coulomb a cada carga individual.

El resultado se guarda como imagen PNG con tres capas de visualización:
1. Mapa de color del potencial eléctrico `V(x, y)`
2. Líneas equipotenciales
3. Líneas de campo eléctrico (streamlines)

---

##  Ejemplo de salida

```
campo_placas_malaria.png
```

La imagen generada muestra el plano XY con las dos placas, el gradiente de potencial en escala de grises (`bone`), líneas equipotenciales en blanco y líneas de campo en verde.

---

## Estructura del código

```
campo_placas_malaria.py
│
├── Parámetros físicos          # Constante k, carga q, número de cargas Nq
├── Geometría de las placas     # Posiciones, largos y ancho visual
├── Posiciones de las cargas    # Arrays de coordenadas (xp, yp, xn, yn)
├── Malla de cálculo 2D         # Grilla 1000×1000 sobre [-3, 3] × [-3, 3]
├── Bucle de superposición      # Acumula E y V por cada carga
└── Visualización 2D            # contourf + contour + streamplot + patches
```

---

## Parámetros configurables

| Parámetro    | Valor por defecto | Descripción |
|---|---|---|
| `k`          | `1`               | Constante de Coulomb (adimensional) |
| `q`          | `1`               | Magnitud de la carga elemental |
| `Nq`         | `500`             | Cargas por placa (resolución de la simulación) |
| `dx_placa`   | `-1.0`            | Posición X de la placa positiva |
| `largo_roja` | `4`               | Longitud de la placa positiva (m) |
| `largo_azul` | `1`               | Longitud de la placa negativa (m) |
| `ancho`      | `-0.2`            | Grosor visual de las placas |

La separación entre placas es fija en `2` unidades (`x_azul = dx_placa + 2`).

---

##Fundamento físico

### Campo eléctrico (Ley de Coulomb vectorial)

Para cada carga puntual $q_i$ en la posición $\vec{r}_i$, el campo en el punto $\vec{r}$ es:

$$\vec{E}(\vec{r}) = k \sum_{i=1}^{N_q} q_i \frac{\vec{r} - \vec{r}_i}{|\vec{r} - \vec{r}_i|^3}$$

### Potencial eléctrico

$$V(\vec{r}) = k \sum_{i=1}^{N_q} \left( \frac{q}{r_{p,i}} - \frac{q}{r_{n,i}} \right)$$

donde $r_{p,i}$ y $r_{n,i}$ son las distancias al punto desde la i-ésima carga positiva y negativa respectivamente.

### Singularidades

Para evitar divergencias numéricas, las distancias menores a `0.15 m` se tratan de la siguiente manera:
- En el cálculo del campo: se asigna `NaN` (el punto se excluye del graficado)
- En el cálculo del potencial: se clampea a `0.15` (valor mínimo)

---

## Dependencias

```bash
pip install numpy matplotlib
```

| Librería    | Versión mínima | Uso |
|---|---|---|
| `numpy`     | 1.20+          | Álgebra vectorial, mallas numéricas |
| `matplotlib`| 3.3+           | Visualización 2D (contourf, streamplot, patches) |

---

## Ejecución

```bash
python campo_placas_malaria.py
```

La imagen se guarda automáticamente en la misma carpeta donde se encuentra el script:

```
./campo_placas_malaria.png
```

No se abre ninguna ventana gráfica (se usa el backend `Agg` de matplotlib).

---

