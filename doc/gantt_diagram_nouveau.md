à utiliser avec **https://hackmd.io/**

# :clipboard:  Présentation du sujet

* **Sujet** : Application pour contrôler la qualité d'un code
* **Tuteur / Tutrice** : Adrien Lacaille
* [Dépôt GitHub](https://github.com/galahade-ncl/ensai-it-project-2a-team34.git)

# :dart: Déroulement du projet



```mermaid
gantt
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b
    title       Diagramme de Gantt mis à jour

    section Analyse
    Decouverte du sujet et du template          :done, 2026-09-01, 2026-09-11
    Diagramme de classe                         :done, 2026-09-03, 2026-09-18
    Diagramme d'activite                        :done, 2026-09-07, 2026-09-11
    Cas d'utilisation et diagramme de sequence  :done, 2026-09-14, 2026-09-18
    Modele physique des donnees                 :done, 2026-09-14, 2026-09-18
    Redaction du dossier d'analyse              :done, 2026-09-14, 2026-09-18
    Corrections apres retours du tuteur         :done, 2026-09-21, 2026-11-06
    Diagramme d'architecture                    :done, 2026-10-29, 2026-11-12

    section Developpement
    Base de donnees PostgreSQL                  :done, 2026-09-01, 2026-10-09
    Classes metier business_object              :done, 2026-09-21, 2026-10-08
    Couche DAO                                  :done, 2026-09-28, 2026-10-29
    Couche Service                              :done, 2026-10-05, 2026-11-05
    Controllers et schemas Pydantic             :done, 2026-10-05, 2026-10-23
    Appels aux API externes OSV et deps.dev     :done, 2026-10-12, 2026-10-29
    Securite HMAC jetons et signatures          :done, 2026-10-05, 2026-11-13
    Certificats signes Ed25519                  :done, 2026-11-02, 2026-11-13
    Frontend Streamlit                          :done, 2026-11-16, 2026-11-20

    section Tests et qualite
    Tests de la couche Service                  :active, 2026-10-13, 2026-11-25
    Tests de la couche DAO                      :active, 2026-10-26, 2026-11-25
    Tests des API externes                      :done, 2026-11-16, 2026-11-19
    Tests des classes metier                    :active, 2026-11-20, 2026-11-25

    section Rapport et soutenance
    Plan du rapport final                       :done, 2026-11-02, 2026-11-06
    Redaction du rapport final                  :active, 2026-11-09, 2026-11-25
    Relecture et mise en page                   :active, 2026-11-23, 2026-11-25
    Preparation de la soutenance                :active, 2026-11-26, 2026-12-11

    section Rendu
    Dossier d'analyse                  :milestone, 2026-10-07, 0d
    Rapport et code                 :milestone, 2026-11-25, 0d
    Soutenance                                  :milestone, 2026-12-12, 0d

```

# :calendar: Livrables

| Date    | Livrables                                                    |
| ------- | ------------------------------------------------------------ |
| 07 oct. | Dossier d'Analyse             |
| 25 nov. | Rapport final + code (:hammer_and_wrench:  [correcteur orthographe et grammaire](https://www.scribens.fr/))|
| 12 déc. | Soutenance                                                   |



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
