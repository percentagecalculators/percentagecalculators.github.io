# Persian / Farsi (fa) glossary for articles and FAQs

Decisions (made 2026-10-29):
- Variety: standard Iranian Persian (فارسی ایران), written, neutral; RTL page. Search terms real users type in Iran: «ماشین حساب درصد», «محاسبه درصد».
- Register: neutral, instructional, formal-polite. Address with «شما» or impersonal constructions («وارد کنید», «می‌توانید», «کافی است…»). No colloquial contractions.
- Digits: Western digits (0-9), decimal point `.` and thousands comma `,` exactly as in English (1,250, 12.5) — they match the calculator output and the validator. Never Persian digits (۰-۹), never `٫` or `٬`. `$` stays before the number.
- Percent: `%` attached after the number (20%). Prose: «درصد»; «علامت درصد» for the sign.
- Letters: Persian ی and ک only (never Arabic ي / ك). Use ZWNJ (نیم‌فاصله, U+200C) in compounds and verb prefixes: می‌شود, ماشین‌حساب‌ها, پرسش‌های, بازنشانی‌شده. «ماشین حساب» (spaced) in titles/nav as searched; «ماشین‌حساب» with ZWNJ acceptable in running prose, but stay consistent per page.
- Punctuation: Persian comma `،`, semicolon `؛`, question mark `؟`; guillemets «…» for quotation. Not inside formulas/LaTeX.
- Latin acronyms (APR, APY, GPA, CGPA, SGPA, ppm, ABV, COGS, ROI) stay in Latin letters, glossed in Persian at first use. Formulas, numbers and `<output>` render LTR.
- FAQ label «Q.» is «پ.» (UI string faq_q_label). Question headings end with `؟`.
- Facts about countries stay attributed (US tipping, US proof scale, Indian SGPA, US sales tax).

| English | Persian (use this) | Notes |
|---|---|---|
| calculator | ماشین حساب | nav/h1 pattern: «ماشین حساب …» |
| percentage / percent | درصد | |
| percentage point | واحد درصد | not «نقطه درصد» |
| percentage change / increase / decrease | تغییر درصدی / افزایش درصدی / کاهش درصدی | |
| percentage difference / error | تفاوت درصدی / خطای درصدی | |
| reverse percentage | درصد معکوس | |
| discount, discounted price | تخفیف، قیمت پس از تخفیف | |
| markup / margin | مارک‌آپ (درصد سود نسبت به هزینه) / حاشیه سود | gloss Markup in Latin at first use |
| profit | سود | gross/net: سود ناخالص / سود خالص |
| cost price | قیمت تمام‌شده | |
| commission / tip | کمیسیون (پورسانت) / انعام | |
| salary | حقوق | raise: افزایش حقوق |
| interest simple / compound | بهره ساده / بهره مرکب | rate: نرخ بهره |
| loan | وام | |
| principal | اصل پول (سرمایه) | |
| APR / APY | APR (نرخ درصد سالانه) / APY (بازده درصدی سالانه) | acronyms kept |
| basis point | واحد پایه (bp) | 1 bp = 0.01% |
| ppm | ppm (قسمت در میلیون) | |
| GPA / CGPA / SGPA | GPA / CGPA (معدل کل) / SGPA (معدل نیم‌سال) | |
| marks, percentile | نمره، صدک | |
| ratio / fraction / decimal | نسبت / کسر / عدد اعشاری | |
| depreciation | استهلاک | |
| proof (alcohol) | پروف (Proof) | ABV: درصد الکل (ABV) |
| slope / grade | شیب / درصد شیب | |
| baker's percentage | درصد نانوا | |
| food cost | هزینه مواد غذایی | |
| win/loss rate | نرخ برد و باخت | |
| solution concentration | غلظت محلول | percent solution: محلول درصدی |
| growth | رشد | |

Open for review: no native reviewer yet.
