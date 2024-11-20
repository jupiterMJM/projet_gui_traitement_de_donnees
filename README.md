Projet : Interface graphique pour affichage des données du TOF
Auteur : Maxence BARRE

Utilisation :
- Enregistrer les données des 2 TOF au format .h5 .
  - Attention : les données doivent être compatibles avec l'algorithme d'ouverture (voir fichier ouverture_et_traitement_de_fichier.py)
- Enregistrer les données de la théorie au format .txt
  - Attention : les données de la théorie doivent d'abord contenir toutes les données de QUEL AXE puis les données de QUEL AXE (voir fichir ouverture_et_traitement_de_fichier.py > fonction apply_theory_on_bottle1)
- Lancer le fichier interface_graphique.py
- Renseigner toutes les informations. Une fois que toutes les données sont rentrées, appuyer sur "Submit" et les données apparaissent
  - Note : rien ne s'affichera tant qu'il reste des informations en rouge (= non remplies)


Roadmap :
- vérification de la cohérence des graphiques
- ajouter un encadré de notes
- permettre l'enregistrement des graphiques et du workspace
- mieux gérer les erreurs (éviter les erreurs fatales)
- mieux organiser l'affichage pour entrer les données