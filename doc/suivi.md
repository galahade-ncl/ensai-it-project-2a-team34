à utiliser avec **https://hackmd.io/**

# :clipboard:  Présentation du sujet

* **Sujet** : Application pour gérer et analyser des projets informatiques
* **Tuteur / Tutrice** : Adrien Lacaille (adrien.lacaille@gmail.com)
* [Dépôt GitHub](https://github.com/galahade-ncl/ensai-it-project-2a-team34.git)

# :dart: Échéances

---
Dossier d'Analyse :  :clock1: <iframe src="https://free.timeanddate.com/countdown/i83zdl7u/n1264/cf11/cm0/cu2/ct4/cs0/ca0/co0/cr0/ss0/cac009/cpcf00/pcfff/tcfff/fs100/szw256/szh108/iso2023-10-07T12:00:00" allowtransparency="true" frameborder="0" width="130" height="16"></iframe>

---

```mermaid
gantt
    %% doc : https://mermaid-js.github.io/mermaid/#/./gantt
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b
    title       Diagramme de Gantt
    %%excludes  YYYY-MM-DD and/or sunday and/or weekends 
    section Suivi
    TP1 et Suivi 1               :milestone, 2023-09-01,
    TP2 et Suivi 2               :milestone, 2023-09-08,
    TP3 et suivi 3                         :milestone, 2023-09-15,
    TP4                
    :milestone, 2023-09-29,
    Suivi 4                      :milestone, 2023-10-13,
    3j immersion                 :active,    2023-10-25, 3d
    Suivi 7                      :milestone, 2023-11-17,
    
    section Rendu
    Dossier Analyse              :milestone, 2023-10-07,
    Rapport + Code               :milestone, 2023-11-25,
    Soutenance                   :milestone, 2023-12-11,
    
    section Vac
    Toussaint                    :crit,    2023-10-28, 2023-11-05
    
    section Analyse
    analyse sujet                :done,      2023-09-01, 15d
    modélisation                 :active,    2023-09-08, 15d
    rédaction                    :active,    2023-09-20, 2023-10-05
    relecture                    :active,    2023-10-05, 2023-10-07
    
    section Code
    coder une v0                 :active,    2023-09-20, 15d
    lister classes à coder       :active,    2023-10-07, 7d
    

    %%Stats univariées retraités   :done,         2021-11-28, 3d
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
