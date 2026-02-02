# run.py
from campo import CampoCMR
from emissor import emitir
from receptor import observar
from observer_log import registrar

campo = CampoCMR()

real = emitir()
campo.excitar(real)

impactos = [campo.projetar() for _ in range(200)]

inferido = observar(impactos)

registrar(real, inferido)
