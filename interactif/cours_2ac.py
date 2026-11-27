# -*- coding: utf-8 -*-
"""Cours 2AC (2APIC) — d'après les cours de Pr. Youness HAFIDI : l'essentiel, définitions, relations et applications."""
from cours_lib import *

H4 = lambda t: f"<h4>{t}</h4>"
H5 = lambda t: f"<h5>{t}</h5>"
PIE = ('<div class="pie"><div class="pie-c" style="background:conic-gradient(#1d4ed8 0 78%,#d62828 78% 99%,#e6c200 99% 100%)"></div>'
       '<ul><li><i style="background:#1d4ed8"></i>Diazote N<sub>2</sub> : 78 %</li><li><i style="background:#d62828"></i>Dioxygène O<sub>2</sub> : 21 %</li>'
       '<li><i style="background:#e6c200"></i>Autres gaz (argon…) : 1 %</li></ul></div>')

AIR = [
 ("I", "L'atmosphère",
  B("sit", "Dans la cour de l'établissement, Sara et Yassine voient les arbres et les feuilles bouger sous l'effet du vent. Ils se demandent : <b>pourquoi l'air se déplace-t-il d'un endroit à un autre ?</b>" + FIG("2ac_air_sit1.webp", "", 380))
  + H4("1. Définition")
  + B("def", "L'<b>atmosphère</b> est la couche d'air qui entoure la Terre, sur plusieurs centaines de kilomètres d'altitude. Elle se divise en <b>plusieurs couches</b>.")
  + H4("2. Les principales couches de l'atmosphère et le rôle de la couche d'ozone")
  + FIGS(FIG("2ac_air_doc1.webp", "Doc. 1 : les différentes couches de l'atmosphère terrestre"), FIG("2ac_air_couches.svg", "Schéma des cinq couches (pas à l'échelle)"))
  + TAB(["Couche", "Altitude", "Caractéristiques"], [
      ["<b>Troposphère</b>", "0 – 15 km", "en contact avec la Terre ; nuages, vent, pluie ; 90 % de la masse de l'air ; la température diminue (15 °C → −56 °C)"],
      ["<b>Stratosphère</b>", "15 – 50 km", "contient la <b>couche d'ozone</b> ; la température augmente (−56 °C → 0 °C)"],
      ["<b>Mésosphère</b>", "50 – 80 km", "la couche la plus froide ; les météorites y brûlent"],
      ["<b>Thermosphère</b>", "80 – 800 km", "très peu d'air ; la température augmente fortement ; pression très faible"],
      ["<b>Exosphère</b>", "au-delà de 800 km", "couche la plus externe, transition avec l'espace ; certains satellites"]])
  + B("rem", "La <b>pression atmosphérique diminue</b> quand l'altitude augmente. La température, elle, peut diminuer ou augmenter selon la couche.")
  + B("ret", "Rôle de la <b>couche d'ozone</b> : elle absorbe une grande partie des rayons <b>ultraviolets (UV)</b> dangereux du Soleil et protège ainsi les êtres vivants.")
  + APP(QCM("Dans quelle couche vivons-nous ?", ["Stratosphère", "Troposphère", "Exosphère"], 1, "La troposphère est la couche en contact avec la Terre."),
        QCM("La couche d'ozone se trouve dans :", ["la troposphère", "la stratosphère", "la mésosphère"], 1, "Elle est dans la stratosphère, entre 15 et 50 km."),
        VF("Plus on monte en altitude, plus la pression atmosphérique augmente.", False, "La pression diminue quand l'altitude augmente."))),
 ("II", "Mouvement de l'air – formation du vent",
  H4("1. Mouvement vertical de l'air")
  + B("ret", UL("<b>Zone chaude</b> : l'air chaud, plus léger, <b>monte</b> → il se crée une zone de <b>basse pression</b>.",
                "<b>Zone froide</b> : l'air froid, plus lourd, <b>descend</b> → il se crée une zone de <b>haute pression</b>."))
  + FIGS(FIG("2ac_air_tourniquet.webp", "Le tourniquet tourne au-dessus de la bougie allumée"), FIG("2ac_air_chaudfroid.webp", "L'air chaud monte, l'air froid descend"))
  + EC("Au-dessus d'une bougie, l'air se réchauffe, devient plus léger et monte : c'est lui qui fait tourner le tourniquet.")
  + H4("2. Mouvement horizontal de l'air")
  + B("ret", "L'air se déplace <b>horizontalement</b> d'une zone de <b>haute pression</b> vers une zone de <b>basse pression</b>.")
  + FIG("2ac_air_feuilles.svg", "On souffle entre deux feuilles : elles se rapprochent", 360)
  + EC("Quand on souffle entre deux feuilles, la pression baisse entre elles : l'air autour, à plus haute pression, les pousse l'une vers l'autre.")
  + FIG("2ac_air_vent.webp", "Le vent : de la haute pression vers la basse pression", 560)
  + B("def", "Le <b>vent</b> est un mouvement <b>horizontal</b> de l'air, dirigé de la zone de <b>haute pression</b> atmosphérique vers la zone de <b>basse pression</b> atmosphérique.")
  + APP(QCM("Région A : 1000 hPa ; région B : 1020 hPa. Le vent souffle :", ["de A vers B", "de B vers A"], 1, "De la haute pression (B, 1020 hPa) vers la basse pression (A, 1000 hPa)."),
        QCM("Au-dessus d'une zone chaude, l'air :", ["descend et crée une haute pression", "monte et crée une basse pression"], 1, "L'air chaud est plus léger : il monte et laisse une zone de basse pression."))),
 ("III", "Les constituants de l'air",
  B("sit", "Au bord du lac, Salma gonfle un ballon : elle peut encore y pousser de l'air quand il semble plein, et le ballon gonflé paraît plus lourd. Le soir, une bougie couverte d'un verre s'éteint et l'eau monte dans le verre. <b>Quels sont les constituants de l'air et quelles sont ses propriétés ?</b>" + FIG("2ac_air_sit2.webp", "", 380))
  + B("def", "L'air est un <b>mélange homogène</b> composé essentiellement de <b>78 % de diazote</b>, <b>21 % de dioxygène</b> et <b>1 % d'autres gaz</b>.")
  + PIE
  + FIGS(FIG("2ac_air_bougie1.webp", "Bougie allumée sous un flacon renversé"), FIG("2ac_air_bougie2.webp", "La bougie s'éteint : l'eau monte d'environ 1/5"))
  + EC("Une bougie allumée sous un flacon renversé consomme le dioxygène : l'eau monte d'environ 1/5 du volume du flacon (≈ 20 %), la place laissée par le dioxygène.")
  + APP(QCM("Le gaz le plus abondant dans l'air est :", ["le dioxygène", "le diazote", "le dioxyde de carbone"], 1, "Le diazote représente environ 78 % de l'air."),
        Q("Un flacon contient 500 mL d'air. Quel volume de dioxygène contient-il environ ?", "$V = \\dfrac{21}{100} \\times 500 = 105\\ \\text{mL}$ (environ 1/5 du volume)."))),
 ("IV", "Quelques propriétés de l'air",
  H4("1. L'air est compressible et expansible")
  + FIG("2ac_air_seringue.webp", "Seringue reliée à un manomètre : on pousse puis on tire le piston", 560)
  + B("ret", "L'air n'a pas de volume propre : comme tous les gaz, il est <b>compressible</b> et <b>expansible</b>. À température constante :"
      + UL("si le volume <b>diminue</b>, la pression <b>augmente</b> (compression) ;", "si le volume <b>augmente</b>, la pression <b>diminue</b> (expansion)."))
  + EC("Pousser le piston serre l'air dans moins de place : le manomètre indique une pression plus grande.")
  + SIM
  + APP(VF("Quand on pousse le piston d'une seringue bouchée, la pression de l'air diminue.", False, "Le volume diminue, donc la pression augmente."))
  + H4("2. L'air possède une masse")
  + "<h5>a) L'air a-t-il une masse ?</h5>"
  + FIG("2ac_air_ballons.webp", "Ballon mal gonflé : 439 g — ballon gonflé : 445 g", 520)
  + B("ret", "L'air est <b>pesant</b> : l'air possède une masse.$$m_{\\text{air}} = m_2 - m_1$$")
  + EC("En gonflant le ballon, sa masse passe de 439 g à 445 g : les 6 g en plus sont la masse de l'air ajouté.")
  + "<h5>b) Quelle est la masse d'un litre d'air ?</h5>"
  + FIG("2ac_air_litre.webp", "On retire 1 L d'air du ballon : 445,0 g → 443,7 g", 620)
  + B("ret", "Dans les conditions habituelles de température et de pression, la <b>masse d'un litre d'air</b> est voisine de <b>1,3 g</b>.$$m = m_1 - m_2 = 445{,}0 - 443{,}7 = 1{,}3\\ \\text{g}$$")
  + B("rem", "Conditions habituelles : température ≈ <b>20 °C</b> et pression atmosphérique ≈ <b>1013 hPa</b>. Si la température ou la pression change, la masse d'un litre d'air change aussi.")
  + APP(Q("Un ballon pèse 439 g ; on le gonfle et il pèse 445 g. Quelle est la masse de l'air ajouté ?", "$m = 445 - 439 = 6\\ \\text{g}$."),
        Q("Quelle est la masse de 5 L d'air dans les conditions habituelles ?", "$m = 5 \\times 1{,}3 = 6{,}5\\ \\text{g}$."))),
]
AIR_TRAD = [("Atmosphère", "الغلاف الجوي"), ("Couche", "طبقة"), ("Pression atmosphérique", "الضغط الجوي"), ("Vent", "الرياح"),
            ("Pression", "ضغط"), ("Compression", "انضغاط"), ("Expansion", "توسع"), ("Mélange", "خليط"), ("Manomètre", "مانومتر")]

