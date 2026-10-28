# German (de) glossary for articles and FAQs

Decisions (made 2026-10-28):
- Variety: standard German for Germany/Austria/Switzerland (no regional forms; Swiss ß-less spelling not used).
- Address: formal `Sie` (capitalised), impersonal where possible. Headings in German sentence case (nouns capitalised, no title case); question headings end with `?`.
- Compound nouns are written solid (Zinseszinsrechner) or with hyphens only when needed for readability (APR-Rechner).
- Numbers, decimal point, thousands comma and `$` stay as in English (they match the calculator output and the validator): 12.5 %, $1,250, never 12,5 or 1.250. `$` goes before the number as in English.
- Percent: `20 %` with a non-breaking space (DIN 5008), applied automatically by `add_content.py`; write plain spaces. "Prozent" in running text.
- Quotation marks: „…“ (low-high), never "…".
- Reuse the first-pass nav names and h1s (…rechner).

| English | German (use this) | Notes |
|---|---|---|
| percentage / percent sign | Prozentsatz, Prozent / Prozentzeichen (%) | "Prozentwert" for the computed part |
| percentage change / increase / decrease | prozentuale Veränderung / Erhöhung / Verminderung | matches nav |
| percentage difference / error | prozentuale Differenz / prozentualer Fehler | |
| percentage point | Prozentpunkt | |
| reverse percentage | umgekehrte Prozentrechnung | |
| discount, discounted price | Rabatt, reduzierter Preis (Preis nach Rabatt) | |
| markup / margin | Aufschlag (markup) / Marge | nav says "Aufschlag" |
| profit | Gewinn | gross/net: Bruttomarge, Nettogewinn |
| cost price | Einkaufspreis / Selbstkosten | |
| commission / tip | Provision / Trinkgeld | |
| VAT / sales tax | Mehrwertsteuer (MwSt.) / Sales Tax (Umsatzsteuer in den USA) | sales tax stays attributed to the US |
| compound / simple interest | Zinseszins / einfache Zinsen | |
| principal | Kapital | |
| interest rate | Zinssatz (nominal: Nominalzins) | |
| compounding frequency | Verzinsungshäufigkeit | |
| future / present value | Endwert / Barwert | |
| APY / effective annual rate | effektiver Jahreszins (APY) / effektiver Jahreszins | |
| rate of return, RoR, TWR | Rendite, RoR, zeitgewichtete Rendite (TWR) | |
| GPA / CGPA / SGPA | GPA / CGPA (kumulierter GPA) / SGPA (Semester-GPA) | acronyms kept |
| grading scale, letter grade | Notenskala, Buchstabennote | |
| weighted / unweighted | gewichtet / ungewichtet | |
| credit hours | Credits | |
| food cost | Wareneinsatz | as in nav |
| depreciation | Abschreibung | as in nav |
| COGS | COGS (Herstellungskosten bzw. Wareneinsatz) | glossed once |
| proof, ABV | Proof, ABV (Alkoholgehalt in Vol.-%) | |
| baker's percentage | Bäckerprozent | |
| ratio / fraction / decimal | Verhältnis / Bruch / Dezimalzahl | |
| cost of goods | Warenkosten / Wareneinsatz | Wareneinsatz for the percentage |
| gross profit | Rohertrag | |
| hydration (baking) | Teigausbeute | |
| accelerator / draw / clawback | Beschleuniger / Vorschuss auf die Provision / Clawback | |
| Dollar amounts | `$` before the number, as in English ($1,250) | |

Open for review: APR/APY labels differ between articles (apr-calculator: "effektiver Jahreszins (APR)", which is the German legal usage; apr-apy-converter and apy-calculator: "Nominalzins (APR)" / "effektiver Jahreszins" or "Jahresrendite (APY)"). Pick one pair site-wide.
The win-loss nav name ("Siegquoten-Rechner") differs from its h1 ("Sieg-Niederlage-Prozent-Rechner").
