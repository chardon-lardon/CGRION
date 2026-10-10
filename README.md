# CGRION — première interface

## Démarrer

1. Installe Python 3 avec la prise en charge de Tcl/Tk et IDLE
   (option proposée par l'installateur officiel sur Windows).
2. Décompresse l'archive et ouvre le dossier CGRION dans VS Code.
3. Ouvre le terminal dans ce dossier et lance `python main.py`
   (ou `py main.py` sur Windows).
4. Écris ta demande puis clique sur Envoyer, ou appuie sur Entrée.
5. Ferme la fenêtre pour quitter.

L'interface utilise Tkinter, fourni avec les installations usuelles de Python.
Si une erreur indique que tkinter manque, ajoute la prise en charge Tcl/Tk
via ton installation Python.

## Fichiers

| Fichier | Rôle |
| --- | --- |
| main.py | Ouvre l'interface. |
| ui.py | Construit la fenêtre et gère l'envoi des messages. |
| assistant.py | Coordonne la réponse et la mémoire. |
| ai.py | Renvoie une réponse provisoire ; le modèle local reste à connecter. |
| memory.py | Garde les échanges pendant l'exécution. |
| config.py | Contient le nom du programme et le chemin des données. |
| data/ | Dossier réservé à la future mémoire sauvegardée. |

## Le code de l'interface, simplement

- `ChatWindow` regroupe la fenêtre et ses éléments.
- `Label` affiche le titre et les textes descriptifs.
- `ScrolledText` affiche une conversation avec une barre de défilement.
- `Entry` est le champ dans lequel tu écris.
- `Button` déclenche `send_message` quand tu cliques sur Envoyer.
- `grid` organise les éléments en lignes et colonnes.
- `send_message` ignore une demande vide, affiche ta demande, appelle
  `respond` puis affiche la réponse. Il vide ensuite le champ pour la suite.
- `append_message` ajoute du texte dans la conversation. La zone reste
  protégée contre la modification manuelle.
- `launch` crée la fenêtre ; `mainloop` la garde ouverte et attend tes actions.

## Limites actuelles

La réponse est fixe : aucun modèle d'IA n'est connecté et aucun accès réseau
n'est effectué. L’écran est réinitialisé à la fermeture ; les échanges restent sauvegardés localement dans `data/history.json`.
L'appel à l'assistant est immédiat ici ; avant de connecter un modèle plus lent,
il faudra exécuter cet appel en arrière-plan pour garder la fenêtre réactive.

## Nouveautés

- **Message d'accueil** au démarrage et après Nouvelle conversation.
- **Effacer** vide la conversation affichée et le champ de saisie. Il conserve l'historique.
- **Historique** ouvre les échanges précédents, datés et regroupés par conversation.
- **Nouvelle conversation** commence un nouveau groupe d'échanges et réaffiche l'accueil.

`memory.py` lit et écrit un fichier JSON (un fichier texte structuré). Chaque échange
contient la demande, la réponse, la date et un identifiant de conversation.
La sauvegarde intervient après chaque réponse. Si le fichier est endommagé,
une erreur s'affiche et il n'est pas écrasé.

Pour mettre à jour une installation existante, remplace les fichiers Python et
README.md ; conserve ton dossier data/ pour garder ton historique.

## Épurer l'historique

Le bouton **Épurer l’historique** demande confirmation Oui/Non (les libellés
natifs suivent la langue du système). Oui supprime tous les échanges
sauvegardés et ferme les fenêtres d'historique ouvertes. Non conserve
l'état précédent. La conversation actuellement affichée reste visible.
Les prochains échanges seront sauvegardés normalement.
