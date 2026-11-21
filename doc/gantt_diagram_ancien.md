à utiliser avec **https://hackmd.io/**

# :clipboard:  Présentation du sujet

* **Sujet** : Application pour contrôler la qualité d'un code
* **Tuteur / Tutrice** : Adrien Lacaille
* [Dépôt GitHub](https://github.com/galahade-ncl/ensai-it-project-2a-team34.git)

# :dart: Planning des avancées et prévisionnel



```mermaid
gantt
    %% doc : https://mermaid-js.github.io/mermaid/#/./gantt
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b
    title       Diagramme de Gantt
    %%excludes  YYYY-MM-DD and/or sunday and/or weekends 
     
    section Analyse  
    Découverte et compréhension du sujet        :active, 2023-09-01, 14d
    Diagramme des classes                       :active, 2023-09-01, 14d
    Diagramme d'activité                        :milestone, 2023-09-08,
    Diagramme de cas d'utilisation et de Gantt             :milestone, 2023-09-13
    Rédaction dossier d'analyse                           :active,    2023-09-12, 2023-09-17
    Relecture                                   :active,    2023-09-16, 2023-09-17
    Rédaction du rapport                           :active,    2023-10-12, 2023-11-20
    Relecture                                   :active,    2023-11-17, 2023-11-20


    section Code
    Adaptation du template du projet            :milestone, 2023-09-01, 
    Création des BDD                      :active, 2023-09-01, 33d 
    Lister les classes à coder                       :active,    2023-09-07, 7d
    Implémenter les classes business object       :active, 2023-09-20, 14d
    Mise en place de la DAO (v0)                        :active,    2023-09-30, 15d
    Coder user et project service (v0)                        :active,    2023-10-4, 15d
    Mise en place de l'API (v0)                        :active,    2023-10-4, 15d
    Coder l'audit service (v0)                            :active,    2023-10-10, 25d
    Gestion des bugs et améliorations                      :active,    2023-10-18, 33d
    Ajout de fonctionnalités obtionnelles (facultatif)   :active, 2023-11-01, 19d

    
    section Rendu
    Dossier Analyse              :milestone, 2023-09-17,
    Rapport + Code               :milestone, 2023-11-21,
    Soutenance                   :milestone, 2023-12-11,
    

    %%Stats univariées retraités   :done,         2021-11-28, 3d
```

# :calendar: Livrables

| Date    | Livrables                                                    |
| ------- | ------------------------------------------------------------ |
| 07 oct. | Dossier d'Analyse             |
| 25 nov. | Rapport final + code (:hammer_and_wrench:  [correcteur orthographe et grammaire](https://www.scribens.fr/))|
| 12 déc. | Soutenance                                                   |

# :construction: Todo List

## Dossier Analyse

* [ ] Diagramme de Gantt 
* [ ] Diagramme de cas d'utilisation
* [x] Diagramme de classe
* [x] Diagramme physique des données
* [ ] Répartition des parties à rédiger

## Code

* [x] Créer dépôt Git commun
  * [x] vérifier que tout le monde peut **push** et **pull**
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
