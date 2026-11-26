# Instalação de Totens Inteligentes Multifunções no Campus USP São Carlos

Projeto desenvolvido para a disciplina de **Introdução a Pesquisa Operacional**, focado na modelagem matemática e resolução exata de um problema de **Programação Linear Inteira Binária (PLIB)** aplicado à localização de infraestrutura inteligente no campus da Universidade de São Paulo (USP) em São Carlos.

---

## Sobre o Projeto - Cenário Fictício

A USP planeja implantar totens inteligentes multifuncionais na **Área 1 do campus de São Carlos** (abrangendo EESC, ICMC, IFSC, IQSC, IAU, Prefeitura do Campus, CEFER, RU, bibliotecas e moradia estudantil). Esses terminais concentram serviços como mapas interativos, consulta de horários, recarga de saldo do Restaurante Universitário e um **botão de emergência** integrado à segurança universitária.

Como os equipamentos possuem alto custo de aquisição e cabeamento, o grupo formulou o problema como uma variante do **Problema de Cobertura de Conjuntos (*Set Covering*)** com **cobertura dupla obrigatória em pontos críticos** (áreas abertas, vias isoladas e moradia estudantil) para garantir redundância de segurança. O objetivo do modelo é **minimizar o custo total de implantação** atendendo a 48 pontos de demanda a partir de 192 locais candidatos.



## 📂 Estrutura do Repositório

```text
projeto-ipo/
├── demandas.csv                 # Base de dados com os 48 pontos de demanda (coordenadas, fluxo e criticidade)
├── candidatos.csv               # Base de dados com os 192 locais candidatos (coordenadas, infraestrutura e custo)
├── resolver_totens.py           # Script principal de modelagem, resolução exata (SciPy/HiGHS) e geração de mapas
├── resultados_experimentos.csv  # Tabela consolidada gerada automaticamente após a execução do solver
├── mapa_solucao_R50.png         # Gráfico da distribuição espacial ótima para raio R = 50 m
├── mapa_solucao_R75.png         # Gráfico da distribuição espacial ótima para raio R = 75 m
├── mapa_solucao_R100.png        # Gráfico da distribuição espacial ótima para raio R = 100 m
├── mapa_solucao_R150.png        # Gráfico da distribuição espacial ótima para raio R = 150 m
└── README.md                    # Documentação do projeto
```

* **`demandas.csv`**: Contém os 48 pontos mapeados na Área 1 (portarias, bibliotecas, restaurantes, serviços, praças, cruzamentos, áreas esportivas, moradia e vias isoladas), incluindo suas coordenadas $(x, y)$ em metros e a sinalização de quais dos 10 locais são críticos.
* **`candidatos.csv`**: Lista os 192 pontos viáveis para instalação (fachadas, portarias, praças, postes e áreas livres), indicando se já possuem rede elétrica/lógica (custo base de R\$ 25.000,00) ou se exigem cabeamento adicional (R\$ 150,00/m até a infraestrutura mais próxima).
* **`resolver_totens.py`**: Constrói a matriz de distâncias a pé ($d_{ij} = 1{,}3 \times \text{distância euclidiana}$), formula as restrições de cobertura simples e dupla, executa o solver exato para os cenários de raio $R \in \{50, 75, 100, 150\}\text{ m}$, exporta o CSV de resultados e salva os mapas em PNG.

---

## Como Rodar

### Pré-requisitos
* **Python 3.10+** instalado no sistema.
* Gerenciador de pacotes `pip` e suporte a ambientes virtuais (`venv`).

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/GustavoFantato/projeto-ipo.git
   cd projeto-ipo
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```bash
   pip install numpy pandas scipy matplotlib
   ```

4. **Execute o modelo de otimização:**
   ```bash
   python3 resolver_totens.py
   ```

Ao finalizar, o resumo comparativo será exibido diretamente no terminal, e os arquivos `resultados_experimentos.csv` e `mapa_solucao_R*.png` serão atualizados na raiz do projeto.

---

## Resumo dos Resultados Obtidos

Os experimentos foram executados utilizando a biblioteca **SciPy** (`scipy.optimize.milp`) integrada ao solver **HiGHS** (*Branch-and-Bound*). Todos os cenários atingiram a otimalidade global em menos de $15\text{ ms}$:

| Raio de Cobertura ($R$) | Status | Custo Total (R$) | Totens Instalados | Com Infraestrutura | Sem Infraestrutura | Tempo (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **50 m** | Ótima | R$ 1.705.627,00 | 55 | 35 (63,6%) | 20 (36,4%) | 0,0135 |
| **75 m** | Ótima | R$ 1.443.127,00 | 46 | 29 (63,0%) | 17 (37,0%) | 0,0106 |
| **100 m** | Ótima | R$ 1.161.127,00 | 37 | 24 (64,9%) | 13 (35,1%) | 0,0100 |
| **150 m** | Ótima | R$ 767.560,00 | 25 | 18 (72,0%) | 7 (28,0%) | 0,0095 |

---

## Tecnologias Utilizadas

* **Python 3.12** — Linguagem base para modelagem e automação
* **SciPy (HiGHS)** — Solver de Programação Linear Inteira Mista (MILP)
* **NumPy & Pandas** — Cálculo matricial de distâncias e manipulação tabular
* **Matplotlib** — Visualização espacial dos pontos de demanda, candidatos e totens selecionados

---

### Autores
* **Gustavo Fantato Fernandes**
* **João Marcelo Geraldo Cintra Faria**
* **Lucas Xavier Carvalho Santos**
