# -*- coding: utf-8 -*-
from cours_lib import *

GRAV = [
 ("I", "Écriture scientifique et ordre de grandeur",
  B("def", "$$X = a \\times 10^{n} \\quad \\text{avec } 1 \\le a < 10 \\text{ et } n \\in \\mathbb{Z}$$ Ordre de grandeur : $10^{n}$ si $a < 5$ ; $10^{n+1}$ si $a \\ge 5$.")
  + TAB(["T", "G", "M", "k", "m", "µ", "n", "p", "f"], [["$10^{12}$", "$10^{9}$", "$10^{6}$", "$10^{3}$", "$10^{-3}$", "$10^{-6}$", "$10^{-9}$", "$10^{-12}$", "$10^{-15}$"]])
  + APP(QCM("Ordre de grandeur de 650 km :", ["$10^{5}$ m", "$10^{6}$ m", "$10^{2}$ m"], 1, "$650\\ \\text{km} = 6{,}5 \\times 10^{5}\\ \\text{m}$ et $6{,}5 \\ge 5$ donc $10^{6}$ m."),
        QCM("Ordre de grandeur de 5 µm :", ["$10^{-6}$ m", "$10^{-5}$ m"], 1, "$5 \\times 10^{-6}$ m avec $a = 5 \\ge 5$ donc $10^{-5}$ m."))),
 ("II", "Loi de la gravitation universelle",
  B("ret", "Deux corps A et B s'attirent mutuellement :$$F_{A/B} = F_{B/A} = G\\,\\frac{m_A\\,m_B}{d^{2}}$$ $G = 6{,}67 \\times 10^{-11}\\ \\text{N·m}^2\\text{·kg}^{-2}$ ; $m$ en kg, $d$ en m (distance entre les centres), $F$ en N.<br>Même droite d'action, sens opposés : $\\vec F_{A/B} = -\\vec F_{B/A}$.")
  + B("ret", "Terre – corps à l'altitude $h$ :$$F = G\\,\\frac{M_T\\,m}{(R_T + h)^{2}}$$")
  + SIM
  + B("att", "On utilise $d = R_T + h$ (et pas $h$), et toutes les distances en mètres.")
  + APP(QCM("Si la distance entre deux corps double, la force de gravitation est :", ["divisée par 2", "divisée par 4", "multipliée par 2"], 1, "$F$ est proportionnelle à $\\dfrac{1}{d^2}$ : $(2d)^2 = 4d^2$."))),
 ("III", "Le poids d'un corps",
  B("def", "Le <b>poids</b> $\\vec P$ : force exercée par la Terre ; point d'application G, direction verticale, sens vers le bas.$$P = m\\,g$$")
  + B("ret", "$$g_0 = G\\,\\frac{M_T}{R_T^{2}} \\approx 9{,}8\\ \\text{N/kg} \\qquad g_h = g_0\\left(\\frac{R_T}{R_T + h}\\right)^{2}$$ Quand $h$ augmente, le poids diminue ; la masse ne change pas.")
  + TAB(["Données", ""], [["$M_T$", "$5{,}98 \\times 10^{24}\\ \\text{kg}$"], ["$R_T$", "$6380\\ \\text{km} = 6{,}38 \\times 10^{6}\\ \\text{m}$"]])
  + APP(Q("Satellite $m = 4{,}5 \\times 10^{3}$ kg au sol ($g_0 = 9{,}8$ N/kg) : poids ?", "$P_0 = 4{,}5 \\times 10^{3} \\times 9{,}8 \\approx 4{,}41 \\times 10^{4}\\ \\text{N}$."),
        QCM("À l'altitude $h = 2R_T$, le poids devient :", ["$P_0/2$", "$P_0/4$", "$P_0/9$"], 2, "$R_T + h = 3R_T$, donc $g_h = g_0/9$."))),
]
GRAV_TRAD = [("Gravitation universelle", "التجاذب الكوني"), ("Ordre de grandeur", "رتبة القدر"), ("Force", "قوة"), ("Poids", "الوزن"), ("Masse", "الكتلة"), ("Intensité de la pesanteur", "شدة الثقالة")]

