# CMR — Campo de Materialização Relacional

Autor: Flávio Oliveira  
Status: CMR v1.0 — Stable Operational Release

Este repositório contém a implementação experimental e operacional do
Framework CMR (Campo de Materialização Relacional).

O CMR é um framework operacional para investigar como fatos emergem,
divergem e se estabilizam em função do método de observação, do meio
físico e da integração temporal do observador.

Não se trata de uma nova teoria física nem de uma simulação da mecânica
quântica, mas de uma organização operacional do que os experimentos
mostram.


### Ambiente de Execução

Os experimentos podem ser executados localmente ou via GitHub Codespaces.
O uso de Codespaces é opcional e serve apenas para facilitar a reprodução.



### Nota sobre os métodos

Os scripts implementam experimentos operacionais segundo o Framework CMR.
Nenhum código pretende modelar diretamente fenômenos físicos reais, 
mas sim **capturar a lógica operacional** de como fatos emergem sob diferentes
regimes de observação.

O experimento conceitual inspirado na dupla fenda é apenas isso — um modelo
operacional — e **não uma simulação física da dupla fenda real**.

Experimentos que dependem de ruído físico real devem ser executados em
ambiente local, não em container ou máquinas virtuais.

## 📄 Documentação Formal

No diretório `docs/` estão os materiais formais associados ao Framework CMR v1.0:

- **CMR_Mathematical_Formulation.md** — Formulação matemática operacional do framework.
- **CMR_Math_Reproduction.py** — Implementação em Python que reproduz a matemática diretamente linha por linha.


Experimentos empíricos com ruído físico devem ser executados em ambiente local.


📁 Mapa Completo de Experimentos CMR (v1.0 → v1.5)
Estrutura Geral
Todos os experimentos estão organizados no diretório:
Copiar código

/experiments
Eles são agrupados por séries temáticas, cada uma explorando um aspecto operacional do Framework CMR.

🔬 Série A — Física Operacional (Base)
Local: experiments/Serie_A/
Explora regimes inspirados em fenômenos quânticos e clássicos, sem assumir ontologia física.
A1 — Medição: Política Rígida vs Elástica
A2 — Interferência como Conflito de Políticas
A3 — Supressão de Interferência por Política Dominante
A4 — Decoerência como Saturação Gradual
📄 Relatório: docs/REPORT_A1_A4.md

🧠 Série B — Alinhamento e IA (LLM Alignment)
Local: experiments/Serie_B/
Testa alinhamento como estabilidade operacional, não como verdade.
B1 — Alinhamento básico de agentes
B2 — Task shift
B3 — Custo do alinhamento
B4 — Over-alignment
B5 — Ausência de verdade global
B6 — Falha silenciosa
Script consolidado:
Copiar código
cmr_B2_to_B6_alignment_chain.py

🧩 Série C — Fragmentação e Irreversibilidade
Local: experiments/Serie_C/
Investiga quando divergência se torna permanente.
C1–C4 — Fragmentação progressiva
C4 — Fragmentação permanente (sem reconvergência)

🔁 Série D — Auto-Referência e Observadores
Local: experiments/Serie_D/
Explora observadores que observam a si mesmos.
D1–D5 — Auto-referência, loops cognitivos e instabilidade reflexiva

🗺️ Série E — Regimes e Mapas de Realidade
Local: experiments/Serie_E/
Constrói mapas operacionais de regimes CMR.
E1–E3c — Mapeamento de regimes, transições e fronteiras operacionais

🪐 Série T — Sistemas Dinâmicos e Caos (Três Corpos)
Local: experiments/Serie_T/
Aplica CMR a sistemas clássicos caóticos.
T1 — Três corpos observacionais (Euler vs Verlet)
T2 — Reconvergência forçada
T3 — Política adaptativa
T4 — Governança preventiva
T5 — Fragmentação irreversível
T6 — Auto-sincronização sem autoridade
Resultado-chave:
Não existe reconvergência espontânea após certos limiares.

🧠 Série G — Geometria, Curvatura e Topologia
Local: experiments/Serie_G/
Explora geometria como efeito de memória e observação.
G1 — Espaço observacional
G2 — Curvatura como erro de fechamento
G2B — Governança da curvatura
G3 — Topologia observacional (bloqueios)

🧠 Série I — Sistemas Aeroespaciais e Tráfego
Local: experiments/Serie_I/ (ou Serie_1, conforme estrutura)
Aplica CMR a múltiplos sensores e gestão de segurança.
I-A1 — Observadores divergentes (Radar vs ADS-B)
I-A2 — Alinhamento rígido vs concessão
I-A3 — Envelope probabilístico de segurança
I-A4 — (em fechamento)

🎮 Série J — HUDs e Autopilotos Relacionais
Local: experiments/Serie_J/
Explora interfaces e controle.
J1 — HUD multi-observador
J2 — Autopiloto relacional (A+B+C)

💹 Série K — Mercados e Regimes Econômicos
Local: experiments/Serie_K/
Mercado como sistema relacional, não verídico.
K1 — Mercado relacional
K2 — Bolha narrativa
K3 — Estouro por esquecimento
K4–K6 — Regimes: autoridade, consenso, liquidez, fragmentação
Conclusão:
Estabilidade emerge do menor custo, não da verdade.

🗣️ Série L — Linguagem e Semântica
Local: experiments/Serie_L/
Explora colapso semântico.
L1–L4 — Linguagem relacional, consenso e esquecimento

🏛️ Série S — Soberania e Governança
Local: experiments/Serie_S/
IA como operador de regimes.
S1 — IA como trocador de regime
S2 — Falha de soberania (troca tardia)
S3.1 — Detector de ponto de não-retorno
Resultado:
Alguns colapsos são estruturalmente inevitáveis.

📄 Documentação Complementar
Local: docs/
CMR_Mathematical_Formulation.md
CMR_Math_Reproduction.py
Leis_CMR.md — Leis operacionais derivadas dos experimentos

📦 Releases e Publicação
GitHub Releases:
https://github.com/BondfinderBR/CMR-v1.0-Operational-Release/releases�
Zenodo (DOI):
https://zenodo.org/records/18463264�

🔚 Observação Final
O CMR não busca substituir teorias físicas existentes.
Ele organiza como realidades funcionais emergem, quando falham, e quanto custam operacionalmente.
Estabilidade não é verdade.
É o regime de menor custo possível.


https://zenodo.org/records/18463264
