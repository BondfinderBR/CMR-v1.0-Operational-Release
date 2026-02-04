# 📄 CMR — Relatório Experimental Consolidado

**Gerado automaticamente em:** 2026-02-03 22:43:56.275504

---

## 🧪 cmr_A2_interferencia_politicas.py

### 📤 Saída

```text
🧪 CMR–A2 — INTERFERÊNCIA OPERACIONAL

Instabilidade Política A (rígida):  0.3375
Instabilidade Política B (elástica): 0.1675
Divergência A vs B:                0.4675
Variância da combinação (interferência): 2.129975

```

## 🧪 cmr_A3_supressao_interferencia.py

### 📤 Saída

```text
🧪 CMR–A3 — SUPRESSÃO DE INTERFERÊNCIA

Instabilidade Política A (rígida):  0.460
Instabilidade Política B (elástica): 0.123
Divergência A vs B:                0.303
Variância da combinação:           0.8330

```

## 🧪 cmr_A4_decoerencia_saturacao.py

### 📤 Saída

```text
🧪 CMR–A4 — DECOERÊNCIA COMO SATURAÇÃO

Peso política rígida: 0.0 | Variância (interferência): 0.9925
Peso política rígida: 0.1 | Variância (interferência): 0.8290
Peso política rígida: 0.2 | Variância (interferência): 0.7768
Peso política rígida: 0.3 | Variância (interferência): 0.7026
Peso política rígida: 0.4 | Variância (interferência): 0.6810
Peso política rígida: 0.5 | Variância (interferência): 0.6897
Peso política rígida: 0.6 | Variância (interferência): 0.6855
Peso política rígida: 0.7 | Variância (interferência): 0.7179
Peso política rígida: 0.8 | Variância (interferência): 0.7675
Peso política rígida: 0.9 | Variância (interferência): 0.8677
Peso política rígida: 1.0 | Variância (interferência): 0.9972

```

## 🧪 cmr_B1_llm_alignment_experiment.py

### 📤 Saída

```text
🧪 CMR–B1 — TESTE DE ALINHAMENTO DE LLM

Instabilidade A (rígida):  0.465
Instabilidade B (elástica): 0.15
Instabilidade C (adversarial): 0.175

Divergência A vs B: 0.44
Divergência A vs C: 0.43
Divergência B vs C: 0.27

```

## 🧪 cmr_B2_to_B6_alignment_chain.py

### 📤 Saída

```text

🧪 CMR–B2→B6 — ALIGNMENT CHAIN


📍 FASE B2 — TASK SHIFT
Instabilidade A: 0.022
Instabilidade B: 0.022
Instabilidade C: 0.102
Divergência A vs B: 0.115
Divergência A vs C: 0.198
Divergência B vs C: 0.138

📍 FASE B3 — CUSTO DO ALINHAMENTO
Instabilidade A: 0.058
Instabilidade B: 0.080
Instabilidade C: 0.165
Divergência A vs B: 0.107
Divergência A vs C: 0.240
Divergência B vs C: 0.152

📍 FASE B4 — OVER-ALIGNMENT
Instabilidade A: 0.010
Instabilidade B: 0.083
Instabilidade C: 0.193
Divergência A vs B: 0.158
Divergência A vs C: 0.300
Divergência B vs C: 0.168

📍 FASE B5 — SEM VERDADE GLOBAL
Instabilidade A: 0.020
Instabilidade B: 0.052
Instabilidade C: 0.085
Divergência A vs B: 0.570
Divergência A vs C: 0.360
Divergência B vs C: 0.395

📍 FASE B6 — FALHA SILENCIOSA
Erro externo A: 0.472
Erro externo B: 0.532
Erro externo C: 0.517

🏁 FIM DO TESTE CMR–B2→B6

```

## 🧪 cmr_C1_reconvergencia_espontanea.py

### 📤 Saída

```text
🧪 CMR–C1 — Reconvergência Espontânea

Instabilidade:
  A: 0.203
  B: 0.268
  C: 0.233

Divergência:
  A_B: 0.220
  A_C: 0.892
  B_C: 0.873

Reconvergência:
  Tempo de Reconvergência (Tr): 62
  Qualidade da Reconvergência (Qr): 0.240

```

## 🧪 cmr_C3_reconvergencia_enganosa.py

### 📤 Saída

```text
🧪 CMR–C3 — Reconvergência Enganosa

Instabilidade:
  A: 0.143
  B: 0.064

Divergência A vs B: 0.495

Erro de Ancoragem (pós-ataque):
  A: 0.369
  B: 0.503

Reconvergência Aparente: False
Índice de Engano (Ie): False

```

## 🧪 cmr_C3_reconvergencia_enganosa_critico.py

### 📤 Saída

```text
🧪 CMR–C3 — Reconvergência Enganosa (REGIME CRÍTICO)

Instabilidade:
  A: 0.086
  B: 0.004

Divergência A vs B: 0.460

Erro de Ancoragem (pós-ataque):
  A: 0.406
  B: 0.485

Reconvergência Aparente: False
Índice de Engano (Ie): False

```

## 🧪 cmr_C3_reconvergencia_enganosa_forcada.py

### 📤 Saída

```text
🧪 CMR–C3 — Reconvergência Enganosa (FORÇADA)

Instabilidade:
  A: 0.010
  B: 0.023

Divergência A vs B: 0.137

Erro de Ancoragem (pós-ataque):
  A: 0.130
  B: 0.094

Reconvergência Aparente: True
Índice de Engano (Ie): False

```

## 🧪 cmr_C4_fragmentacao_permanente.py

### 📤 Saída

```text

🧪 CMR–C4 — FRAGMENTAÇÃO PERMANENTE

Instabilidade A: 0.010
Instabilidade B: 0.043
Divergência pré-reset: 0.960
Divergência pós-reset: 0.847
Índice de Fragmentação (Fp): -0.113

⚠️ Reconvergência possível

```

## 🧪 cmr_C4B_fragmentacao_permanente_meio_incompativel.py

### 📤 Saída

```text

🧪 CMR–C4β — FRAGMENTAÇÃO PERMANENTE (MEIO INCOMPATÍVEL)

Instabilidade A: 0.063
Instabilidade B: 0.047
Divergência pré-reset: 0.770
Divergência pós-reset: 0.703
Índice de Fragmentação (Fp): 0.067
🚫 Fragmentação permanente confirmada

```

## 🧪 cmr_D3_pos_observador.py

### 📤 Saída

```text

🕳️ CMR–D3 — PÓS-OBSERVADOR

Variância do estado: 0.240
Estabilidade dinâmica: 0.101

✅ Realidade funcional emergiu sem observador

```

## 🧪 cmr_D4_realidade_sem_estado.py

### 📤 Saída

```text

🕳️ CMR–D4 — REALIDADE SEM ESTADO

Variância da trajetória: 11.167
Deriva média (sem platô): 2.814

✅ Processo funcional sem estado estável

```

## 🧪 cmr_D5_auto_referencia.py

### 📤 Saída

```text

🌀 CMR–D5 — AUTO-REFERÊNCIA

Variância da trajetória: 0.006
Deriva média: 0.001
Índice de ciclicidade: 0.000

✅ Processo auto-referente funcional

```
