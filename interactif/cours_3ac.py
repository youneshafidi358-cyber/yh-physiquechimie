# -*- coding: utf-8 -*-
from cours_lib import *

MAT = [
 ("I", "Matériau et objet",
  B("def", UL("Un <b>matériau</b> est une matière employée pour fabriquer des objets.", "Un <b>objet</b> est fabriqué à partir d'un ou de plusieurs matériaux et sert à un usage précis."))
  + B("ret", "Trois familles : <b>les métaux</b> (fer, cuivre, aluminium, zinc), <b>les verres</b>, <b>les matières organiques</b> (plastiques, bois, papier). Le choix du matériau dépend de ses <b>propriétés</b> et de la <b>fonction</b> de l'objet.")
  + APP(QCM("« Bouteille en plastique » est :", ["un matériau", "un objet"], 1, "C'est un objet fabriqué en plastique (matériau)."))),
 ("II", "Propriétés des matériaux",
  TAB(["", "Électricité", "Chaleur", "Chocs"], [["Métaux", "conducteurs", "bons conducteurs", "résistent"], ["Verre", "isolant", "mauvais conducteur", "fragile"], ["Plastique", "isolant", "isolant", "certains résistent"]])
  + B("def", "<b>Conducteur</b> : laisse passer le courant (ou la chaleur) ; <b>isolant</b> : ne le laisse pas passer.")),
 ("III", "Reconnaître un métal ou un plastique",
  TAB(["Métal", "Propriété caractéristique"], [["Cuivre", "couleur rouge brique"], ["Fer", "attiré par l'aimant"], ["Aluminium", "gris, le plus léger"], ["Zinc", "gris, non attiré par l'aimant"]])
  + TAB(["Plastique", "Test caractéristique"], [["PE", "flotte dans l'eau douce"], ["PS", "flotte dans l'eau salée ; se dissout dans l'acétone"], ["PVC", "colore la flamme en vert"], ["PET", "se déforme dans l'eau bouillante"]])
  + SIM
  + APP(QCM("Un métal gris attiré par l'aimant est :", ["l'aluminium", "le fer", "le zinc"], 1, "Le fer est le seul attiré par l'aimant."),
        QCM("Un plastique qui se dissout dans l'acétone est :", ["PE", "PS", "PVC"], 1, "Le polystyrène (PS) se dissout dans l'acétone."),
        QCM("Une flamme verte indique :", ["le PET", "le PVC", "le PE"], 1, "Le PVC (contient du chlore) colore la flamme en vert."))),
 ("IV", "Choix des matériaux d'emballage",
  B("rule", "L'emballage protège et conserve le produit : son matériau ne doit pas réagir avec le produit.")),
]
MAT_TRAD = [("Matériau", "مادة"), ("Objet", "شيء"), ("Métal", "فلز"), ("Verre", "زجاج"), ("Matière plastique", "مادة بلاستيكية"), ("Conducteur", "موصل"), ("Isolant", "عازل")]