MOLA = [
 ("I", "Les atomes",
  B("sit", "En classe, un élève demande : « Monsieur, la trousse, le stylo, la table et même l'air… ils sont faits de quoi exactement ? » <b>Qu'y a-t-il à l'intérieur de toute cette matière ?</b>" + FIG("2ac_mol_sit.webp", "", 380))
  + FIG("2ac_mol_sucre.webp", "Le sucre se dissout dans l'eau", 560)
  + EC("Le sucre versé dans l'eau ne disparaît pas : il se dissout, il se divise en particules si petites qu'on ne les voit plus.")
  + H4("1. Définition")
  + B("def", "La matière est constituée de très petites particules invisibles à l'œil nu : ces particules s'appellent des <b>atomes</b>.")
  + FIGS(FIG("2ac_mol_or.webp", "L'or : des atomes d'or"), FIG("2ac_mol_fer.webp", "Le fer : des atomes de fer"))
  + H4("2. Le symbole chimique")
  + B("rule", "Le symbole d'un atome est la <b>première lettre</b> de son nom en <b>majuscule</b>, parfois suivie d'une <b>deuxième lettre en minuscule</b> pour différencier deux atomes dont les noms commencent par la même lettre.")
  + B("ex", "Carbone → C ; Chlore → Cl ; Fer → Fe")
  + H4("3. Modèle de l'atome")
  + B("def", "Dans un modèle simplifié, un atome est représenté par une <b>sphère</b>. Son diamètre est de l'ordre de <b>0,1 nm</b>.$$1\\ \\text{nm} = 10^{-9}\\ \\text{m}$$")
  + B("ret", "Les atomes sont représentés par des sphères de <b>couleurs</b> et de <b>tailles</b> différentes.")
  + TAB(["Nom de l'atome", "Symbole", "Modèle"], [["Hydrogène", "H", MOL("H")], ["Oxygène", "O", MOL("O")], ["Carbone", "C", MOL("C")], ["Azote", "N", MOL("N")],
                                                ["Chlore", "Cl", MOL("Cl")], ["Soufre", "S", MOL("S")], ["Fer", "Fe", "—"]])
  + APP(Q("Corriger les symboles mal écrits : cl ; FE ; n ; So (soufre).", "Cl ; Fe ; N ; S."),
        QCM("Le symbole S représente l'atome de :", ["sodium", "soufre", "silicium"], 1, "Dans ce cours : S = soufre ; C = carbone ; H = hydrogène."))),
 ("II", "Les molécules",
  H4("1. Définition")
  + B("def", "Une <b>molécule</b> est un ensemble d'<b>atomes liés</b> entre eux.")
  + EC("Les atomes ne restent pas toujours isolés : ils peuvent s'associer pour former des molécules.")
  + H4("2. Méthode : écriture de la formule d'une molécule")
  + B("meth", OL("On écrit les <b>symboles</b> des atomes qui la composent.",
                 "On écrit le <b>nombre d'atomes</b> de même type <b>en indice</b>, en bas à droite du symbole (le chiffre 1 ne s'écrit pas)."))
  + B("ex", "CO<sub>2</sub> : 1 atome de carbone et 2 atomes d'oxygène.")
  + H4("3. Exemples de molécules")
  + TAB(["Modèle", "Formule", "Nom", "Composition"], [
      ["<b>Cas 1 : deux atomes identiques</b>", "", "", ""],
      [MOL("O2"), "O<sub>2</sub>", "dioxygène", "2 O"], [MOL("N2"), "N<sub>2</sub>", "diazote", "2 N"], [MOL("Cl2"), "Cl<sub>2</sub>", "dichlore", "2 Cl"], [MOL("H2"), "H<sub>2</sub>", "dihydrogène", "2 H"],
      ["<b>Cas 2 : deux atomes d'oxygène + un atome</b>", "", "", ""],
      [MOL("CO2"), "CO<sub>2</sub>", "dioxyde de carbone", "1 C + 2 O"], [MOL("NO2"), "NO<sub>2</sub>", "dioxyde d'azote", "1 N + 2 O"],
      ["<b>Cas 3 : des atomes différents</b>", "", "", ""],
      [MOL("H2O"), "H<sub>2</sub>O", "eau", "2 H + 1 O"], [MOL("CH4"), "CH<sub>4</sub>", "méthane", "1 C + 4 H"], [MOL("CO"), "CO", "monoxyde de carbone", "1 C + 1 O"]], "mols")
  + SIM
  + APP(Q("La molécule d'ammoniac est formée d'un atome d'azote et de trois atomes d'hydrogène. Écrire sa formule.", "NH<sub>3</sub>"),
        Q("La molécule de butane est formée de 4 atomes de carbone et de 10 atomes d'hydrogène. Écrire sa formule.", "C<sub>4</sub>H<sub>10</sub>"),
        Q("Donner la composition de la molécule de glucose C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>.", "6 atomes de carbone, 12 atomes d'hydrogène et 6 atomes d'oxygène."))
  + H4("4. Corps pur simple et corps composé")
  + B("def", UL("<b>Corps pur simple</b> : ses molécules sont formées d'<b>une seule sorte</b> d'atome. Ex. : O<sub>2</sub>, H<sub>2</sub>, N<sub>2</sub>.",
                "<b>Corps composé</b> : ses molécules sont formées de <b>deux sortes d'atomes ou plus</b>. Ex. : H<sub>2</sub>O, CO<sub>2</sub>, C<sub>4</sub>H<sub>10</sub>."))
  + APP(Q("Classer : Cl<sub>2</sub> ; CH<sub>4</sub> ; O<sub>3</sub> (ozone) ; NO<sub>2</sub> ; H<sub>2</sub> ; C<sub>4</sub>H<sub>10</sub> ; SO<sub>2</sub> ; N<sub>2</sub>.",
            "Corps purs simples : Cl<sub>2</sub> ; O<sub>3</sub> ; H<sub>2</sub> ; N<sub>2</sub>.<br>Corps composés : CH<sub>4</sub> ; NO<sub>2</sub> ; C<sub>4</sub>H<sub>10</sub> ; SO<sub>2</sub>."),
        QCM("H<sub>2</sub>O est :", ["un corps pur simple", "un corps composé"], 1, "Deux sortes d'atomes : H et O."))),
 ("III", "Interprétation moléculaire de l'air",
  B("def", "L'air est un mélange de molécules : surtout du diazote N<sub>2</sub> (78 %) et du dioxygène O<sub>2</sub> (21 %).")
  + B("ret", "Lors de la compression ou de l'expansion de l'air, le <b>nombre</b> et la <b>taille</b> des molécules <b>ne changent pas</b>. Seul l'<b>espace entre les molécules</b> varie.")
  + TAB(["", "Compression (on pousse le piston)", "Expansion (on tire le piston)"], [
      ["Volume de l'air", "diminue", "augmente"], ["Espace entre les molécules", "diminue", "augmente"], ["Nombre de molécules", "ne change pas", "ne change pas"]])
  + APP(Q("Une seringue bouchée contient 60 mL d'air. On pousse le piston jusqu'à 30 mL. Comment appelle-t-on cette transformation ? Le nombre de molécules change-t-il ? Que devient l'espace entre les molécules ?",
          "C'est une <b>compression</b> (le volume diminue). Le nombre (et la taille) des molécules ne change pas. L'espace entre les molécules diminue."))),
]
MOLA.append(("IV", "Synthèse du cours",
  TAB(["Notion", "À retenir"], [["Atome", "particule qui constitue la matière, représentée par une sphère"], ["Symbole chimique", "une ou deux lettres qui identifient l'atome"],
      ["Molécule", "ensemble d'atomes liés entre eux"], ["Indice", "petit nombre en bas à droite du symbole : le nombre d'atomes de ce type"],
      ["Corps pur simple", "molécules d'une seule sorte d'atome"], ["Corps composé", "molécules de plusieurs sortes d'atomes"],
      ["Compression de l'air", "le volume et l'espace entre les molécules diminuent"], ["Expansion de l'air", "le volume et l'espace entre les molécules augmentent"]])
  + B("conc", "Retour à la situation : les objets qui nous entourent (trousse, stylo, table, air) sont faits de matière, formée de très petites particules invisibles, les <b>atomes</b>, qui s'associent en <b>molécules</b>. On représente un atome par une sphère et un symbole (H, O, C…) et une molécule par une formule (H<sub>2</sub>O, CO<sub>2</sub>…).", "Retour à la situation")))
