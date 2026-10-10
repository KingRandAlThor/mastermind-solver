"""
Exemple d'utilisation du solveur Mastermind
Simulation d'une partie interactive
"""

import sys
import tempfile
from pathlib import Path

from mastermind_solver import COLORS, MastermindSolver


def demo_interactive():
    """
    Démonstration du mode interactif avec un code prédéfini
    """
    secret_code = ("blue", "yellow", "purple", "brown")
    solver = MastermindSolver(Path(tempfile.gettempdir()) / "mm_demo.json")
    print("=== DÉMONSTRATION INTERACTIVE ===")
    print(f"Code secret (pour la démo) : {solver.format_code(secret_code)}")
    print("Simulation d'une partie où le joueur répond aux questions du solveur\n")

    attempts = 0
    
    while attempts < 10:
        attempts += 1
        guess = solver.choose_next_guess()
        
        print(f"Essai {attempts}/10 : {solver.format_code(guess)}")
        print(f"Codes possibles restants : {len(solver.possible_codes)}")
        
        if guess == secret_code:
            print(f"\nTROUVE ! Le code secret est : {solver.format_code(guess)}")
            print(f"Résolu en {attempts} essais !")
            return
        
        # Calculer automatiquement le score pour la démo
        well_placed, misplaced = solver.calculate_score(guess, secret_code)
        print(f"Score automatique : {well_placed} bien placés, {misplaced} mal placés")
        print("(Dans une vraie partie, c'est vous qui donneriez cette réponse)\n")
        
        solver.filter_possible_codes(guess, well_placed, misplaced)
    
    print("Échec : non résolu en 10 essais")


def show_strategy_explanation():
    """
    Explique la stratégie utilisée par le solveur
    """
    print("=== STRATÉGIE DU SOLVEUR ===\n")
    
    print("1. PREMIER ESSAI :")
    print(f"   - Utilise '{' '.join(COLORS[:4])}' pour maximiser l'information")
    print("   - 4 couleurs différentes donnent le maximum de renseignements\n")
    
    print("2. FILTRAGE :")
    print("   - Élimine tous les codes incompatibles avec les réponses")
    print("   - Réduit drastiquement l'espace de recherche\n")
    
    print("3. CHOIX DU PROCHAIN ESSAI :")
    print("   - Utilise la stratégie minimax")
    print("   - Choisit l'essai qui minimise le pire cas")
    print("   - Garantit la résolution en maximum 10 essais\n")
    
    print("4. OPTIMISATIONS :")
    print("   - Échantillonnage intelligent pour les gros calculs")
    print("   - Heuristiques pour accélérer la sélection")
    print("   - Gestion efficace de la mémoire\n")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    show_strategy_explanation()
    demo_interactive()