IONS = [
 ("I", "Structure de l'atome",
  FIGS(FIG("ions_p3_107.jpg", "Modèle de Bohr"), FIG("ions_p3_109.jpg", "Modèle de Schrödinger (actuel)"))
  + B("def", "Un atome est formé d'un <b>noyau</b> (au centre, presque toute la masse, charges <b>positives</b>) et d'<b>électrons</b> e<sup>−</sup> (charge <b>négative</b>, masse négligeable) qui forment un <b>nuage électronique</b>.")
  + B("def", "Le <b>numéro atomique Z</b> est le nombre de charges positives du noyau. Charge élémentaire : $e = 1{,}6 \\times 10^{-19}\\ \\text{C}$.")
  + B("ret", "$$q_{noyau} = +Z\\,e \\qquad q_{électrons} = -Z\\,e \\qquad q_{atome} = +Z\\,e - Z\\,e = 0$$ L'atome est <b>électriquement neutre</b> : nombre d'électrons = Z.")
  + EC("Le noyau porte autant de charges + que les électrons portent de charges − : elles s'annulent, l'atome n'est pas chargé.")
  + APP(Q("Le soufre a Z = 16. Nombre d'électrons, charge du noyau et charge de l'atome ?", "16 électrons ; $q_n = +16\\,e$ ; $q_a = 0$."),
        VF("Le noyau contient presque toute la masse de l'atome.", True, "Les électrons ont une masse négligeable."))),
 ("II", "Les ions",
  B("def", "Un <b>ion</b> est un atome ou un groupe d'atomes qui a <b>perdu</b> ou <b>gagné</b> un ou plusieurs électrons."
      + UL("<b>Cation</b> : ion positif (électrons perdus). Ex. : Na<sup>+</sup>, Cu<sup>2+</sup>.", "<b>Anion</b> : ion négatif (électrons gagnés). Ex. : Cl<sup>−</sup>, S<sup>2−</sup>."))
  + B("rule", "Formule : symbole (ou formule) + en haut à droite le nombre d'électrons gagnés (−) ou perdus (+). <b>Monoatomique</b> : un seul atome (Fe<sup>3+</sup>) ; <b>polyatomique</b> : plusieurs atomes (SO<sub>4</sub><sup>2−</sup>, NH<sub>4</sub><sup>+</sup>, OH<sup>−</sup>).")
  + B("att", "Quand un atome devient un ion, <b>seul le nombre d'électrons change</b> : la charge du noyau reste $+Z\\,e$.")
  + EC("Perdre des électrons (négatifs) rend l'ion positif ; en gagner le rend négatif. Le chiffre en haut à droite indique combien d'électrons.")
  + SIM
  + APP(QCM("L'ion Na<sup>+</sup> provient d'un atome qui a :", ["gagné 1 électron", "perdu 1 électron"], 1, "Perdre un électron (négatif) donne une charge +."),
        QCM("OH<sup>−</sup> est un ion :", ["monoatomique", "polyatomique"], 1, "Il contient deux atomes (O et H)."),
        Q("L'atome de soufre (Z = 16) gagne 2 électrons. Nombre d'électrons, charge et formule de l'ion ?", "18 électrons ; $q = 16e - 18e = -2e = -3{,}2 \\times 10^{-19}\\ \\text{C}$ ; S<sup>2−</sup> (anion monoatomique)."))),
]
IONS_TRAD = [("Noyau", "نواة"), ("Électron", "إلكترون"), ("Nuage électronique", "سحابة إلكترونية"), ("Numéro atomique", "العدد الذري"),
             ("Charge électrique", "شحنة كهربائية"), ("Ion", "أيون"), ("Cation", "كاتيون"), ("Anion", "أنيون")]

OXY = [
 ("I", "Oxydation du fer : la rouille",
  B("def", "En présence de <b>dioxygène</b> et d'<b>eau</b> (humidité), le fer s'oxyde lentement et forme la <b>rouille</b> (oxyde de fer).<br><b>fer + dioxygène → oxyde de fer</b>")
  + B("ret", "La rouille est <b>poreuse et perméable</b> : l'oxydation continue jusqu'à la destruction du fer. Le sel et l'humidité l'accélèrent.")
  + SIM
  + APP(QCM("Pour rouiller, le fer a besoin :", ["de dioxygène seulement", "d'eau seulement", "de dioxygène et d'eau"], 2, "Il faut à la fois le dioxygène de l'air et l'humidité."))),
 ("II", "Oxydation du cuivre, de l'aluminium et du zinc",
  TAB(["Métal", "Couche formée", "Rôle"], [["Cuivre", "vert-de-gris (vert)", "imperméable : protège"], ["Aluminium", "alumine Al<sub>2</sub>O<sub>3</sub>", "imperméable : protège"], ["Zinc", "couche grise", "imperméable : protège"]])
  + APP(VF("La couche d'alumine protège l'aluminium contre la corrosion.", True, "Elle est imperméable, contrairement à la rouille."))),
 ("III", "Protéger le fer",
  B("meth", UL("Isoler le fer de l'air humide : peinture, graisse, plastique.", "Galvanisation : couche de zinc.", "Chromage, nickelage ; acier inoxydable."))
  + B("ret", "Combustion vive d'un métal : il forme un <b>oxyde métallique</b> (fer → Fe<sub>3</sub>O<sub>4</sub>, aluminium → Al<sub>2</sub>O<sub>3</sub>, cuivre → CuO).")
  + APP(Q("Pourquoi peint-on les portails en fer ?", "La peinture isole le fer de l'air humide et empêche la rouille."))),
]
OXY_TRAD = [("Oxydation", "أكسدة"), ("Rouille", "الصدأ"), ("Oxyde", "أكسيد"), ("Corrosion", "تآكل"), ("Perméable", "نفوذ"), ("Imperméable", "كتيم")]
