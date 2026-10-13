
from file_manager import obtenir_categorie

from pathlib import Path
from file_manager import deplacer_fichier
from file_manager import trouver_nom_unique


def test_image():
    assert obtenir_categorie(".jpg") == "Images"


def test_pdf():
    assert obtenir_categorie(".pdf") == "PDF"


def test_extension_inconnue():
    assert obtenir_categorie(".xyz") == "Autres"


def test_deplacer_fichier(tmp_path):
    # Créer un fichier temporaire
    fichier = tmp_path / "photo.jpg"
    fichier.write_text("contenu de test")

    # Créer le dossier de destination
    destination = tmp_path / "Images"
    destination.mkdir()

    # Déplacer le fichier
    succes = deplacer_fichier(fichier, destination)

    # Vérifier le résultat
    assert succes is True
    assert not fichier.exists()
    assert (destination / "photo.jpg").exists()


def test_nom_unique():
    from pathlib import Path
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as dossier_temp:
        dossier = Path(dossier_temp)

        fichier = dossier / "photo.jpg"
        fichier.write_text("première photo")

        resultat = trouver_nom_unique(fichier)

        assert resultat.name == "photo_1.jpg"
        assert not resultat.exists()
