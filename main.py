
from pathlib import Path
from file_manager import organiser_fichiers
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="smart_file_manager.log",
    encoding="utf-8"
)


def organiser() -> None:
    chemin = input("Entrez le chemin du dossier à organiser : ")
    dossier = Path(chemin)

    if not dossier.exists():
        print("Ce dossier n'existe pas.")
        return

    if not dossier.is_dir():
        print("Le chemin indiqué n'est pas un dossier.")
        return

    choix = input(
        "Activer le mode simulation ? (o/n) : "
    ).strip().lower()

    simulation = choix != "n"
    organiser_fichiers(dossier, simulation=simulation)


def main() -> None:
    while True:
        print("\n==============================")
        print("     SMART FILE MANAGER")
        print("==============================")
        print("1. Organiser les fichiers")
        print("2. Quitter")

        choix = input("Choisis une option : ").strip()

        if choix == "1":
            organiser()
        elif choix == "2":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Tape 1 ou 2.")


if __name__ == "__main__":
    main()
