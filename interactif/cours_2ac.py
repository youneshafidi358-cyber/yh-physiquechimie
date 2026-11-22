# -*- coding: utf-8 -*-
from cours_lib import *

AIR = [
 ("I", "L'atmosphère et la composition de l'air",
  B("def", "L'<b>atmosphère</b> est la couche d'air qui entoure la Terre : troposphère (on y vit), stratosphère (couche d'<b>ozone</b> qui absorbe les rayons <b>ultraviolets</b>), mésosphère, thermosphère, exosphère.")
  + B("def", "L'air est un <b>mélange homogène</b> de gaz : <b>78 % de diazote</b> N<sub>2</sub>, <b>21 % de dioxygène</b> O<sub>2</sub> et <b>1 %</b> d'autres gaz.")
  + '<div class="pie"><div class="pie-c" style="background:conic-gradient(#1d4ed8 0 78%,#d62828 78% 99%,#e6c200 99% 100%)"></div><ul><li><i style="background:#1d4ed8"></i>Diazote : 78 %</li><li><i style="background:#d62828"></i>Dioxygène : 21 %</li><li><i style="background:#e6c200"></i>Autres gaz : 1 %</li></ul></div>'
  + APP(QCM("Dans quelle couche vivons-nous ?", ["Stratosphère", "Troposphère", "Exosphère"], 1, "Nous vivons dans la troposphère, la couche la plus proche du sol."),
        QCM("Le gaz le plus abondant dans l'air est :", ["le dioxygène", "le diazote", "le dioxyde de carbone"], 1, "Le diazote représente environ 78 % de l'air."))),
 ("II", "L'air est compressible et expansible",
  B("ret", "L'air n'a pas de volume propre : il est <b>compressible</b> et <b>expansible</b>. À température constante :"
      + UL("volume $\\downarrow$ &nbsp;⇒&nbsp; pression $\\uparrow$ (compression)", "volume $\\uparrow$ &nbsp;⇒&nbsp; pression $\\downarrow$ (détente)"))
  + EC("Dans une seringue bouchée, on peut serrer l'air : ses molécules se rapprochent, elles cognent plus souvent les parois, donc la pression monte.")
  + SIM
  + APP(VF("Quand on pousse le piston d'une seringue bouchée, la pression de l'air diminue.", False, "Le volume diminue, donc la pression augmente."))),
 ("III", "L'air a une masse",
  B("ret", "L'air est pesant. Dans les conditions habituelles (20 °C, 1013 hPa) : <b>1 L d'air a une masse d'environ 1,3 g</b>.")
  + EC("On pèse un ballon, on retire (ou on ajoute) de l'air, on pèse à nouveau : la différence de masse divisée par le volume donne la masse d'un litre.")
  + B("meth", "Masse d'air retirée (ou ajoutée) : $m = m_1 - m_2$ &nbsp; puis &nbsp; masse de 1 L : $\\dfrac{m}{V}$")
  + APP(Q("Un ballon pèse 445,0 g ; après avoir retiré 1 L d'air, il pèse 443,7 g. Masse de 1 L d'air ?", "$m = 445{,}0 - 443{,}7 = 1{,}3\\ \\text{g}$."),
        Q("Une bouteille rigide pèse 250,0 g ; on y ajoute 5 L d'air : 256,5 g. Masse de 1 L d'air ?", "$\\dfrac{256{,}5 - 250{,}0}{5} = \\dfrac{6{,}5}{5} = 1{,}3\\ \\text{g}$."))),
 ("IV", "Pression atmosphérique et vent",
  B("def", "La <b>pression atmosphérique</b> est la pression exercée par l'air ; on la mesure avec un <b>baromètre</b>, en hectopascal (hPa). Elle <b>diminue</b> quand l'altitude augmente.")
  + B("ret", "Le <b>vent</b> est le déplacement de l'air d'une zone de <b>haute pression</b> vers une zone de <b>basse pression</b>. L'air chaud, plus léger, monte et crée une basse pression.")
  + APP(QCM("Région A : 1000 hPa ; région B : 1020 hPa. Le vent souffle :", ["de A vers B", "de B vers A"], 1, "De la haute pression (B) vers la basse pression (A)."))),
]
AIR_TRAD = [("Air", "الهواء"), ("Mélange homogène", "خليط متجانس"), ("Dioxygène", "ثنائي الأكسجين"), ("Diazote", "ثنائي الآزوت"),
            ("Compressible", "قابل للانضغاط"), ("Expansible", "قابل للتمدد"), ("Pression", "الضغط"), ("Masse", "الكتلة"), ("Vent", "الرياح")]

