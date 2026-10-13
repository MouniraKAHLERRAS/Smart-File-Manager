
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from threading import Thread
from datetime import datetime
import queue

from file_manager import organiser_fichiers


# =========================================================
# CONFIGURATION DU DESIGN
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#080F20"
SIDEBAR = "#0B1530"
CARD = "#101D38"
CARD_LIGHT = "#152544"
BORDER = "#24375C"

WHITE = "#F1F5FF"
MUTED = "#91A3C7"

PURPLE = "#7657FF"
BLUE = "#258BFF"
GREEN = "#19C99A"
RED = "#FF5576"
ORANGE = "#FFAA55"

FONT = "Segoe UI"


# =========================================================
# APPLICATION
# =========================================================

class SmartFileManager(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Smart File Manager")
        self.geometry("1250x820")
        self.minsize(1000, 700)
        self.configure(fg_color=BG)

        self.dossier_selectionne = ""
        self.en_cours = False
        self.file_queue = queue.Queue()
        self.historique = []

        self._creer_interface()
        self.after(100, self._verifier_resultats)

    # =====================================================
    # STRUCTURE PRINCIPALE
    # =====================================================

    def _creer_interface(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._creer_sidebar()

        self.contenu = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )
        self.contenu.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=24,
            pady=20
        )

        self.contenu.grid_columnconfigure(0, weight=3)
        self.contenu.grid_columnconfigure(1, weight=2)
        self.contenu.grid_rowconfigure(2, weight=1)

        self._creer_entete()
        self._creer_zone_principale()
        self._creer_colonne_droite()

    def _creer_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=SIDEBAR
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(6, weight=1)

        logo = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        logo.pack(fill="x", padx=20, pady=(28, 35))

        ctk.CTkLabel(
            logo,
            text="📁",
            font=(FONT, 30)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            logo,
            text="Smart File\nManager",
            font=(FONT, 17, "bold"),
            text_color=WHITE,
            justify="left"
        ).pack(side="left")

        self.boutons_navigation = {}

        elements = [
            ("⌂", "Accueil"),
            ("▣", "Organiser"),
            ("⚙", "Paramètres"),
            ("ⓘ", "À propos"),
        ]

        for symbole, nom in elements:
            bouton = ctk.CTkButton(
                self.sidebar,
                text=f"   {symbole}    {nom}",
                anchor="w",
                height=45,
                corner_radius=10,
                font=(FONT, 13),
                fg_color=PURPLE if nom == "Accueil" else "transparent",
                hover_color=CARD_LIGHT,
                text_color=WHITE,
                command=lambda n=nom: self._navigation(n)
            )
            bouton.pack(fill="x", padx=14, pady=5)
            self.boutons_navigation[nom] = bouton

        bas = ctk.CTkFrame(
            self.sidebar,
            fg_color=CARD,
            corner_radius=14
        )
        bas.pack(side="bottom", fill="x", padx=14, pady=20)

        ctk.CTkLabel(
            bas,
            text="✦",
            font=(FONT, 28),
            text_color=PURPLE
        ).pack(pady=(14, 0))

        ctk.CTkLabel(
            bas,
            text="Un espace bien rangé,\nun esprit plus léger.",
            font=(FONT, 11),
            text_color=MUTED,
            justify="center"
        ).pack(pady=(3, 15))

    # =====================================================
    # ENTÊTE
    # =====================================================

    def _creer_entete(self):
        entete = ctk.CTkFrame(
            self.contenu,
            fg_color="transparent"
        )
        entete.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 20)
        )

        entete.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            entete,
            text="Smart File Manager",
            font=(FONT, 28, "bold"),
            text_color=WHITE
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            entete,
            text="Organisez vos fichiers simplement et en toute sécurité.",
            font=(FONT, 12),
            text_color=MUTED
        ).grid(row=1, column=0, sticky="w", pady=(5, 0))

        self.label_statut = ctk.CTkLabel(
            entete,
            text="●  Prêt",
            font=(FONT, 12, "bold"),
            text_color=GREEN,
            fg_color=CARD,
            corner_radius=12
        )
        self.label_statut.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(15, 0),
            ipadx=12,
            ipady=8
        )

    # =====================================================
    # CARTES DE LA COLONNE PRINCIPALE
    # =====================================================

    def _creer_zone_principale(self):
        gauche = ctk.CTkFrame(
            self.contenu,
            fg_color="transparent"
        )
        gauche.grid(
            row=1,
            column=0,
            rowspan=2,
            sticky="nsew",
            padx=(0, 12)
        )
        gauche.grid_columnconfigure(0, weight=1)
        gauche.grid_rowconfigure(3, weight=1)

        # Sélection du dossier
        dossier_card = self._carte(gauche)
        dossier_card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        dossier_card.grid_columnconfigure(0, weight=1)

        self._titre_carte(dossier_card, "01", "Sélection du dossier")

        self.entree_chemin = ctk.CTkEntry(
            dossier_card,
            height=42,
            corner_radius=9,
            placeholder_text="Choisissez un dossier...",
            font=(FONT, 12),
            fg_color=BG,
            border_color=BORDER,
            text_color=WHITE
        )
        self.entree_chemin.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(16, 8),
            pady=(14, 10)
        )

        ctk.CTkButton(
            dossier_card,
            text="Parcourir",
            width=100,
            height=42,
            corner_radius=9,
            fg_color=PURPLE,
            hover_color="#6345E8",
            font=(FONT, 12, "bold"),
            command=self.choisir_dossier
        ).grid(row=1, column=1, padx=(0, 16), pady=(14, 10))

        self.label_dossier = ctk.CTkLabel(
            dossier_card,
            text="●  Aucun dossier sélectionné",
            text_color=MUTED,
            font=(FONT, 11),
            anchor="w"
        )
        self.label_dossier.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=16,
            pady=(0, 16)
        )

        # Mode de fonctionnement
        mode_card = self._carte(gauche)
        mode_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        mode_card.grid_columnconfigure((0, 1), weight=1)

        self._titre_carte(mode_card, "02", "Mode de fonctionnement")

        self.mode = ctk.StringVar(value="simulation")

        self.carte_simulation = ctk.CTkRadioButton(
            mode_card,
            text="Mode simulation\n\nPrévisualiser les changements\nsans déplacer les fichiers.",
            variable=self.mode,
            value="simulation",
            font=(FONT, 12),
            text_color=WHITE,
            fg_color=PURPLE,
            hover_color=PURPLE,
            border_color=BORDER,
            radiobutton_width=20,
            radiobutton_height=20
        )
        self.carte_simulation.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(18, 8),
            pady=(18, 20)
        )

        self.carte_reel = ctk.CTkRadioButton(
            mode_card,
            text="Mode réel\n\nDéplacer les fichiers\nvers leurs catégories.",
            variable=self.mode,
            value="reel",
            font=(FONT, 12),
            text_color=WHITE,
            fg_color=GREEN,
            hover_color=GREEN,
            border_color=BORDER,
            radiobutton_width=20,
            radiobutton_height=20
        )
        self.carte_reel.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(8, 18),
            pady=(18, 20)
        )

        # Bouton principal
        self.bouton_lancer = ctk.CTkButton(
            gauche,
            text="▶    Lancer l'organisation",
            height=48,
            corner_radius=12,
            fg_color=PURPLE,
            hover_color="#6345E8",
            font=(FONT, 14, "bold"),
            command=self.lancer_organisation
        )
        self.bouton_lancer.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 14)
        )

        # Progression
        progression = self._carte(gauche)
        progression.grid(row=3, column=0, sticky="nsew", pady=(0, 14))
        progression.grid_columnconfigure(0, weight=1)

        self._titre_carte(progression, "03", "Progression de l'organisation")

        self.barre_progression = ctk.CTkProgressBar(
            progression,
            height=12,
            corner_radius=8,
            fg_color=CARD_LIGHT,
            progress_color=PURPLE
        )
        self.barre_progression.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(20, 8)
        )
        self.barre_progression.set(0)

        self.label_progression = ctk.CTkLabel(
            progression,
            text="En attente...",
            font=(FONT, 11),
            text_color=MUTED
        )
        self.label_progression.grid(
            row=2,
            column=0,
            sticky="w",
            padx=18,
            pady=(0, 14)
        )

        # Résultats
        resultat_card = self._carte(gauche)
        resultat_card.grid(row=4, column=0, sticky="ew")
        resultat_card.grid_columnconfigure(0, weight=1)

        self._titre_carte(resultat_card, "04", "Résultats")

        self.zone_resultats = ctk.CTkTextbox(
            resultat_card,
            height=150,
            corner_radius=10,
            fg_color=BG,
            border_width=1,
            border_color=BORDER,
            text_color=WHITE,
            font=("Consolas", 11),
            wrap="word"
        )
        self.zone_resultats.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=16,
            pady=(12, 10)
        )
        self.zone_resultats.insert(
            "1.0",
            "Bienvenue !\n\n"
            "Sélectionnez un dossier, puis lancez une simulation "
            "pour prévisualiser l'organisation."
        )
        self.zone_resultats.configure(state="disabled")

        ctk.CTkButton(
            resultat_card,
            text="Effacer les résultats",
            height=30,
            fg_color="transparent",
            border_width=1,
            border_color=BORDER,
            hover_color=CARD_LIGHT,
            text_color=MUTED,
            command=self.effacer_resultats
        ).grid(row=2, column=0, sticky="e", padx=16, pady=(0, 12))

    # =====================================================
    # COLONNE DROITE : STATISTIQUES ET HISTORIQUE
    # =====================================================

    def _creer_colonne_droite(self):
        droite = ctk.CTkFrame(
            self.contenu,
            fg_color="transparent"
        )
        droite.grid(row=1, column=1, rowspan=2, sticky="nsew")
        droite.grid_columnconfigure(0, weight=1)

        # Statistiques
        stats = self._carte(droite)
        stats.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        stats.grid_columnconfigure(0, weight=1)

        self._titre_carte(stats, "✦", "Statistiques")

        self.stat_deplaces = self._carte_stat(
            stats, 1, "Fichiers déplacés", "0", GREEN, "✓"
        )
        self.stat_ignores = self._carte_stat(
            stats, 2, "Éléments ignorés", "0", BLUE, "◉"
        )
        self.stat_erreurs = self._carte_stat(
            stats, 3, "Erreurs", "0", RED, "×"
        )

        ctk.CTkLabel(
            stats,
            text="RÉPARTITION PAR CATÉGORIE",
            font=(FONT, 11, "bold"),
            text_color=MUTED
        ).grid(row=4, column=0, sticky="w", padx=16, pady=(16, 8))

        self.categories_ui = {}

        for ligne, categorie, couleur in [
            (5, "Images", BLUE),
            (6, "PDF", RED),
            (7, "Documents", ORANGE),
            (8, "Musique", PURPLE),
            (9, "Videos", GREEN),
            (10, "Autres", MUTED),
        ]:
            ligne_frame = ctk.CTkFrame(stats, fg_color="transparent")
            ligne_frame.grid(
                row=ligne,
                column=0,
                sticky="ew",
                padx=16,
                pady=4
            )
            ligne_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                ligne_frame,
                text="●",
                text_color=couleur,
                font=(FONT, 13)
            ).grid(row=0, column=0, padx=(0, 8))

            ctk.CTkLabel(
                ligne_frame,
                text=categorie,
                text_color=WHITE,
                font=(FONT, 11)
            ).grid(row=0, column=1, sticky="w")

            valeur = ctk.CTkLabel(
                ligne_frame,
                text="0",
                text_color=MUTED,
                font=(FONT, 11, "bold")
            )
            valeur.grid(row=0, column=2, sticky="e")

            self.categories_ui[categorie] = valeur

        # Historique
        historique_card = self._carte(droite)
        historique_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        historique_card.grid_columnconfigure(0, weight=1)

        self._titre_carte(historique_card, "◷", "Dernières actions")

        self.zone_historique = ctk.CTkTextbox(
            historique_card,
            height=155,
            corner_radius=8,
            fg_color=BG,
            text_color=MUTED,
            font=(FONT, 11),
            wrap="word"
        )
        self.zone_historique.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=14,
            pady=(8, 14)
        )
        self.zone_historique.insert(
            "1.0",
            "Application lancée\n"
            "Prête à organiser vos fichiers."
        )
        self.zone_historique.configure(state="disabled")

        # Astuce
        astuce = ctk.CTkFrame(
            droite,
            fg_color="#14264C",
            corner_radius=14,
            border_width=1,
            border_color="#29467C"
        )
        astuce.grid(row=2, column=0, sticky="ew")

        ctk.CTkLabel(
            astuce,
            text="💡  CONSEIL",
            text_color="#FFD166",
            font=(FONT, 12, "bold")
        ).pack(anchor="w", padx=15, pady=(13, 5))

        ctk.CTkLabel(
            astuce,
            text="Utilisez d'abord le mode simulation\n"
                 "pour vérifier le résultat avant de\n"
                 "déplacer réellement vos fichiers.",
            text_color=WHITE,
            font=(FONT, 11),
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 14))

    # =====================================================
    # COMPOSANTS RÉUTILISABLES
    # =====================================================

    def _carte(self, parent):
        return ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

    def _titre_carte(self, parent, numero, titre):
        ligne = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        ligne.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=16,
            pady=(16, 0)
        )

        ctk.CTkLabel(
            ligne,
            text=str(numero),
            text_color=PURPLE,
            font=(FONT, 13, "bold")
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            ligne,
            text=titre,
            text_color=WHITE,
            font=(FONT, 13, "bold")
        ).pack(side="left")

    def _carte_stat(self, parent, ligne, titre, valeur, couleur, symbole):
        cadre = ctk.CTkFrame(
            parent,
            fg_color=CARD_LIGHT,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )
        cadre.grid(
            row=ligne,
            column=0,
            sticky="ew",
            padx=14,
            pady=4
        )
        cadre.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            cadre,
            text=symbole,
            font=(FONT, 19, "bold"),
            text_color=couleur
        ).grid(row=0, column=0, rowspan=2, padx=12, pady=8)

        ctk.CTkLabel(
            cadre,
            text=titre,
            font=(FONT, 10),
            text_color=MUTED
        ).grid(row=0, column=1, sticky="w", pady=(7, 0))

        label_valeur = ctk.CTkLabel(
            cadre,
            text=valeur,
            font=(FONT, 21, "bold"),
            text_color=couleur
        )
        label_valeur.grid(
            row=1,
            column=1,
            sticky="w",
            pady=(0, 7)
        )

        return label_valeur

    # =====================================================
    # ACTIONS
    # =====================================================

    def choisir_dossier(self):
        chemin = filedialog.askdirectory(
            title="Choisir un dossier à organiser"
        )

        if chemin:
            self.dossier_selectionne = chemin

            self.entree_chemin.delete(0, "end")
            self.entree_chemin.insert(0, chemin)

            self.label_dossier.configure(
                text=f"✓ Dossier sélectionné : {chemin}",
                text_color=GREEN
            )

            self._ajouter_historique("Dossier sélectionné : " + chemin)

    def lancer_organisation(self):
        if self.en_cours:
            return

        chemin = self.entree_chemin.get().strip()
        dossier = Path(chemin)

        if not chemin or not dossier.exists() or not dossier.is_dir():
            messagebox.showerror(
                "Dossier invalide",
                "Veuillez sélectionner un dossier existant."
            )
            return

        simulation = self.mode.get() == "simulation"

        if not simulation:
            confirmer = messagebox.askyesno(
                "Confirmer le déplacement",
                "Le mode réel va déplacer les fichiers.\n\n"
                "Il est recommandé de faire une simulation d'abord.\n\n"
                "Voulez-vous continuer ?"
            )
            if not confirmer:
                return

        self.en_cours = True
        self.bouton_lancer.configure(state="disabled")
        self.label_statut.configure(
            text="●  En cours...",
            text_color=ORANGE
        )
        self.label_progression.configure(
            text="Traitement en cours... La progression exacte "
                 "n'est pas disponible dans le moteur actuel."
        )
        self.barre_progression.configure(mode="indeterminate")
        self.barre_progression.start()

        self._ajouter_historique(
            "Début de la simulation" if simulation
            else "Début du déplacement réel"
        )

        thread = Thread(
            target=self._executer_en_arriere_plan,
            args=(dossier, simulation),
            daemon=True
        )
        thread.start()

    def _executer_en_arriere_plan(self, dossier, simulation):
        try:
            resultat = organiser_fichiers(
                dossier,
                simulation=simulation
            )
            self.file_queue.put(("succes", resultat, simulation))
        except Exception as erreur:
            self.file_queue.put(("erreur", str(erreur), simulation))

    def _verifier_resultats(self):
        try:
            while True:
                type_resultat, resultat, simulation = self.file_queue.get_nowait()

                self.barre_progression.stop()
                self.barre_progression.configure(mode="determinate")
                self.barre_progression.set(1)

                self.en_cours = False
                self.bouton_lancer.configure(state="normal")

                if type_resultat == "erreur":
                    self.label_statut.configure(
                        text="●  Erreur",
                        text_color=RED
                    )
                    messagebox.showerror("Erreur", resultat)
                    self.label_progression.configure(
                        text="L'opération a échoué."
                    )
                    continue

                self._afficher_statistiques(resultat, simulation)

                erreurs = resultat.get("erreurs", 0)

                if erreurs:
                    self.label_statut.configure(
                        text="●  Terminé avec erreurs",
                        text_color=RED
                    )
                else:
                    self.label_statut.configure(
                        text="●  Terminé",
                        text_color=GREEN
                    )

                if simulation:
                    nombre = resultat.get("a_organiser", 0)
                    self.label_progression.configure(
                        text=f"Simulation terminée : {nombre} fichier(s) "
                             "à organiser. Aucun fichier déplacé."
                    )
                else:
                    self.label_progression.configure(
                        text=f"Organisation terminée : "
                             f"{resultat.get('deplaces', 0)} fichier(s) déplacé(s)."
                    )

                self._ajouter_historique(
                    "Simulation terminée" if simulation
                    else "Organisation réelle terminée"
                )

                if erreurs:
                    details = resultat.get("details_erreurs", [])
                    message = (
                        f"{erreurs} erreur(s) détectée(s).\n"
                        "Consultez les résultats pour voir les détails."
                    )
                    messagebox.showwarning("Opération terminée", message)
                elif simulation:
                    messagebox.showinfo(
                        "Simulation terminée",
                        f"{resultat.get('a_organiser', 0)} fichier(s) "
                        "à organiser.\nAucun fichier n'a été déplacé."
                    )
                else:
                    messagebox.showinfo(
                        "Organisation terminée",
                        f"{resultat.get('deplaces', 0)} fichier(s) déplacé(s)."
                    )

        except queue.Empty:
            pass

        self.after(100, self._verifier_resultats)

    def _afficher_statistiques(self, resultat, simulation):
        self.stat_deplaces.configure(
            text=str(resultat.get("deplaces", 0))
        )
        self.stat_ignores.configure(
            text=str(resultat.get("ignores", 0))
        )
        self.stat_erreurs.configure(
            text=str(resultat.get("erreurs", 0))
        )

        categories = resultat.get("categories", {})

        correspondances = {
            "Images": ["Images"],
            "PDF": ["PDF"],
            "Documents": ["Documents"],
            "Musique": ["Musique"],
            "Videos": ["Videos", "Vidéos"],
            "Autres": ["Autres"],
        }

        for categorie, label in self.categories_ui.items():
            nombre = 0
            for nom in correspondances[categorie]:
                nombre += categories.get(nom, 0)
            label.configure(text=str(nombre))

        self.zone_resultats.configure(state="normal")
        self.zone_resultats.delete("1.0", "end")

        if simulation:
            self.zone_resultats.insert(
                "end",
                "APERÇU DE LA SIMULATION\n"
                "--------------------------------\n"
                f"Fichiers à organiser : {resultat.get('a_organiser', 0)}\n"
                f"Éléments ignorés : {resultat.get('ignores', 0)}\n"
                f"Erreurs : {resultat.get('erreurs', 0)}\n\n"
                "Aucun fichier n'a été déplacé.\n"
            )
        else:
            self.zone_resultats.insert(
                "end",
                "RÉSULTAT DE L'ORGANISATION\n"
                "--------------------------------\n"
                f"Fichiers déplacés : {resultat.get('deplaces', 0)}\n"
                f"Éléments ignorés : {resultat.get('ignores', 0)}\n"
                f"Erreurs : {resultat.get('erreurs', 0)}\n\n"
                "RÉPARTITION PAR CATÉGORIE\n"
            )

            for categorie, nombre in sorted(categories.items()):
                self.zone_resultats.insert(
                    "end",
                    f"  {categorie} : {nombre}\n"
                )

        details_erreurs = resultat.get("details_erreurs", [])

        if details_erreurs:
            self.zone_resultats.insert(
                "end",
                "\nFICHIERS EN ERREUR\n"
                "--------------------------------\n"
            )
            for detail in details_erreurs:
                self.zone_resultats.insert("end", f"• {detail}\n")

        details_ignores = resultat.get("details_ignores", [])

        if details_ignores:
            self.zone_resultats.insert(
                "end",
                "\nÉLÉMENTS IGNORÉS\n"
                "--------------------------------\n"
            )
            for detail in details_ignores:
                self.zone_resultats.insert("end", f"• {detail}\n")

        self.zone_resultats.configure(state="disabled")

    def effacer_resultats(self):
        self.zone_resultats.configure(state="normal")
        self.zone_resultats.delete("1.0", "end")
        self.zone_resultats.configure(state="disabled")

    def _ajouter_historique(self, message):
        heure = datetime.now().strftime("%H:%M:%S")
        self.historique.append(f"[{heure}] {message}")

        self.zone_historique.configure(state="normal")
        self.zone_historique.delete("1.0", "end")
        self.zone_historique.insert(
            "1.0",
            "\n\n".join(reversed(self.historique[-8:]))
        )
        self.zone_historique.configure(state="disabled")

    def _navigation(self, nom):
        for nom_bouton, bouton in self.boutons_navigation.items():
            bouton.configure(
                fg_color=PURPLE if nom_bouton == nom else "transparent"
            )

        if nom == "Accueil" or nom == "Organiser":
            self.label_statut.configure(
                text="●  Prêt" if not self.en_cours else "●  En cours...",
                text_color=GREEN if not self.en_cours else ORANGE
            )
        elif nom == "Paramètres":
            messagebox.showinfo(
                "Paramètres",
                "Les options de personnalisation seront ajoutées "
                "dans une prochaine version."
            )
        elif nom == "À propos":
            messagebox.showinfo(
                "À propos de Smart File Manager",
                "Smart File Manager\n\n"
                "Application de gestion et d'organisation de fichiers.\n"
                "Développée avec Python et CustomTkinter."
            )


if __name__ == "__main__":
    app = SmartFileManager()
    app.mainloop()
