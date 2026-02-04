import subprocess
from pathlib import Path
from datetime import datetime

# Lista explícita dos testes
TESTS = [
    "cmr_A2_interferencia_politicas.py",
    "cmr_A3_supressao_interferencia.py",
    "cmr_A4_decoerencia_saturacao.py",
    "cmr_B1_llm_alignment_experiment.py",
    "cmr_B2_to_B6_alignment_chain.py",
    "cmr_C1_reconvergencia_espontanea.py",
    "cmr_C3_reconvergencia_enganosa.py",
    "cmr_C3_reconvergencia_enganosa_critico.py",
    "cmr_C3_reconvergencia_enganosa_forcada.py",
    "cmr_C4_fragmentacao_permanente.py",
    "cmr_C4B_fragmentacao_permanente_meio_incompativel.py",
    "cmr_D3_pos_observador.py",
    "cmr_D4_realidade_sem_estado.py",
    "cmr_D5_auto_referencia.py",
]

REPORT = Path("CMR_Experimental_Report.md")

with REPORT.open("w", encoding="utf-8") as f:
    f.write("# 📄 CMR — Relatório Experimental Consolidado\n\n")
    f.write(f"**Gerado automaticamente em:** {datetime.now()}\n\n---\n")

    for test in TESTS:
        f.write(f"\n## 🧪 {test}\n\n")

        if not Path(test).exists():
            f.write("### ❌ Arquivo não encontrado\n\n")
            continue

        try:
            result = subprocess.run(
                ["python", test],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.stdout.strip():
                f.write("### 📤 Saída\n\n```text\n")
                f.write(result.stdout)
                f.write("\n```\n")

            if result.stderr.strip():
                f.write("### ⚠️ Erro\n\n```text\n")
                f.write(result.stderr)
                f.write("\n```\n")

        except Exception as e:
            f.write("### ❌ Falha de execução\n\n")
            f.write(f"`{e}`\n")
