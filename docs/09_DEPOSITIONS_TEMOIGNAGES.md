# ARK-16 — Dépositions et témoignages

## Raison d'être

Conserver de façon traçable **la déclaration attribuée à une personne dans un contexte de recueil**, sans conclure à la vérité des propos. La structure ne dépend pas d'un usage particulier : enquête interne, histoire orale, recherche qualitative, audition, incident, projet communautaire. Les exigences de collecte et les droits varient selon le contexte.

## Objets conceptuels

| Objet | Sens | Frontière |
|---|---|---|
| Dossier | Cadre et portée du recueil | Ne prouve aucun événement |
| Séance | Quand, où et par qui le témoignage est recueilli | Date de la séance ≠ date des faits allégués |
| Déclarant | Rôle, identité protégée ou pseudonyme | Identité civile conservée selon autorisation externe |
| Question/réponse | Contenu attribué aux intervenants | Citations originales ≠ notes du rédacteur |
| Support original | Audio, vidéo, écrit, manuscrit, avec référence | Empreinte de fichier ≠ authenticité ni vérité |
| Transcription / traduction | Représentations du support | Signaler corrections, incertitudes et relectures |
| Attestation | Validation, relecture, signature ou serment si applicable | Ne jamais présumer qu'une formalité existe |
| Version / rectification | Évolution du dossier, rétractation ou ajout | Ne jamais écraser l'historique sans procédure applicable |
| Corroboration | Référence vers une enquête ou preuve indépendante | Ne se confond jamais avec la déposition |
| Restrictions | Confidentialité, accès, retentions et droits | Dépendent des autorités et règles opérationnelles |

## Règles épistémiques

- **Déclaration attribuée** : `X déclare P` ne certifie pas `P`.
- Préserver l'original et conserver les transformations comme représentations/versions distinctes.
- Une déclaration peut être complète, partielle, contestée, rectifiée, rétractée, contradictoire ou non vérifiée.
- Une contradiction entre témoins n'autorise pas la suppression de l'un des récits.
- Les analyses de crédibilité, résumés IA, traductions, chronologies et hypothèses sont des couches dérivées ou des artefacts externes.
- La date du fait allégué, celle de l'entretien et celle de l'enregistrement ne doivent jamais être confondues.

## Trame pour un recueil réel (à adapter par responsable autorisé)

1. Identifier l'organisme, le cadre, le responsable, les droits et les restrictions applicables.
2. Expliquer les modalités de traitement et consigner le consentement ou autre fondement approprié, sans les confondre avec une autorisation de publication.
3. Distinguer intervenants et rôles; consigner le lieu/moyen et les horodatages avec fuseau.
4. Conserver les questions, réponses, notes et éventuels supports originaux sans fabriquer de citations.
5. Consigner la méthode de transcription et les corrections; ne pas attribuer un résumé au témoin sans validation.
6. Enregistrer les restrictions d'accès, la conservation et les références des pièces selon le système autorisé.
7. Éventuellement référencer une analyse et une corroboration, sans promouvoir automatiquement le récit en vérité.

## Modèle livré

Le modèle `modeles/deposition-temoignage/design/fiche-deposition-vierge.json` est un **spécimen vide**, pas un outil de collecte sécurisé. Le copier hors d’un dépôt public ne suffit pas à constituer un système conforme pour recevoir des témoignages réels. Le canon v9 est vide; tout contrat logique, toute provenance et toute politique de lecture doivent être définis et qualifiés par le propriétaire du domaine.

**Limites :** la bibliothèque ne prend pas d'enregistrement, ne garantit ni chain of custody judiciaire ni validité d'un témoignage assermenté. Elle ne gère pas de données de santé, dossiers individuels ni conservation sécurisée de données personnelles.
