# Sécurité, confidentialité et limites

- **Pas de réseau** : Arketype fonctionne hors ligne; aucune clé/token n’est requis. Les exemples n’autorisent aucune publication ni activation.
- **Local Kit propriétaire** : `arketype.py` appelle le vrai `outils/kristal.py init` et `check`. Il n’implémente pas son propre moteur de state commitment.
- **Préservation** : refuse les slugs non sûrs, vérifie que le dossier parent existe, crée en staging au même niveau, ne remplace jamais une destination préexistante, supprime le staging après erreur.
- **Domaine neutre** : zéro assertion métier, `canon/state.index.json` vide, `design/` hors canon, `arketype.instance.json` hors canon.
- **Composition limitée** : un plan est produit, pas un assemblage de fichiers de connaissance. Les références de preuve ne sont pas inventées.
- **Pas de transfert d'autorité** : les noms PoliceOps, HospitalOps et MediKristal sont des cas de description de structure, pas des protocoles validés, des conseils médicaux, des mandats légaux ou des droits d'exécution.
- **Données sensibles** : ne pas placer des dossiers individuels, données de patients, secrets, clés ou renseignements confidentiels dans des modèles ni des releases publiques; les ACL doivent être appliquées par les propriétaires.
- **Conformité technique bornée** : `check` vérifie un workspace, pas la justesse des assertions, la légalité des contenus, les contrats de domaine ni les interopérabilités avec Moodle/Kompiler/Konstellation.
- **Interface Windows** : `Lancer_Arketype.pyw` nécessite Python 3.10+ avec Tkinter. Non exécutée graphiquement sur un poste Windows dans cet environnement.
- **Évolution** : les versions de Framework/Kit sont épinglées à celles des archives examinées; vérifier toute compatibilité lors de la mise à jour.

## Contrôles effectués ici

- Audit en lecture seule du catalogue et des modèles.
- `check` du Local Kit pour chaque modèle.
- Tests d'instances et de plans, sans données externes ni réseau.
- Aucune évaluation clinique, scientifique ou juridique effectuée.

## Dépositions / témoignages (ARK-16)

- Les modèles et l’interface de création n’enregistrent pas les témoignages. `design/fiche-deposition-vierge.json` est un schéma illustratif, pas un formulaire opérationnel sécurisé.
- Confidentialité par défaut; ne pas recopier d'identités, d'audio, de vidéos, de pièces ou de propos sensibles dans le dépôt ou un Context Pack public.
- La signature, l'assermentation, la validité légale, l'identification, la conservation des preuves, les droits d'accès et la rétention nécessitent des systèmes et procédures compétents.
- Ne pas transformer une affirmation en fait ni confondre empreinte de représentation et authenticité du témoin.
