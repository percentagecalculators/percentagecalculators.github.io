# Ukrainian (uk) glossary for articles and FAQs

Decisions (made 2026-10-29):
- Address: `ви` (lower case), neutral instructional register; imperative for actions (`Введіть`, `Натисніть`), impersonal where possible. Headings in sentence case; question headings end with `?`.
- Ukrainian, not Russian: never calque from ru. Use і/ї/є/ґ correctly, the apostrophe `’` (U+2019) as in `зв’язок`, `м’ясо`; avoid Russianisms (`процентний` only in fixed terms, prefer `відсотковий`; `розрахунок/обчислення`, not `калькуляція`).
- Numbers, decimal point, thousands comma and `$` stay as in English (12.5 %, $1,250), matching calculator output and the validator.
- Percent: as in ru, a space before `%` (20 %); in articles `add_content.py` can convert a plain space to a non-breaking one, so write `20 %` with a plain space. In first-pass strings follow ru: `X %` with a space.
- Quotation marks: «…» (nested „…“).
- Plurals: correct forms (1 відсоток, 2 відсотки, 5 відсотків); where the count is a variable, rephrase or use the genitive plural.
- Latin acronyms kept and glossed (APR, APY, GPA, CGPA, SGPA, ppm).
- Reuse first-pass nav names and h1s (Калькулятор …).

| English | Ukrainian (use this) | Notes |
|---|---|---|
| calculator | калькулятор | |
| percentage / percent / % | відсоток (відсотки) / знак відсотка | search term: `калькулятор відсотків` |
| percentage change / increase / decrease | зміна / збільшення / зменшення у відсотках | matches nav |
| percentage difference / error | відсоткова різниця / відсоткова похибка | `відносна похибка` allowed in text |
| percentage point | відсотковий пункт (в. п.) | |
| reverse percentage | зворотний відсоток | |
| discount, discounted price | знижка, ціна зі знижкою | |
| markup / margin | націнка / маржа | |
| profit | прибуток | gross/net: валовий / чистий |
| cost price | собівартість | |
| commission / tip | комісія / чайові | tip is US-attributed |
| salary / raise | зарплата / підвищення зарплати | |
| simple / compound interest | прості відсотки / складні відсотки | |
| interest rate | відсоткова ставка | |
| loan | кредит, позика | `кредит` in titles |
| APR / APY | APR (річна відсоткова ставка) / APY (ефективна річна дохідність) | acronyms kept |
| basis point | базисний пункт (б. п.) | |
| ppm | ppm (частин на мільйон) | |
| GPA / CGPA / SGPA | GPA / CGPA (накопичувальний GPA) / SGPA (GPA за семестр) | |
| marks / grade | бали / оцінка | |
| percentile | процентиль | |
| ratio / fraction / decimal | співвідношення / дріб / десятковий дріб | |
| depreciation | амортизація | |
| slope / grade (road) | ухил | |
| alcohol proof | міцність (proof) алкоголю | US proof scale stays US |
| baker's percentage | відсотки пекаря | as in nav |
| food cost | фудкост (відсоток собівартості страви) | |
| win/loss rate | відсоток перемог і поразок | |
| solution concentration | концентрація розчину | |

Open for review: no native reviewer yet.
