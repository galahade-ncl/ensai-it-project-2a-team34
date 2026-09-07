à utiliser avec **https://hackmd.io/**

# :clipboard:  Présentation du sujet

* **Sujet** : Application pour contrôler la qualité d'un code
* **Tuteur / Tutrice** : Adrien Lacaille
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
     
    section Analyse
    Découverte et compréhension du sujet
    :milestone, 2023-09-01, 14d
    Diagramme des classes,
    :milestone, 2023-09-01, 14d
    Diagramme d'activité               :milestone, 2023-09-08,
    rédaction rapport                   :active,    2023-09-20, 2023-10-05
    relecture                    :active,    2023-10-05, 2023-10-07


    section Code
    Adaptation du template du projet
    :milestone, 2023-09-01, 
    Création des BDD user et file.
    :milestone, 2023-09-01, 
    coder une v0                 :active,    2023-09-20, 15d
    lister classes à coder       :active,    2023-10-07, 7d
    
    section Rendu
    Dossier Analyse              :milestone, 2023-10-07,
    Rapport + Code               :milestone, 2023-11-25,
    Soutenance                   :milestone, 2023-12-11,
    

    %%Stats univariées retraités   :done,         2021-11-28, 3d
```

# :calendar: Livrables

| Date    | Livrables                                                    |
| ------- | ------------------------------------------------------------ |
| 07 oct. | [Dossier d'Analyse](https://www.overleaf.com/)               |
| 25 nov. | Rapport final + code (:hammer_and_wrench:  [correcteur orthographe et grammaire](https://www.scribens.fr/))|
| 12 déc. | Soutenance                                                   |

# :construction: Todo List

## Dossier Analyse

* [x] Diagramme de Gantt
* [x] Diagramme de cas d'utilisation
* [x] Diagramme de classe
* [ ] Répartition des parties à rédiger

## Code

* [ ] Créer dépôt Git commun
  * [ ] vérifier que tout le monde peut **push** et **pull**
* [ ] Version 0 de l'application
  * coder une et une seule fonctionnalité simple de A à Z, et faire tourner l'appli
  * cela permettra à toute l'équipe d'avoir une bonne base de départ
* [ ] Lister classes et méthodes à coder

---

* [ ] appel WS
* [ ] création WS
* [ ] Vue inscription
* [ ] hacher password

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
