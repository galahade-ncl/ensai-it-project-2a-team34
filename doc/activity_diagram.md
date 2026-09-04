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
    login : Login
    menu_player : Menu Utilisateur
    signup : Sign Up
    ajout_projet : Importer un projet
    fournir_clef : Fournir une clef pour la clef Hmac
    check_clef : Vérification de la clef
    fournir_fichiers : Fournir les fichiers du projet (code et fichier de dépendance)
    liste_fichier : Fichier importé dans la liste des fichier
    code_check : Examiner un projet (2 fichiers)
    fichier_1 : Code
    fichier_2 : Fichier de dépendance
    vulnerability_list : Liste des vulnérabilités détéctées et contrôles effectués
    logout : Logout

    [*] --> Home

    Home --> login
    login --> menu_player

    Home --> signup

    Home --> quit
    quit --> [*]

    state menu_player {
        [*] --> ajout_projet
        ajout_projet --> fournir_clef
        fournir_clef --> check_clef
        check_clef --> liste_fichier
        ajout_projet --> fournir_fichiers
        fournir_fichiers --> liste_fichier
        [*] --> code_check
        code_check --> fichier_1
        fichier_1 --> vulnerability_list
        code_check --> fichier_2
        fichier_2 --> vulnerability_list
        [*] --> logout
        logout --> [*]: return to home
    }
```