# Thomas le fait

ensai-it-2a-team34/
│
├── .github/                          # Configuration CI/CD (GitHub Actions)
├── .vscode/                          # Fichiers de configuration vscode
│
├── backend/                          
│   ├── logs/                         # fichiers contenant les logs du backend
│   │
│   ├── src/                          # Code source principal
│   │   ├── api_deps_dev/
│   │   │   ├── __init__.py
│   │   │   └── api_deps_dev.py
│   │   ├── api_osv/
│   │   │   ├── __init__.py
│   │   │   ├── api_osv.py
│   │   │   └── test_provisoire_api.py
│   │   ├── business_object/                          
│   │   │   ├── antipattern/
│   │   │   │   ├── anttipatern.py
│   │   │   │   ├── nestedloop.py
│   │   │   │   └── recursivecall.py
│   │   │   ├── file/
│   │   │   │   ├── certificatefile.py
│   │   │   │   ├── codefile.py
│   │   │   │   ├── dependancyfile.py
│   │   │   │   ├── file.py
│   │   │   │   └── sbomfile.py



## Template
│   │   ├── controllers/
│   │   │   └── userController.js  
│   ├── 📂 controllers/       # Logique de routage et réception des requêtes (API/Backend)
│   │   └── userController.js
│   │
│   ├── 📂 models/            # Structures de données et schémas (Base de données)
│   │   └── userModel.js
│   │
│   ├── 📂 routes/            # Définition des points d'accès (Endpoints)
│   │   └── userRoutes.js
│   │
│   ├── 📂 services/          # Logique métier (Business logic) du projet
│   │   └── userService.js
│   │
│   ├── 📂 utils/             # Fonctions d'aide et outils génériques (helpers, multi-usage)
│   │
│   ├── app.js                # Point d'entrée de l'application (initialisation)
│   └── server.js             # Démarrage du serveur web
│
├── 📂 tests/                 # Tests unitaires et d'intégration
│   ├── user.test.js
│   └── setup.js
│
├── .env.example              # Modèle de configuration des variables d'environnement
├── .gitignore                # Fichiers et dossiers à ignorer par Git
├── package.json              # Dépendances et scripts du projet (Node.js/JS exemple)
└── README.md                 # Documentation principale du projet