MOLA = [
 ("I", "Les atomes",
  B("def", "La matière est constituée de très petites particules invisibles à l'œil nu : les <b>atomes</b>. Modèle : une <b>sphère</b> de diamètre $\\approx 0{,}1\\ \\text{nm}$ ($1\\ \\text{nm} = 10^{-9}\\ \\text{m}$).")
  + B("rule", "Symbole = première lettre du nom en <b>majuscule</b>, parfois suivie d'une deuxième lettre en <b>minuscule</b>.")
  + TAB(["Atome", "Symbole", "Modèle"], [["Hydrogène", "H", MOL("H")], ["Oxygène", "O", MOL("O")], ["Carbone", "C", MOL("C")], ["Azote", "N", MOL("N")],
                                         ["Chlore", "Cl", MOL("Cl")], ["Soufre", "S", MOL("S")], ["Fer", "Fe", "—"]])
  + APP(QCM("Le symbole du chlore s'écrit :", ["CL", "cl", "Cl"], 2, "Majuscule puis minuscule : Cl."),
        Q("Corriger : FE ; n ; So (soufre).", "Fe ; N ; S."))),
 ("II", "Les molécules",
  B("def", "Une <b>molécule</b> est un ensemble d'atomes liés entre eux.")
  + B("meth", "Formule : on écrit les symboles des atomes et, en <b>indice</b> en bas à droite, le nombre d'atomes de chaque sorte (1 ne s'écrit pas). Ex. : CO<sub>2</sub> = 1 C + 2 O.")
  + EC("Le petit chiffre en bas à droite compte les atomes du symbole juste avant lui. Pas de chiffre = 1 atome.")
  + TAB(["Modèle", "Formule", "Nom", "Atomes"], [[MOL("O2"), "O<sub>2</sub>", "dioxygène", "2"], [MOL("N2"), "N<sub>2</sub>", "diazote", "2"], [MOL("H2"), "H<sub>2</sub>", "dihydrogène", "2"],
      [MOL("CO2"), "CO<sub>2</sub>", "dioxyde de carbone", "3"], [MOL("H2O"), "H<sub>2</sub>O", "eau", "3"], [MOL("CH4"), "CH<sub>4</sub>", "méthane", "5"], [MOL("CO"), "CO", "monoxyde de carbone", "2"]], "mols")
  + SIM
  + B("def", UL("<b>Corps pur simple</b> : molécules formées d'<b>une seule sorte</b> d'atomes (O<sub>2</sub>, H<sub>2</sub>, N<sub>2</sub>).",
                "<b>Corps composé</b> : molécules formées de <b>plusieurs sortes</b> d'atomes (H<sub>2</sub>O, CO<sub>2</sub>, CH<sub>4</sub>)."))
  + APP(QCM("Combien d'atomes contient la molécule CH<sub>4</sub> ?", ["4", "5", "2"], 1, "1 carbone + 4 hydrogène = 5 atomes."),
        QCM("H<sub>2</sub>O est :", ["un corps pur simple", "un corps composé"], 1, "Deux sortes d'atomes : H et O."),
        VF("O<sub>2</sub> contient deux sortes d'atomes.", False, "Deux atomes de la même sorte (oxygène)."))),
 ("III", "Interprétation moléculaire de l'air",
  B("ret", "Lors d'une compression ou d'une détente, le <b>nombre</b> et la <b>taille</b> des molécules ne changent pas : seul l'<b>espace entre les molécules</b> varie (il diminue à la compression, augmente à la détente).")
  + APP(VF("Quand on chauffe un ballon fermé, le nombre de molécules d'air augmente.", False, "Le nombre ne change pas ; ce sont les distances entre molécules qui augmentent."))),
]
MOLA_TRAD = [("Atome", "ذرة"), ("Molécule", "جزيئة"), ("Symbole", "رمز"), ("Formule", "صيغة"), ("Modèle", "نموذج"),
             ("Corps pur simple", "جسم خالص بسيط"), ("Corps composé", "جسم مركب")]

COMB = [
 ("I", "La combustion",
  B("def", "Une <b>combustion</b> est une transformation chimique : un <b>combustible</b> réagit avec le dioxygène (le <b>comburant</b>) en dégageant de la chaleur. Les corps consommés sont les <b>réactifs</b>, les corps formés sont les <b>produits</b>.")
  + B("ret", "Combustion du carbone : <b>carbone + dioxygène → dioxyde de carbone</b>")
  + B("rule", UL("<b>Eau de chaux</b> qui se trouble → présence de dioxyde de carbone CO<sub>2</sub>.", "<b>Sulfate de cuivre anhydre</b> qui devient bleu → présence d'eau."), "Tests à connaître")
  + APP(QCM("Le comburant d'une combustion est :", ["le carbone", "le dioxygène", "le butane"], 1, "Le dioxygène permet la combustion du combustible."),
        QCM("L'eau de chaux se trouble en présence de :", ["l'eau", "le dioxyde de carbone", "le dioxygène"], 1, "C'est le test du CO<sub>2</sub>."))),
 ("II", "Combustion du butane",
  TAB(["", "Combustion complète", "Combustion incomplète"], [["Air (virole)", "suffisant (ouverte)", "insuffisant (fermée)"], ["Flamme", "bleue, très chaude", "jaune, éclairante"],
      ["Produits", "CO<sub>2</sub> + H<sub>2</sub>O", "CO<sub>2</sub> + H<sub>2</sub>O + C (suie) + CO"]])
  + B("ret", "Combustion complète : <b>butane + dioxygène → dioxyde de carbone + eau</b>")
  + SIM
  + APP(QCM("Une flamme jaune qui noircit une soucoupe indique une combustion :", ["complète", "incomplète"], 1, "Le noir de carbone (suie) apparaît quand il manque du dioxygène."))),
 ("III", "Dangers et précautions",
  B("att", "Le <b>monoxyde de carbone</b> CO (combustion incomplète) est un gaz <b>invisible, inodore et mortel</b>. Le CO<sub>2</sub> contribue à l'effet de serre.")
  + B("ret", UL("Aérer les pièces où fonctionne un appareil à combustion.", "Faire vérifier chauffe-eau et appareils à gaz.", "Ne jamais utiliser un brasero dans une pièce fermée."), "Précautions")
  + APP(VF("Le monoxyde de carbone a une odeur qui permet de le détecter.", False, "Il est inodore : c'est ce qui le rend très dangereux."))),
]
COMB_TRAD = [("Combustion", "احتراق"), ("Combustible", "وقود"), ("Comburant", "محرق"), ("Réactif", "متفاعل"), ("Produit", "ناتج"),
             ("Eau de chaux", "ماء الجير"), ("Dioxyde de carbone", "ثنائي أكسيد الكربون"), ("Monoxyde de carbone", "أحادي أكسيد الكربون")]
