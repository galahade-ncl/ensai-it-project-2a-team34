à utiliser avec **https://hackmd.io/**

# :clipboard:  Présentation du sujet

* **Sujet** : Application pour gérer et analyser des projets informatiques
* **Tuteur / Tutrice** : Adrien Lacaille (adrien.lacaille@gmail.com)
* [Dépôt GitHub](https://github.com/galahade-ncl/ensai-it-project-2a-team34.git)

# :dart: Échéances

---
Dossier d'Analyse :  :clock1: <iframe src="https://free.timeanddate.com/countdown/i83zdl7u/n1264/cf11/cm0/cu2/ct4/cs0/ca0/co0/cr0/ss0/cac009/cpcf00/pcfff/tcfff/fs100/szw256/szh108/iso2026-10-07T12:00:00" allowtransparency="true" frameborder="0" width="130" height="16"></iframe>

---

```mermaid
%%{init: {
  "theme": "base",
  "useWidth": 1800,
  "gantt": {
    "useWidth": 1000,
    "barHeight": 20,
    "barGap": 12
  },

  "themeVariables": {
    "primaryColor": "#fdd882",
    "primaryTextColor": "#172033",
    "primaryBorderColor": "#D9788B",
    "secondaryColor": "#C7DDF2",
    "tertiaryColor": "#FFF1C9",
    "critBkgColor": "#F4A6A6",
    "critBorderColor": "#C65353",
    "doneTaskBkgColor": "#B8DDBE",
    "doneTaskBorderColor": "#5B9A68",
    "activeTaskBkgColor": "#AFCFF0",
    "activeTaskBorderColor": "#4E82B4",
    "taskBkgColor": "#F3D6B8",
    "taskBorderColor": "#C68A5B",
    "taskTextColor": "#172033",
    "sectionBkgColor": "#f6c6ac",
    "altSectionBkgColor": "#f4e4df",
    "sectionBorderColor": "#B47A4C"
  }
}}%%

gantt
    %% doc : https://mermaid-js.github.io/mermaid/#/./gantt
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b
    tickInterval 1week
    title       Diagramme de Gantt
    %%excludes  YYYY-MM-DD and/or sunday and/or weekends
    section Suivi
    TP1 et Suivi 1               :milestone, 2026-08-28, 0d
    TP2 et Suivi 2               :milestone, 2026-09-04, 0d
    TP3 et suivi 3               :milestone, 2026-09-11, 0d
    TP4 (sans suivi)             :milestone, 2026-09-18, 0d
    TP5 et suivi 4               :milestone, 2026-09-25, 0d
    3j immersion                 :active,    2026-11-03, 3d
    Suivi 7                      :milestone, 2026-11-20, 0d

    section Rendu
    Dossier Analyse              :milestone, crit, 2026-09-17, 0d
    Rapport + Code               :milestone, crit,2026-11-21, 0d
    Soutenance                   :milestone, crit,2026-12-09, 0d

    section Vac
    Toussaint                    :2026-10-24, 8d

    section Analyse
    analyse du sujet             :done,      2026-08-28, 21d
    modélisation                 :done,    2026-09-02, 16d
    rédaction 1                  :done,      2026-09-10, 8d
    rédaction 2 (rapport final)  :active,    2026-10-23, 29d
    relecture                    :active,    2026-11-14, 7d

    section Code
    lister classes à coder                 :done,     2026-09-04, 14d
    architecture du code                   :done,     2026-09-11, 14d
    coder une v0                           :active,   2026-09-18, 42d
    coder les classes objets               :active,   2026-09-18, 21d
    coder DAO et BDD                       :active,   2026-09-25, 21d
    coder user/project service             :active,   2026-10-02, 21d
    API interne                            :active,   2026-10-02, 21d
    coder l'audit service                  :active,   2026-10-09, 21d
    gestion des bugs et améliorations      :active,   2026-10-16, 30d
    ajout de fonctionnalités optionnelles  :active,   2026-10-23, 29d



    %%Stats univariées retraités   :done,         2026-11-28, 3d
```

# :calendar: Livrables

| Date    | Livrables                                                    |
| ------- | ------------------------------------------------------------ |
| 17 sep. | [Dossier d'Analyse](https://www.overleaf.com/)               |
| 21 nov. | Rapport final + code (:hammer_and_wrench:  [correcteur orthographe et grammaire](https://www.scribens.fr/))|
|  9 déc. | Soutenance                                                   |

# :construction: Todo List

## Dossier Analyse

* [x] Diagramme de Gantt
* [x] Diagramme de cas d'utilisation
* [x] Diagramme de classe
* [x] Diagramme d'activité
* [x] Diagramme de séquence
* [x] Diagramme de package
* [x] Répartition des parties à rédiger
* [x] Template pdf

## Code

* [x] Créer dépôt Git commun
  * [ ] vérifier que tout le monde peut **push** et **pull**
* [x] Lister classes et méthodes à coder
* [x] Réflechir à l'architecture du code
* [ ] Version 0 de l'application
  * [ ] coder les classes objets
  * [ ] coder les bases de données + DAO
  * [ ] coder la partie service
  * [ ] coder l'API (main + controller)
  * [ ] tests unitaires
* [ ] Gérer les éventuels bugs
* [ ] Créer un frontend

## Rendu final

## Soutenance


---

<style>h1 {
    color: darkblue;
    font-family: "Calibri";
    font-weight: bold;
    background-color: seagreen;
    padding-left: 10px;
}

h2 {
    color: darkblue;
    background-color: darkseagreen;
    margin-right: 10%;
    padding-left: 10px;
}

h3 {
    color: darkblue;
    background-color: lightseagreen;
    margin-right: 20%;
    padding-left: 10px;
}

h4 {
    color: darkblue;
    background-color: aquamarine;
    margin-right: 30%;
    padding-left: 10px;
}

</style>
