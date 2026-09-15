# Diagramme d'activité

> Un diagramme UML d'activité modélise le flux de travail d'un processus, montrant la séquence d'activités et de décisions dans un système. Il illustre comment les actions s'enchaînent et comment les choix sont faits.

Ce diagramme est codé avec [mermaid](https://mermaid.js.org/syntax/stateDiagram.html) :

- avantage : facile à coder
- inconvénient : on ne maîtrise pas bien l'affichage

Pour afficher ce diagramme dans VScode :

- à gauche aller dans **Extensions** (ou CTRL + SHIFT + X)
- rechercher `mermaid`
  - installer l'extension **Markdown Preview Mermaid Support**
- revenir sur ce fichier
  - faire **CTRL + K**, puis **V**


```mermaid
stateDiagram
    login : Connexion
    menu_player : Menu Utilisateur
    signup : Créer un compte
    ajout_projet : Importer un projet
    update_project : Modifier un projet
    update_dependencies : Modifier le fichier de dépendances
    update_code : Modifier le fichier de code
    fournir_clef : Fournir une clef secrète pour la clef HMAC
    fournir_fichiers : Fournir les fichiers du projet (code et fichier de dépendances)
    select_project : Sélectionner un projet
    code_check :  Demander un audit
    audit_history : Consulter l'historique des audits
    project_history : Consulter l'historique des fichiers
    dashboard : Tableau de bord
    audit_result : Résultat de l'audit
    logout : Déconnexion

    [*] --> Accueil

    Accueil --> login
    login --> menu_player

    Accueil --> signup

    Accueil --> Quitter

    state menu_player {
        [*] --> dashboard
        dashboard --> ajout_projet
        ajout_projet --> fournir_clef
        ajout_projet --> fournir_fichiers
        dashboard --> code_check
        code_check --> select_project
        select_project --> audit_result
        dashboard --> audit_history
        dashboard --> project_history
        dashboard --> update_project
        update_project --> update_code
        update_project --> update_dependencies
        dashboard --> logout
        logout --> [*]:  retour à l'accueil
    }
```