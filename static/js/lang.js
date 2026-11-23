/* Interface en arabe (bouton « AR / FR »).
   Règles : une phrase est traduite en entier ou pas du tout (jamais à moitié) ; chaque élément traduit est isolé (dir="rtl")
   pour que l'arabe et le français ne se mélangent pas ; les cours, exercices et examens restent en français (BIOF). */
(function () {
  var KEY = 'yh_lang';
  function get() { try { return localStorage.getItem(KEY) || 'fr'; } catch (e) { return 'fr'; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  var WA = '<a href="https://wa.me/212652236922" target="_blank" rel="noopener">واتساب 06 52 23 69 22</a>';

  /* 1) Libellés courts (texte exact) */
  var D = {
    "Accueil": "الرئيسية", "Niveaux": "المستويات", "Leçons": "الدروس", "À propos": "من أنا", "Contact": "اتصل بي", "☰ Menu": "☰",
    "Noter le site": "قيّم الموقع", "★ Noter le site": "★ قيّم الموقع", "Suivre": "تابع", "🔔 Suivre": "🔔 تابع", "Suivi ✓": "متابَع ✓", "🔔 Suivi ✓": "🔔 متابَع ✓",
    "Merci pour ton avis": "شكراً على رأيك", "★ Merci pour ton avis": "★ شكراً على رأيك", "Donne ta note au site :": "قيّم الموقع :",
    "Aller au contenu": "انتقل إلى المحتوى", "Fermer": "إغلاق", "Rechercher": "بحث", "Rechercher une leçon": "ابحث عن درس", "Populaire :": "الأكثر بحثاً :",
    "Choisir mon niveau": "اختر مستواي", "Choisis ton niveau": "اختر مستواك", "Tous les niveaux": "كل المستويات",
    "Physique-Chimie · Collège et lycée · Gratuit": "الفيزياء والكيمياء · الإعدادي والثانوي · مجاناً",
    "Professeur de Physique-Chimie · Cycle secondaire": "أستاذ الفيزياء والكيمياء · التعليم الثانوي", "Professeur de physique-chimie · Cycle secondaire": "أستاذ الفيزياء والكيمياء · التعليم الثانوي", "Pr. Youness HAFIDI": "ذ. يونس حافظي",
    "1re année collège": "الأولى إعدادي", "2e année collège": "الثانية إعدادي", "3e année collège": "الثالثة إعدادي",
    "Tronc commun scientifique": "الجذع المشترك العلمي", "Tronc commun": "الجذع المشترك", "1re année Baccalauréat": "الأولى باكالوريا", "2e année Baccalauréat": "الثانية باكالوريا",
    "1AC – 1re année collège": "1AC – الأولى إعدادي", "2AC – 2e année collège": "2AC – الثانية إعدادي", "3AC – 3e année collège": "3AC – الثالثة إعدادي",
    "TCS – Tronc commun scientifique": "TCS – الجذع المشترك العلمي", "1BAC – 1re année Baccalauréat": "1BAC – الأولى باكالوريا", "2BAC – 2e année Baccalauréat": "2BAC – الثانية باكالوريا",
    "1BAC (bientôt)": "1BAC (قريباً)", "2BAC (bientôt)": "2BAC (قريباً)",
    "Cours": "الدروس", "Exercices": "التمارين", "Devoirs": "الفروض", "Examens": "الامتحانات", "Simulations": "المحاكاة", "Quiz": "اختبار ذاتي", "Vidéos": "الفيديوهات",
    "Tout": "الكل", "Séries": "السلاسل", "Corrigés": "التصحيحات", "Contrôles": "الفروض",
    "Cours · simulation · quiz": "درس · محاكاة · اختبار ذاتي", "📖 Cours · 🧪 Simulation · ✍️ Exercices corrigés · ✅ Quiz": "📖 درس · 🧪 محاكاة · ✍️ تمارين مصححة · ✅ اختبار ذاتي",
    "✍️ Exercices corrigés · ✅ Quiz": "✍️ تمارين مصححة · ✅ اختبار ذاتي", "Cours, simulation, exercices et corrigés": "درس، محاكاة، تمارين وتصحيحات",
    "Lire le cours →": "اقرأ الدرس ←", "S'entraîner →": "تدرّب ←", "Ouvrir →": "افتح ←", "Voir la correction →": "شاهد التصحيح ←", "Voir les examens →": "شاهد الامتحانات ←",
    "Voir toutes les simulations →": "كل المحاكاة ←", "Choisir la version →": "اختر النسخة ←", "Page de la leçon →": "صفحة الدرس ←", "Résumé et exercices →": "الملخص والتمارين ←",
    "Bientôt": "قريباً", "Bientôt disponible": "قريباً", "Bientôt disponible.": "قريباً.", "Gratuit": "مجاني", "Gratuit · en ligne": "مجاني · عبر الإنترنت",
    "Série d'exercices + corrigé côte à côte": "سلسلة تمارين + التصحيح جنباً إلى جنب", "Énoncé + corrigé pas à pas": "النص + التصحيح خطوة بخطوة", "Énoncé + corrigé détaillé": "النص + تصحيح مفصل",
    "Chaque version corrigée en détail, exercice par exercice": "كل نسخة مصححة بالتفصيل، تمريناً تمريناً", "Sujet + correction détaillée pas à pas": "الموضوع + تصحيح مفصل خطوة بخطوة",
    "Sujet": "الموضوع", "Corrigé": "التصحيح", "📄 Sujet": "📄 الموضوع", "✅ Corrigé": "✅ التصحيح", "✅ Corrigé détaillé": "✅ تصحيح مفصل", "📄 Sujet (PDF)": "📄 الموضوع",
    "Normale": "عادية", "Rattrapage": "استدراكية", "Semestre 1": "الدورة الأولى", "Physique": "فيزياء", "Chimie": "كيمياء", "Physique-Chimie": "فيزياء وكيمياء",
    "Toutes les leçons": "كل الدروس", "Toutes les leçons par niveau": "كل الدروس حسب المستوى", "Résultats de la recherche": "نتائج البحث",
    "Tout pour réussir, au même endroit": "كل ما تحتاجه للنجاح في مكان واحد", "Résumés interactifs": "ملخصات تفاعلية", "Chaque leçon en carte mentale cliquable.": "كل درس في خريطة ذهنية تفاعلية.",
    "Exercices corrigés": "تمارين مصححة", "✍️ Exercices corrigés": "✍️ تمارين مصححة", "Énoncé et correction côte à côte + erreurs fréquentes.": "النص والتصحيح جنباً إلى جنب + الأخطاء الشائعة.",
    "Teste-toi et obtiens ta note tout de suite.": "اختبر نفسك واحصل على نقطتك فوراً.", "Fais les expériences en ligne, sans danger.": "أنجز التجارب عبر الإنترنت دون خطر.",
    "Devoirs surveillés": "الفروض المحروسة", "Sujets + corrigés + barèmes, pour s'entraîner.": "مواضيع + تصحيحات + سلم التنقيط للتدرّب.",
    "Le labo virtuel": "المختبر الافتراضي", "🧪 Labo virtuel": "🧪 المختبر الافتراضي", "Comment réviser avec le site ?": "كيف تراجع بالموقع ؟",
    "Cours de soutien": "دروس الدعم", "★ Cours de soutien": "★ دروس الدعم", "Cours de soutien en Physique-Chimie": "دروس الدعم في الفيزياء والكيمياء",
    "Réserver sur WhatsApp": "احجز عبر واتساب", "réserver sur WhatsApp": "احجز عبر واتساب", "Appeler": "اتصل", "Page Facebook": "صفحة فيسبوك",
    "Affiche en français": "الملصق بالفرنسية", "Affiche en arabe": "الملصق بالعربية",
    "Partager sur WhatsApp": "شارك على واتساب", "Partager sur Facebook": "شارك على فيسبوك", "🔗 Copier le lien": "🔗 انسخ الرابط", "Lien copié ✓": "تم نسخ الرابط ✓", "✓ Lien copié": "✓ تم نسخ الرابط",
    "Lecture seule — téléchargement désactivé": "قراءة فقط — التحميل غير متاح", "Le site": "الموقع", "Contactez-moi sur WhatsApp": "تواصل معي عبر واتساب",
    "Contrôles surveillés – Semestre 1": "الفروض المحروسة – الدورة الأولى", "Examens locaux – Semestre 1": "الامتحانات المحلية – الدورة الأولى",
    "Examens nationaux – 2BAC Sciences Mathématiques": "الامتحانات الوطنية – 2BAC علوم رياضية",
    "Tous les examens locaux 3AC": "كل الامتحانات المحلية 3AC", "Page dédiée · sujets + corrigés": "صفحة خاصة · مواضيع + تصحيحات", "Liste complète par année": "اللائحة الكاملة حسب السنة",
    "Sciences Mathématiques (SM A et B)": "العلوم الرياضية (أ و ب)", "Sciences Physiques (PC)": "العلوم الفيزيائية", "Sessions normale et rattrapage · sujet + corrigé": "الدورتان العادية والاستدراكية · موضوع + تصحيح",
    "Tous les examens SM et PC": "كل امتحانات العلوم الرياضية والفيزيائية", "Examens nationaux : tableau, mode examen et mes notes": "الامتحانات الوطنية : الجدول، وضع الامتحان ونقطي",
    "Chronomètre 4 h / 3 h · exercices par thème · calcul de la note du bac": "عداد 4 س / 3 س · تمارين حسب الدرس · حساب معدل الباكالوريا",
    "2BAC Sciences Mathématiques · 4 heures": "2BAC علوم رياضية · 4 ساعات", "2BAC Sciences Physiques · 3 heures": "2BAC علوم فيزيائية · 3 ساعات",
    "📐 Sciences Maths": "📐 العلوم الرياضية", "🔬 Sciences Physiques": "🔬 العلوم الفيزيائية", "📝 Sujets et corrigés": "📝 المواضيع والتصحيحات", "📊 Mes résultats": "📊 نتائجي", "📚 Exercices par thème": "📚 التمارين حسب الدرس",
    "📐 Sciences Mathématiques – examens nationaux": "📐 العلوم الرياضية – الامتحانات الوطنية", "🔬 Sciences Physiques – examens nationaux": "🔬 العلوم الفيزيائية – الامتحانات الوطنية",
    "Année": "السنة", "Session": "الدورة", "Ma note": "نقطتي", "S'entraîner (4 h)": "تدرّب (4 س)", "S'entraîner (3 h)": "تدرّب (3 س)", "⏱ Mode examen": "⏱ وضع الامتحان", "Terminer": "إنهاء", "Sûr ? Terminer": "متأكد ؟ إنهاء",
    "✅ Voir le corrigé": "✅ شاهد التصحيح", "Enregistrer": "حفظ", "✔ Enregistré": "✔ تم الحفظ", "Ma note :": "نقطتي :", "⏰ Temps écoulé !": "⏰ انتهى الوقت !", "✅ Examen terminé.": "✅ انتهى الامتحان.", "⏰ Terminé": "⏰ انتهى",
    "meilleure note": "أحسن نقطة", "moyenne /20": "المعدل /20", "examen faits": "امتحان منجز", "examens faits": "امتحانات منجزة",
    "Bac SM · PC": "باكالوريا علوم رياضية · فيزيائية", "Format officiel": "الشكل الرسمي",
    "Ondes mécaniques et lumineuses": "الموجات الميكانيكية والضوئية", "Transformations nucléaires": "التحولات النووية", "Dipôles RC et RL": "ثنائيا القطب RC و RL",
    "Oscillations électriques (LC, RLC libre et forcé)": "التذبذبات الكهربائية (LC، RLC الحرة والقسرية)", "Modulation d'amplitude": "تضمين الوسع",
    "Mécanique : lois de Newton, chutes, projectiles, champs": "الميكانيك : قوانين نيوتن، السقوط، المقذوفات، المجالات", "Oscillateurs mécaniques et énergie": "المتذبذبات الميكانيكية والطاقة",
    "Chimie : acide-base, dosages, indicateurs": "الكيمياء : الأحماض والقواعد، المعايرة، الكواشف", "Chimie : électrolyse et piles": "الكيمياء : التحليل الكهربائي والأعمدة", "Chimie : cinétique et estérification": "الكيمياء : الحركية والأسترة",
    "Calcul de la note du bac (Maroc)": "حساب معدل البكالوريا", "Contrôle continu (2BAC)": "المراقبة المستمرة (الثانية باك)", "Examen régional (1BAC)": "الامتحان الجهوي (الأولى باك)",
    "Examen national": "الامتحان الوطني", "(laisse vide pour savoir la note nécessaire)": "(اتركه فارغاً لمعرفة النقطة اللازمة)",
    "📖 Cours": "📖 الدرس", "🧠 Résumé": "🧠 الملخص", "✅ Quiz": "✅ اختبار ذاتي", "📄 PDF": "📄 PDF", "📖 Le cours": "📖 الدرس",
    "🧠 Résumé de la leçon (carte mentale)": "🧠 ملخص الدرس (خريطة ذهنية)", "✍️ Exercices : énoncé et correction côte à côte": "✍️ التمارين : النص والتصحيح جنباً إلى جنب",
    "✅ Quiz : teste-toi !": "✅ اختبر نفسك !", "📄 Série et corrigé (PDF)": "📄 السلسلة والتصحيح (PDF)",
    "Suivant →": "التالي ←", "← Précédent": "→ السابق", "Voir la réponse": "شاهد الجواب", "Masquer la réponse": "إخفاء الجواب", "Tout ouvrir": "فتح الكل", "Tout fermer": "إغلاق الكل",
    "Afficher toutes les réponses": "إظهار كل الأجوبة", "Masquer toutes les réponses": "إخفاء كل الأجوبة", "⚠ Erreur fréquente": "⚠ خطأ شائع",
    "💬 Ce que disent les visiteurs": "💬 آراء الزوار", "Corrige-toi avec le corrigé, puis note-toi sur 20.": "صحّح ورقتك بالتصحيح، ثم نقّط نفسك على 20.", "Envoyer": "إرسال", "Merci !": "شكراً !", "Annuler": "إلغاء"
  };

  /* 2) Phrases entières (texte exact -> HTML arabe). Valeur "" = élément masqué en arabe. */
  var B = {
    "Comprendre la physique-chimie, simplement.": "افهم الفيزياء والكيمياء، <em>ببساطة.</em>",
    "Résumés en cartes mentales, séries et corrigés côte à côte, quiz, simulations et devoirs surveillés — par Pr. Youness HAFIDI.": "ملخصات على شكل خرائط ذهنية، سلاسل وتصحيحات جنباً إلى جنب، اختبارات ذاتية، محاكاة وفروض محروسة — مع <b>ذ. يونس حافظي</b>.",
    "Lis le résumé de la leçon (carte mentale).": "<strong>اقرأ ملخص</strong> الدرس (الخريطة الذهنية).",
    "Cherche les exercices seul, sur ta feuille.": "<strong>حلّ التمارين</strong> وحدك على ورقتك.",
    "Vérifie avec « Voir la réponse » et « Erreur fréquente ».": "<strong>تحقّق</strong> بـ « شاهد الجواب » و« خطأ شائع ».",
    "Fais le quiz et la simulation, puis un devoir.": "<strong>أنجز الاختبار الذاتي</strong> والمحاكاة، ثم فرضاً.",
    "Comprends aujourd'hui, réussis demain ! Du 1AC au 2BAC, à distance ou à domicile.": "افهم اليوم، تنجح غداً ! من الأولى إعدادي إلى الثانية باكالوريا، عن بعد أو بالمنزل.",
    "Niveaux : 1AC, 2AC, 3AC, Tronc commun scientifique, 1BAC, 2BAC": "<b>المستويات :</b> الأولى والثانية والثالثة إعدادي، الجذع المشترك العلمي، الأولى والثانية باكالوريا",
    "Programme : explication claire des cours, exercices d'application corrigés, préparation aux contrôles et examens": "<b>البرنامج :</b> شرح واضح للدروس، تمارين تطبيقية مصححة، تحضير للفروض والامتحانات",
    "Suivi personnalisé selon le niveau de chaque élève, remise à niveau et consolidation des acquis": "<b>تتبّع شخصي</b> حسب مستوى كل تلميذ، تقوية وترسيخ المكتسبات",
    "Modes : cours à distance (en ligne) ou à domicile (individuel ou petit groupe)": "<b>الصيغ :</b> دروس عن بعد (عبر الإنترنت) أو بالمنزل (فردية أو في مجموعة صغيرة)",
    "Ressources gratuites de physique-chimie par Pr. Youness HAFIDI, professeur au cycle secondaire.": "موارد مجانية في الفيزياء والكيمياء من إعداد ذ. يونس حافظي، أستاذ بالتعليم الثانوي.",
    "© Pr. Youness HAFIDI — Consultation en ligne uniquement · Reproduction interdite sans autorisation": "© ذ. يونس حافظي — للاطلاع عبر الإنترنت فقط · يمنع النسخ دون إذن",
    "© Pr. Youness HAFIDI — Physique-Chimie · Consultation en ligne uniquement": "© ذ. يونس حافظي — الفيزياء والكيمياء · للاطلاع عبر الإنترنت فقط",
    "Les séries, corrigés et résumés de ce niveau arrivent très prochainement.": "السلاسل والتصحيحات والملخصات الخاصة بهذا المستوى ستتوفر قريباً جداً.",
    "Entraîne-toi avec les examens nationaux du baccalauréat : sujet au format officiel et corrigé détaillé vérifié avec la grille du ministère. Lance le ⏱ mode examen pour composer en temps réel (4 h en SM, 3 h en PC) : le corrigé s'ouvre quand tu termines, puis tu notes ta copie pour suivre ta progression.": "تدرّب على <b>الامتحانات الوطنية للبكالوريا</b> : الموضوع <b>بالشكل الرسمي</b> مع <b>تصحيح مفصل</b> مطابق لعناصر الإجابة الرسمية للوزارة. شغّل <b>⏱ وضع الامتحان</b> لتجتاز الامتحان في الوقت الحقيقي (4 ساعات للعلوم الرياضية، 3 ساعات للعلوم الفيزيائية) : يُفتح التصحيح عند انتهائك، ثم تنقّط ورقتك لتتبّع تقدّمك.",
    "Fais un examen en mode examen ou écris ta note dans le tableau : ta progression apparaîtra ici (elle reste sur ton appareil).": "اجتز امتحاناً في <b>وضع الامتحان</b> أو اكتب نقطتك في الجدول : سيظهر تقدّمك هنا (يبقى محفوظاً في جهازك فقط).",
    "Révise un chapitre précis : chaque lien ouvre directement l'exercice dans le sujet ou dans le corrigé.": "راجع درساً محدداً : كل رابط يفتح التمرين مباشرة في الموضوع أو في التصحيح.",
    "Les examens nationaux de la filière Sciences Physiques arrivent bientôt.": "الامتحانات الوطنية لشعبة العلوم الفيزيائية ستتوفر قريباً.",
    "🧮 Calcule ta moyenne générale avec le calculateur de note du bac.": "🧮 احسب معدلك العام بـ<a href=\"/calcul-note-bac/\"><b>حاسبة معدل البكالوريا</b></a>.",
    "Formule officielle : Moyenne = 25 % contrôle continu + 25 % examen régional + 50 % examen national.": "الصيغة الرسمية : <b>المعدل = 25% المراقبة المستمرة + 25% الامتحان الجهوي + 50% الامتحان الوطني</b>.",
    "Mentions : Passable de 10 à 12, Assez bien de 12 à 14, Bien de 14 à 16, Très bien à partir de 16.": "الميزات : <b>مقبول</b> من 10 إلى 12، <b>مستحسن</b> من 12 إلى 14، <b>حسن</b> من 14 إلى 16، <b>حسن جداً</b> ابتداءً من 16.",
    "Prépare l'examen national avec les examens nationaux corrigés et le mode examen chronométré.": "حضّر للامتحان الوطني بـ<a href=\"/examens-nationaux-2bac/\"><b>الامتحانات الوطنية المصححة</b></a> ووضع الامتحان بالتوقيت.",
    "Écris ta note de contrôle continu et ta note régionale.": "اكتب نقطة المراقبة المستمرة ونقطة الامتحان الجهوي.",
    "Conseils pour réussir l'examen local de physique-chimie 3AC": "نصائح للنجاح في الامتحان المحلي للفيزياء والكيمياء 3AC",
    "Fais d'abord le sujet seul, en 1 heure, puis compare avec la correction détaillée.": "أنجز الموضوع أولاً وحدك في <b>ساعة واحدة</b>، ثم قارن مع التصحيح المفصل.",
    "Retrouve aussi les cours, exercices et devoirs corrigés de 3AC.": "تجد أيضاً <a href=\"/niveau/3ac/\">الدروس والتمارين والفروض المصححة للثالثة إعدادي</a>.",
    "Examens nationaux Physique-Chimie 2BAC avec corrigés": "الامتحانات الوطنية في الفيزياء والكيمياء 2BAC مع التصحيح",
    "Examens locaux Physique-Chimie 3AC avec corrigés": "الامتحانات المحلية في الفيزياء والكيمياء 3AC مع التصحيح",
    "📝 Sujets et corrigés des examens locaux 3AC": "📝 مواضيع وتصحيحات الامتحانات المحلية 3AC",
    "Lis le cours, manipule la simulation, puis entraîne-toi avec les exercices corrigés et le quiz.": "اقرأ الدرس، جرّب المحاكاة، ثم تدرّب بالتمارين المصححة والاختبار الذاتي.",
    "Méthodes, réponses encadrées et erreurs fréquentes": "طرق الحل، أجوبة مؤطرة وأخطاء شائعة",
    "📚 Cours de soutien en physique-chimie, à distance ou à domicile, tous niveaux": ""
  };

  /* 3) Modèles (phrases qui changent selon le niveau ou le nombre) */
  function w(s) { return D[s] || s; }
  var P = [
    [/^(\d+) leçons?$/, function (m, n) { return n + ' دروس'; }], [/^(\d+) documents? →$/, function (m, n) { return n + ' وثيقة ←'; }],
    [/^(\d+) leçons? · (\d+) documents →$/, function (m, a, b) { return a + ' دروس · ' + b + ' وثيقة ←'; }], [/^(\d+) ressources$/, function (m, n) { return n + ' مورد'; }],
    [/^(\d+) séries? corrigées?$/, function (m, n) { return n + ' سلسلة مصححة'; }], [/^(\d+) devoirs? corrigés?( \((\d+) versions\))?$/, function (m, n, x, v) { return n + ' فرض مصحح' + (v ? ' (' + v + ' نسخ)' : ''); }],
    [/^(\d+) exercices?$/, function (m, n) { return n + ' تمارين'; }], [/^(\d+) exercices? · corrigé détaillé$/, function (m, n) { return n + ' تمارين · تصحيح مفصل'; }],
    [/^(\d+) exercices? · corrigé détaillé · vidéos$/, function (m, n) { return n + ' تمارين · تصحيح مفصل · فيديوهات'; }],
    [/^(\d+) examens? (?:nationa\w+ |locaux |local )?corrigés?$/, function (m, n) { return n + ' امتحانات مصححة'; }],
    [/^Examen national (\d{4}) – session normale$/, function (m, a) { return 'الامتحان الوطني ' + a + ' – الدورة العادية'; }],
    [/^Examen national (\d{4}) – session de rattrapage$/, function (m, a) { return 'الامتحان الوطني ' + a + ' – الدورة الاستدراكية'; }],
    [/^(\d{4}) · Normale$/, function (m, a) { return a + ' · عادية'; }], [/^(\d{4}) · Rattrapage$/, function (m, a) { return a + ' · استدراكية'; }],
    [/^Examen normalisé local (\d{4})$/, function (m, a) { return 'الامتحان المحلي الموحد ' + a; }],
    [/^(SM|PC) (\d{4}) – (normale|rattrapage)$/, function (m, f, a, x) { return f + ' ' + a + ' – ' + (x === 'normale' ? 'عادية' : 'استدراكية'); }],
    [/^▶ Reprendre \((.+)\)$/, function (m, t) { return '▶ استئناف (' + t + ')'; }],
    [/^(📖|✍️|📝|🎓) (Cours|Exercices|Devoirs|Examens) – (\w+)$/, function (m, e, x, n) { return e + ' ' + D[x] + ' – ' + n; }],
    [/^Devoir surveillé n°(\d+)$/, function (m, n) { return 'الفرض المحروس رقم ' + n; }], [/^Devoir n°(\d+) – Sujet (\w)$/, function (m, n, l) { return 'الفرض رقم ' + n + ' – الموضوع ' + l; }],
    [/^Version (\w)$/, function (m, l) { return 'النسخة ' + l; }], [/^(\d+) versions : (.+)$/, function (m, n, l) { return n + ' نسخ : ' + l; }],
    [/^📁 (DS\d+) – choisis ta version$/, function (m, d) { return '📁 ' + d + ' – اختر نسختك'; }], [/^Sujet (\w)$/, function (m, l) { return 'الموضوع ' + l; }],
    [/^Page (\d+) \/ (\d+)$/, function (m, a, b) { return 'الصفحة ' + a + ' / ' + b; }], [/^Autres leçons – (\w+)$/, function (m, n) { return 'دروس أخرى – ' + n; }],
    [/^Physique-Chimie – (.+)$/, function (m, n) { return D[n] ? 'الفيزياء والكيمياء – ' + D[n] : null; }],
    [/^Que veux-tu faire \? Choisis : (.+)\.$/, function (m, l) { var a = l.split(/, | ou /).map(function (x) { return '<b>' + w(x) + '</b>'; }); return 'ماذا تريد أن تفعل ؟ اختر : ' + (a.length > 1 ? a.slice(0, -1).join('، ') + ' أو ' + a[a.length - 1] : a[0]) + '.'; }],
    [/^⭐ Cours de soutien (\w+) \(en ligne ou à domicile\) — WhatsApp 06 52 23 69 22$/, function (m, n) { return '⭐ <b>دروس الدعم</b> ' + n + ' (عن بعد أو بالمنزل) — ' + WA; }],
    [/^⭐ Cours de soutien (\w+) dès maintenant — WhatsApp 06 52 23 69 22$/, function (m, n) { return '⭐ <b>دروس الدعم</b> ' + n + ' متوفرة الآن — ' + WA; }],
    [/^⭐ Cours de soutien (\w+) \(en ligne ou à domicile\) pour préparer (?:l'examen|le national) — WhatsApp 06 52 23 69 22$/, function (m, n) { return '⭐ <b>دروس الدعم</b> ' + n + ' (عن بعد أو بالمنزل) للتحضير للامتحان — ' + WA; }],
    [/^Examen normalisé local 3APIC · (.+) · 1 heure$/, function (m, l) { return 'الامتحان المحلي الموحد 3APIC · ' + l + ' · ساعة واحدة'; }],
    [/^(.+) · (janvier )?(\d{4}) · 1 heure$/, function (m, l, j, a) { return l + ' · ' + (j ? 'يناير ' : '') + a + ' · ساعة واحدة'; }]
  ];

  var LABELISH = 'A,BUTTON,LABEL,SUMMARY,H1,H2,H3,H4,TH,SMALL,OPTION';
  var NOFULL = 'input,select,textarea,button,canvas,svg,img,video,iframe,details,[class],[id],[onclick],[data-imgs],[data-k],[data-t]';
  var saved = [], lang = get();
  function norm(s) { return s.replace(/\s+/g, ' ').trim(); }
  function skip(e) { return !!(e.closest && e.closest('script,style,textarea,.dv-pages,.katex,[data-noar],.lang-b')); }
  function isAr(s) { return /[؀-ۿ]/.test(s); }
  function lookup(t) {
    if (Object.prototype.hasOwnProperty.call(B, t)) return B[t];
    if (D[t]) return D[t];
    for (var i = 0; i < P.length; i++) { var m = t.match(P[i][0]); if (m) { var r = P[i][1].apply(null, m); if (r != null) return r; } }
    return null;
  }
  function plain(s) { if (D[s]) return D[s]; for (var i = 0; i < P.length; i++) { var m = s.match(P[i][0]); if (m) { var x = P[i][1].apply(null, m); if (x != null && x.indexOf('<') < 0) return x; } } return null; }
  function mark(e) { if (!e.hasAttribute('dir')) { e.setAttribute('dir', 'rtl'); e.dataset.arDir = 1; } }
  function doEl(e) {
    if (e.nodeType !== 1 || skip(e) || e.dataset.arDone) return;
    if (e.dataset.l && D[e.dataset.l]) { saved.push([e, '__dl', e.dataset.l]); e.dataset.l = D[e.dataset.l]; }
    var t = norm(e.textContent);
    if (t && !isAr(t)) {
      var r = lookup(t);
      if (r === '') { saved.push([e, null, e.style.display]); e.style.display = 'none'; e.dataset.arDone = 1; return; }
      if (r != null && !e.querySelector(NOFULL)) { saved.push([e, e.innerHTML]); e.innerHTML = r; e.dataset.arDone = 1; mark(e); return; }
    }
    Array.prototype.slice.call(e.childNodes).forEach(function (n) {
      if (n.nodeType === 1) return doEl(n);
      if (n.nodeType !== 3) return;
      var s = norm(n.nodeValue); if (!s || isAr(s)) return;
      /* un morceau de texte n'est traduit que s'il forme tout l'élément, ou si l'élément est un libellé (bouton, lien, titre…) */
      if (s !== t && LABELISH.indexOf(e.tagName) < 0 && !e.classList.contains('dv-fin')) return;
      var r2 = plain(s); if (r2 == null) return;
      saved.push([n, n.nodeValue]); n.nodeValue = n.nodeValue.replace(s, r2);
      if (s === t) mark(e);
      else { var sp = document.createElement('span'); sp.setAttribute('dir', 'rtl'); n.parentNode.insertBefore(sp, n); sp.appendChild(n); saved.push([sp, '__wrap']); }
    });
    if (e.placeholder) {
      var ph = { "Que veux-tu réviser ? (combustion, gravitation...)": "ماذا تريد أن تراجع ؟ (الاحتراق، التجاذب...)", "Que veux-tu réviser ? (combustion, gravitation…)": "ماذا تريد أن تراجع ؟ (الاحتراق، التجاذب…)" }[e.placeholder];
      if (ph) { saved.push([e, '__ph', e.placeholder]); e.placeholder = ph; }
    }
  }
  function restore() {
    for (var i = saved.length - 1; i >= 0; i--) {
      var s = saved[i], n = s[0];
      if (s[1] === '__wrap') { if (n.parentNode) { while (n.firstChild) n.parentNode.insertBefore(n.firstChild, n); n.parentNode.removeChild(n); } continue; }
      if (s[1] === '__ph') { n.placeholder = s[2]; continue; }
      if (s[1] === '__dl') { n.dataset.l = s[2]; continue; }
      if (n.nodeType === 3) { n.nodeValue = s[1]; continue; }
      if (s[1] === null) n.style.display = s[2] || ''; else n.innerHTML = s[1];
      delete n.dataset.arDone;
    }
    saved = [];
    document.querySelectorAll('[data-ar-dir]').forEach(function (x) { x.removeAttribute('dir'); delete x.dataset.arDir; });
  }
  var busy = false;
  var mo = new MutationObserver(function (ms) {
    if (lang !== 'ar' || busy) return; busy = true;
    ms.forEach(function (m) {
      if (m.type === 'characterData') { var p = m.target.parentNode; if (p && p.nodeType === 1) { delete p.dataset.arDone; doEl(p); } }
      else { if (m.target && m.target.dataset) delete m.target.dataset.arDone; m.addedNodes.forEach(function (n) { if (n.nodeType === 1) doEl(n); else if (n.nodeType === 3 && n.parentNode) { delete n.parentNode.dataset.arDone; doEl(n.parentNode); } }); }
    });
    busy = false;
  });
  var btn;
  function apply() {
    busy = true;
    document.documentElement.classList.toggle('ui-ar', lang === 'ar');
    if (lang === 'ar') doEl(document.body); else restore();
    busy = false;
    if (btn) { btn.textContent = lang === 'ar' ? 'FR' : 'AR'; btn.title = lang === 'ar' ? 'Afficher en français' : 'عرض الواجهة بالعربية'; }
  }
  var st = document.createElement('style');
  st.textContent = '.lang-b{border:2px solid rgba(255,255,255,.55);background:transparent;color:#fff;border-radius:99px;min-width:40px;height:36px;padding:0 10px;font:800 15px/1 Inter,system-ui,sans-serif;cursor:pointer;margin-left:8px;flex-shrink:0}.lang-b:hover{background:rgba(255,255,255,.12)}' +
    'html.ui-ar [dir=rtl]{font-family:"Noto Sans Arabic","Segoe UI",Tahoma,Inter,sans-serif}html.ui-ar p[dir=rtl],html.ui-ar li[dir=rtl],html.ui-ar div[dir=rtl]{line-height:1.8}' +
    '@media(max-width:760px){.lang-b{min-width:34px;height:34px;padding:0 6px;margin-left:0}header.top .wrap{gap:6px;padding:10px}header.top .wrap>a>img{width:38px;height:38px}header.top .brand{font-size:15px;line-height:1.15}header.top .brand small{display:none}header.top .burger{padding:8px 10px;flex-shrink:0}}' +
    '@media(max-width:400px){header.top .av-badge{font-size:13px;padding:7px 9px}header.top .wrap{gap:4px;padding:8px}.lang-b{min-width:30px;padding:0 4px}}';
  document.head.appendChild(st);
  btn = document.createElement('button'); btn.type = 'button'; btn.className = 'lang-b'; btn.setAttribute('aria-label', 'Langue de l’interface / لغة الواجهة');
  btn.onclick = function () { lang = lang === 'ar' ? 'fr' : 'ar'; set(lang); apply(); try { fetch('https://script.google.com/macros/s/AKfycbxta1pz0xrqrIa9RiENIXd_CQwiQpkvcwtm_sWBH15-UfBTCN4clgsdmtc3HXZtXh4I/exec', { method: 'POST', mode: 'no-cors', body: JSON.stringify({ ev: 'langue', titre: lang, vid: localStorage.getItem('yh_vid') || '', src: 'site' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' }, keepalive: true }).catch(function () {}); } catch (e) {} };
  function mount() {
    var anchor = document.querySelector('header.top .wrap .brand'), stop = document.querySelector('header.top .wrap .burger') || document.querySelector('header.top .wrap nav');
    if (anchor) { if (stop && stop.parentNode === anchor.parentNode) stop.parentNode.insertBefore(btn, stop); else anchor.insertAdjacentElement('afterend', btn); }
    else { btn.style.cssText = 'position:fixed;top:10px;right:10px;z-index:90;background:#0f2350'; document.body.appendChild(btn); }
    var bg = document.querySelector('header.top .burger'); if (bg && innerWidth <= 760) { bg.textContent = '☰'; bg.setAttribute('aria-label', 'Menu'); }
    apply(); mo.observe(document.body, { childList: true, subtree: true, characterData: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
