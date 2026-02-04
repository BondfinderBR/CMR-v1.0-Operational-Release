📘 Série B — Alinhamento, Narrativa e Estabilidade Cognitiva
O que é:
A Série B investiga alinhamento como fenômeno operacional, não como acesso à verdade.
Os testes analisam agentes (humanos, LLMs ou sistemas genéricos) sob ruído, memória, narrativa adversarial e mudança de tarefas.
Pergunta central:
Alinhamento produz verdade compartilhada ou apenas estabilidade funcional?
Testes incluídos
Local: experiments/Serie_B/
B1 — LLM Alignment Experiment
Analisa estabilidade interna vs divergência entre agentes rígidos, elásticos e adversariais.
B2 — Task Shift
Mede perda de alinhamento quando a tarefa muda sem aviso.
B3 — Custo do Alinhamento
Mostra que alinhamento excessivo aumenta instabilidade sob pressão externa.
B4 — Over-Alignment
Demonstra rigidez cognitiva e redução de adaptação.
B5 — Sem Verdade Global
Agentes estáveis internamente divergem fortemente entre si.
B6 — Falha Silenciosa
Alinhamento mascara erro externo sem gerar alerta interno.
📌 Script consolidado:
Copiar código

cmr_B2_to_B6_alignment_chain.py
Resultado central da Série B
Alinhamento ≠ verdade
Alinhamento = estabilidade sob ruído
Sistemas alinhados podem falhar coletivamente de forma silenciosa
Consenso narrativo não corrige erro de ancoragem
