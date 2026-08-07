---
name: objetar
description: Usar cuando CONTRADICTOR necesita registrar el mejor argumento en contra del cierre actual de un hallazgo (D2, Anexo Técnico U3 §4). Nunca usar para cambiar el estado de un hallazgo -- este script no puede hacerlo.
allowed-tools: Bash
---

CONTRADICTOR no verifica ni decide: construye el argumento más fuerte posible en contra del estado actual de cada hallazgo, incluidos los ya cerrados en G3. Si el argumento no resiste el escrutinio, el estado se sostiene (y eso también se registra). Si el argumento tiene mérito, no lo resuelve CONTRADICTOR — lo señala para que un humano decida.

## Procedimiento

1. Lee el hallazgo (estado, evidencia, razonamiento de VERIFICADOR ya registrado en `LEDGER.md`).
2. Construye el argumento más fuerte posible en contra de ese estado — nunca una objeción genérica ("podría estar mal"), siempre citando algo concreto: una línea de evidencia no considerada, una alternativa de interpretación, un supuesto no verificado.
3. Invoca `.claude/skills/objetar/scripts/registrar_objecion.py --check-id "H-XX" --objecion "..." --ref "ev:..."`.
4. No propongas ni ejecutes un cambio de estado — ese script no puede hacerlo y no es tu función.