MOLA_TRAD = [("Atome", "ذرة"), ("Molécule", "جزيئة"), ("Particule", "دقيقة"), ("Symbole", "رمز"), ("Formule", "صيغة"), ("Modèle", "نموذج"),
             ("Chimique", "كيميائي"), ("Corps pur", "جسم خالص"), ("Simple", "بسيط"), ("Composé", "مركب")]

COMB = [
 ("I", "La combustion",
  B("sit", "Le jour de l'Aïd, le père de Hakim active le charbon du barbecue avec un soufflet : il brûle beaucoup mieux. Dans la cuisine, une tache noire apparaît sous la marmite chauffée au butane. Le soir, on annonce des intoxications causées par un chauffe-eau à gaz dans une salle de bain mal aérée. <b>Pourquoi ?</b>" + FIG("2ac_comb_sit.webp", "", 420))
  + H4("1. Définition")
  + B("def", "La <b>combustion</b> est une <b>transformation chimique</b> : des corps sont consommés et de nouveaux corps se forment. Il faut trois éléments :"
      + UL("le <b>combustible</b> : le corps qui brûle (charbon, butane, bois, papier…) ;",
           "le <b>comburant</b> : le corps qui permet la combustion, généralement le <b>dioxygène</b> de l'air ;",
           "la <b>source de chaleur</b> : elle déclenche la combustion (flamme, étincelle…)."))
  + H4("2. Combustion du carbone")
  + FIG("2ac_comb_charbon.webp", "Le charbon de bois est constitué essentiellement de carbone (C)", 520)
  + FIG("2ac_comb_carbone.webp", "Charbon incandescent dans l'air puis dans le dioxygène, puis test à l'eau de chaux", 560)
  + B("ret", "Le carbone et le dioxygène (les <b>réactifs</b>) sont consommés ; du dioxyde de carbone (le <b>produit</b>) se forme.<br>Carbone + Dioxygène → Dioxyde de carbone$$C + O_2 \\longrightarrow CO_2$$")
  + FIG("2ac_comb_eq_carbone.webp", "Modèle moléculaire de la combustion du carbone", 560)
  + B("rule", "L'<b>eau de chaux</b> se trouble en présence de <b>dioxyde de carbone</b>.", "Test à connaître")
  + EC("La combustion est plus vive dans le dioxygène pur que dans l'air : c'est pour cela que le soufflet fait mieux brûler le charbon.")
  + APP(Q("Le jour de l'Aïd, on fait brûler du charbon de bois dans le barbecue. Quel est le combustible ? le comburant ? Quel gaz se forme et comment le mettre en évidence ?",
          "Combustible : le carbone (charbon de bois) ; comburant : le dioxygène de l'air. Il se forme du dioxyde de carbone : il trouble l'eau de chaux."),
        QCM("Pourquoi le charbon brûle-t-il mieux quand on souffle dessus ?", ["le soufflet refroidit le charbon", "le soufflet apporte plus de dioxygène"], 1, "Plus de dioxygène : la combustion est plus vive."))
  + H4("3. Combustion du butane")
  + H5("a) Combustion complète")
  + FIGS(FIG("2ac_comb_complete.webp", "Virole ouverte : flamme bleue"), FIG("2ac_comb_complete2.webp", "Après : buée et eau de chaux troublée"))
  + B("ret", "Flamme <b>bleue</b> : le dioxygène est <b>suffisant</b>. Il se forme de l'<b>eau</b> (buée) et du <b>dioxyde de carbone</b> (l'eau de chaux se trouble).<br>Butane + Dioxygène → Dioxyde de carbone + Eau$$C_4H_{10} + O_2 \\longrightarrow CO_2 + H_2O$$")
  + FIG("2ac_comb_eq_butane.webp", "Modèle moléculaire de la combustion complète du butane", 640)
  + H5("b) Combustion incomplète")
  + FIGS(FIG("2ac_comb_incomplete.webp", "Virole fermée : flamme jaune"), FIG("2ac_comb_incomplete2.webp", "Après : dépôt noir de carbone"))
  + B("ret", "Flamme <b>jaune</b> : le dioxygène est <b>insuffisant</b>. Il se forme de l'eau, du dioxyde de carbone, du <b>carbone</b> (dépôt noir) et du <b>monoxyde de carbone</b>.$$C_4H_{10} + O_2 \\longrightarrow CO_2 + H_2O + C + CO$$")
  + H5("c) Le monoxyde de carbone CO")
  + TAB(["Carte d'identité", ""], [["Formule", "CO"], ["Couleur et odeur", "incolore et inodore"], ["État physique", "gaz"],
                                  ["Toxicité", "il se fixe sur le sang et bloque le transport du dioxygène : maux de tête, fatigue, nausées… jusqu'au coma et à la mort"]])
  + B("att", "Le monoxyde de carbone est un gaz <b>invisible, sans odeur et très toxique</b> : on ne le sent pas venir.")
  + FIG("2ac_comb_comparaison.webp", "Combustion complète et combustion incomplète du butane", 620)
  + SIM
  + APP(VF("Une flamme bleue indique une combustion incomplète.", False, "Flamme bleue → combustion complète."),
        VF("Pour obtenir une combustion complète, on ferme la virole.", False, "On ouvre la virole pour faire entrer plus d'air."),
        VF("Le dépôt noir montre la formation du carbone.", True, "Le carbone apparaît quand le dioxygène manque."))),
 ("II", "La combustion de la cigarette",
  B("def", "La combustion de la cigarette dans le dioxygène de l'air est une <b>transformation chimique</b>. Sa fumée contient <b>plus de 4000 substances chimiques</b>, dont la <b>nicotine</b>, le <b>goudron</b> et le <b>monoxyde de carbone</b>.")
  + FIG("2ac_comb_cigarette.webp", "Quelques substances toxiques de la fumée du tabac", 420)
  + B("att", UL("Ces substances passent des poumons dans le sang : maladies du cœur et des vaisseaux sanguins, nombreux cancers.",
                "La nicotine provoque la <b>dépendance</b>.", "La fumée est aussi dangereuse pour l'entourage : c'est le <b>tabagisme passif</b>."))
  + APP(QCM("Quelle substance de la fumée du tabac provoque la dépendance ?", ["le goudron", "la nicotine", "l'eau"], 1, "C'est la nicotine."))),
 ("III", "Dangers et précautions",
  TAB(["Danger", "Précaution"], [["Incendie", "faire attention aux produits combustibles"], ["Explosion", "faire attention aux fuites de gaz (butane)"],
                                 ["Asphyxie", "aérer le lieu de la combustion"], ["Empoisonnement", "régler la virole pour limiter la production de monoxyde de carbone (CO)"]])
  + B("rem", "<b>Combustion explosive</b> : si le combustible est mélangé au dioxygène dans une certaine proportion, une étincelle peut déclencher une combustion qui dégage beaucoup d'énergie en un temps très court.")
  + FIG("2ac_comb_co.webp", "Le monoxyde de carbone est dangereux : précautions", 560)
  + APP(Q("Un chauffe-eau à gaz fonctionne dans une salle de bain fermée et mal aérée. Une personne a mal à la tête et des vertiges. Quel est le type de combustion ? Quel gaz est responsable ? Donner deux précautions.",
          "Combustion <b>incomplète</b> (dioxygène insuffisant, pièce mal aérée). Le responsable est le <b>monoxyde de carbone</b> CO. Précautions : aérer la pièce ; régler la virole pour avoir une flamme bleue (installer le chauffe-eau hors de la salle de bain)."))),
]
COMB.append(("IV", "Retour à la situation",
  B("conc", UL("<b>Le soufflet</b> apporte plus de dioxygène : la combustion du charbon est plus vive.",
               "<b>La tache noire</b> sous la marmite est du carbone : la combustion du butane est incomplète (dioxygène insuffisant).",
               "<b>Le chauffe-eau</b> dans une pièce mal aérée fait une combustion incomplète qui produit du monoxyde de carbone, gaz toxique, incolore et inodore."), "Retour à la situation")))
COMB_TRAD = [("Combustion", "احتراق"), ("Combustible", "المحروق"), ("Comburant", "المحرق"), ("Combustion complète", "احتراق كامل"),
             ("Combustion incomplète", "احتراق غير كامل"), ("Butane", "البوتان"), ("Eau de chaux", "ماء الجير"), ("Charbon de bois", "الفحم الخشبي"),
             ("Substance toxique", "مادة سامة"), ("Intoxication", "تسمم")]
