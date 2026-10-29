# Native review sheet: Polish (`pl`)

Status: **not yet reviewed by a native speaker.** Everything below was written and self-reviewed by Claude. This sheet lists what needs a human decision.

## Scope
- 42 tool pages (title, description, H1, subtitle, hint, card labels/placeholders), 42 articles (about 59,994 words), 11 FAQ sets (127 Q&A), 6 static pages, UI strings.
- Glossary and binding style decisions: `src/content/i18n/pl/glossary.md`; LaTeX label table: `src/content/i18n/pl/latex_labels.tsv`.
- Mechanical checks already passed: tag skeleton, LaTeX, digit sequences, FAQ counts (`validate.py`), calculator results (`test_tools.js`), hreflang/canonical/sitemap/switcher (`hreflang_audit.py`), script purity (no wrong-variant letters or digits), no leftover English runs.

## How to review
Open `/pl/` and a few tool pages. Read the table below first (these are the pages' search-facing text), then 3 articles: `percentage-calculator`, `compound-interest-calculator`, `gpa-to-percentage-calculator` (mandatory per the content guide). Apply decisions to the glossary first, then to all 42 pages.

## Style decisions to confirm
- Register: impersonal/neutral, reader addressed as "Ty" only when needed; no Pan/Pani.
- Percent attached to digits (20%); numbers, decimal point, thousands comma and `$` kept exactly as in English so they match the calculator output.
- Quotation marks „…”.

## Terms the translators flagged as uncertain
- APR → «RRSO» (consumer-credit term; strictly the effective rate incl. fees), APY → «efektywna roczna stopa zwrotu»
- depreciation → «amortyzacja» everywhere (alternative «utrata wartości»), including insurance-claim context
- win/loss rate: «procent wygranych» vs «współczynnik wygranych»
- tool names: «Kalkulator odsetek składanych», «Kalkulator tempa wzrostu» (growth) vs «wzrostu procentowego» (increase), «Odwrotny kalkulator procentowy», «Kalkulator proporcji na procenty»
- w/v → «m/v», «procent masowo-objętościowy»
- commission glossary: left as loanwords draw/quota/clawback/SPIFF/OTE; «zaliczka na poczet prowizji»; «doradca handlowy» for Account Executive
- savings terms: «lokata cykliczna», «certyfikat depozytowy», «godziny kredytowe», «liczba pacjentów, których trzeba leczyć», «dziesięciotysięczna» (permyriad)
- baking: «procent piekarski», «uwodnienie», «przedferment», «procent łączny»
- «kapitalizacja» (compounding), «rata amortyzowana», «pożyczka gotówkowa», «Matura Międzynarodowa» (IB)
- Indian degree bands «Pierwsza klasa / Druga klasa / Zaliczenie», «wyciąg ocen», «NWD» (GCF); UK honours terms left in English
- alcohol: «nastaw cukrowy», «surówka» (low wines), «piwo słodowe o wysokiej mocy», «wynik Copelanda»; «games behind», «passer rating», «term sheet» left in English
- About page uses neutral forms; «Zwolnienie z odpowiedzialności» for Indemnification; ratio page article now says 1:2 = 33.3% (English fixed)

## Static pages
- Legal pages (disclaimer, privacy policy, terms) were translated faithfully but have had no legal-language review.

## Tool names, titles and descriptions

| Slug | Nav name | Meta title | Meta description |
|---|---|---|---|
| `alcohol-proof-calculator` | Kalkulator mocy alkoholu (proof na ABV) | Kalkulator mocy alkoholu proof | Przelicz proof na % ABV | Darmowy kalkulator mocy alkoholu. Wpisz wartość w skali proof (USA), aby od razu przeliczyć ją na zawartość alkoholu w procentach objętościowych (ABV) — szybko i dokładnie. |
| `apr-apy-converter` | Przelicznik RRSO na APY | Przelicznik RRSO na APY | Efektywna roczna stopa zwrotu | Darmowy przelicznik RRSO na APY. Wpisz RRSO i częstotliwość kapitalizacji, aby od razu zobaczyć równoważną efektywną roczną stopę zwrotu (APY). |
| `apr-calculator` | Kalkulator RRSO | Kalkulator RRSO | Rzeczywista roczna stopa oprocentowania | Darmowy kalkulator RRSO. Przelicz stopę oprocentowania za okres na roczną stopę procentową (RRSO) — standardowy sposób podawania kosztu kredytów i kart kredytowych. |
| `apy-calculator` | Kalkulator APY | Kalkulator APY | Efektywna roczna stopa zwrotu | Darmowy kalkulator APY. Przelicz nominalną stopę oprocentowania i częstotliwość kapitalizacji na efektywną roczną stopę zwrotu (APY) w jednej chwili. |
| `average-percentage-calculator` | Kalkulator średniej procentowej | Kalkulator średniej procentowej | Średnia prosta i ważona | Darmowy kalkulator średniej procentowej z trybem prostym i ważonym. Poprawnie łącz procenty z grup o różnej liczebności, np. przy ocenach i ankietach. |
| `bakers-percentage-calculator` | Kalkulator procentu piekarskiego | Kalkulator procentu piekarskiego | Proporcje składników | Darmowy kalkulator procentu piekarskiego. Wpisz masę mąki i masę składnika, aby od razu obliczyć jego procent piekarski. |
| `basis-points-calculator` | Kalkulator punktów bazowych | Kalkulator punktów bazowych | Przelicz pb na procent | Darmowy kalkulator punktów bazowych. Wpisz wartość w punktach bazowych (pb), aby od razu przeliczyć ją na procent — dokładne wyniki dla finansów i inwestowania. |
| `cgpa-to-percentage-calculator` | Kalkulator CGPA na procent | Kalkulator CGPA na procent | Przelicz CGPA (skala 10) na % | Darmowy kalkulator CGPA na procent według standardowego wzoru CGPA x 9.5 (skala 10-punktowa). Przelicz CGPA na procent na potrzeby dokumentów uczelni. |
| `commission-calculator` | Kalkulator prowizji | Kalkulator prowizji | Oblicz prowizję od sprzedaży | Darmowy kalkulator prowizji. Wpisz kwotę sprzedaży i stawkę prowizji, aby od razu obliczyć, ile prowizji zarobiłeś. |
| `compound-interest-calculator` | Kalkulator odsetek składanych | Kalkulator odsetek składanych | Oblicz wzrost w czasie | Darmowy kalkulator odsetek składanych. Wpisz kapitał, roczną stopę, czas i częstotliwość kapitalizacji, aby od razu obliczyć odsetki i łączną kwotę. |
| `decimal-to-percentage-calculator` | Kalkulator liczby dziesiętnej na procent | Kalkulator liczby dziesiętnej na procent | Zamień na % | Darmowy kalkulator zamiany liczby dziesiętnej na procent. Wpisz dowolną liczbę dziesiętną, aby od razu zamienić ją na procent — dokładnie do szkoły, pracy i finansów. |
| `depreciation-calculator` | Kalkulator amortyzacji | Kalkulator amortyzacji | Metoda liniowa | Darmowy kalkulator amortyzacji metodą liniową. Wpisz koszt środka trwałego, wartość końcową i okres użytkowania, aby obliczyć roczny odpis amortyzacyjny. |
| `food-cost-percentage-calculator` | Kalkulator food cost (koszt żywności w %) | Kalkulator food cost | Oblicz procent kosztu dania | Darmowy kalkulator food cost. Wpisz koszt składników i cenę w menu, aby od razu obliczyć procentowy koszt żywności dla danej pozycji menu. |
| `fraction-to-percentage-calculator` | Kalkulator ułamka na procent | Kalkulator ułamka na procent | Zamień ułamek na % | Darmowy kalkulator ułamka na procent. Zamień dowolny ułamek na procent w jednej chwili — idealny do wyników testów, proporcji i stosunków. |
| `gpa-to-percentage-calculator` | Kalkulator GPA na procenty | Kalkulator GPA na procenty | Przelicz GPA w skali 4.0 na % | Darmowy kalkulator GPA na procenty. Przelicz swoją średnią ocen GPA w skali 4.0 na odpowiadający jej procent od razu. Dokładnie, prosto, bez rejestracji. |
| `gross-margin-calculator` | Kalkulator marży brutto | Kalkulator marży brutto | Oblicz marżę zysku brutto w % | Darmowy kalkulator marży brutto. Wpisz przychody i koszt własny sprzedanych towarów (COGS), aby od razu obliczyć zysk brutto i procentową marżę brutto. |
| `loan-interest-calculator` | Kalkulator odsetek od kredytu | Kalkulator odsetek od kredytu | Rata miesięczna i odsetki | Darmowy kalkulator odsetek od kredytu. Wpisz kwotę, roczne oprocentowanie i okres spłaty, aby od razu obliczyć miesięczną ratę (EMI) i łączne odsetki do zapłaty. |
| `marks-percentage-calculator` | Kalkulator procentu punktów | Kalkulator procentu punktów | Oblicz wynik egzaminu w % | Darmowy kalkulator procentu punktów. Wpisz uzyskane i maksymalne punkty, aby od razu obliczyć swój wynik z egzaminu lub sprawdzianu w procentach. |
| `markup-calculator` | Kalkulator narzutu | Kalkulator narzutu | Cena sprzedaży z kosztu i narzutu % | Darmowy kalkulator narzutu. Wpisz cenę zakupu i oczekiwany narzut procentowy, aby od razu obliczyć cenę sprzedaży, którą powinieneś zastosować. |
| `percent-solution-calculator` | Kalkulator roztworu procentowego | Kalkulator roztworu procentowego | Stężenie masa/objętość | Darmowy kalkulator roztworu procentowego. Wpisz masę substancji rozpuszczonej i objętość roztworu, aby od razu obliczyć stężenie procentowe (% m/v). |
| `percentage-calculator` | Kalkulator procentowy | Kalkulator procentowy online | Szybkie obliczanie procentów | Obliczaj procenty od razu dzięki naszym darmowym kalkulatorom procentowym online. Proste narzędzia do wzrostu, spadku, różnicy i zmiany procentowej. |
| `percentage-change-calculator` | Kalkulator zmiany procentowej | Kalkulator zmiany procentowej | Wzrost i spadek w % | Darmowy kalkulator zmiany procentowej. Oblicz wzrost lub spadek procentowy między dwiema wartościami — śledź zmiany kursów akcji i cen. |
| `percentage-decrease-calculator` | Kalkulator spadku procentowego | Kalkulator spadku procentowego | Odejmij procent od liczby | Darmowy kalkulator spadku procentowego. Odejmij dowolny procent od liczby od razu — oblicz utratę wartości, spadek wagi i cięcia budżetu. |
| `percentage-difference-calculator` | Kalkulator różnicy procentowej | Kalkulator różnicy procentowej | Porównaj dwie wartości | Darmowy kalkulator różnicy procentowej. Porównaj dwie liczby i oblicz różnicę procentową. Jako podstawy używa średniej, co daje symetryczne, bezstronne porównanie. |
| `percentage-error-calculator` | Kalkulator błędu procentowego | Kalkulator błędu procentowego | Błąd względny w laboratorium | Darmowy kalkulator błędu procentowego. Oblicz błąd procentowy między wartością doświadczalną a teoretyczną w laboratoriach fizyki, chemii i biologii. |
| `percentage-growth-calculator` | Kalkulator tempa wzrostu | Kalkulator tempa wzrostu | Wzrost firmy i przychodów w % | Darmowy kalkulator wzrostu procentowego. Oblicz tempo wzrostu przychodów, klientów, sprzedaży i wskaźników KPI. Śledź wyniki firmy dzięki dokładnym miarom. |
| `percentage-increase-calculator` | Kalkulator wzrostu procentowego | Kalkulator wzrostu procentowego | Dodaj procent do liczby | Darmowy kalkulator wzrostu procentowego. Dodaj dowolny procent do liczby od razu. Oblicz podwyżki, narzuty cenowe, zyski z inwestycji i więcej. |
| `percentage-of-a-percentage-calculator` | Kalkulator procentu z procentu | Kalkulator procentu z procentu | Połącz dwa procenty | Darmowy kalkulator procentu z procentu. Pomnóż dwa kolejne procenty, a potem zastosuj łączną stawkę do wartości, np. przy łączeniu podatków lub rabatów. |
| `percentage-off-calculator` | Kalkulator zniżki procentowej | Kalkulator zniżki procentowej | Cena po rabacie i oszczędność | Darmowy kalkulator zniżki procentowej. Oblicz cenę po rabacie i kwotę oszczędności w kilka sekund. Sprawdź, ile zapłacisz po przecenie, i kupuj mądrzej. |
| `percentage-point-calculator` | Kalkulator punktów procentowych | Kalkulator punktów procentowych | Różnica w punktach | Darmowy kalkulator punktów procentowych. Wpisz dwa procenty, aby od razu zobaczyć różnicę w punktach procentowych oraz względną zmianę procentową. |
| `percentile-to-percentage-calculator` | Kalkulator percentyla na procent | Kalkulator percentyla na procent | Szacowany wynik w % | Darmowy kalkulator percentyla na procent. Szybko oszacuj wynik procentowy na podstawie percentyla z egzaminu, korzystając z powszechnie stosowanego wzoru przybliżonego. |
| `ppm-to-percentage-calculator` | Kalkulator ppm na procent | Kalkulator ppm na procent | Przelicz części na milion | Darmowy kalkulator ppm na procent. Wpisz wartość w częściach na milion (ppm), aby od razu zamienić ją na procent — dokładnie, do chemii i inżynierii. |
| `profit-margin-calculator` | Kalkulator marży zysku | Kalkulator marży zysku | Oblicz marżę zysku w % | Darmowy kalkulator marży zysku. Wpisz cenę zakupu i cenę sprzedaży, aby od razu obliczyć zysk oraz marżę zysku jako procent ceny sprzedaży. |
| `profit-percentage-calculator` | Kalkulator procentu zysku | Kalkulator procentu zysku | Oblicz zysk w % od kosztu | Darmowy kalkulator procentu zysku. Wpisz cenę zakupu i cenę sprzedaży, aby od razu obliczyć kwotę zysku oraz procent zysku. |
| `ratio-to-percentage-calculator` | Kalkulator proporcji na procent | Kalkulator proporcji na procent | Zamień stosunek na % | Darmowy kalkulator proporcji na procent. Wpisz obie części stosunku, aby od razu zobaczyć sumę i jaki procent stanowi pierwsza część. |
| `reverse-percentage-calculator` | Odwrotny kalkulator procentowy | Odwrotny kalkulator procentowy | Znajdź wartość początkową | Darmowy odwrotny kalkulator procentowy. Znajdź liczbę początkową, gdy znasz wartość i jej procent — oblicz cenę przed rabatem i nie tylko. |
| `salary-increase-calculator` | Kalkulator podwyżki wynagrodzenia | Kalkulator podwyżki wynagrodzenia | Nowa pensja | Darmowy kalkulator podwyżki wynagrodzenia. Wpisz obecną pensję i procent podwyżki, aby od razu obliczyć kwotę podwyżki i nowe wynagrodzenie. |
| `sgpa-to-percentage-calculator` | Kalkulator SGPA na procent | Kalkulator SGPA na procent | Przelicz SGPA na procent | Darmowy kalkulator SGPA na procent według standardowego wzoru SGPA × 9.5. Od razu przelicz semestralną średnią SGPA na równoważny procent. |
| `simple-interest-calculator` | Kalkulator odsetek prostych | Kalkulator odsetek prostych | Odsetki i kwota końcowa | Darmowy kalkulator odsetek prostych. Wpisz kapitał, roczną stopę i czas, aby od razu obliczyć odsetki i kwotę końcową. |
| `slope-percentage-calculator` | Kalkulator nachylenia w procentach | Kalkulator nachylenia w procentach | Spadek i kąt | Darmowy kalkulator nachylenia w procentach. Wpisz wzniesienie i odległość poziomą, aby od razu obliczyć nachylenie w % i równoważny kąt w stopniach. |
| `tip-calculator` | Kalkulator napiwku | Kalkulator napiwku | Oblicz napiwek i podziel rachunek | Darmowy kalkulator napiwku. Wpisz kwotę rachunku, procent napiwku i liczbę osób, aby od razu obliczyć napiwek, sumę i kwotę na osobę. |
| `win-loss-percentage-calculator` | Kalkulator procentu wygranych i porażek | Kalkulator procentu wygranych | Oblicz współczynnik wygranych | Darmowy kalkulator procentu wygranych i porażek. Wpisz wygrane, porażki i remisy, aby od razu obliczyć procent wygranych w sporcie, grze lub rywalizacji. |
