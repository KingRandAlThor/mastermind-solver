"""Solveur Mastermind a 10 couleurs, avec sauvegarde de progression."""

import json
import random
from itertools import product
from pathlib import Path
from typing import List, Tuple


COLORS = (
    "red", "blue", "green", "yellow", "white", "black", "orange", "purple",
    "pink", "brown",
)
Code = Tuple[str, str, str, str]
DEFAULT_CHECKPOINT_FILE = Path("mastermind_checkpoint.json")


class MastermindSolver:
    def __init__(self, checkpoint_file: Path = DEFAULT_CHECKPOINT_FILE):
        self.checkpoint_file = checkpoint_file
        self.all_codes: List[Code] = list(product(COLORS, repeat=4))
        self.possible_codes = self.all_codes.copy()
        self.attempts = []
        
    @staticmethod
    def format_code(code: Code) -> str:
        return " ".join(code)

    def calculate_score(self, guess: Code, secret: Code) -> Tuple[int, int]:
        """
        Calcule le score (bien placés, mal placés) entre une supposition et un code secret
        """
        well_placed = 0  # Chiffres bien placés (noirs)
        misplaced = 0    # Chiffres mal placés (blancs)
        
        # Compter les bien placés
        guess_remaining = []
        secret_remaining = []
        
        for i in range(4):
            if guess[i] == secret[i]:
                well_placed += 1
            else:
                guess_remaining.append(guess[i])
                secret_remaining.append(secret[i])
        
        # Compter les mal placés
        for color in guess_remaining:
            if color in secret_remaining:
                misplaced += 1
                secret_remaining.remove(color)
        
        return well_placed, misplaced
    
    def is_consistent(self, code: Code, attempts: List[Tuple[Code, int, int]]) -> bool:
        """
        Vérifie si un code est compatible avec tous les essais précédents
        """
        for guess, expected_well, expected_mis in attempts:
            actual_well, actual_mis = self.calculate_score(guess, code)
            if actual_well != expected_well or actual_mis != expected_mis:
                return False
        return True
    
    def filter_possible_codes(self, guess: Code, well_placed: int, misplaced: int):
        """
        Filtre les codes possibles basé sur le dernier essai
        """
        self.attempts.append((guess, well_placed, misplaced))
        self.possible_codes = [
            code for code in self.possible_codes
            if self.is_consistent(code, [(guess, well_placed, misplaced)])
        ]
        self.save_checkpoint()

    def save_checkpoint(self) -> None:
        """Enregistre uniquement les réponses, afin de reconstruire un état fiable."""
        data = {
            "attempts": [
                {"guess": list(guess), "well_placed": well_placed, "misplaced": misplaced}
                for guess, well_placed, misplaced in self.attempts
            ]
        }
        self.checkpoint_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def restore_checkpoint(self) -> bool:
        """Restaure les essais sauvegardés et recalcule les codes compatibles."""
        if not self.checkpoint_file.exists():
            return False

        try:
            data = json.loads(self.checkpoint_file.read_text(encoding="utf-8"))
            restored_attempts = []
            for attempt in data["attempts"]:
                guess = tuple(attempt["guess"])
                well_placed = attempt["well_placed"]
                misplaced = attempt["misplaced"]
                if (
                    len(guess) != 4 or any(color not in COLORS for color in guess)
                    or not isinstance(well_placed, int) or not isinstance(misplaced, int)
                    or well_placed < 0 or misplaced < 0 or well_placed + misplaced > 4
                ):
                    raise ValueError("checkpoint invalide")
                restored_attempts.append((guess, well_placed, misplaced))
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            return False

        self.attempts = restored_attempts
        self.possible_codes = [
            code for code in self.all_codes if self.is_consistent(code, self.attempts)
        ]
        return True

    def clear_checkpoint(self) -> None:
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()
    
    def choose_next_guess(self) -> Code:
        """
        Choisit le prochain essai en utilisant la stratégie de Knuth modifiée
        """
        if len(self.attempts) == 0:
            return COLORS[:4]
        
        if len(self.possible_codes) == 1:
            return self.possible_codes[0]
        
        # Stratégie minimax : choisir le code qui minimise le pire cas
        best_guess = None
        min_worst_case = float('inf')
        
        # Tester un échantillon des codes possibles pour optimiser la performance
        candidates = self.possible_codes[:min(50, len(self.possible_codes))]
        
        for candidate in candidates:
            worst_case = 0
            
            # Calculer pour chaque score possible combien de codes restent
            score_counts = {}
            for possible_code in self.possible_codes:
                score = self.calculate_score(candidate, possible_code)
                score_counts[score] = score_counts.get(score, 0) + 1
            
            # Le pire cas est le plus grand groupe restant
            worst_case = max(score_counts.values()) if score_counts else 0
            
            if worst_case < min_worst_case:
                min_worst_case = worst_case
                best_guess = candidate
        
        return best_guess if best_guess else self.possible_codes[0]
    
    def solve_interactive(self, restore_checkpoint: bool = False):
        """
        Mode interactif pour résoudre un Mastermind
        """
        print("=== SOLVEUR MASTERMIND ===")
        print("Je vais trouver votre code secret a 4 couleurs (doublons autorises)")
        print(f"Couleurs : {', '.join(COLORS)}")
        print("Pour chaque essai, donnez-moi :")
        print("- Nombre de chiffres bien placés (noirs)")
        print("- Nombre de chiffres mal placés (blancs)")
        print("Exemple : si j'ai 2 chiffres corrects bien placés et 1 mal placé, tapez : 2 1")
        print("\n" + "="*50)
        
        if restore_checkpoint:
            if self.restore_checkpoint():
                print(f"Checkpoint restaure : {len(self.attempts)} essai(s) deja enregistre(s).")
            else:
                print("Aucun checkpoint valide a restaurer.")

        attempt_count = len(self.attempts)
        max_attempts = 10
        
        while attempt_count < max_attempts:
            attempt_count += 1
            guess = self.choose_next_guess()
            
            print(f"\nEssai {attempt_count}/10 : {self.format_code(guess)}")
            print(f"Codes possibles restants : {len(self.possible_codes)}")
            
            # Vérifier si on a trouvé
            if len(self.possible_codes) == 1:
                print(f"\nTROUVE ! Le code secret est : {self.format_code(guess)}")
                self.clear_checkpoint()
                return guess
            
            # Demander le score
            while True:
                try:
                    response = input("Score (bien_placés mal_placés) : ").strip()
                    if response == "":
                        continue
                    
                    parts = response.split()
                    if len(parts) != 2:
                        print("Veuillez entrer deux nombres séparés par un espace")
                        continue
                    
                    well_placed = int(parts[0])
                    misplaced = int(parts[1])
                    
                    if well_placed < 0 or well_placed > 4 or misplaced < 0 or misplaced > 4:
                        print("Les scores doivent être entre 0 et 4")
                        continue
                    
                    if well_placed + misplaced > 4:
                        print("La somme des scores ne peut pas dépasser 4")
                        continue
                    
                    if well_placed == 4:
                        print(f"\nTROUVE ! Le code secret est : {self.format_code(guess)}")
                        self.clear_checkpoint()
                        return guess
                    
                    break
                    
                except ValueError:
                    print("Veuillez entrer des nombres valides")
            
            # Filtrer les codes possibles
            self.filter_possible_codes(guess, well_placed, misplaced)
            
            if len(self.possible_codes) == 0:
                print("\n❌ Erreur : Aucun code ne correspond aux réponses données.")
                print("Vérifiez vos réponses précédentes.")
                return None
        
        print(f"\n⚠️ Échec : Je n'ai pas trouvé le code en {max_attempts} essais.")
        if len(self.possible_codes) > 0:
            print(f"Codes possibles restants : {self.possible_codes[:10]}")
        return None


