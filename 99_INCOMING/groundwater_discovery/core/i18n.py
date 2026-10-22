"""Reference-module i18n contract: Python UI strings and Markdown English fallback."""

from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {
    "en": ("🇬🇧", "English"),
    "de": ("🇩🇪", "Deutsch"),
    "it": ("🇮🇹", "Italiano"),
    "es": ("🇪🇸", "Español"),
    "pt": ("🇵🇹", "Português"),
    "fr": ("🇫🇷", "Français"),
    "zh": ("🇨🇳", "简体中文"),
    "ar": ("🌐", "العربية"),
    "hi": ("🇮🇳", "हिन्दी"),
    "fa": ("🇮🇷", "فارسی"),
    "pl": ("🇵🇱", "Polski"),
    "cs": ("🇨🇿", "Čeština"),
}
TEXT = {
    "title": {
        "en": "Groundwater discovery",
        "de": "Grundwasser entdecken",
        "pl": "Odkryj wody podziemne",
        "fr": "Découvrir les eaux souterraines",
        "es": "Descubre el agua subterránea",
        "ar": "اكتشف المياه الجوفية",
        "cs": "Objevte podzemní vodu",
        "it": "Scopri le acque sotterranee",
    },
    "home": {
        "en": "Start here",
        "de": "Hier starten",
        "pl": "Zacznij tutaj",
        "fr": "Commencer ici",
        "es": "Empieza aquí",
        "ar": "ابدأ هنا",
        "cs": "Začněte zde",
        "it": "Inizia qui",
    },
    "importance": {
        "en": "Why groundwater matters",
        "de": "Warum Grundwasser wichtig ist",
        "pl": "Dlaczego wody podziemne są ważne",
        "fr": "Pourquoi cette eau compte",
        "es": "Por qué importa",
        "ar": "أهمية المياه الجوفية",
        "cs": "Proč je podzemní voda důležitá",
        "it": "Perché è importante",
    },
    "pores": {
        "en": "Water underground",
        "de": "Wasser im Untergrund",
        "pl": "Woda pod ziemią",
        "fr": "L’eau dans le sous-sol",
        "es": "El agua bajo tierra",
        "ar": "الماء تحت الأرض",
        "cs": "Voda pod zemí",
        "it": "L’acqua nel sottosuolo",
    },
    "beach": {
        "en": "Groundwater in our surroundings",
        "de": "Grundwasser in unserer Umgebung",
        "pl": "Wody podziemne w naszym otoczeniu",
        "fr": "L’eau souterraine autour de nous",
        "es": "El agua subterránea en nuestro entorno",
        "ar": "المياه الجوفية في محيطنا",
        "cs": "Podzemní voda v našem okolí",
        "it": "L’acqua sotterranea intorno a noi",
    },
    "resources": {
        "en": "Reflect & explore",
        "de": "Rückblick & Weiterlernen",
        "pl": "Podsumuj i odkrywaj",
        "fr": "Bilan et découverte",
        "es": "Reflexiona y explora",
        "ar": "تأمل واستكشف",
        "cs": "Ohlédnutí a další poznávání",
        "it": "Rifletti ed esplora",
    },
    "lab": {
        "en": "Optional · Go deeper",
        "de": "Optional · Vertiefung",
        "pl": "Opcjonalnie · Dowiedz się więcej",
        "fr": "Option · Aller plus loin",
        "es": "Opcional · Profundiza",
        "ar": "اختياري · تعمّق أكثر",
        "cs": "Volitelně · Více do hloubky",
        "it": "Facoltativo · Approfondisci",
    },
    "core": {
        "en": "Your learning path",
        "de": "Dein Lernpfad",
        "pl": "Twoja ścieżka nauki",
        "fr": "Votre parcours",
        "es": "Tu recorrido",
        "ar": "مسار التعلم",
        "cs": "Vaše cesta poznáním",
        "it": "Il tuo percorso",
    },
    "extra": {
        "en": "Optional exploration",
        "de": "Optionale Vertiefung",
        "pl": "Dodatkowe odkrycia",
        "fr": "Exploration facultative",
        "es": "Exploración opcional",
        "ar": "استكشاف اختياري",
        "cs": "Volitelné zkoumání",
        "it": "Esplorazione facoltativa",
    },
    "language": {
        "en": "Language",
        "de": "Sprache",
        "pl": "Język",
        "fr": "Langue",
        "es": "Idioma",
        "ar": "اللغة",
        "cs": "Jazyk",
        "it": "Lingua",
    },
    "module_language": {
        "en": "Module language",
        "de": "Modulsprache",
        "pl": "Język modułu",
        "fr": "Langue du module",
        "es": "Idioma del módulo",
        "ar": "لغة الوحدة",
        "cs": "Jazyk modulu",
        "it": "Lingua del modulo",
    },
    "layout": {
        "en": "Page layout",
        "de": "Seitenlayout",
        "pl": "Układ strony",
        "fr": "Mise en page",
        "es": "Diseño de página",
        "ar": "تخطيط الصفحة",
        "cs": "Rozložení stránky",
        "it": "Layout della pagina",
    },
    "centered": {
        "en": "Standard",
        "de": "Standard",
        "pl": "Standardowy",
        "fr": "Standard",
        "es": "Estándar",
        "ar": "عادي",
        "cs": "Standardní",
        "it": "Standard",
    },
    "wide": {
        "en": "Wide",
        "de": "Breit",
        "pl": "Szeroki",
        "fr": "Large",
        "es": "Ancho",
        "ar": "عريض",
        "cs": "Široké",
        "it": "Ampio",
    },
    "next": {
        "en": "Continue",
        "de": "Weiter",
        "pl": "Dalej",
        "fr": "Continuer",
        "es": "Continuar",
        "ar": "متابعة",
        "cs": "Pokračovat",
        "it": "Continua",
    },
    "source": {
        "en": "Explore the source",
        "de": "Zur Quelle",
        "pl": "Przejdź do źródła",
        "fr": "Explorer la source",
        "es": "Explora la fuente",
        "ar": "استكشف المصدر",
        "cs": "Prozkoumat zdroj",
        "it": "Esplora la fonte",
    },
    "check": {
        "en": "Check my answer",
        "de": "Antwort prüfen",
        "pl": "Sprawdź odpowiedź",
        "fr": "Vérifier ma réponse",
        "es": "Comprueba mi respuesta",
        "ar": "تحقق من إجابتي",
        "cs": "Ověřit odpověď",
        "it": "Verifica la risposta",
    },
    "choose": {
        "en": "Choose an answer first.",
        "de": "Wähle zuerst eine Antwort.",
        "pl": "Najpierw wybierz odpowiedź.",
        "fr": "Choisissez d’abord une réponse.",
        "es": "Primero elige una respuesta.",
        "ar": "اختر إجابة أولاً.",
        "cs": "Nejprve vyberte odpověď.",
        "it": "Scegli prima una risposta.",
    },
    "correct": {
        "en": "Well reasoned.",
        "de": "Gut überlegt.",
        "pl": "Dobre rozumowanie.",
        "fr": "Bien raisonné.",
        "es": "Buen razonamiento.",
        "ar": "أحسنت التفكير.",
        "cs": "Správná úvaha.",
        "it": "Ragionamento corretto.",
    },
    "retry": {
        "en": "Not quite — consider the explanation and try again.",
        "de": "Noch nicht ganz — lies die Erklärung und versuche es erneut.",
        "pl": "Jeszcze nie — przeczytaj wyjaśnienie i spróbuj ponownie.",
        "fr": "Pas tout à fait — lisez l’explication et réessayez.",
        "es": "Aún no — lee la explicación e inténtalo otra vez.",
        "ar": "ليس تماماً؛ اقرأ التفسير وحاول مجدداً.",
        "cs": "Ještě ne. Přečtěte si vysvětlení a zkuste to znovu.",
        "it": "Non ancora. Leggi la spiegazione e riprova.",
    },
    "quiz": {
        "en": "Reflection · Check your understanding",
        "de": "Reflexion · Verständnis prüfen",
        "pl": "Refleksja · Sprawdź, co rozumiesz",
        "fr": "Réflexion · Vérifier sa compréhension",
        "es": "Reflexión · Comprueba lo aprendido",
        "ar": "تأمل · تحقق من فهمك",
        "cs": "Zamyšlení · Ověřte si porozumění",
        "it": "Riflessione · Verifica ciò che hai capito",
    },
    "guess": {
        "en": "What percentage of liquid freshwater is groundwater?",
        "de": "Wie viel Prozent des flüssigen Süßwassers ist Grundwasser?",
        "pl": "Jaki procent ciekłej wody słodkiej stanowią wody podziemne?",
        "fr": "Quel pourcentage de l’eau douce liquide est souterrain ?",
        "es": "¿Qué porcentaje del agua dulce líquida es subterránea?",
        "ar": "ما نسبة المياه الجوفية من المياه العذبة السائلة؟",
        "cs": "Kolik procent kapalné sladké vody tvoří podzemní voda?",
        "it": "Quale percentuale dell’acqua dolce liquida è sotterranea?",
    },
    "reveal": {
        "en": "Click here to see the fact",
        "de": "Hier klicken und die Zahl entdecken",
        "pl": "Kliknij, aby poznać fakt",
        "fr": "Cliquez pour découvrir le résultat",
        "es": "Haz clic para descubrir el dato",
        "ar": "اضغط هنا لاكتشاف الحقيقة",
        "cs": "Klikněte a zjistěte skutečnost",
        "it": "Clicca per scoprire il dato",
    },
    "groundwater": {
        "en": "Groundwater",
        "de": "Grundwasser",
        "pl": "Wody podziemne",
        "fr": "Eaux souterraines",
        "es": "Agua subterránea",
        "ar": "المياه الجوفية",
        "cs": "Podzemní voda",
        "it": "Acqua sotterranea",
    },
    "other_liquid": {
        "en": "Other liquid freshwater",
        "de": "Sonstiges flüssiges Süßwasser",
        "pl": "Pozostała ciekła woda słodka",
        "fr": "Autre eau douce liquide",
        "es": "Otra agua dulce líquida",
        "ar": "مياه عذبة سائلة أخرى",
        "cs": "Ostatní kapalná sladká voda",
        "it": "Altra acqua dolce liquida",
    },
    "waffle": {
        "en": "About 99 of 100 equal units",
        "de": "Etwa 99 von 100 gleichen Einheiten",
        "pl": "Około 99 ze 100 równych jednostek",
        "fr": "Environ 99 unités égales sur 100",
        "es": "Unas 99 de cada 100 unidades iguales",
        "ar": "نحو 99 من 100 وحدة متساوية",
        "cs": "Přibližně 99 ze 100 stejných jednotek",
        "it": "Circa 99 unità uguali su 100",
    },
    "controls": {
        "en": "Try it yourself",
        "de": "Selbst ausprobieren",
        "pl": "Wypróbuj samodzielnie",
        "fr": "À vous d’essayer",
        "es": "Pruébalo",
        "ar": "جرّب بنفسك",
        "cs": "Vyzkoušejte si to",
        "it": "Prova tu",
    },
    "saturated": {
        "en": "Fill the spaces with water",
        "de": "Poren mit Wasser füllen",
        "pl": "Wypełnij pory wodą",
        "fr": "Remplir les pores d’eau",
        "es": "Llena los poros de agua",
        "ar": "املأ المسام بالماء",
        "cs": "Vyplnit póry vodou",
        "it": "Riempi i pori d’acqua",
    },
    "grains": {
        "en": "Solid grains",
        "de": "Feste Körner",
        "pl": "Ziarna materiału",
        "fr": "Grains solides",
        "es": "Granos sólidos",
        "ar": "حبيبات صلبة",
        "cs": "Pevná zrna",
        "it": "Granuli solidi",
    },
    "pore_water": {
        "en": "Water in pores",
        "de": "Porenwasser",
        "pl": "Woda w porach",
        "fr": "Eau dans les pores",
        "es": "Agua en los poros",
        "ar": "الماء في المسام",
        "cs": "Voda v pórech",
        "it": "Acqua nei pori",
    },
    "air": {
        "en": "Air in pores",
        "de": "Luft in Poren",
        "pl": "Powietrze w porach",
        "fr": "Air dans les pores",
        "es": "Aire en los poros",
        "ar": "الهواء في المسام",
        "cs": "Vzduch v pórech",
        "it": "Aria nei pori",
    },
    "pore_caption": {
        "en": "Illustrative grain section; areas are not a measurement of 3D porosity.",
        "de": "Schematischer Kornschnitt; Flächen sind keine Messung der 3D-Porosität.",
        "pl": "Schemat ziaren; pola powierzchni nie mierzą porowatości 3D.",
        "fr": "Coupe schématique ; les surfaces ne mesurent pas la porosité en 3D.",
        "es": "Corte esquemático; las áreas no miden la porosidad en 3D.",
        "ar": "مقطع تخطيطي لحبيبات متلامسة؛ المساحات لا تقيس المسامية ثلاثية الأبعاد.",
        "cs": "Schematický řez dotýkajícími se zrny; plochy neměří trojrozměrnou "
        "pórovitost.",
        "it": "Sezione schematica di granuli a contatto; le aree non misurano la "
        "porosità tridimensionale.",
    },
    "experiment": {
        "en": "A cup full of spaces",
        "de": "Ein Becher voller Zwischenräume",
        "pl": "Kubek pełen przestrzeni",
        "fr": "Un gobelet plein d’espaces",
        "es": "Un vaso lleno de espacios",
        "ar": "كوب مليء بالفراغات",
        "cs": "Kelímek plný mezer",
        "it": "Un bicchiere pieno di spazi",
    },
    "bulk": {
        "en": "Bulk sample volume: grains + pores (mL)",
        "de": "Gesamtvolumen: Körner + Poren (mL)",
        "pl": "Objętość próbki: ziarna + pory (mL)",
        "fr": "Volume total : grains + pores (mL)",
        "es": "Volumen total: granos + poros (mL)",
        "ar": "حجم العينة الكلي: حبيبات ومسام (مل)",
        "cs": "Celkový objem vzorku: zrna a póry (mL)",
        "it": "Volume totale: granuli e pori (mL)",
    },
    "water_added": {
        "en": "Water added to fill the pores (mL)",
        "de": "Wasser zum Füllen der Poren (mL)",
        "pl": "Woda dodana do wypełnienia porów (mL)",
        "fr": "Eau ajoutée pour remplir les pores (mL)",
        "es": "Agua añadida para llenar los poros (mL)",
        "ar": "الماء المضاف لملء المسام (مل)",
        "cs": "Voda přidaná k vyplnění pórů (mL)",
        "it": "Acqua aggiunta per riempire i pori (mL)",
    },
    "apparent_porosity": {
        "en": "Estimated accessible porosity",
        "de": "Geschätzte zugängliche Porosität",
        "pl": "Szacowana porowatość dostępna",
        "fr": "Porosité accessible estimée",
        "es": "Porosidad accesible estimada",
        "ar": "المسامية المتاحة المقدّرة",
        "cs": "Odhad přístupné pórovitosti",
        "it": "Porosità accessibile stimata",
    },
    "invalid_volume": {
        "en": "Check the measurements: pore water cannot exceed the total sample "
        "volume.",
        "de": "Messwerte prüfen: Das Porenwasser darf das Gesamtvolumen nicht "
        "überschreiten.",
        "pl": "Sprawdź pomiary: woda w porach nie może przekraczać objętości próbki.",
        "fr": "Vérifiez : l’eau des pores ne peut dépasser le volume total.",
        "es": "Revisa los datos: el agua en los poros no puede superar el volumen "
        "total.",
        "ar": "تحقق من القياس: لا يمكن أن يتجاوز ماء المسام حجم العينة الكلي.",
        "cs": "Zkontrolujte měření: voda v pórech nemůže přesáhnout celkový objem "
        "vzorku.",
        "it": "Controlla le misure: l’acqua nei pori non può superare il volume "
        "totale.",
    },
    "end_volume": {
        "en": "This endpoint is mathematically possible but is not a realistic "
        "packed-grain sample.",
        "de": "Dieser Grenzwert ist mathematisch möglich, aber keine realistische "
        "Kornpackung.",
        "pl": "Ta wartość graniczna jest matematycznie możliwa, ale nie odpowiada "
        "rzeczywistej próbce ziaren.",
        "fr": "Cette limite mathématique ne représente pas un assemblage réaliste de "
        "grains.",
        "es": "Este extremo matemático no representa una muestra realista de granos.",
        "ar": "هذه قيمة حدية ممكنة رياضياً، لكنها لا تمثل عينة واقعية من الحبيبات.",
        "cs": "Tato mezní hodnota je matematicky možná, ale neodpovídá reálnému vzorku "
        "zrn.",
        "it": "Questo valore limite è matematicamente possibile, ma non rappresenta un "
        "campione realistico di granuli.",
    },
    "volume_fraction": {
        "en": "Share of bulk volume (%)",
        "de": "Anteil am Gesamtvolumen (%)",
        "pl": "Udział w objętości próbki (%)",
        "fr": "Part du volume total (%)",
        "es": "Fracción del volumen total (%)",
        "ar": "النسبة من الحجم الكلي (%)",
        "cs": "Podíl celkového objemu (%)",
        "it": "Quota del volume totale (%)",
    },
    "dig": {
        "en": "Choose a small observation hole",
        "de": "Eine kleine Beobachtungsmulde wählen",
        "pl": "Wybierz mały dołek obserwacyjny",
        "fr": "Choisir un petit trou d’observation",
        "es": "Elige un pequeño hoyo",
        "ar": "اختر حفرة ملاحظة صغيرة",
        "cs": "Zvolte malou pozorovací jamku",
        "it": "Scegli una piccola buca di osservazione",
    },
    "show_water": {
        "en": "Reveal the groundwater table",
        "de": "Grundwasserspiegel einblenden",
        "pl": "Pokaż zwierciadło wód podziemnych",
        "fr": "Afficher la surface de la nappe",
        "es": "Mostrar el nivel freático",
        "ar": "أظهر منسوب المياه الجوفية",
        "cs": "Zobrazit hladinu podzemní vody",
        "it": "Mostra la superficie della falda",
    },
    "sea": {
        "en": "Sea level",
        "de": "Meeresspiegel",
        "pl": "Poziom morza",
        "fr": "Niveau marin",
        "es": "Nivel del mar",
        "ar": "مستوى البحر",
        "cs": "Hladina moře",
        "it": "Livello del mare",
    },
    "water_table": {
        "en": "Groundwater table",
        "de": "Grundwasserspiegel",
        "pl": "Zwierciadło wód podziemnych",
        "fr": "Surface de la nappe",
        "es": "Nivel freático",
        "ar": "منسوب المياه الجوفية",
        "cs": "Hladina podzemní vody",
        "it": "Superficie della falda",
    },
    "sand_surface": {
        "en": "Sand surface",
        "de": "Sandoberfläche",
        "pl": "Powierzchnia piasku",
        "fr": "Surface du sable",
        "es": "Superficie de arena",
        "ar": "سطح الرمل",
        "cs": "Povrch písku",
        "it": "Superficie della sabbia",
    },
    "hole": {
        "en": "Observation hole",
        "de": "Beobachtungsmulde",
        "pl": "Dołek obserwacyjny",
        "fr": "Trou d’observation",
        "es": "Hoyo de observación",
        "ar": "حفرة الملاحظة",
        "cs": "Pozorovací jamka",
        "it": "Buca di osservazione",
    },
    "water_found": {
        "en": "Water collects in the hole after equilibration.",
        "de": "Nach dem Ausgleich sammelt sich Wasser in der Mulde.",
        "pl": "Po wyrównaniu poziomów w dołku zbiera się woda.",
        "fr": "L’eau s’accumule après équilibrage.",
        "es": "El agua se acumula tras equilibrarse.",
        "ar": "يتجمع الماء في الحفرة بعد استقرار المنسوب.",
        "cs": "Po ustálení hladiny se v jamce hromadí voda.",
        "it": "L’acqua si raccoglie nella buca dopo l’equilibrio.",
    },
    "no_water": {
        "en": "The hole does not extend below the water table.",
        "de": "Die Mulde reicht nicht unter den Grundwasserspiegel.",
        "pl": "Dołek nie sięga poniżej zwierciadła wody.",
        "fr": "Le trou ne descend pas sous la nappe.",
        "es": "El hoyo no llega por debajo del nivel freático.",
        "ar": "لا يصل قاع الحفرة إلى ما دون منسوب المياه الجوفية.",
        "cs": "Jamka nesahá pod hladinu podzemní vody.",
        "it": "La buca non scende sotto la falda.",
    },
    "schematic": {
        "en": "Idealised beach · vertically exaggerated · not Sopot measurements",
        "de": "Idealisierter Strand · vertikal überhöht · keine Messdaten aus Sopot",
        "pl": "Plaża idealizowana · skala pionowa powiększona · bez pomiarów z Sopotu",
        "fr": "Plage idéalisée · échelle verticale exagérée · sans mesures de Sopot",
        "es": "Playa idealizada · escala vertical exagerada · sin mediciones de Sopot",
        "ar": "شاطئ مثالي؛ مقياس رأسي مبالغ فيه؛ ليس قياسات من سوبوت",
        "cs": "Idealizovaná pláž · svislé převýšení · nejde o měření v Sopotech",
        "it": "Spiaggia idealizzata · scala verticale esagerata · nessuna misura di Sopot",
    },
    "field": {
        "en": "Observe at a beach",
        "de": "Am Strand beobachten",
        "pl": "Obserwacja na plaży",
        "fr": "Observer sur une plage",
        "es": "Observa en una playa",
        "ar": "راقب على الشاطئ",
        "cs": "Pozorování na pláži",
        "it": "Osserva su una spiaggia",
    },
    "equations": {
        "en": "Model and assumptions",
        "de": "Modell und Annahmen",
        "pl": "Model i założenia",
        "fr": "Modèle et hypothèses",
        "es": "Modelo y supuestos",
        "ar": "الفكرة وحدودها",
        "cs": "Myšlenka a její meze",
        "it": "L’idea e i suoi limiti",
    },
    "interface": {
        "en": "Idealised interface",
        "de": "Idealisierte Grenzfläche",
        "pl": "Idealizowana granica",
        "fr": "Interface idéalisée",
        "es": "Interfaz idealizada",
        "ar": "حد فاصل مثالي",
        "cs": "Idealizované rozhraní",
        "it": "Interfaccia idealizzata",
    },
    "freshwater": {
        "en": "Freshwater",
        "de": "Süßwasser",
        "pl": "Woda słodka",
        "fr": "Eau douce",
        "es": "Agua dulce",
        "ar": "مياه عذبة",
        "cs": "Sladká voda",
        "it": "Acqua dolce",
    },
    "saltwater": {
        "en": "Saltwater",
        "de": "Salzwasser",
        "pl": "Woda słona",
        "fr": "Eau salée",
        "es": "Agua salada",
        "ar": "مياه مالحة",
        "cs": "Slaná voda",
        "it": "Acqua salata",
    },
    "reflection": {
        "en": "Explain it to a partner",
        "de": "Einem Partner erklären",
        "pl": "Wyjaśnij drugiej osobie",
        "fr": "Expliquer à un partenaire",
        "es": "Explícaselo a otra persona",
        "ar": "اشرح لشخص آخر",
        "cs": "Vysvětlete to druhému",
        "it": "Spiegalo a un’altra persona",
    },
    "learn_more": {
        "en": "Continue with The Groundwater Project",
        "de": "Mit The Groundwater Project weiterlernen",
        "pl": "Ucz się dalej z The Groundwater Project",
        "fr": "Continuer avec The Groundwater Project",
        "es": "Sigue con The Groundwater Project",
        "ar": "تابع مع The Groundwater Project",
        "cs": "Pokračujte s The Groundwater Project",
        "it": "Continua con The Groundwater Project",
    },
    "all_sources": {
        "en": "Sources and scope",
        "de": "Quellen und Geltungsbereich",
        "pl": "Źródła i zakres",
        "fr": "Sources et limites",
        "es": "Fuentes y alcance",
        "ar": "المصادر ونطاق التطبيق",
        "cs": "Zdroje a rozsah použití",
        "it": "Fonti e ambito",
    },
    "facilitator": {
        "en": "For facilitators",
        "de": "Für Lehrende",
        "pl": "Dla prowadzących",
        "fr": "Pour les animateurs",
        "es": "Para facilitadores",
        "ar": "للميسّرين",
        "cs": "Pro lektory",
        "it": "Per chi conduce l’attività",
    },
    "reset": {
        "en": "Reset this session",
        "de": "Diese Sitzung zurücksetzen",
        "pl": "Zresetuj tę sesję",
        "fr": "Réinitialiser cette session",
        "es": "Reinicia esta sesión",
        "ar": "أعد ضبط الجلسة",
        "cs": "Obnovit tuto relaci",
        "it": "Reimposta la sessione",
    },
    "progress": {
        "en": "Questions answered correctly in this session",
        "de": "Richtig beantwortete Fragen in dieser Sitzung",
        "pl": "Poprawne odpowiedzi w tej sesji",
        "fr": "Bonnes réponses dans cette session",
        "es": "Respuestas correctas en esta sesión",
        "ar": "إجابات صحيحة في هذه الجلسة",
        "cs": "Správné odpovědi v této relaci",
        "it": "Risposte corrette in questa sessione",
    },
    "book": {
        "en": "Open the free book",
        "de": "Kostenloses Buch öffnen",
        "pl": "Otwórz bezpłatną książkę",
        "fr": "Ouvrir le livre gratuit",
        "es": "Abre el libro gratuito",
        "ar": "افتح الكتاب المجاني",
        "cs": "Otevřít bezplatnou knihu",
        "it": "Apri il libro gratuito",
    },
    "position": {
        "en": "Where will you dig?",
        "de": "Wo wirst du graben?",
        "pl": "Gdzie wykopiesz dołek?",
        "fr": "Où creuserez-vous ?",
        "es": "¿Dónde cavarás?",
        "ar": "أين ستحفر؟",
        "cs": "Kde budete kopat?",
        "it": "Dove scaverai?",
    },
    "near": {
        "en": "Near the shore",
        "de": "Nah am Ufer",
        "pl": "Blisko brzegu",
        "fr": "Près du rivage",
        "es": "Cerca de la orilla",
        "ar": "قرب الشاطئ",
        "cs": "Blízko břehu",
        "it": "Vicino alla riva",
    },
    "middle": {
        "en": "A little inland",
        "de": "Etwas landeinwärts",
        "pl": "Nieco w głębi lądu",
        "fr": "Un peu à l’intérieur",
        "es": "Un poco tierra adentro",
        "ar": "قليلاً نحو اليابسة",
        "cs": "Kousek do vnitrozemí",
        "it": "Un poco nell’entroterra",
    },
    "inland": {
        "en": "Further inland",
        "de": "Weiter landeinwärts",
        "pl": "Dalej w głębi lądu",
        "fr": "Plus à l’intérieur",
        "es": "Más tierra adentro",
        "ar": "أبعد نحو اليابسة",
        "cs": "Dále do vnitrozemí",
        "it": "Più nell’entroterra",
    },
    "depth": {
        "en": "How deep?",
        "de": "Wie tief?",
        "pl": "Jak głęboko?",
        "fr": "À quelle profondeur ?",
        "es": "¿A qué profundidad?",
        "ar": "ما العمق؟",
        "cs": "Jak hluboko?",
        "it": "Quanto in profondità?",
    },
    "shallow": {
        "en": "Shallow",
        "de": "Flach",
        "pl": "Płytko",
        "fr": "Peu profond",
        "es": "Poco profundo",
        "ar": "ضحلة",
        "cs": "Mělce",
        "it": "Poco profonda",
    },
    "deeper": {
        "en": "A little deeper",
        "de": "Etwas tiefer",
        "pl": "Trochę głębiej",
        "fr": "Un peu plus profond",
        "es": "Un poco más profundo",
        "ar": "أعمق قليلاً",
        "cs": "Trochu hlouběji",
        "it": "Un poco più profonda",
    },
    "cycle_title": {
        "en": "One connected water cycle",
        "de": "Ein zusammenhängender Wasserkreislauf",
        "pl": "Jeden połączony obieg wody",
        "fr": "Un seul cycle de l’eau",
        "es": "Un ciclo del agua conectado",
        "ar": "دورة مياه مترابطة",
        "cs": "Jeden propojený koloběh vody",
        "it": "Un unico ciclo dell’acqua",
    },
    "evaporation": {
        "en": "Evaporation",
        "de": "Verdunstung",
        "pl": "Parowanie",
        "fr": "Évaporation",
        "es": "Evaporación",
        "ar": "التبخر",
        "cs": "Vypařování",
        "it": "Evaporazione",
    },
    "clouds": {
        "en": "Cooling → clouds",
        "de": "Abkühlung → Wolken",
        "pl": "Ochładzanie → chmury",
        "fr": "Refroidissement → nuages",
        "es": "Enfriamiento → nubes",
        "ar": "تبريد ← سحب",
        "cs": "Ochlazení → oblaka",
        "it": "Raffreddamento → nubi",
    },
    "rain": {
        "en": "Precipitation",
        "de": "Niederschlag",
        "pl": "Opad",
        "fr": "Précipitations",
        "es": "Precipitación",
        "ar": "الهطول",
        "cs": "Srážky",
        "it": "Precipitazioni",
    },
    "recharge_simple": {
        "en": "Recharge",
        "de": "Grundwasserneubildung",
        "pl": "Zasilanie",
        "fr": "Recharge",
        "es": "Recarga",
        "ar": "تغذية جوفية",
        "cs": "Doplňování",
        "it": "Ricarica",
    },
    "flow": {
        "en": "Groundwater flow",
        "de": "Grundwasserströmung",
        "pl": "Przepływ wód podziemnych",
        "fr": "Écoulement souterrain",
        "es": "Flujo subterráneo",
        "ar": "جريان المياه الجوفية",
        "cs": "Proudění podzemní vody",
        "it": "Flusso sotterraneo",
    },
    "surface_water": {
        "en": "Surface water",
        "de": "Oberflächenwasser",
        "pl": "Woda powierzchniowa",
        "fr": "Eau de surface",
        "es": "Agua superficial",
        "ar": "مياه سطحية",
        "cs": "Povrchová voda",
        "it": "Acqua superficiale",
    },
    "cycle_caption": {
        "en": "One pathway in the global cycle; plants, runoff and ice are omitted "
        "here.",
        "de": "Ein Weg im globalen Kreislauf; Pflanzen, Oberflächenabfluss und Eis sind "
        "hier nicht dargestellt.",
        "pl": "Jeden z obiegów w cyklu globalnym; pominięto rośliny, spływ "
        "powierzchniowy i lód.",
        "fr": "Un trajet du cycle global ; plantes, ruissellement et glace ne sont pas "
        "représentés.",
        "es": "Una ruta del ciclo global; aquí se omiten plantas, escorrentía y hielo.",
        "ar": "مسار واحد في الدورة العالمية؛ لا تظهر هنا النباتات والجريان السطحي "
        "والجليد.",
        "cs": "Jedna cesta v globálním koloběhu; rostliny, povrchový odtok a led zde "
        "nejsou zobrazeny.",
        "it": "Un percorso del ciclo globale; piante, ruscellamento e ghiaccio sono "
        "omessi.",
    },
    "more": {
        "en": "A little more detail",
        "de": "Etwas genauer",
        "pl": "Trochę więcej szczegółów",
        "fr": "Un peu plus de détails",
        "es": "Un poco más de detalle",
        "ar": "تفاصيل إضافية",
        "cs": "Trochu podrobněji",
        "it": "Qualche dettaglio in più",
    },
    "land_surface": {
        "en": "Land surface",
        "de": "Geländeoberfläche",
        "pl": "Powierzchnia terenu",
        "fr": "Surface du terrain",
        "es": "Superficie del terreno",
        "ar": "سطح الأرض",
        "cs": "Povrch terénu",
        "it": "Superficie del terreno",
    },
    "lens_level": {
        "en": "Compare freshwater levels",
        "de": "Süßwasserstände vergleichen",
        "pl": "Porównaj poziomy wody słodkiej",
        "fr": "Comparer les niveaux d’eau douce",
        "es": "Compara niveles de agua dulce",
        "ar": "قارن مناسيب المياه العذبة",
        "cs": "Porovnejte hladiny sladké vody",
        "it": "Confronta i livelli di acqua dolce",
    },
    "higher": {
        "en": "Higher",
        "de": "Höher",
        "pl": "Wyższy",
        "fr": "Plus élevé",
        "es": "Más alto",
        "ar": "أعلى",
        "cs": "Vyšší",
        "it": "Più alto",
    },
    "lower": {
        "en": "Lower",
        "de": "Niedriger",
        "pl": "Niższy",
        "fr": "Plus bas",
        "es": "Más bajo",
        "ar": "أخفض",
        "cs": "Nižší",
        "it": "Più basso",
    },
    "lens_caption": {
        "en": "Idealised island; fixed scales, vertical exaggeration; comparison of "
        "equilibria, not a pumping simulation.",
        "de": "Idealisierte Insel; feste Skalen, vertikal überhöht; "
        "Gleichgewichtsvergleich, keine Pumpsimulation.",
        "pl": "Idealizowana wyspa; stałe skale, powiększenie pionowe; porównanie "
        "równowag, nie symulacja pompowania.",
        "fr": "Île idéalisée ; échelles fixes, exagération verticale ; comparaison "
        "d’équilibres, sans simulation de pompage.",
        "es": "Isla idealizada; escalas fijas, exageración vertical; comparación de "
        "equilibrios, sin simular bombeo.",
        "ar": "جزيرة مثالية؛ مقاييس ثابتة ومبالغة رأسية؛ مقارنة حالات اتزان وليست محاكاة "
        "ضخ.",
        "cs": "Idealizovaný ostrov; pevná měřítka, svislé převýšení; srovnání rovnováh, "
        "nikoli simulace čerpání.",
        "it": "Isola idealizzata; scale fisse, esagerazione verticale; confronto di "
        "equilibri, non simulazione di pompaggio.",
    },
    "advanced_link": {
        "en": "Explore the existing flow module",
        "de": "Zum bestehenden Strömungsmodul",
        "pl": "Przejdź do istniejącego modułu przepływu",
        "fr": "Explorer le module d’écoulement existant",
        "es": "Explora el módulo de flujo existente",
        "ar": "استكشف وحدة الجريان الموجودة",
        "cs": "Prozkoumat stávající modul proudění",
        "it": "Esplora il modulo di flusso esistente",
    },
    "poster_link": {
        "en": "USGS water-cycle illustrations in many languages",
        "de": "USGS-Wasserkreislaufbilder in vielen Sprachen",
        "pl": "Ilustracje obiegu wody USGS w wielu językach",
        "fr": "Illustrations USGS du cycle de l’eau en plusieurs langues",
        "es": "Ilustraciones USGS del ciclo del agua en varios idiomas",
        "ar": "رسوم دورة المياه من USGS بلغات عديدة",
        "cs": "Obrázky koloběhu vody USGS v mnoha jazycích",
        "it": "Illustrazioni USGS del ciclo dell’acqua in varie lingue",
    },
    "figure_placeholder": {
        "en": "Illustration space: USGS global water cycle. A simplified diagram "
        "is shown below until the selected poster is added.",
        "de": "Bildplatz: globaler USGS-Wasserkreislauf. Bis das ausgewählte "
        "Poster eingefügt ist, zeigt die Grafik unten einen vereinfachten "
        "Ausschnitt.",
        "pl": "Miejsce na ilustrację: globalny obieg wody USGS. Poniżej "
        "uproszczony schemat do czasu dodania wybranego plakatu.",
        "fr": "Emplacement pour le cycle global de l’eau USGS. Le schéma simplifié "
        "ci-dessous est affiché en attendant l’affiche choisie.",
        "es": "Espacio para el ciclo global del agua USGS. Se muestra un esquema "
        "simplificado hasta añadir el póster elegido.",
        "ar": "مكان لرسم دورة المياه العالمية من USGS. يظهر مخطط مبسّط أدناه إلى "
        "حين إضافة الرسم المختار.",
        "cs": "Místo pro obrázek globálního koloběhu vody USGS. Do vložení "
        "vybraného plakátu je níže zjednodušené schéma.",
        "it": "Spazio per il ciclo globale dell’acqua USGS. In attesa del poster "
        "scelto, sotto compare uno schema semplificato.",
    },
    "learning_objectives": {
        "en": "Learning objectives",
        "de": "Lernziele",
        "pl": "Cele nauki",
        "fr": "Objectifs d’apprentissage",
        "es": "Objetivos de aprendizaje",
        "ar": "أهداف التعلم",
        "cs": "Cíle učení",
        "it": "Obiettivi di apprendimento",
    },
    "solid_volume": {
        "en": "Solid material volume, excluding pores (mL)",
        "de": "Volumen des Feststoffs, ohne Poren (mL)",
        "pl": "Objętość materiału stałego, bez porów (mL)",
        "fr": "Volume du matériau solide, sans les pores (mL)",
        "es": "Volumen del material sólido, sin poros (mL)",
        "ar": "حجم المادة الصلبة دون المسام (مل)",
        "cs": "Objem pevné hmoty bez pórů (mL)",
        "it": "Volume del materiale solido, esclusi i pori (mL)",
    },
    "porosity_value": {
        "en": "Porosity",
        "de": "Porosität",
        "pl": "Porowatość",
        "fr": "Porosité",
        "es": "Porosidad",
        "ar": "المسامية",
        "cs": "Pórovitost",
        "it": "Porosità",
    },
    "pore_volume": {
        "en": "Pore volume",
        "de": "Porenvolumen",
        "pl": "Objętość porów",
        "fr": "Volume des pores",
        "es": "Volumen de poros",
        "ar": "حجم المسام",
        "cs": "Objem pórů",
        "it": "Volume dei pori",
    },
    "sample_volume": {
        "en": "Sample volume",
        "de": "Probenvolumen",
        "pl": "Objętość próbki",
        "fr": "Volume de l’échantillon",
        "es": "Volumen de la muestra",
        "ar": "حجم العينة",
        "cs": "Objem vzorku",
        "it": "Volume del campione",
    },
    "solid_short": {
        "en": "Solid volume",
        "de": "Feststoffvolumen",
        "pl": "Objętość części stałej",
        "fr": "Volume solide",
        "es": "Volumen sólido",
        "ar": "حجم المادة الصلبة",
        "cs": "Objem pevné hmoty",
        "it": "Volume solido",
    },
    "empty_sample": {
        "en": "Start by adding a sample volume. For an empty cup, porosity is undefined.",
        "de": "Beginne mit einem Probenvolumen. Für einen leeren Becher ist die "
        "Porosität nicht definiert.",
        "pl": "Zacznij od zwiększenia objętości próbki. Dla pustego kubka porowatość "
        "jest nieokreślona.",
        "fr": "Commencez par ajouter un volume d’échantillon. La porosité d’un gobelet "
        "vide n’est pas définie.",
        "es": "Empieza añadiendo un volumen de muestra. En un vaso vacío, la porosidad "
        "no está definida.",
        "ar": "ابدأ بإضافة حجم للعينة. لا تُعرَّف المسامية لكوب فارغ.",
        "cs": "Začněte přidáním objemu vzorku. Pro prázdný kelímek není pórovitost "
        "definována.",
        "it": "Inizia aggiungendo un volume di campione. Per un bicchiere vuoto la "
        "porosità non è definita.",
    },
    "invalid_solids": {
        "en": "The solid volume cannot exceed the total sample volume.",
        "de": "Das Feststoffvolumen darf das Gesamtvolumen nicht überschreiten.",
        "pl": "Objętość części stałej nie może przekraczać objętości całej próbki.",
        "fr": "Le volume solide ne peut pas dépasser le volume total.",
        "es": "El volumen sólido no puede superar el volumen total de la muestra.",
        "ar": "لا يمكن أن يتجاوز حجم المادة الصلبة الحجم الكلي للعينة.",
        "cs": "Objem pevné hmoty nemůže přesáhnout celkový objem vzorku.",
        "it": "Il volume solido non può superare il volume totale del campione.",
    },
    "cup_caption": {
        "en": "The whole cup grows with sample volume; its colored areas represent solids "
        "and pores. These are volume shares, not real layers. Cup dimensions are "
        "illustrative.",
        "de": "Der ganze Becher wächst mit dem Probenvolumen; seine Farbflächen stellen "
        "Feststoff- und Porenanteile dar, keine echten Schichten. Die "
        "Becherabmessungen sind schematisch.",
        "pl": "Cały kubek rośnie wraz z objętością próbki; kolorowe pola przedstawiają "
        "udziały części stałej i porów, nie rzeczywiste warstwy. Wymiary kubka są "
        "schematyczne.",
        "fr": "Le gobelet grandit avec le volume de l’échantillon ; ses surfaces colorées "
        "représentent les parts de solides et de pores, pas de vraies couches. Ses "
        "dimensions sont schématiques.",
        "es": "El vaso crece con el volumen de muestra; las áreas de color representan "
        "las proporciones de sólidos y poros, no capas reales. Sus dimensiones son "
        "ilustrativas.",
        "ar": "يكبر الكوب كله مع حجم العينة؛ وتمثل المساحات الملوّنة حصص المادة الصلبة "
        "والمسام، وليس طبقات حقيقية. أبعاد الكوب توضيحية.",
        "cs": "Celý kelímek roste s objemem vzorku; barevné plochy představují podíly "
        "pevné hmoty a pórů, nikoli skutečné vrstvy. Rozměry kelímku jsou "
        "schematické.",
        "it": "Il bicchiere cresce con il volume del campione; le aree colorate "
        "rappresentano le quote di solidi e pori, non strati reali. Le dimensioni "
        "sono illustrative.",
    },
    "hands_on": {
        "en": "Try the real cup experiment",
        "de": "Das echte Becherexperiment",
        "pl": "Wykonaj doświadczenie z kubkiem",
        "fr": "Essayer avec un vrai gobelet",
        "es": "Haz el experimento con un vaso real",
        "ar": "جرّب التجربة بكوب حقيقي",
        "cs": "Vyzkoušejte pokus se skutečným kelímkem",
        "it": "Prova l’esperimento con un vero bicchiere",
    },
    "divide": {
        "en": "Groundwater divide",
        "de": "Grundwasserscheide",
        "pl": "Dział wód podziemnych",
        "fr": "Ligne de partage des eaux souterraines",
        "es": "Divisoria de aguas subterráneas",
        "ar": "خط تقسيم المياه الجوفية",
        "cs": "Rozvodnice podzemní vody",
        "it": "Spartiacque sotterraneo",
    },
    "no_flow": {
        "en": "No flow across this boundary",
        "de": "Kein Fluss durch diese Grenze",
        "pl": "Brak przepływu przez tę granicę",
        "fr": "Aucun écoulement à travers cette limite",
        "es": "Sin flujo a través de este límite",
        "ar": "لا تدفق عبر هذا الحد",
        "cs": "Přes tuto hranici voda neproudí",
        "it": "Nessun flusso attraverso questo limite",
    },
    "cycle_boundary": {
        "en": "The left edge is an ideal groundwater divide: no water crosses it "
        "sideways. On this side of the divide, the water table slopes gently "
        "toward the surface-water sink. This is a selected pathway, not the "
        "whole water cycle.",
        "de": "Links liegt eine ideale Grundwasserscheide: Seitlich strömt kein Wasser "
        "darüber. Auf dieser Seite der Scheide fällt der Grundwasserspiegel "
        "sanft zum aufnehmenden Oberflächengewässer ab. Gezeigt ist ein Teil des "
        "Wasserkreislaufs.",
        "pl": "Lewa krawędź to idealny dział wód podziemnych: woda nie przepływa przez "
        "niego na boki. Po tej stronie działu zwierciadło łagodnie opada ku "
        "wodzie powierzchniowej, która odbiera przepływ. To wybrana droga, nie "
        "cały obieg wody.",
        "fr": "À gauche, une ligne idéale de partage des eaux souterraines : aucun "
        "écoulement latéral ne la traverse. De ce côté, la nappe descend "
        "doucement vers l’eau de surface qui reçoit l’écoulement. Ce n’est qu’un "
        "trajet du cycle de l’eau.",
        "es": "El borde izquierdo es una divisoria ideal de aguas subterráneas: no la "
        "cruza flujo lateral. A este lado, el nivel freático desciende "
        "suavemente hacia el agua superficial que recibe el flujo. Se muestra "
        "una parte del ciclo del agua.",
        "ar": "يمثل الحد الأيسر خط تقسيم مثالياً للمياه الجوفية: لا يعبره الماء "
        "جانبياً. على هذا الجانب ينخفض منسوب المياه الجوفية برفق نحو المياه "
        "السطحية التي تستقبل التدفق. هذا مسار مختار، وليس دورة الماء بأكملها.",
        "cs": "Levý okraj je ideální rozvodnice podzemní vody: voda ji bočně "
        "nepřekračuje. Na této straně rozvodnice hladina mírně klesá k povrchové "
        "vodě, která proudění přijímá. Jde o vybranou cestu, nikoli celý koloběh "
        "vody.",
        "it": "Il bordo sinistro è uno spartiacque sotterraneo ideale: nessun flusso "
        "laterale lo attraversa. Da questo lato la falda scende dolcemente verso "
        "l’acqua superficiale che riceve il flusso. È un percorso, non l’intero "
        "ciclo dell’acqua.",
    },
    "medium_low": {
        "en": "Moderately low",
        "de": "Mäßig niedrig",
        "pl": "Umiarkowanie niski",
        "fr": "Modérément bas",
        "es": "Moderadamente bajo",
        "ar": "منخفض نسبياً",
        "cs": "Středně nízká",
        "it": "Moderatamente basso",
    },
    "medium_high": {
        "en": "Moderately high",
        "de": "Mäßig hoch",
        "pl": "Umiarkowanie wysoki",
        "fr": "Modérément élevé",
        "es": "Moderadamente alto",
        "ar": "مرتفع نسبياً",
        "cs": "Středně vysoká",
        "it": "Moderatamente alto",
    },
    "peak_head": {
        "en": "Highest freshwater level above sea level",
        "de": "Höchster Süßwasserspiegel über dem Meeresspiegel",
        "pl": "Najwyższy poziom wody słodkiej nad poziomem morza",
        "fr": "Niveau maximal d’eau douce au-dessus de la mer",
        "es": "Nivel máximo de agua dulce sobre el nivel del mar",
        "ar": "أعلى منسوب للمياه العذبة فوق مستوى البحر",
        "cs": "Nejvyšší hladina sladké vody nad hladinou moře",
        "it": "Livello massimo dell’acqua dolce sopra il mare",
    },
    "interface_depth": {
        "en": "Interface depth below sea level at the island centre",
        "de": "Grenzflächentiefe unter dem Meeresspiegel in der Inselmitte",
        "pl": "Głębokość granicy pod poziomem morza w środku wyspy",
        "fr": "Profondeur de l’interface sous la mer au centre de l’île",
        "es": "Profundidad de la interfaz bajo el nivel del mar en el centro de la "
        "isla",
        "ar": "عمق السطح الفاصل تحت مستوى البحر في مركز الجزيرة",
        "cs": "Hloubka rozhraní pod hladinou moře ve středu ostrova",
        "it": "Profondità dell’interfaccia sotto il mare al centro dell’isola",
    },
    "lens_values_note": {
        "en": "Illustrative equilibrium values at the island centre, using "
        "freshwater density 1000 kg/m³ and seawater density 1025 kg/m³. Not "
        "measurements from Sopot; not a pumping forecast.",
        "de": "Illustrative Gleichgewichtswerte in der Inselmitte bei 1000 kg/m³ für "
        "Süßwasser und 1025 kg/m³ für Meerwasser. Keine Messwerte aus Sopot "
        "und keine Pumpvorhersage.",
        "pl": "Przykładowe wartości równowagi w środku wyspy dla gęstości wody "
        "słodkiej 1000 kg/m³ i morskiej 1025 kg/m³. To nie pomiary z Sopotu "
        "ani prognoza pompowania.",
        "fr": "Valeurs d’équilibre illustratives au centre de l’île, avec des masses "
        "volumiques de 1000 kg/m³ pour l’eau douce et 1025 kg/m³ pour l’eau de "
        "mer. Ni mesures de Sopot, ni prévision de pompage.",
        "es": "Valores ilustrativos de equilibrio en el centro de la isla, con "
        "densidades de 1000 kg/m³ para agua dulce y 1025 kg/m³ para agua "
        "marina. No son mediciones de Sopot ni una previsión de bombeo.",
        "ar": "قيم توازن توضيحية في مركز الجزيرة، بكثافة 1000 كغ/م³ للمياه العذبة "
        "و1025 كغ/م³ لمياه البحر. ليست قياسات من سوبوت ولا تنبؤاً بتأثير الضخ.",
        "cs": "Ilustrační rovnovážné hodnoty ve středu ostrova při hustotě sladké "
        "vody 1000 kg/m³ a mořské vody 1025 kg/m³. Nejde o měření ze Sopot ani "
        "o předpověď čerpání.",
        "it": "Valori di equilibrio illustrativi al centro dell’isola, con densità "
        "di 1000 kg/m³ per l’acqua dolce e 1025 kg/m³ per quella marina. Non "
        "sono misure di Sopot né previsioni del pompaggio.",
    },
    "cover_credit": {
        "en": "Original English covers · © the authors · The Groundwater Project. Follow "
        "the book links for available translations.",
        "de": "Englische Originaltitelbilder · © die Autoren · The Groundwater Project. "
        "Verfügbare Übersetzungen stehen auf den Buchseiten.",
        "pl": "Oryginalne okładki angielskie · © autorzy · The Groundwater Project. "
        "Dostępne tłumaczenia znajdziesz na stronach książek.",
        "fr": "Couvertures originales en anglais · © les auteurs · The Groundwater "
        "Project. Les traductions disponibles figurent sur les pages des livres.",
        "es": "Portadas originales en inglés · © los autores · The Groundwater Project. "
        "Consulta las traducciones disponibles en las páginas de los libros.",
        "ar": "الأغلفة الإنجليزية الأصلية · © المؤلفون · The Groundwater Project. راجع "
        "روابط الكتب للاطلاع على الترجمات المتاحة.",
        "cs": "Původní anglické obálky · © autoři · The Groundwater Project. Dostupné "
        "překlady najdete na stránkách knih.",
        "it": "Copertine originali in inglese · © gli autori · The Groundwater Project. "
        "Le traduzioni disponibili sono indicate nelle pagine dei libri.",
    },
    "water_cycle_heading": {
        "en": "The water cycle",
        "de": "Der Wasserkreislauf",
        "pl": "Obieg wody",
        "fr": "Le cycle de l’eau",
        "es": "El ciclo del agua",
        "ar": "دورة الماء",
        "cs": "Koloběh vody",
        "it": "Il ciclo dell’acqua",
    },
    "freshwater_heading": {
        "en": "Where is our freshwater stored?",
        "de": "Wo ist unser Süßwasser gespeichert?",
        "pl": "Gdzie zgromadzona jest woda słodka?",
        "fr": "Où l’eau douce est-elle stockée ?",
        "es": "¿Dónde se almacena el agua dulce?",
        "ar": "أين تُخزَّن المياه العذبة؟",
        "cs": "Kde je uložena sladká voda?",
        "it": "Dove si trova la nostra riserva d’acqua dolce?",
    },
    "meaning_heading": {
        "en": "What this store means for us",
        "de": "Was dieser Speicher für uns bedeutet",
        "pl": "Co ten zasób oznacza dla nas",
        "fr": "Ce que cette réserve représente pour nous",
        "es": "Qué significa esta reserva para nosotros",
        "ar": "ماذا يعني هذا المخزون لنا؟",
        "cs": "Co pro nás tato zásoba znamená",
        "it": "Che cosa significa questa riserva per noi",
    },
    "underground_heading": {
        "en": "Look beneath the surface",
        "de": "Ein Blick unter die Oberfläche",
        "pl": "Spójrz pod powierzchnię",
        "fr": "Regarder sous la surface",
        "es": "Mira bajo la superficie",
        "ar": "انظر تحت السطح",
        "cs": "Nahlédněte pod povrch",
        "it": "Guarda sotto la superficie",
    },
    "cycle_path_heading": {
        "en": "From rain to groundwater flow",
        "de": "Vom Regen zur Grundwasserströmung",
        "pl": "Od deszczu do przepływu podziemnego",
        "fr": "De la pluie à l’écoulement souterrain",
        "es": "De la lluvia al flujo subterráneo",
        "ar": "من المطر إلى جريان المياه الجوفية",
        "cs": "Od deště k proudění podzemní vody",
        "it": "Dalla pioggia al flusso sotterraneo",
    },
    "lens_heading": {
        "en": "Reading a freshwater lens",
        "de": "Eine Süßwasserlinse verstehen",
        "pl": "Jak odczytać soczewkę wody słodkiej",
        "fr": "Comprendre une lentille d’eau douce",
        "es": "Interpretar una lente de agua dulce",
        "ar": "فهم عدسة المياه العذبة",
        "cs": "Jak číst čočku sladké vody",
        "it": "Interpretare una lente d’acqua dolce",
    },
    "river_heading": {
        "en": "Beyond the beach: beside a river",
        "de": "Vom Strand zum Fluss",
        "pl": "Od plaży do brzegu rzeki",
        "fr": "De la plage au bord d’une rivière",
        "es": "De la playa a la orilla de un río",
        "ar": "من الشاطئ إلى ضفة النهر",
        "cs": "Od pláže k řece",
        "it": "Dalla spiaggia alla riva di un fiume",
    },
    "river_mode": {
        "en": "Which way does the water move?",
        "de": "In welche Richtung fließt das Wasser?",
        "pl": "W którą stronę płynie woda?",
        "fr": "Dans quel sens l’eau circule-t-elle ?",
        "es": "¿En qué dirección se mueve el agua?",
        "ar": "في أي اتجاه يتحرك الماء؟",
        "cs": "Kterým směrem voda proudí?",
        "it": "In quale direzione si muove l’acqua?",
    },
    "river_gaining": {
        "en": "Exfiltrating / gaining river · groundwater → river",
        "de": "Exfiltrierender Fluss · Grundwasser → Fluss",
        "pl": "Rzeka drenująca · woda podziemna → rzeka",
        "fr": "Rivière drainante (exfiltration) · nappe → rivière",
        "es": "Río ganador (exfiltración) · agua subterránea → río",
        "ar": "نهر يكتسب الماء (تصريف جوفي) · من المياه الجوفية إلى النهر",
        "cs": "Drenující tok (exfiltrace) · podzemní voda → řeka",
        "it": "Fiume drenante (esfiltrazione) · falda → fiume",
    },
    "river_losing": {
        "en": "Infiltrating / losing river · river → groundwater",
        "de": "Infiltrierender Fluss · Fluss → Grundwasser",
        "pl": "Rzeka infiltrująca · rzeka → woda podziemna",
        "fr": "Rivière infiltrante · rivière → nappe",
        "es": "Río perdedor (infiltración) · río → agua subterránea",
        "ar": "نهر يفقد الماء بالتسرب · من النهر إلى المياه الجوفية",
        "cs": "Infiltrující tok · řeka → podzemní voda",
        "it": "Fiume infiltrante · fiume → falda",
    },
    "river_position": {
        "en": "Place the observation hole",
        "de": "Beobachtungsloch platzieren",
        "pl": "Umieść otwór obserwacyjny",
        "fr": "Placer le trou d’observation",
        "es": "Sitúa el hoyo de observación",
        "ar": "حدّد موضع حفرة الملاحظة",
        "cs": "Umístěte pozorovací otvor",
        "it": "Posiziona la buca di osservazione",
    },
    "river_near": {
        "en": "Close to the river",
        "de": "Nah am Fluss",
        "pl": "Blisko rzeki",
        "fr": "Près de la rivière",
        "es": "Cerca del río",
        "ar": "قرب النهر",
        "cs": "Blízko řeky",
        "it": "Vicino al fiume",
    },
    "river_inland": {
        "en": "Farther inland",
        "de": "Weiter im Landesinneren",
        "pl": "Dalej od rzeki",
        "fr": "Plus loin dans les terres",
        "es": "Más hacia el interior",
        "ar": "أبعد نحو الداخل",
        "cs": "Dále od řeky",
        "it": "Più lontano dalla riva",
    },
    "river_depth": {
        "en": "Choose the bottom of the virtual hole",
        "de": "Sohle des virtuellen Lochs wählen",
        "pl": "Wybierz położenie dna wirtualnego otworu",
        "fr": "Choisir le fond du trou virtuel",
        "es": "Elige el fondo del hoyo virtual",
        "ar": "اختر موضع قاع الحفرة الافتراضية",
        "cs": "Zvolte dno virtuálního otvoru",
        "it": "Scegli il fondo della buca virtuale",
    },
    "river_shallow": {
        "en": "Shallow: just below the ground surface",
        "de": "Flach: knapp unter der Geländeoberfläche",
        "pl": "Płytko: tuż pod powierzchnią terenu",
        "fr": "Peu profond : juste sous le sol",
        "es": "Poco profundo: justo bajo el terreno",
        "ar": "ضحلة: أسفل سطح الأرض مباشرة",
        "cs": "Mělce: těsně pod povrchem terénu",
        "it": "Poco profonda: appena sotto il terreno",
    },
    "river_level_depth": {
        "en": "Slightly deeper: just below river water level",
        "de": "Etwas tiefer: knapp unter dem Flusswasserspiegel",
        "pl": "Nieco głębiej: tuż poniżej poziomu wody w rzece",
        "fr": "Un peu plus profond : juste sous le niveau de la rivière",
        "es": "Algo más profundo: justo bajo el nivel del río",
        "ar": "أعمق قليلاً: أسفل منسوب النهر مباشرة",
        "cs": "O něco hlouběji: těsně pod hladinou řeky",
        "it": "Un po’ più profonda: appena sotto il livello del fiume",
    },
    "river_deep": {
        "en": "Deeper: well below river water level",
        "de": "Tiefer: deutlich unter dem Flusswasserspiegel",
        "pl": "Głębiej: znacznie poniżej poziomu wody w rzece",
        "fr": "Plus profond : bien sous le niveau de la rivière",
        "es": "Más profundo: bastante por debajo del nivel del río",
        "ar": "أعمق: أسفل منسوب النهر بوضوح",
        "cs": "Hlouběji: výrazně pod hladinou řeky",
        "it": "Più profonda: ben sotto il livello del fiume",
    },
    "virtual_hole": {
        "en": "Virtual observation hole",
        "de": "Virtuelles Beobachtungsloch",
        "pl": "Wirtualny otwór obserwacyjny",
        "fr": "Trou d’observation virtuel",
        "es": "Hoyo de observación virtual",
        "ar": "حفرة ملاحظة افتراضية",
        "cs": "Virtuální pozorovací otvor",
        "it": "Buca di osservazione virtuale",
    },
    "river_label": {
        "en": "Surface water",
        "de": "Oberflächenwasser",
        "pl": "Wody powierzchniowe",
        "fr": "Eau de surface",
        "es": "Agua superficial",
        "ar": "مياه سطحية",
        "cs": "Povrchová voda",
        "it": "Acqua superficiale",
    },
    "river_water_level": {
        "en": "Surface-water level · reference",
        "de": "Gewässerstand · Bezugslinie",
        "pl": "Poziom wód powierzchniowych · odniesienie",
        "fr": "Niveau de l’eau de surface · repère",
        "es": "Nivel del agua superficial · referencia",
        "ar": "منسوب المياه السطحية · خط مرجعي",
        "cs": "Hladina povrchové vody · reference",
        "it": "Livello dell’acqua superficiale · riferimento",
    },
    "river_caption": {
        "en": "The dotted line extends the surface-water level inland as a visual "
        "reference; it is not water inside the ground. The blue curve marks the "
        "groundwater table when revealed. Ideal connected aquifer; vertical scale "
        "enlarged, no site measurements.",
        "de": "Die gepunktete Linie verlängert den Gewässerstand ins Land als "
        "Orientierung; sie stellt kein Wasser im Untergrund dar. Die blaue Kurve "
        "zeigt den eingeblendeten Grundwasserspiegel. Idealisierter verbundener "
        "Aquifer; vertikal überhöht, keine Standortmessungen.",
        "pl": "Kropkowana linia przedłuża poziom wód powierzchniowych w głąb lądu jako "
        "punkt odniesienia; nie przedstawia wody w podłożu. Niebieska krzywa "
        "pokazuje odkryte zwierciadło wód podziemnych. Idealne połączenie "
        "hydrauliczne; skala pionowa powiększona, bez pomiarów terenowych.",
        "fr": "La ligne pointillée prolonge le niveau de l’eau de surface vers "
        "l’intérieur comme repère ; elle ne représente pas de l’eau dans le sol. "
        "La courbe bleue indique la nappe lorsqu’elle est affichée. Aquifère "
        "idéal connecté ; échelle verticale amplifiée, sans mesures de terrain.",
        "es": "La línea de puntos prolonga el nivel del agua superficial tierra adentro "
        "como referencia; no representa agua dentro del terreno. La curva azul "
        "indica el nivel freático al mostrarlo. Acuífero ideal conectado; escala "
        "vertical ampliada, sin mediciones de campo.",
        "ar": "يمتد الخط المنقّط بمنسوب المياه السطحية نحو الداخل كمرجع بصري؛ ولا يمثّل "
        "ماءً داخل الأرض. ويبيّن المنحنى الأزرق منسوب المياه الجوفية عند إظهاره. "
        "خزان مثالي متصل بالمياه السطحية؛ المقياس الرأسي مكبّر، ولا توجد قياسات "
        "ميدانية.",
        "cs": "Tečkovaná čára prodlužuje hladinu povrchové vody do vnitrozemí jako "
        "orientační úroveň; nepředstavuje vodu uvnitř podloží. Modrá křivka "
        "ukazuje odkrytou hladinu podzemní vody. Ideální propojená zvodeň; "
        "zvětšené svislé měřítko, bez místních měření.",
        "it": "La linea tratteggiata prolunga il livello dell’acqua superficiale verso "
        "l’interno come riferimento; non rappresenta acqua nel terreno. La curva "
        "blu indica la falda quando viene mostrata. Acquifero ideale collegato; "
        "scala verticale amplificata, senza misure sul campo.",
    },
    "river_explain_gaining": {
        "en": "Groundwater feeds the river. Its level is higher inland and "
        "approaches river level near the bank. A deeper hole holds more "
        "water but shows the same local water-table elevation.",
        "de": "Grundwasser speist den Fluss. Sein Spiegel ist im Landesinneren "
        "höher und nähert sich am Ufer dem Flussspiegel. Ein tieferes "
        "Loch enthält mehr Wasser, zeigt aber dieselbe örtliche "
        "Grundwasserhöhe.",
        "pl": "Woda podziemna zasila rzekę. Jej zwierciadło jest wyższe dalej "
        "od brzegu, a przy brzegu zbliża się do poziomu rzeki. Głębszy "
        "otwór mieści więcej wody, ale wskazuje tę samą lokalną rzędną "
        "zwierciadła.",
        "fr": "La nappe alimente la rivière. Son niveau est plus haut à "
        "l’intérieur des terres et se rapproche de celui de la rivière "
        "près de la berge. Un trou plus profond contient davantage d’eau "
        "mais indique la même altitude locale de nappe.",
        "es": "El agua subterránea alimenta el río. Su nivel es mayor hacia el "
        "interior y se aproxima al del río junto a la orilla. Un hoyo más "
        "profundo contiene más agua, pero muestra la misma elevación "
        "local del nivel freático.",
        "ar": "تغذّي المياه الجوفية النهر. يكون منسوبها أعلى نحو الداخل ويقترب "
        "من منسوب النهر عند الضفة. تحتوي الحفرة الأعمق على ماء أكثر، "
        "لكنها تُظهر المنسوب الجوفي المحلي نفسه.",
        "cs": "Podzemní voda napájí řeku. Dále od břehu má vyšší hladinu, která "
        "se u břehu blíží hladině řeky. Hlubší otvor obsahuje více vody, "
        "ale ukazuje stejnou místní výšku hladiny.",
        "it": "La falda alimenta il fiume. Il suo livello è più alto "
        "nell’entroterra e si avvicina a quello del fiume presso la riva. "
        "Una buca più profonda contiene più acqua, ma indica la stessa "
        "quota locale della falda.",
    },
    "river_explain_losing": {
        "en": "River water enters the aquifer. The groundwater level is lower "
        "inland. A hole ending just below river level may still be dry "
        "there: it has not reached the local water table.",
        "de": "Flusswasser gelangt in den Aquifer. Der Grundwasserspiegel liegt "
        "im Landesinneren tiefer. Ein Loch bis knapp unter den "
        "Flussspiegel kann dort trocken bleiben: Es erreicht den örtlichen "
        "Grundwasserspiegel noch nicht.",
        "pl": "Woda z rzeki infiltruje do poziomu wodonośnego. Zwierciadło wody "
        "podziemnej jest niższe dalej od brzegu. Otwór kończący się tuż "
        "poniżej poziomu rzeki może tam pozostać suchy: nie sięga "
        "lokalnego zwierciadła.",
        "fr": "L’eau de la rivière entre dans l’aquifère. La nappe est plus "
        "basse dans les terres. Un trou s’arrêtant juste sous le niveau de "
        "la rivière peut y rester sec : il n’atteint pas la nappe locale.",
        "es": "El agua del río entra en el acuífero. El nivel freático es menor "
        "hacia el interior. Un hoyo que termina justo bajo el nivel del "
        "río puede seguir seco allí: aún no alcanza el nivel freático "
        "local.",
        "ar": "يتسرب ماء النهر إلى الخزان الجوفي. يكون المنسوب الجوفي أخفض نحو "
        "الداخل. وقد تبقى حفرة تنتهي أسفل منسوب النهر بقليل جافة هناك "
        "لأنها لم تصل إلى المنسوب الجوفي المحلي.",
        "cs": "Voda z řeky vstupuje do kolektoru. Dále od břehu je hladina "
        "podzemní vody nižší. Otvor končící těsně pod hladinou řeky tam "
        "může zůstat suchý, protože ještě nedosáhl místní hladiny podzemní "
        "vody.",
        "it": "L’acqua del fiume entra nell’acquifero. La falda è più bassa "
        "nell’entroterra. Una buca che termina appena sotto il livello del "
        "fiume può restare asciutta: non ha ancora raggiunto la falda "
        "locale.",
    },
    "reflection_guidance": {
        "en": "Discuss, then compare with these explanations",
        "de": "Erst diskutieren, dann mit diesen Erklärungen vergleichen",
        "pl": "Najpierw porozmawiaj, potem porównaj wyjaśnienia",
        "fr": "Discutez, puis comparez avec ces explications",
        "es": "Comenta y luego compara con estas explicaciones",
        "ar": "ناقش أولاً، ثم قارن بهذه التفسيرات",
        "cs": "Nejprve diskutujte, pak porovnejte s vysvětlením",
        "it": "Discuti, poi confronta con queste spiegazioni",
    },
    "draft_notice": {
        "en": "About this draft · development and review",
        "de": "Zu diesem Entwurf · Entwicklung und Begutachtung",
        "pl": "O tej wersji roboczej · rozwój i recenzja",
        "fr": "À propos de cette ébauche · développement et évaluation",
        "es": "Sobre este borrador · desarrollo y revisión",
        "ar": "عن هذه المسودة · التطوير والمراجعة",
        "cs": "O této pracovní verzi · vývoj a posouzení",
        "it": "Informazioni sulla bozza · sviluppo e revisione",
    },
    "review_module": {
        "en": "Share feedback through the module review form",
        "de": "Feedback im Formular zur Modulbegutachtung geben",
        "pl": "Przekaż uwagi w formularzu oceny modułu",
        "fr": "Donner un avis via le formulaire d’évaluation",
        "es": "Enviar comentarios en el formulario de revisión",
        "ar": "شارك ملاحظاتك عبر استمارة مراجعة الوحدة",
        "cs": "Sdílet připomínky ve formuláři hodnocení modulu",
        "it": "Invia commenti tramite il modulo di valutazione",
    },
    "cup_slider_input": {
        "en": "Use sliders instead of number inputs",
        "de": "Schieberegler statt Zahleneingabe verwenden",
        "pl": "Użyj suwaków zamiast pól liczbowych",
        "fr": "Utiliser des curseurs plutôt que des champs numériques",
        "es": "Usar deslizadores en lugar de campos numéricos",
        "ar": "استخدم أشرطة التمرير بدلاً من إدخال الأرقام",
        "cs": "Použít posuvníky místo číselných polí",
        "it": "Usa cursori al posto dei campi numerici",
    },
    "distribution_heading": {
        "en": "Earth’s water · the wider picture",
        "de": "Das Wasser der Erde · der größere Zusammenhang",
        "pl": "Woda na Ziemi · szerszy obraz",
        "fr": "L’eau sur Terre · une vue d’ensemble",
        "es": "El agua de la Tierra · una visión general",
        "ar": "ماء الأرض · الصورة الأوسع",
        "cs": "Voda na Zemi · širší souvislosti",
        "it": "L’acqua della Terra · il quadro generale",
    },
    "distribution_credit": {
        "en": "USGS Water Science School · supplied excerpt · original labels in "
        "English [S4]",
        "de": "USGS Water Science School · bereitgestellter Ausschnitt · "
        "Originalbeschriftung auf Englisch [S4]",
        "pl": "USGS Water Science School · udostępniony fragment · oryginalne "
        "podpisy po angielsku [S4]",
        "fr": "USGS Water Science School · extrait fourni · légendes originales "
        "en anglais [S4]",
        "es": "USGS Water Science School · extracto facilitado · rótulos "
        "originales en inglés [S4]",
        "ar": "USGS Water Science School · مقتطف مقدَّم · التسميات الأصلية "
        "بالإنجليزية [S4]",
        "cs": "USGS Water Science School · dodaný výřez · původní anglické "
        "popisky [S4]",
        "it": "USGS Water Science School · estratto fornito · etichette originali "
        "in inglese [S4]",
    },
    "cherry_talk": {
        "en": "Watch and reflect · a talk by John Cherry",
        "de": "Ansehen und reflektieren · ein Vortrag von John Cherry",
        "pl": "Obejrzyj i przemyśl · wykład Johna Cherry’ego",
        "fr": "Regarder et réfléchir · une conférence de John Cherry",
        "es": "Mira y reflexiona · una charla de John Cherry",
        "ar": "شاهد وتأمّل · محاضرة لجون تشيري",
        "cs": "Podívejte se a zamyslete · přednáška Johna Cherryho",
        "it": "Guarda e rifletti · un intervento di John Cherry",
    },
    "watch_youtube": {
        "en": "Open on YouTube at 15:00",
        "de": "Auf YouTube ab 15:00 öffnen",
        "pl": "Otwórz w YouTube od 15:00",
        "fr": "Ouvrir sur YouTube à 15:00",
        "es": "Abrir en YouTube desde 15:00",
        "ar": "افتح في YouTube عند 15:00",
        "cs": "Otevřít na YouTube od 15:00",
        "it": "Apri su YouTube da 15:00",
    },
    "sidebar_hint": {
        "en": "Open the menu at the top left to choose a section or language.",
        "de": "Öffne das Menü oben links, um einen Abschnitt oder eine Sprache "
        "auszuwählen.",
        "pl": "Otwórz menu w lewym górnym rogu, aby wybrać sekcję lub język.",
        "fr": "Ouvrez le menu en haut à gauche pour choisir une section ou une langue.",
        "es": "Abre el menú de arriba a la izquierda para elegir una sección o un "
        "idioma.",
        "ar": "افتح القائمة في أعلى اليسار لاختيار القسم أو اللغة.",
        "cs": "Otevřete nabídku vlevo nahoře a vyberte část nebo jazyk.",
        "it": "Apri il menu in alto a sinistra per scegliere una sezione o una lingua.",
    },
    "poster_versions": {
        "en": "This USGS source offers different diagram versions, languages and "
        "download formats.",
        "de": "Diese USGS-Quelle bietet verschiedene Diagrammversionen, Sprachen und "
        "Downloadformate.",
        "pl": "To źródło USGS zawiera różne wersje diagramu, języki i formaty do "
        "pobrania.",
        "fr": "Cette source de l’USGS propose plusieurs versions, langues et formats "
        "de téléchargement.",
        "es": "Esta fuente del USGS ofrece distintas versiones del diagrama, idiomas "
        "y formatos de descarga.",
        "ar": "يوفر هذا المصدر من USGS نسخاً مختلفة من الرسم بلغات وصيغ تنزيل متعددة.",
        "cs": "Tento zdroj USGS nabízí různé verze schématu, jazyky a formáty ke "
        "stažení.",
        "it": "Questa fonte USGS offre diverse versioni del diagramma, lingue e "
        "formati da scaricare.",
    },
    "guess_close": {
        "en": "Your estimate is close!",
        "de": "Deine Schätzung liegt schon nahe!",
        "pl": "Twoje oszacowanie jest bliskie!",
        "fr": "Votre estimation est proche !",
        "es": "¡Tu estimación está cerca!",
        "ar": "تقديرك قريب!",
        "cs": "Váš odhad je blízko!",
        "it": "La tua stima è vicina!",
    },
    "guess_far": {
        "en": "Groundwater’s share is much larger than your guess.",
        "de": "Der Grundwasseranteil ist deutlich größer als deine Schätzung.",
        "pl": "Udział wód podziemnych jest znacznie większy niż Twój szacunek.",
        "fr": "La part de l’eau souterraine est bien plus grande que votre estimation.",
        "es": "La proporción de agua subterránea es mucho mayor que tu estimación.",
        "ar": "حصة المياه الجوفية أكبر بكثير من تقديرك.",
        "cs": "Podíl podzemní vody je mnohem větší než váš odhad.",
        "it": "La quota di acqua sotterranea è molto più grande della tua stima.",
    },
    "scroll_result": {
        "en": "(Scroll down to see the result.)",
        "de": "(Scrolle nach unten zum Ergebnis.)",
        "pl": "(Przewiń w dół, aby zobaczyć wynik.)",
        "fr": "(Faites défiler vers le bas pour voir le résultat.)",
        "es": "(Desplázate hacia abajo para ver el resultado.)",
        "ar": "(مرّر إلى أسفل لرؤية النتيجة.)",
        "cs": "(Výsledek zobrazíte posunutím dolů.)",
        "it": "(Scorri verso il basso per vedere il risultato.)",
    },
    "cup_step_1": {
        "en": "Fill and mark",
        "de": "Füllen und markieren",
        "pl": "Napełnij i zaznacz",
        "fr": "Remplir et marquer",
        "es": "Llena y marca",
        "ar": "املأ وحدّد المستوى",
        "cs": "Naplňte a označte",
        "it": "Riempi e segna",
    },
    "cup_step_2": {
        "en": "Add measured water",
        "de": "Wassermenge messen",
        "pl": "Dodaj odmierzoną wodę",
        "fr": "Ajouter de l’eau mesurée",
        "es": "Añade agua medida",
        "ar": "أضف ماءً مقاساً",
        "cs": "Přidejte odměřenou vodu",
        "it": "Aggiungi acqua misurata",
    },
    "cup_step_3": {
        "en": "Compare volumes",
        "de": "Volumen vergleichen",
        "pl": "Porównaj objętości",
        "fr": "Comparer les volumes",
        "es": "Compara los volúmenes",
        "ar": "قارن الأحجام",
        "cs": "Porovnejte objemy",
        "it": "Confronta i volumi",
    },
    "cup_step_note_1": {
        "en": "Fill to a marked level with dry, non-absorbent grains.",
        "de": "Fülle trockene, nicht saugende Körner bis zu einer Markierung ein.",
        "pl": "Napełnij do zaznaczonego poziomu suchymi ziarnami, które nie chłoną "
        "wody.",
        "fr": "Remplissez jusqu’au repère avec des grains secs et non absorbants.",
        "es": "Llena hasta una marca con granos secos que no absorban agua.",
        "ar": "املأ حتى العلامة بحبيبات جافة لا تمتص الماء.",
        "cs": "Naplňte po značku suchými zrny, která nenasakují vodu.",
        "it": "Riempi fino al segno con granuli asciutti e non assorbenti.",
    },
    "cup_step_note_2": {
        "en": "Record the water added just to the top of the grains.",
        "de": "Notiere die Wassermenge, die bis zur Oberkante der Körner passt.",
        "pl": "Zapisz ilość wody dodanej dokładnie do górnej powierzchni ziaren.",
        "fr": "Notez le volume d’eau ajouté jusqu’au sommet des grains.",
        "es": "Anota el agua añadida hasta la parte superior de los granos.",
        "ar": "سجّل حجم الماء المضاف حتى سطح الحبيبات فقط.",
        "cs": "Zapište objem vody přidané právě po horní povrch zrn.",
        "it": "Annota il volume d’acqua aggiunto fino alla sommità dei granuli.",
    },
    "cup_step_note_3": {
        "en": "Water added ÷ total sample volume × 100 gives an approximate porosity.",
        "de": "Zugegebenes Wasser ÷ Gesamtvolumen der Probe × 100 ergibt die "
        "ungefähre Porosität.",
        "pl": "Dodana woda ÷ całkowita objętość próbki × 100 daje przybliżoną "
        "porowatość.",
        "fr": "Eau ajoutée ÷ volume total de l’échantillon × 100 donne une porosité "
        "approximative.",
        "es": "Agua añadida ÷ volumen total de la muestra × 100 da una porosidad "
        "aproximada.",
        "ar": "حجم الماء المضاف ÷ الحجم الكلي للعينة × 100 يعطي مسامية تقريبية.",
        "cs": "Přidaná voda ÷ celkový objem vzorku × 100 udává přibližnou pórovitost.",
        "it": "Acqua aggiunta ÷ volume totale del campione × 100 dà una porosità "
        "approssimativa.",
    },
    "about": {
        "en": "About this module",
        "de": "Über dieses Modul",
        "pl": "O tym module",
        "fr": "À propos du module",
        "es": "Acerca del módulo",
        "ar": "عن هذه الوحدة",
        "cs": "O tomto modulu",
        "it": "Informazioni sul modulo",
    },
    "about_description": {
        "en": "Purpose",
        "de": "Ziel",
        "pl": "Cel",
        "fr": "Objectif",
        "es": "Objetivo",
        "ar": "الهدف",
        "cs": "Účel",
        "it": "Obiettivo",
    },
    "about_development": {
        "en": "Development",
        "de": "Entwicklung",
        "pl": "Opracowanie",
        "fr": "Développement",
        "es": "Desarrollo",
        "ar": "التطوير",
        "cs": "Vývoj",
        "it": "Sviluppo",
    },
    "about_author": {
        "en": "About the developer",
        "de": "Über den Entwickler",
        "pl": "O autorze",
        "fr": "À propos de l’auteur",
        "es": "Sobre el autor",
        "ar": "عن المطوّر",
        "cs": "O autorovi",
        "it": "Informazioni sull’autore",
    },
    "about_contact": {
        "en": "Contact and feedback",
        "de": "Kontakt und Feedback",
        "pl": "Kontakt i uwagi",
        "fr": "Contact et commentaires",
        "es": "Contacto y comentarios",
        "ar": "التواصل والملاحظات",
        "cs": "Kontakt a připomínky",
        "it": "Contatti e commenti",
    },
}

# New/revised UI strings live in editable UTF-8 JSON, one file per language.
import json

for _lang in LANGUAGES:
    _path = ROOT / "assets/ui" / (_lang + ".json")
    if _path.is_file():
        for _key, _value in json.loads(_path.read_text(encoding="utf-8")).items():
            TEXT.setdefault(_key, {})[_lang] = _value


def ui_text(en, **translations):
    return translations.get(st.session_state.get("language", "en"), en)


def tr(key):
    values = TEXT[key]
    return values.get(st.session_state.get("language", "en"), values["en"])


def load_md(directory, filename, language="en"):
    base = Path(filename)
    if base.name != filename or base.suffix != ".md":
        raise ValueError("Expected a simple Markdown filename.")
    directory = Path(directory)
    translated = directory / f"{base.stem}_{language}{base.suffix}"
    path = (
        translated
        if language != "en" and translated.is_file()
        else directory / filename
    )
    return path.read_text(encoding="utf-8")


def md(name):
    st.markdown(
        load_md(
            ROOT / "assets/markdown",
            name + ".md",
            st.session_state.get("language", "en"),
        )
    )
