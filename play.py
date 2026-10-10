"""
MASTERMIND SOLVER - Lancement rapide
Pour jouer immédiatement
"""

from mastermind_solver import MastermindSolver, test_solver_auto


def main_menu():
    """
    Menu principal simplifié
    """
    print("╔" + "="*50 + "╗")
    print("║" + " "*15 + "MASTERMIND SOLVER" + " "*17 + "║")
    print("║" + " "*9 + "Code 4 couleurs - 10 essais max" + " "*7 + "║")
    print("╠" + "="*50 + "╣")
    print("║ 1. 🎯 Mode Interactif (Vous avez un code)     ║")
    print("║ 2. 🤖 Test Automatique (Code généré)         ║")
    print("║ 3. Restore Checkpoint                        ║")
    print("║ 4. Comment ca marche ?                       ║")
    print("║ 5. Quitter                                   ║")
    print("╚" + "="*50 + "╝")


def how_it_works():
    """
    Explication simple du fonctionnement
    """
    print("\n" + "="*50)
    print("COMMENT ÇA MARCHE ?")
    print("="*50)
    print("🎯 OBJECTIF :")
    print("   Trouver votre code secret a 4 couleurs")
    print("   Couleurs : red, blue, green, yellow, white, black, orange, purple, pink, brown")
    print("   Doublons autorises")
    print()
    print("🎮 MODE INTERACTIF :")
    print("   1. Pensez a un code (ex: red blue green yellow)")
    print("   2. Je vous propose des essais")
    print("   3. Vous me donnez le score de chaque essai :")
    print("      - Bien placés (chiffre correct, bonne position)")
    print("      - Mal placés (chiffre correct, mauvaise position)")
    print()
    print("📝 EXEMPLE :")
    print("   Votre code secret : red blue green yellow")
    print("   Mon essai : red blue yellow green")
    print("   Votre réponse : 2 2")
    print("   (1 et 2 bien placés, 4 et 3 mal placés)")
    print()
    print("🧠 ALGORITHME :")
    print("   - Stratégie minimax optimisée")
    print("   - Garantit la résolution en 10 essais max")
    print("   - Moyenne : 5-6 essais")
    print("\nAppuyez sur Entrée pour continuer...")
    input()


if __name__ == "__main__":
    while True:
        main_menu()
        
        choice = input("\nVotre choix (1-5) : ").strip()
        
        if choice == "1":
            print("\n" + "🎯 MODE INTERACTIF" + "\n")
            solver = MastermindSolver()
            result = solver.solve_interactive()
            
            if result:
                print(f"\n🎉 Partie terminée avec succès !")
            print("\nAppuyez sur Entrée pour continuer...")
            input()
            
        elif choice == "2":
            print("\n" + "🤖 TEST AUTOMATIQUE" + "\n")
            success = test_solver_auto()
            
            if success:
                print("✅ Test réussi !")
            else:
                print("❌ Test échoué")
            print("\nAppuyez sur Entrée pour continuer...")
            input()
            
        elif choice == "3":
            print("\nRESTORE CHECKPOINT\n")
            solver = MastermindSolver()
            solver.solve_interactive(restore_checkpoint=True)
            print("\nAppuyez sur Entrée pour continuer...")
            input()

        elif choice == "4":
            how_it_works()
            
        elif choice == "5":
            print("\n👋 Au revoir ! Merci d'avoir utilisé Mastermind Solver")
            break
            
        else:
            print("❌ Choix invalide, veuillez choisir 1, 2, 3 ou 4")
            print("Appuyez sur Entrée pour continuer...")
            input()