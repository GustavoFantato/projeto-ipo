import math
import time
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds
import matplotlib.pyplot as plt

df_dem = pd.read_csv("demandas.csv")
df_cand = pd.read_csv("candidatos.csv")

I = df_dem["id"].tolist()
critico_flags = (df_dem["critico"].str.strip().str.lower() == "sim").tolist()
J = df_cand["id"].tolist()

n_dem = len(I)
n_cand = len(J)

coord_i = list(zip(df_dem["x"], df_dem["y"]))
coord_j = list(zip(df_cand["x"], df_cand["y"]))
c = df_cand["custo"].astype(float).to_numpy()
infra_j = (df_cand["infra"].str.strip().str.lower() == "sim").to_numpy()

# Matriz de distâncias a pé (n_dem x n_cand)
dist = np.zeros((n_dem, n_cand))
for idx_i, (xi, yi) in enumerate(coord_i):
    for idx_j, (xj, yj) in enumerate(coord_j):
        dist[idx_i, idx_j] = 1.3 * math.hypot(xi - xj, yi - yj)

# Vetor de cobertura mínima exigida: 2 para críticos, 1 para comuns
b_l = np.array([2.0 if crit else 1.0 for crit in critico_flags])
b_u = np.full(n_dem, np.inf)

# Limites das variáveis binárias x_j in {0, 1}
bounds = Bounds(np.zeros(n_cand), np.ones(n_cand))
integrality = np.ones(n_cand)  # 1 = variável inteira

raios = [50, 75, 100, 150]
resultados = []

for R in raios:
    A = (dist <= R).astype(float)
    constraints = LinearConstraint(A, b_l, b_u)

    inicio = time.perf_counter()
    res = milp(c=c, integrality=integrality, bounds=bounds, constraints=constraints)
    tempo_exec = time.perf_counter() - inicio

    if res.success:
        x_sol = np.round(res.x).astype(int)
        escolhidos_idx = np.where(x_sol == 1)[0]
        escolhidos_ids = [J[idx] for idx in escolhidos_idx]
        custo_total = float(res.fun)
        qtd_totens = len(escolhidos_ids)
        com_infra = int(np.sum(infra_j[escolhidos_idx]))
        sem_infra = qtd_totens - com_infra

        resultados.append({
            "Raio_R (m)": R,
            "Status": "Ótima",
            "Custo_Total (R$)": custo_total,
            "Total_Totens": qtd_totens,
            "Com_Infra": com_infra,
            "Sem_Infra": sem_infra,
            "Tempo (s)": round(tempo_exec, 4),
            "Locais_Escolhidos": escolhidos_ids
        })

        # Plotar mapa da solução
        plt.figure(figsize=(8, 10))
        nao_esc_idx = np.where(x_sol == 0)[0]
        plt.scatter([coord_j[idx][0] for idx in nao_esc_idx], [coord_j[idx][1] for idx in nao_esc_idx],
                    c="lightgray", s=15, label="Candidatos não escolhidos")

        comuns_idx = [idx for idx, flag in enumerate(critico_flags) if not flag]
        crit_idx = [idx for idx, flag in enumerate(critico_flags) if flag]

        plt.scatter([coord_i[idx][0] for idx in comuns_idx], [coord_i[idx][1] for idx in comuns_idx],
                    c="royalblue", marker="^", s=45, label="Demanda comum (38)")
        plt.scatter([coord_i[idx][0] for idx in crit_idx], [coord_i[idx][1] for idx in crit_idx],
                    c="crimson", marker="s", s=55, label="Ponto crítico (10)")
        plt.scatter([coord_j[idx][0] for idx in escolhidos_idx], [coord_j[idx][1] for idx in escolhidos_idx],
                    c="limegreen", edgecolors="black", s=90, zorder=5, label=f"Totens instalados ({qtd_totens})")

        plt.title(f"Solução Ótima - Raio R = {R}m | Custo: R$ {custo_total:,.2f}")
        plt.xlabel("Coordenada X - Leste (m)")
        plt.ylabel("Coordenada Y - Norte (m)")
        plt.legend(loc="best")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.savefig(f"mapa_solucao_R{R}.png", dpi=300)
        plt.close()
    else:
        disponiveis = A.sum(axis=1)
        gargalos = [
            f"{I[idx]} (disp={int(disponiveis[idx])}, req={int(b_l[idx])})"
            for idx in range(n_dem) if disponiveis[idx] < b_l[idx]
        ]
        resultados.append({
            "Raio_R (m)": R,
            "Status": "Inviável",
            "Custo_Total (R$)": None,
            "Total_Totens": None,
            "Com_Infra": None,
            "Sem_Infra": None,
            "Tempo (s)": round(tempo_exec, 4),
            "Locais_Escolhidos": f"Gargalos: {', '.join(gargalos)}"
        })

df_res = pd.DataFrame(resultados)
print("\n=== RESUMO DOS EXPERIMENTOS COMPUTACIONAIS ===")
print(df_res.to_string(index=False))
df_res.to_csv("resultados_experimentos.csv", index=False)