# BUILD-2B — Observabilité & Preuve (Read-Only)

## Périmètre

BUILD-2B introduit des capteurs read-only qui produisent des faits observables et des évidences
primaires/secondaires sans exécution, sans correction automatique, sans heuristique.

## Non-objectifs

- Aucune action sur le système (start/stop/restart interdits).
- Aucun scan réseau agressif.
- Aucun scoring, aucun “best effort”.
- Aucune décision automatique : sans preuve primaire → UNKNOWN + trace.

## Capteurs read-only

### Processus (PID)
- Fait : `process.status` (présent/absent, état).
- Évidence primaire : `process <pid> present/absent`.

### Ports locaux
- Fait : `port.listen` (listening/absent).
- Évidence primaire : `port <port> listening/absent`.

### Fichiers / artefacts
- Fait : `file.status` (present/absent).
- Évidence primaire : `file <path> present/absent`.
- Évidence secondaire (optionnelle) : checksum SHA256.

### Services (systemd)
- Fait : `systemd.unit` (loaded/absent via runtime).
- Évidence secondaire : `systemd unit <name> loaded/absent`.

## Exemples de faits

- `process.status` avec `pid=1234`, `status=present`, `state=R`.
- `port.listen` avec `port=8080`, `status=listening`.
- `file.status` avec `path=/etc/ikoma/manifest`, `status=absent`.
- `systemd.unit` avec `unit=nginx.service`, `status=loaded`.

## Alimentation des états (sans décision)

Les capteurs produisent des faits et des évidences. La gouvernance applique :

- Sans évidence primaire : état UNKNOWN + trace.
- Avec évidence primaire : état éligible (UP/DOWN) selon les Actes II–III.

Aucune transition n’est déclenchée ici.
