import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logging.debug("Détail technique")
logging.info("Programme démarré")
logging.warning("Extension inconnue")
logging.error("Impossible de déplacer le fichier")