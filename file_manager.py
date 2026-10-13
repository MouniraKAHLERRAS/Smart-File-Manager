
from pathlib import Path
import shutil
import logging
from dataclasses import dataclass

from config import categories


@dataclass
class Fichier:
    nom: str
    extension: str
    categorie: str


def obtenir_categorie(extension: str) -> str:
    return categories.get(extension.lower(), "Autres")


def creer_dossier(dossier: Path, categorie: str) -> Path:
    dossier_destination = dossier / categorie
    dossier_destination.mkdir(parents=True, exist_ok=True)
    return dossier_destination


def trouver_nom_unique(fichier_destination: Path) -> Path:
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


def deplacer_fichier(
    fichier: Path,
    destination: Path,
    details_erreurs: list[str] | None = None
) -> bool:
    try:
        fichier_destination = destination / fichier.name
        nouveau_chemin = trouver_nom_unique(fichier_destination)

        shutil.move(str(fichier), str(nouveau_chemin))
        return True

    except OSError as erreur:
        message = f"{fichier.name} : {erreur}"
        logging.error("Échec du déplacement : %s", message)

        if details_erreurs is not None:
            details_erreurs.append(message)

        return False


def organiser_fichiers(
    dossier: Path,
    simulation: bool = True
) -> dict:
    statistiques = {
        "deplaces": 0,
        "ignores": 0,
        "erreurs": 0,
        "a_organiser": 0,
        "details_erreurs": [],
        "details_ignores": [],
        "categories": {}
    }

    if not dossier.exists() or not dossier.is_dir():
        statistiques["erreurs"] = 1
        statistiques["details_erreurs"].append(
            f"{dossier} : chemin invalide ou dossier inexistant."
        )
        return statistiques

    # On prend une liste fixe pour éviter de traiter
    # les nouveaux dossiers créés pendant l'organisation.
    elements = list(dossier.iterdir())

    for fichier in elements:
        if not fichier.is_file():
            statistiques["ignores"] += 1
            statistiques["details_ignores"].append(
                f"{fichier.name} : ce n'est pas un fichier."
            )
            continue

        categorie = obtenir_categorie(fichier.suffix)

        if simulation:
            statistiques["a_organiser"] += 1
            statistiques["categories"][categorie] = (
                statistiques["categories"].get(categorie, 0) + 1
            )
            continue

        try:
            destination = creer_dossier(dossier, categorie)

            succes = deplacer_fichier(
                fichier,
                destination,
                statistiques["details_erreurs"]
            )

            if succes:
                statistiques["deplaces"] += 1
                statistiques["categories"][categorie] = (
                    statistiques["categories"].get(categorie, 0) + 1
                )
            else:
                statistiques["erreurs"] += 1

        except OSError as erreur:
            message = f"{fichier.name} : {erreur}"
            logging.error("Échec du traitement : %s", message)
            statistiques["erreurs"] += 1
            statistiques["details_erreurs"].append(message)

    return statistiques