def test_solver_auto():
    """
    Test automatique du solveur
    """
    print("=== TEST AUTOMATIQUE ===")
    
    # Générer un code secret aléatoire
    solver = MastermindSolver()
    secret_code = tuple(random.choices(COLORS, k=4))
    print(f"Code secret généré : {solver.format_code(secret_code)}")

    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        attempts += 1
        guess = solver.choose_next_guess()
        
        print(f"Essai {attempts} : {solver.format_code(guess)}")
        
        if guess == secret_code:
            print(f"Code trouve en {attempts} essais !")
            solver.clear_checkpoint()
            return True
        
        # Calculer le score automatiquement
        well_placed, misplaced = solver.calculate_score(guess, secret_code)
        print(f"Score : {well_placed} bien placés, {misplaced} mal placés")
        
        solver.filter_possible_codes(guess, well_placed, misplaced)
        
        if len(solver.possible_codes) == 0:
            print("❌ Erreur dans l'algorithme !")
            return False
    
    print(f"⚠️ Échec : Code non trouvé en {max_attempts} essais")
    return False


if __name__ == "__main__":
    print("MASTERMIND SOLVER")
    print("1. Mode interactif (vous avez un code, je le trouve)")
    print("2. Test automatique (génération d'un code aléatoire)")
    
    while True:
        choice = input("\nChoisissez (1 ou 2) : ").strip()
        
        if choice == "1":
            solver = MastermindSolver()
            solver.solve_interactive()
            break
        elif choice == "2":
            test_solver_auto()
            break
        else:
            print("Veuillez choisir 1 ou 2")