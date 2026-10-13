# from api_osv import API_OSV
# from business_object.dependency import Dependency

# dep = Dependency(1, "requests", "2.19.0")
# vulns = API_OSV.find_vulnerabilities(dep, "PyPI")

# for v in vulns:
#     print(type(v).__name__, v.osv_id, v.cve_id, v.package, v.version_package)
# python backend/src/api_osv/test_provisoire_api.py
import sys
from pathlib import Path

from api_osv import API_OSV
from business_object.dependency import Dependency

# ✅ Assure-toi que le dossier `backend/` est dans le PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


if __name__ == "__main__":
    print("🔍 Début du test manuel API_OSV...")
    try:
        # 1. Création de la dépendance à tester
        dep = Dependency(1, "requests", "2.19.0")
        print(f"📦 Test de la dépendance : {dep.name}@{dep.version}")

        # 2. Appel à l'API OSV
        vulns = API_OSV.find_vulnerabilities(dep, "PyPI")

        # 3. Affichage des résultats
        if not vulns:
            print("✅ Aucune vulnérabilité trouvée.")
        else:
            print(f"🐛 {len(vulns)} vulnérabilité(s) trouvée(s) :\n")
            for v in vulns:
                print(
                    f"  - [{v.__class__.__name__}] {v.osv_id} | CVE: {v.cve_id or 'N/A'} | {v.package}@{v.version_package}"
                )

    except Exception as e:
        print(f"❌ Échec du test : {e}")
        import traceback

        traceback.print_exc()
