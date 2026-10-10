# 🎯 Mastermind Solver

Solveur de **Mastermind à 10 couleurs** en Python : le programme devine un code secret de 4 positions (doublons autorisés) en posant des questions à la manière d'un joueur, et sans bibliothèque externe.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Dépendances](https://img.shields.io/badge/d%C3%A9pendances-aucune-2ea44f)
![Algorithme](https://img.shields.io/badge/algorithme-minimax%20(Knuth)-orange)

## Résultats

| | |
|---|---|
| Couleurs | 10 (`red`, `blue`, `green`, `yellow`, `white`, `black`, `orange`, `purple`, `pink`, `brown`) |
| Espace de recherche | 10 000 codes (10⁴) |
| Essais autorisés | 10 |
| Mesure sur 10 codes aléatoires (graine 42) | **5,8 essais en moyenne, 7 au maximum** |

## Comment ça marche

1. **Premier essai fixe** : les quatre premières couleurs.
2. **Retour du jeu** : nombre de couleurs *bien placées* et *mal placées*.
3. **Filtrage** : on ne garde que les codes qui auraient donné exactement les mêmes réponses.
4. **Choix minimax (Knuth)** : parmi 50 codes possibles, on joue celui dont le pire cas laisse le moins de codes candidats.
5. **Sauvegarde de progression** : chaque essai est écrit dans `mastermind_checkpoint.json` pour reprendre une partie interrompue.

## Utilisation

```bash
git clone https://github.com/KingRandAlThor/mastermind-solver.git
cd mastermind-solver
python play.py          # menu : mode interactif, test automatique, reprise
python demo.py          # démonstration complète d'une partie
python test_solver.py   # tests du calcul de score + 10 parties aléatoires
```

Exemple en mode interactif :

```text
Essai 1/10 : red blue green yellow
Codes possibles restants : 10000
Score (bien_placés mal_placés) : 0 1
```

## Structure

| Fichier | Rôle |
|---|---|
| `mastermind_solver.py` | Classe `MastermindSolver` : score, filtrage, choix minimax, sauvegarde |
| `play.py` | Menu interactif |
| `demo.py` | Partie simulée expliquée pas à pas |
| `test_solver.py` | Tests automatiques |

## Pistes d'amélioration

- Évaluer **tous** les codes candidats au lieu d'un échantillon de 50.
- Ajouter une interface graphique.
- Mesurer la moyenne sur les 10 000 codes possibles.
