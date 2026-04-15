import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

carpeta = os.path.dirname(os.path.abspath(__file__))

# ── Parámetros físicos ────────────────────────────────────────────────────
k  = 9e9
q  = 1e-5
Nq = 150   # ↓ reducido para rendimiento

# Parámetros partículas
N_particulas = 30
dt = 0.02          # ↑ más estable
m = 1
max_steps = 2000   # evita loops infinitos

# Diferenciación células
q_sana = 0.8e-6
q_infectada = 1.4e-6
ruido = 0.3e-6  # variabilidad aleatoria en carga de las células
#:v emtemp semch

# ── Geometría ─────────────────────────────────────────────────────────────
v           = 10
dx_placa    = -1.0
largo_roja  = 4
largo_azul  = 1
ancho       = -0.2

x_roja = dx_placa
x_azul = dx_placa + 2

# ── Posiciones de las cargas ──────────────────────────────────────────────
yp = np.linspace(-largo_roja/2, largo_roja/2, Nq)
xp = np.full(Nq, x_roja)

yn = np.linspace(-largo_azul/2, largo_azul/2, Nq)
xn = np.full(Nq, x_azul)

# ── Malla 2D ─────────────────────────────────────────────────────────────
xx = np.linspace(-3, 3, 100)
yy = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(xx, yy)

Ex = np.zeros_like(X)
Ey = np.zeros_like(Y)
V  = np.zeros_like(X)

for k_i in range(Nq):
    rx = X - xp[k_i]; ry = Y - yp[k_i]
    rp = np.sqrt(rx**2 + ry**2)
    rp[rp < 0.15] = np.nan
    Ex += k * q * rx / rp**3
    Ey += k * q * ry / rp**3

    rx = X - xn[k_i]; ry = Y - yn[k_i]
    rn = np.sqrt(rx**2 + ry**2)
    rn[rn < 0.15] = np.nan
    Ex += k * (-q) * rx / rn**3
    Ey += k * (-q) * ry / rn**3

    rp2 = np.sqrt((X - xp[k_i])**2 + (Y - yp[k_i])**2)
    rn2 = np.sqrt((X - xn[k_i])**2 + (Y - yn[k_i])**2)
    rp2[rp2 < 0.15] = 0.15
    rn2[rn2 < 0.15] = 0.15
    V += k * q / rp2 - k * q / rn2

# ── Simulación de partículas ─────────────────────────────────────────────
trayectorias = []

for i in range(N_particulas):
    x = np.random.uniform(-0.2, 0.2)
    y = 2.5
    vx, vy = 0, -v

    if np.random.rand() < 0.5:
        q_base = q_sana
        color = 'green'
    else:
        q_base = q_infectada
        color = 'red'

    # Ruido gaussiano en la carga
    q_part = q_base + np.random.normal(0, ruido)

    # Evitar cargas negativas no físicas
    q_part = max(q_part, 1e-9)

    xs, ys = [x], [y]

    for step in range(max_steps):

        # ── Fuerza vectorizada ──

        # Placa positiva
        rxp = x - xp
        ryp = y - yp
        rp = np.sqrt(rxp**2 + ryp**2)
        mask_p = rp > 0.1

        Fx_p = np.sum(k * q_part * q * rxp[mask_p] / rp[mask_p]**3)
        Fy_p = np.sum(k * q_part * q * ryp[mask_p] / rp[mask_p]**3)

        # Placa negativa
        rxn = x - xn
        ryn = y - yn
        rn = np.sqrt(rxn**2 + ryn**2)
        mask_n = rn > 0.1

        Fx_n = np.sum(k * q_part * (-q) * rxn[mask_n] / rn[mask_n]**3)
        Fy_n = np.sum(k * q_part * (-q) * ryn[mask_n] / rn[mask_n]**3)

        Fx = Fx_p + Fx_n
        Fy = Fy_p + Fy_n

        # Integración (Euler)
        ax = Fx / m
        ay = Fy / m

        vx += ax * dt
        vy += ay * dt

        x += vx * dt
        y += vy * dt

        xs.append(x)
        ys.append(y)

        # Condición de salida
        if y < -2.5 or abs(x) > 3:
            break

    trayectorias.append((xs, ys, color))

# ── Visualización ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9,7))

V_plot = np.clip(V, -500, 500)
cf = ax.contourf(X, Y, V_plot, levels=60, cmap='bone')
plt.colorbar(cf, ax=ax)

ax.contour(X, Y, V_plot, levels=10, colors='white', linewidths=0.5)

with np.errstate(invalid='ignore'):
    Ex_s = np.where(np.isfinite(Ex), Ex, 0.0)
    Ey_s = np.where(np.isfinite(Ey), Ey, 0.0)

ax.streamplot(xx, yy, Ex_s, Ey_s, density=1.2)

# Placas
ax.add_patch(Rectangle((x_roja-abs(ancho), -largo_roja/2),
                       2*abs(ancho), largo_roja, color='red', alpha=0.7))
ax.add_patch(Rectangle((x_azul-abs(ancho), -largo_azul/2),
                       2*abs(ancho), largo_azul, color='blue', alpha=0.7))

# Trayectorias
for xs, ys, color in trayectorias:
    ax.plot(xs, ys, color=color, linewidth=1)

ax.set_xlim(-3,3)
ax.set_ylim(-3,3)
ax.set_aspect('equal')
ax.set_title('Trayectorias de células (sanas vs infectadas)')

plt.tight_layout()
plt.savefig(os.path.join(carpeta, 'trayectorias_malaria.png'), dpi=150)

print("Listo: trayectorias_malaria.png")