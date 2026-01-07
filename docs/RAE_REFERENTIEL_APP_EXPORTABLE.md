📦 RAE — Référentiel App Exportable
IKOMA MCP 2.0

Statut : Annexe descriptive – non normative – informative

1. Rôle du RAE

Le RAE définit ce qu’une application est capable d’exporter vers l’extérieur afin d’être :

déployable par un moteur tiers (IKOMA MCP),

restaurable hors plateforme d’origine (Lovable, Bolt, Codex, Manus),

reproductible sur un serveur souverain.

👉 Le RAE ne contraint pas le moteur.
👉 Le RAE décrit le terrain réel des apps IA Dev.

2. Principe fondamental

Une application compatible IKOMA MCP 2.0 est une application qui :

expose des fichiers explicites

sépare code / données / configuration

n’impose aucune dépendance implicite à une plateforme SaaS

peut être exécutée sans son générateur

3. Catégories de fichiers exportables
3.1 Fichiers racine (socle applicatif)
Fichier	Rôle	Exportable
index.html	Point d’entrée web	Oui
package.json	Dépendances & scripts	Oui
package-lock.json / bun.lockb	Verrou versions	Oui
README.md	Documentation humaine	Oui
.gitignore	Hygiène dépôt	Oui
vite.config.ts	Configuration bundler	Oui
tsconfig*.json	Configuration TypeScript	Oui
tailwind.config.ts	Design system	Oui
postcss.config.js	Pipeline CSS	Oui
eslint.config.js	Qualité code	Oui
components.json	shadcn/ui config	Oui
3.2 Dossier src/ (code applicatif)

Exportable dans son intégralité.

Inclut notamment :

src/main.tsx – bootstrap

src/App.tsx – point de routage

src/pages/* – vues

src/components/* – composants métier

src/components/ui/* – UI générée

src/services/* – logique API

src/hooks/*

src/contexts/*

src/types/*

src/utils/*

src/assets/*

👉 Le moteur ne présume rien du contenu.
👉 Il ne fait qu’orchestrer ce qui existe.

3.3 Dossier public/ (assets statiques)
Élément	Exportable
favicon.ico	Oui
robots.txt	Oui
manifest.json (PWA)	Si présent
sw.js (Service Worker)	Si présent
images/*	Oui
3.4 Dossier supabase/ (si backend cloud activé)

Exportable si et seulement si présent.

Élément	Rôle
supabase/config.toml	Configuration
supabase/migrations/*.sql	État DB
supabase/functions/*	Fonctions Edge

⚠️ Les migrations sont des faits, pas des scripts optionnels.

4. Fichiers NON inclus volontairement
Élément	Raison
.env	Secret local
.env.production	Secret sensible
node_modules/	Reproductible
dist/	Artefact
.lovable/ / .bolt/	Dépendance plateforme
.venv/	Environnement local

👉 Les secrets sont injectés par le moteur, jamais stockés.

5. Ce que le RAE ne fait PAS

❌ n’impose aucune stack

❌ ne définit aucun port

❌ ne parle pas de Docker

❌ ne parle pas de domaine

❌ ne contraint pas la Loi IKOMA MCP

6. Lien avec IKOMA MCP 2.0

Le MCP lit les livrables décrits par le RAE

Le Runner exécute sans interpréter

Le Gateway connecte sans modifier

👉 Le RAE est un contrat de lisibilité, pas un contrat d’exécution.

7. Phrase de clôture (à laisser telle quelle)

Le RAE décrit ce qu’une application peut livrer.
Il ne décide ni de son exécution, ni de son exposition, ni de sa gouvernance.
