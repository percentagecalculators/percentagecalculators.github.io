# Turkish (tr) glossary for articles and FAQs

Decisions (made 2026-10-29):
- Variety: standard Turkey Turkish. Terms are the ones users in Turkey type into a search box (yüzde hesaplama, yüzde hesaplama aracı, indirim hesaplama, yüzde artış hesaplama).
- Address: neutral instructional register, "siz"-form or impersonal. Imperative with the polite plural ("Girin", "Seçin", "Hesaplayın"), never "gir"/"hesapla" (except the button label "Hesapla"). Avoid "sen". Headings in sentence case; question headings end with `?`. Tool names: "… Hesaplama" / "… Hesaplayıcı" as in nav; "hesap makinesi" only for a generic calculator device.
- Numbers, decimal point, thousands comma and `$` stay as in English (they match the calculator output and the validator): 12.5, $1,250, never 12,5 or 1.250. `$` goes before the number.
- Percent sign: Turkish normally writes the sign BEFORE the number (%20). Decision: in prose and formulas write `%20`, `%12.5` (prefix, no space) because the digit sequence is unchanged, so number validation is unaffected. The calculator outputs and card values keep the English `20%` form (JS output); do not touch those. Never add a space after `%`. Word form: "yüzde 20" is fine in running text when the digits are kept.
- Suffixes after digits: use an apostrophe + vowel-harmony suffix only when unavoidable ("%20'si"); prefer rewording ("sayının %20 değeri") to avoid wrong harmony.
- Casing: Turkish has dotted/dotless i. Dotted İ/i and dotless I/ı are different letters: capital of i is İ, lowercase of I is ı ("IŞIK", "İNDİRİM"). Never use Python `.upper()/.lower()`/`.title()` on Turkish text; write capitals by hand. Pages carry `lang="tr"` so CSS uppercase is correct. Sentence case for headings.
- Quotation marks: “…”.
- Reuse the first-pass nav names and h1s.

| English | Turkish (use this) | Notes |
|---|---|---|
| percentage / percent / percent sign | yüzde / yüzde / yüzde işareti (%) | "yüzde hesaplama" is the search term |
| percentage change / increase / decrease | yüzde değişim / yüzde artış / yüzde azalış | matches nav |
| percentage difference / error | yüzde fark / yüzde hata | |
| percentage point | yüzde puanı | not "yüzde noktası" |
| reverse percentage | ters yüzde | |
| discount, discounted price | indirim, indirimli fiyat | "yüzde indirim hesaplama" |
| markup / margin | maliyet üzeri kâr (markup) / kâr marjı | gloss "markup" once |
| profit | kâr | gross/net: brüt/net kâr; brüt marj |
| cost price | maliyet fiyatı | |
| commission / tip | komisyon / bahşiş | US tipping norms stay attributed to the US |
| VAT / sales tax | KDV / satış vergisi (ABD) | |
| compound / simple interest | bileşik faiz / basit faiz | |
| principal / interest rate | anapara / faiz oranı | |
| loan | kredi | "kredi faizi" |
| future / present value | gelecek değer / bugünkü değer | |
| APY / APR | APY (yıllık getiri) / APR (yıllık oran) | acronyms kept |
| basis point | baz puan | |
| ppm | ppm (milyonda bir parça) | |
| GPA / CGPA / SGPA | GPA / CGPA (genel ortalama) / SGPA (dönem ortalaması) | acronyms kept; SGPA stays attributed to India |
| marks, grade | not, harf notu | |
| percentile | yüzdelik dilim | |
| ratio / fraction / decimal | oran / kesir / ondalık sayı | |
| depreciation | amortisman | |
| salary increase | maaş zammı | |
| growth | büyüme | |
| food cost | gıda maliyeti | |
| baker's percentage | fırıncı yüzdesi | |
| alcohol proof | alkol derecesi (proof) | US proof scale stays attributed to the US |
| slope / grade | eğim | "yüzde eğim" |
| win/loss rate | galibiyet/mağlubiyet oranı | |
| solution concentration | çözelti derişimi | |
| average | ortalama | |
| calculator | hesaplama / hesaplayıcı | tool names; "hesap makinesi" for a physical calculator |

Open for review: no native reviewer yet.
