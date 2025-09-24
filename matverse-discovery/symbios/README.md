# SYMBIOS — Provas Criptográficas de Originalidade

Ferramentas para gerar árvores de Merkle determinísticas, emitir provas de inclusão
O(log n) e validar autoria de artefatos digitais.

## Uso rápido

```bash
python symbios/cli_verifier.py symbios/proofs/exemplo.json
```

A CLI retorna `OK` se a prova corresponder à raiz registrada.
