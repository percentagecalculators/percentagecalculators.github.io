# Russian (ru) glossary for articles and FAQs

Decisions (made 2026-10-28):
- Address: `вы` (lower case, polite, impersonal where possible), not `ты`. Headings in sentence case; question headings end with `?`.
- Numbers, decimal point, thousands comma and `$` stay as in English (they match the calculator output and the validator): 12.5 %, $1,250. First-pass `4,0`/`9,5` in the GPA/CGPA/SGPA files were corrected to `4.0`/`9.5`.
- Percent: Russian typography puts a non-breaking space before `%` (20 %); `add_content.py` converts a normal space automatically, so write `20 %` with a plain space.
- Quotation marks: «…».
- Plurals: use correct forms (1 процент, 2 процента, 5 процентов); where the count is a variable, rephrase (`процентов: 5`) or use the genitive plural.
- Latin acronyms kept and glossed (APR, APY, GPA, CGPA, SGPA, ppm).
- Reuse first-pass nav names and h1s (Калькулятор …).

| English | Russian (use this) | Notes |
|---|---|---|
| percentage / percent sign | процент / знак процента (%) | |
| percentage change / increase / decrease | изменение / увеличение / уменьшение в процентах | matches nav |
| percentage difference / error | процентная разница / процентная ошибка | nav; text may say относительная погрешность |
| percentage point | процентный пункт (п. п.) | |
| reverse percentage | обратный процент | |
| discount, discounted price | скидка, цена со скидкой | |
| markup / margin | наценка / маржа | |
| profit | прибыль | gross/net: валовая / чистая |
| cost price | себестоимость | |
| commission / tip | комиссия / чаевые | |
| VAT / sales tax | НДС / налог с продаж (в США) | US attribution kept |
| compound / simple interest | сложные проценты / простые проценты | |
| principal | основная сумма (тело кредита/вклада) | |
| interest rate | процентная ставка | |
| compounding frequency | частота капитализации | |
| future / present value | будущая / приведённая (текущая) стоимость | |
| APY / APR | APY (эффективная годовая доходность) / APR (годовая процентная ставка) | acronyms kept |
| rate of return | доходность | |
| GPA / CGPA / SGPA | GPA / CGPA (накопленный GPA) / SGPA (GPA за семестр) | |
| grading scale, letter grade | шкала оценок, буквенная оценка | |
| weighted / unweighted | взвешенный / невзвешенный | |
| credit hours | кредиты (зачётные единицы) | |
| food cost | фудкост (процент себестоимости блюда) | as in nav |
| depreciation | амортизация | |
| COGS | себестоимость продаж (COGS) | |
| baker's percentage | процент пекаря | as in nav |
| ratio / fraction / decimal | отношение / дробь / десятичная дробь | |
| hydration (baking) | гидратация (доля воды) | |

## Open for review (self-review by Claude, no native reviewer)

- `вы` vs. more informal tone; plural phrasing around digits was reworded to satisfy the digit check.
- Indian CGPA/SGPA classification and US-specific terms are rendered descriptively.
