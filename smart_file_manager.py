from pathlib import Path
import shutil


categories = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".pdf": "PDF",
    ".docx": "Documents",
    ".doc": "Documents",
    ".txt": "Documents",
    ".csv": "Documents",
    ".mp3": "Musique",
    ".mp4": "Videos",
}


def obtenir_categorie(extension):
    if extension in categories:
        return categories[extension]

    return "Autres"


def creer_dossier(dossier, categorie):
    dossier_destination = dossier / categorie
    dossier_destination.mkdir(exist_ok=True)

    return dossier_destination
def trouver_nom_unique(fichier_destination):

    if not fichier_destination.exists():
        return fichier_destination

    compteur = 1

    while True:

        nouveau_nom = (
            f"{fichier_destination.stem}_{compteur}"
            f"{fichier_destination.suffix}"
        )

        nouveau_fichier = fichier_destination.parent / nouveau_nom

        if not nouveau_fichier.exists():
            return nouveau_fichier

        compteur += 1

def deplacer_fichier(fichier, destination):

    try:
        fichier_destination = destination / fichier.name

        nouveau_chemin = trouver_nom_unique(fichier_destination)

        shutil.move(fichier, nouveau_chemin)

        return True

    except OSError as erreur:
        print(f"Erreur avec {fichier.name} : {erreur}")
        return False


def organiser_fichiers(dossier):

    statistiques = {}
    erreurs = 0

    if not dossier.exists():
        print("Le dossier n'existe pas.")
        return

    if not dossier.is_dir():
        print("Le chemin indiqué n'est pas un dossier.")
        return

    for fichier in dossier.iterdir():

        if fichier.is_file():

            extension = fichier.suffix.lower()

            categorie = obtenir_categorie(extension)

            destination = creer_dossier(dossier, categorie)

            succes = deplacer_fichier(fichier, destination)

            if succes:
                statistiques[categorie] = statistiques.get(categorie, 0) + 1
                print(f"✓ {fichier.name} → {categorie}")
            else:
                erreurs += 1

    print("\n" + "=" * 30)
    print("   ORGANISATION TERMINÉE")
    print("=" * 30)

    total = sum(statistiques.values())  

    print(f"\nFichiers traités : {total}")

    for categorie, nombre in statistiques.items():
        print(f"{categorie:<15}: {nombre}")

    print(f"\nErreurs : {erreurs}")

def main():
    chemin = input("Entrez le chemin du dossier à organiser : ")

    dossier = Path(chemin)

    if not dossier.exists():
        print("❌ Ce dossier n'existe pas.")

    elif not dossier.is_dir():
        print("❌ Le chemin indiqué n'est pas un dossier.")

    else:
        organiser_fichiers(dossier)


if __name__ == "__main__":
    main()