MECA = [
 ("I", "Actions mécaniques",
  B("def", "Une <b>action mécanique</b> est toute cause capable de mettre en mouvement, de modifier le mouvement, de maintenir en équilibre ou de déformer un corps.")
  + TAB(["Classification", ""], [["Contact localisée", "sur un point (fil tendu)"], ["Contact répartie", "sur une surface (table, vent)"], ["À distance", "toujours répartie (poids, aimant)"]])
  + B("def", "Force <b>extérieure</b> : exercée par un corps hors du système ; <b>intérieure</b> : entre deux parties du système.")
  + APP(QCM("Le poids est une action :", ["de contact localisée", "de contact répartie", "à distance"], 2, "La Terre agit sans contact, sur tout le volume."))),
 ("II", "La force et la réaction d'un support",
  B("def", "Une force $\\vec F$ : point d'application, droite d'action, sens, intensité en newton (N), mesurée au dynamomètre.")
  + B("ret", "$$\\vec R = \\vec R_N + \\vec R_T \\qquad R = \\sqrt{R_N^{2} + R_T^{2}} \\qquad k = \\tan\\varphi = \\frac{R_T}{R_N}$$ Sans frottement : $R_T = 0$, $\\vec R$ perpendiculaire au plan.")
  + SIM
  + APP(Q("$R_N = 3$ N et $R_T = 4$ N : calculer $R$, $k$ et $\\varphi$.", "$R = \\sqrt{9 + 16} = 5\\ \\text{N}$ ; $k = \\dfrac{4}{3} \\approx 1{,}33$ ; $\\varphi \\approx 53^\\circ$."),
        VF("Sans frottement, la réaction est perpendiculaire au plan de contact.", True, "$R_T = 0$ donc $\\vec R = \\vec R_N$."))),
 ("III", "Force pressante et pression",
  B("def", "Force pressante : force répartie exercée par un fluide sur une surface, <b>perpendiculaire</b> à la surface.")
  + B("ret", "$$P = \\frac{F}{S}$$ $P$ en Pa, $F$ en N, $S$ en m². &nbsp; $1\\ \\text{hPa} = 10^{2}\\ \\text{Pa}$ ; $1\\ \\text{bar} = 10^{5}\\ \\text{Pa}$ ; $1\\ \\text{cm}^2 = 10^{-4}\\ \\text{m}^2$")
  + B("def", "<b>Manomètre</b> : pression d'un gaz enfermé ; <b>baromètre</b> : pression atmosphérique.")
  + APP(Q("$F = 375$ N sur $S = 25\\ \\text{cm}^2$ : pression ?", "$P = \\dfrac{375}{25 \\times 10^{-4}} = 1{,}5 \\times 10^{5}\\ \\text{Pa}$."),
        QCM("Pour une même force, si la surface augmente, la pression :", ["augmente", "diminue"], 1, "$P = F/S$ : S plus grande donne P plus petite."))),
]
MECA_TRAD = [("Action mécanique", "تأثير ميكانيكي"), ("Force", "قوة"), ("Frottement", "احتكاك"), ("Force pressante", "قوة الضغط"), ("Pression", "الضغط")]

ESP = [
 ("I", "Espèce chimique",
  B("def", "Une <b>espèce chimique</b> est un ensemble d'entités (molécules, ions ou atomes) <b>identiques</b>. Elle a un nom, une formule et des caractéristiques physiques (T<sub>fusion</sub>, T<sub>ébullition</sub>, densité…). Un <b>corps pur</b> contient une seule espèce chimique.")
  + B("rem", "Nos cinq sens ne suffisent pas pour détecter toutes les espèces chimiques (et peuvent être dangereux) : on utilise des tests chimiques.")
  + APP(VF("L'eau minérale est un corps pur.", False, "Elle contient des ions en plus des molécules d'eau."))),
 ("II", "Tests d'identification",
  FIG("esp_doc8.jpg", "Tableau récapitulatif des tests", 620)
  + TAB(["Espèce recherchée", "Réactif", "Résultat positif"], [["Eau", "sulfate de cuivre anhydre (blanc)", "devient bleu"], ["Glucose", "liqueur de Fehling + chauffage", "précipité rouge brique"],
        ["Acidité", "pH-mètre / BBT", "pH &lt; 7 / BBT jaune"]])
  + B("ret", "BBT : <b>jaune</b> = acide, <b>vert</b> = neutre, <b>bleu</b> = basique.")
  + SIM
  + APP(QCM("Le sulfate de cuivre anhydre devient bleu : cela prouve la présence de :", ["glucose", "eau", "acide"], 1, "C'est le test de l'eau."),
        QCM("Le BBT devient bleu : le milieu est :", ["acide", "neutre", "basique"], 2, "Bleu = basique."))),
 ("III", "Classification des espèces chimiques",
  TAB(["", "Définition", "Exemple"], [["Organique", "contient surtout C et H ; sa combustion donne CO<sub>2</sub> + H<sub>2</sub>O", "glucose, méthane"],
        ["Inorganique", "sa combustion ne donne pas CO<sub>2</sub> + H<sub>2</sub>O", "fer, sel NaCl"], ["Naturelle", "existe dans la nature", "vitamine C de l'orange"],
        ["Synthétique", "fabriquée, mais existe dans la nature (copie)", "vitamine C de pharmacie"], ["Artificielle", "n'existe pas dans la nature", "nylon, PVC, aspartame"]])
  + APP(QCM("La vitamine C fabriquée au laboratoire est une espèce :", ["naturelle", "synthétique", "artificielle"], 1, "Elle existe aussi dans la nature : c'est une copie."))),
 ("IV", "Sécurité au laboratoire",
  FIG("esp_doc11.jpg", "Pictogrammes : corrosif, toxique, inflammable, comburant, dangereux pour l'environnement", 660)
  + B("rule", "Blouse, lunettes, gants ; ne jamais goûter, toucher ni sentir un produit ; ne pas jeter les produits à l'évier.")),
]
ESP_TRAD = [("Espèce chimique", "نوع كيميائي"), ("Corps pur", "جسم خالص"), ("Réactif", "كاشف"), ("Organique", "عضوي"), ("Synthétique", "مصنع")]

