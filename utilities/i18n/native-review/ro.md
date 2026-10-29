# Native review sheet: Romanian (`ro`)

Status: **not yet reviewed by a native speaker.** Everything below was written and self-reviewed by Claude. This sheet lists what needs a human decision.

## Scope
- 42 tool pages (title, description, H1, subtitle, hint, card labels/placeholders), 42 articles (about 69,443 words), 11 FAQ sets (127 Q&A), 6 static pages, UI strings.
- Glossary and binding style decisions: `src/content/i18n/ro/glossary.md`; LaTeX label table: `src/content/i18n/ro/latex_labels.tsv`.
- Mechanical checks already passed: tag skeleton, LaTeX, digit sequences, FAQ counts (`validate.py`), calculator results (`test_tools.js`), hreflang/canonical/sitemap/switcher (`hreflang_audit.py`), script purity (no wrong-variant letters or digits), no leftover English runs.

## How to review
Open `/ro/` and a few tool pages. Read the table below first (these are the pages' search-facing text), then 3 articles: `percentage-calculator`, `compound-interest-calculator`, `gpa-to-percentage-calculator` (mandatory per the content guide). Apply decisions to the glossary first, then to all 42 pages.

## Style decisions to confirm
- Register: informal-polite 2nd person singular ("Introdu", "Calculează"), no "dumneavoastră". Is this right for a financial/educational site?
- Percent attached (20%); comma-below diacritics only (ș ț).
- Numbers/decimal point/`$` as in English.

## Terms the translators flagged as uncertain
- APR → «DAE» (dobânda anuală efectivă, the term used in Romania) next to APR/APY acronyms; «randament anual efectiv» for APY
- markup → «adaos comercial»; baker's percentage → «procentul brutarului» (awkward as a keyword)
- principal → «Suma inițială» / «Capital»; end balance → «soldul final»
- slope tool: «Diferență de nivel / Distanță orizontală», «calculator de declivitate», «convertor de pantă», «calculator de ecuație a dreptei»
- growth tool named «Calculator rată de creștere» to avoid clashing with «creștere procentuală»
- w/v → «m/v, m/m»; «permiriad», «promil»; «bp» kept in English in the basis-point article vs «pb» in the glossary
- legal: «Despăgubiri» (Indemnification), «Separabilitate», «Declinarea garanțiilor»; «noi» defined inline because Romanian has no direct we/us/our
- loans: «plată finală mare (balloon)», «dobândă fixă pe suma inițială», «cei cinci C ai creditului», «rată lunară (EMI)»
- education: «Clasa I / Clasa a II-a / Promovat» for Indian bands, UK degree classes left in English, «percentilă», «clasa a 6-a»
- «reducere en-gros», «calculator de oferte», «depozit cu depuneri periodice», «livre»; «depreciere» in the car heading vs «amortizare» in the body
- food cost: «pass», «food truck», «fine dining» left as loanwords; «must de zahăr» (sugar wash), «malt liquor» left in English

## Static pages
- Legal pages (disclaimer, privacy policy, terms) were translated faithfully but have had no legal-language review.

## Tool names, titles and descriptions

| Slug | Nav name | Meta title | Meta description |
|---|---|---|---|
| `alcohol-proof-calculator` | Calculator grad alcoolic (proof în ABV) | Calculator grad alcoolic | Convertește proof în ABV (%) | Calculator gratuit pentru gradul alcoolic. Introdu o valoare proof (scara SUA) și o convertești instant în procent de alcool din volum (ABV) — rapid și precis. |
| `apr-apy-converter` | Convertor APR în APY | Convertor APR în APY | Randament anual efectiv (APY) | Convertor gratuit APR în APY. Introdu un APR și frecvența capitalizării pentru a vedea instant randamentul anual efectiv (APY) echivalent. |
| `apr-calculator` | Calculator APR (rata procentuală anuală) | Calculator APR | Rata procentuală anuală | Calculator APR gratuit. Convertește instant o rată a dobânzii periodice în rata procentuală anuală (APR) — modul standard de cotare a costului creditelor și cardurilor. |
| `apy-calculator` | Calculator APY (randament anual efectiv) | Calculator APY | Randament anual efectiv | Calculator APY gratuit. Convertește instant o rată nominală a dobânzii și frecvența capitalizării în randamentul anual efectiv (APY). |
| `average-percentage-calculator` | Calculator medie procente | Calculator medie procente | Medie simplă și ponderată | Calculator gratuit pentru media procentelor, în mod simplu și ponderat. Combină corect procente din grupuri de mărimi diferite, pentru note și sondaje. |
| `bakers-percentage-calculator` | Calculator procentul brutarului | Calculator procentul brutarului | Raporturi ingrediente | Calculator gratuit pentru procentul brutarului. Introdu greutatea făinii și a ingredientului pentru a calcula instant procentul brutarului al ingredientului. |
| `basis-points-calculator` | Calculator puncte de bază | Calculator puncte de bază | Puncte de bază în procente | Calculator gratuit pentru puncte de bază. Introdu o valoare în puncte de bază (pb) și o convertești instant în procent — rezultate precise pentru finanțe și trading. |
| `cgpa-to-percentage-calculator` | Calculator CGPA în procente | Calculator CGPA în procente | CGPA pe 10 puncte în % | Calculator gratuit CGPA în procente, cu formula standard CGPA x 9.5 pentru scala de 10 puncte. Convertește-ți CGPA în procente pentru evidențele universitare. |
| `commission-calculator` | Calculator comision | Calculator comision | Comisionul câștigat din vânzări | Calculator gratuit de comision. Introdu valoarea vânzărilor și rata comisionului pentru a calcula instant comisionul câștigat. |
| `compound-interest-calculator` | Calculator dobândă compusă | Calculator dobândă compusă | Creșterea în timp | Calculator gratuit de dobândă compusă. Introdu suma inițială, rata anuală, durata și frecvența capitalizării pentru a calcula dobânda și suma totală. |
| `decimal-to-percentage-calculator` | Calculator zecimal în procente | Calculator zecimal în procente | Convertește în % | Calculator gratuit zecimal în procente. Introdu orice număr zecimal și îl convertești instant în procent — rezultate precise pentru școală, muncă sau finanțe. |
| `depreciation-calculator` | Calculator amortizare | Calculator amortizare | Metoda liniară | Calculator gratuit de amortizare prin metoda liniară. Introdu costul activului, valoarea reziduală și durata de utilizare pentru a calcula amortizarea anuală. |
| `food-cost-percentage-calculator` | Calculator procentul costului alimentelor | Calculator costul alimentelor % | Costul unui preparat | Calculator gratuit pentru procentul costului alimentelor. Introdu costul ingredientelor și prețul din meniu pentru a calcula instant procentul costului unui preparat. |
| `fraction-to-percentage-calculator` | Calculator fracție în procente | Calculator fracție în procente | Convertește în procent | Calculator gratuit fracție în procente. Convertește instant orice fracție în procent — ideal pentru punctaje la teste, rapoarte și proporții. |
| `gpa-to-percentage-calculator` | Calculator GPA în procente | Calculator GPA în procente | Convertește GPA pe scala 4.0 | Calculator GPA în procente gratuit. Convertește instant GPA-ul pe scala 4.0 în procentul echivalent. Precis, simplu, fără înregistrare. |
| `gross-margin-calculator` | Calculator marjă brută | Calculator marjă brută | Calculează marja brută de profit % | Calculator de marjă brută gratuit. Introdu venitul și costul bunurilor vândute (COGS) pentru a calcula instant profitul brut și marja brută în procente. |
| `loan-interest-calculator` | Calculator dobândă credit | Calculator dobândă credit | Rată lunară și dobândă totală | Calculator de dobândă la credit gratuit. Introdu suma creditului, rata anuală și durata pentru a calcula instant rata lunară (EMI) și dobânda totală de plătit. |
| `marks-percentage-calculator` | Calculator procent din punctaj | Calculator procent note | Calculează procentul la examen | Calculator de procent din punctaj gratuit. Introdu punctajul obținut și punctajul total pentru a calcula instant procentul la examen sau la test. |
| `markup-calculator` | Calculator adaos comercial | Calculator adaos comercial | Preț de vânzare din cost + adaos % | Calculator de adaos comercial gratuit. Introdu prețul de cost și adaosul dorit în procente pentru a calcula instant prețul de vânzare pe care ar trebui să-l practici. |
| `percent-solution-calculator` | Calculator soluție procentuală | Calculator soluție procentuală | Concentrație masă/volum | Calculator de soluție procentuală gratuit. Introdu masa substanței dizolvate și volumul soluției pentru a calcula instant concentrația procentuală (% m/v). |
| `percentage-calculator` | Calculator procente | Calculator procente gratuit | Calculează procente rapid | Calculează procente instant cu calculatoarele noastre online gratuite. Instrumente simple pentru creștere, scădere, diferență și variație procentuală. |
| `percentage-change-calculator` | Calculator variație procentuală | Calculator variație procentuală | Creștere/scădere % | Calculator de variație procentuală gratuit. Calculează creșterea sau scăderea procentuală dintre două valori — urmărește evoluția acțiunilor și a prețurilor. |
| `percentage-decrease-calculator` | Calculator scădere procentuală | Calculator scădere procentuală | Scade un procent | Calculator de scădere procentuală gratuit. Scade instant orice procent dintr-un număr — calculează amortizarea, pierderea în greutate și reducerile bugetare. |
| `percentage-difference-calculator` | Calculator diferență procentuală | Calculator diferență procentuală | Compară două valori | Calculator de diferență procentuală gratuit. Compară două numere și află diferența procentuală. Folosește media ca bază pentru o comparație simetrică și corectă. |
| `percentage-error-calculator` | Calculator eroare procentuală | Calculator eroare procentuală | Eroarea procentuală în laborator | Calculator de eroare procentuală gratuit. Calculează eroarea procentuală dintre valorile experimentale și cele teoretice pentru laboratoare de fizică, chimie și biologie. |
| `percentage-growth-calculator` | Calculator rată de creștere | Calculator rată de creștere | Rata de creștere a afacerii | Calculator de rată de creștere gratuit. Calculează ratele de creștere ale veniturilor, clienților și vânzărilor. Urmărește performanța cu indicatori preciși. |
| `percentage-increase-calculator` | Calculator creștere procentuală | Calculator creștere procentuală | Adaugă un procent la un număr | Calculator de creștere procentuală gratuit. Adaugă instant orice procent la un număr. Calculează majorări salariale, adaosuri de preț, randamentul investițiilor și altele. |
| `percentage-of-a-percentage-calculator` | Calculator procent dintr-un procent | Calculator procent dintr-un procent | Combină două procente | Calculator de procent dintr-un procent gratuit. Înmulțește două procente succesive, apoi aplică rata combinată unei valori pentru taxe sau reduceri cumulate. |
| `percentage-off-calculator` | Calculator reducere procentuală | Calculator reducere procentuală | Preț redus și economie | Calculator gratuit de reducere procentuală. Află instant prețul redus și cât economisești. Calculează prețul final după orice reducere, ideal pentru oferte. |
| `percentage-point-calculator` | Calculator puncte procentuale | Calculator puncte procentuale | Diferența în puncte | Calculator gratuit de puncte procentuale. Introdu două procente și vezi instant diferența în puncte procentuale și variația procentuală relativă. |
| `percentile-to-percentage-calculator` | Calculator percentilă în procent | Calculator percentilă în procent | Estimare procent | Calculator gratuit percentilă în procent. Obține rapid un procent estimat dintr-o percentilă la examen, folosind o formulă de aproximare des întâlnită. |
| `ppm-to-percentage-calculator` | Calculator ppm în procent | Calculator ppm în procent | Convertor părți per milion | Calculator gratuit ppm în procent. Introdu o valoare în părți per milion (ppm) și convert-o instant în procent — precis pentru chimie și inginerie. |
| `profit-margin-calculator` | Calculator marjă de profit | Calculator marjă de profit | Calculează marja în % | Calculator gratuit de marjă de profit. Introdu prețul de cost și prețul de vânzare și calculează instant profitul și marja de profit în procente din prețul de vânzare. |
| `profit-percentage-calculator` | Calculator procent de profit | Calculator procent de profit | Profit în % din cost | Calculator gratuit de procent de profit. Introdu prețul de cost și prețul de vânzare și calculează instant suma profitului și procentul de profit. |
| `ratio-to-percentage-calculator` | Calculator raport în procent | Calculator raport în procent | Convertește raportul în % | Calculator gratuit raport în procent. Introdu cele două părți ale unui raport și vezi instant totalul și ce procent reprezintă prima parte. |
| `reverse-percentage-calculator` | Calculator procent invers | Calculator procent invers | Află numărul inițial | Calculator gratuit de procent invers. Află numărul inițial când cunoști o valoare și procentul ei — calculează, de exemplu, prețul de dinainte de reducere. |
| `salary-increase-calculator` | Calculator majorare salarială | Calculator majorare salarială | Salariul tău nou | Calculator gratuit de majorare salarială. Introdu salariul actual și procentul de majorare și calculează instant suma majorării și noul salariu. |
| `sgpa-to-percentage-calculator` | Calculator SGPA în procent | Calculator SGPA în procent | Convertește SGPA în % | Calculator gratuit SGPA în procent, cu formula standard SGPA × 9.5. Convertește instant media semestrială SGPA într-un procent echivalent. |
| `simple-interest-calculator` | Calculator dobândă simplă | Calculator dobândă simplă | Dobândă și sumă totală | Calculator gratuit de dobândă simplă. Introdu capitalul, rata anuală și perioada pentru a calcula instant dobânda obținută și suma totală. |
| `slope-percentage-calculator` | Calculator pantă în procente | Calculator pantă în procente | Înălțime/distanță în % | Calculator gratuit de pantă în procente. Introdu diferența de nivel și distanța orizontală pentru a calcula instant panta în procente și unghiul echivalent în grade. |
| `tip-calculator` | Calculator bacșiș | Calculator bacșiș | Calculează bacșișul și împarte nota | Calculator gratuit de bacșiș. Introdu nota de plată, procentul de bacșiș și numărul de persoane pentru a afla instant bacșișul, totalul și suma pe persoană. |
| `win-loss-percentage-calculator` | Calculator procent victorii/înfrângeri | Calculator procent victorii/înfrângeri | Rata de câștig | Calculator gratuit de procent victorii/înfrângeri. Introdu victoriile, înfrângerile și egalurile pentru a calcula instant procentul de câștig la orice sport sau joc. |