EXT = [
 ("I", "L'extraction",
  B("def", "L'<b>extraction</b> permet d'extraire et de séparer une ou plusieurs espèces chimiques d'un produit. Techniques traditionnelles : <b>pressage</b>, <b>infusion</b>, <b>enfleurage</b>.")),
 ("II", "Extraction par solvant",
  B("rule", "Le solvant extracteur doit être :" + UL("non miscible à l'eau ;", "un meilleur solvant de l'espèce que l'eau ;", "volatil, de densité connue."), "Choix du solvant")
  + FIG("ext_doc4.jpg", "Protocole avec l'ampoule à décanter", 720)
  + B("ret", "Dans l'ampoule à décanter, la phase la <b>moins dense</b> est <b>en haut</b>.")
  + SIM
  + APP(QCM("Pour extraire le diiode de l'eau, on choisit :", ["l'alcool (miscible, s = 250 g/L)", "l'éther (non miscible, s = 250 g/L)", "le benzène (non miscible, s = 140 g/L)"], 1, "Non miscible à l'eau et meilleure solubilité."),
        QCM("Éther (d = 0,71) et eau (d = 1) : la phase organique est :", ["en haut", "en bas"], 0, "$0{,}71 < 1$ : la phase organique est au-dessus."))),
 ("III", "Hydrodistillation",
  FIG("ext_doc7.jpg", "Montage d'hydrodistillation", 560)
  + B("def", "L'<b>hydrodistillation</b> : la vapeur d'eau entraîne les espèces volatiles d'une plante ; le <b>réfrigérant</b> les condense en un <b>distillat</b>. Pierre ponce : régularise l'ébullition. <b>Relargage</b> : ajout de sel pour diminuer la solubilité de l'huile dans l'eau.")
  + APP(QCM("Le rôle du réfrigérant est de :", ["chauffer le mélange", "condenser les vapeurs", "régulariser l'ébullition"], 1, "Il refroidit et liquéfie les vapeurs."))),
 ("IV", "Chromatographie sur couche mince (CCM)",
  FIGS(FIG("ext_doc12.jpg", "Résultat d'une CCM"), FIG("ext_doc14.jpg", "h et H"))
  + B("def", "La <b>CCM</b> sépare et identifie les espèces d'un mélange. L'<b>éluant</b> (phase mobile) monte par capillarité sur la plaque (phase fixe).")
  + B("ret", UL("Une seule tache → corps pur ; plusieurs taches → mélange.", "Deux taches à la même hauteur → même espèce chimique.")
      + "$$R_f = \\frac{h}{H} \\qquad (0 < R_f < 1,\\ \\text{sans unité})$$")
  + APP(Q("Une tache monte de $h = 3$ cm et le front de l'éluant de $H = 6$ cm. $R_f$ ?", "$R_f = \\dfrac{3}{6} = 0{,}5$."),
        VF("Un dépôt qui donne trois taches est un corps pur.", False, "Plusieurs taches : c'est un mélange."))),
 ("V", "Caractéristiques physiques",
  B("ret", "$$d = \\frac{\\rho}{\\rho_{eau}} \\qquad \\rho_{eau} = 1\\ \\text{g/cm}^3$$ Températures de fusion et d'ébullition (constantes pour un corps pur). <b>Solubilité</b> $s$ : masse maximale dissoute par litre de solvant (g/L).")),
]
EXT_TRAD = [("Extraction", "استخراج"), ("Solvant", "مذيب"), ("Ampoule à décanter", "أنبوب التصفية"), ("Hydrodistillation", "التقطير المائي"), ("Chromatographie", "التحليل الكروماتوغرافي"), ("Densité", "الكثافة")]
