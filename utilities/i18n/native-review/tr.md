# Native review sheet: Turkish (`tr`)

Status: **not yet reviewed by a native speaker.** Everything below was written and self-reviewed by Claude. This sheet lists what needs a human decision.

## Scope
- 42 tool pages (title, description, H1, subtitle, hint, card labels/placeholders), 42 articles (about 55,783 words), 11 FAQ sets (127 Q&A), 6 static pages, UI strings.
- Glossary and binding style decisions: `src/content/i18n/tr/glossary.md`; LaTeX label table: `src/content/i18n/tr/latex_labels.tsv`.
- Mechanical checks already passed: tag skeleton, LaTeX, digit sequences, FAQ counts (`validate.py`), calculator results (`test_tools.js`), hreflang/canonical/sitemap/switcher (`hreflang_audit.py`), script purity (no wrong-variant letters or digits), no leftover English runs.

## How to review
Open `/tr/` and a few tool pages. Read the table below first (these are the pages' search-facing text), then 3 articles: `percentage-calculator`, `compound-interest-calculator`, `gpa-to-percentage-calculator` (mandatory per the content guide). Apply decisions to the glossary first, then to all 42 pages.

## Style decisions to confirm
- Percent sign BEFORE the number in prose (%20), while the calculators still print `20%`. Keep, or switch to a suffix form?
- Register: polite plural imperative ("Girin", "Hesaplayın").
- Numbers/decimal point/`$` as in English (12.5, not 12,5).

## Terms the translators flagged as uncertain
- markup → «maliyet üzeri kâr (markup)», later just «markup»; also «kâr eklemesi», «çarpan» (multiplier method)
- percentage point → «yüzde puanı» (also used for 'percentage score' in places: possible clash)
- baker's percentage → «fırıncı yüzdesi», «ön maya» (preferment), «Instant maya» left as loanword
- COGS → «SMM» (satılan malın maliyeti); EBITDA → «FAVÖK»; «prime cost» → «birincil maliyet (prime cost)»
- w/v, w/w, v/v kept in English notation; «% a/h» in the first-pass title
- %ile unit label «YD» (first-pass guess); percentile «yüzdelik dilim»
- slope: «Yükseliş/Mesafe», «Yatay mesafe», «meyil» for grade; compounding «bileşiklendirme sıklığı» / «bileşik sıklığı»
- depreciation: «kıst amortisman» (partial-year), «hurda değeri» (salvage), «kayan ölçekli komisyon», «hızlandırıcı»
- legal: «Teknik Lider», «Garanti Reddi», «Tazminat»; «Dürüst Kredi Bilgilendirme Yasası» beside English Truth in Lending Act
- loans: «Aylık Taksit» (EMI), «yalnızca faiz ödemeli», «vadesinde ödenen kredi», «Beş C»
- education: Indian classification labels («Üstün dereceli birinci sınıf» …) are the translator's own renderings; «EBOB» for GCF; «desil»/«çeyrek»
- sports/alcohol: «geride kalınan maç», «pasör reytingi», «güçlendirme» (fortification), «onbinde bir/binde bir»
- «Ç» used for quarter in the growth FAQ; some first-pass titles/descriptions exceed 60/160 chars

## Static pages
- Legal pages (disclaimer, privacy policy, terms) were translated faithfully but have had no legal-language review.

## Tool names, titles and descriptions

| Slug | Nav name | Meta title | Meta description |
|---|---|---|---|
| `alcohol-proof-calculator` | Alkol Derecesi (Proof) Hesaplama | Alkol Derecesi (Proof) Hesaplama | Proof’tan ABV Yüzdesine | Ücretsiz alkol proof hesaplama aracı. ABD proof değerini girin, hacimce alkol oranına (ABV) yüzde olarak anında dönüştürün — hızlı, doğru ve kullanımı kolay. |
| `apr-apy-converter` | APR’den APY’ye Dönüştürücü | APR’den APY’ye Dönüştürücü | Yıllık Getiriyi Hesaplama | Ücretsiz APR – APY dönüştürücü. APR ve bileşiklendirme sıklığını girin, karşılık gelen yıllık getiriyi (APY) anında görün. |
| `apr-calculator` | APR Hesaplama | APR Hesaplama | Yıllık Yüzde Oran Hesaplayıcı | Ücretsiz APR hesaplama aracı. Dönemlik faiz oranını yıllık oran (APR) olarak anında hesaplayın — kredi ve kredi kartı maliyetlerinde kullanılan standart gösterim. |
| `apy-calculator` | APY Hesaplama | APY Hesaplama | Yıllık Getiri Hesaplayıcı | Ücretsiz APY hesaplama aracı. Nominal faiz oranını ve bileşiklendirme sıklığını yıllık getiriye (APY) anında dönüştürün. |
| `average-percentage-calculator` | Yüzde Ortalaması Hesaplama | Yüzde Ortalaması Hesaplama | Basit ve Ağırlıklı Ortalama | Basit ve ağırlıklı modlu ücretsiz yüzde ortalaması hesaplama aracı. Farklı büyüklükteki grupların yüzdelerini notlar ve anketler için doğru biçimde birleştirin. |
| `bakers-percentage-calculator` | Fırıncı Yüzdesi Hesaplama | Fırıncı Yüzdesi Hesaplama | Malzeme Oranlarını Bulun | Ücretsiz fırıncı yüzdesi hesaplama aracı. Un ağırlığını ve malzeme ağırlığını girin, malzemenin fırıncı yüzdesini anında hesaplayın. |
| `basis-points-calculator` | Baz Puan Hesaplama | Baz Puan Hesaplama | Baz Puanı Yüzdeye Çevirme | Ücretsiz baz puan hesaplama aracı. Baz puan (bps) değerini girin, yüzdeye anında dönüştürün — finans ve alım satım için doğru sonuçlar. |
| `cgpa-to-percentage-calculator` | CGPA’dan Yüzdeye Çevirme | CGPA’dan Yüzdeye Çevirme | 10’luk CGPA’yı % Yapın | Standart 10’luk CGPA x 9.5 formülünü kullanan ücretsiz CGPA yüzde hesaplama aracı. CGPA’nızı kolej ve üniversite kayıtları için yüzdeye çevirin. |
| `commission-calculator` | Komisyon Hesaplama | Komisyon Hesaplama | Satış Komisyonunu Bulun | Ücretsiz komisyon hesaplama aracı. Satış tutarını ve komisyon oranını girin, kazandığınız komisyonu anında hesaplayın. |
| `compound-interest-calculator` | Bileşik Faiz Hesaplama | Bileşik Faiz Hesaplama | Zaman İçindeki Büyümeyi Bulun | Ücretsiz bileşik faiz hesaplama aracı. Anapara, yıllık oran, süre ve bileşiklendirme sıklığını girin, kazanılan faizi ve toplam tutarı anında hesaplayın. |
| `decimal-to-percentage-calculator` | Ondalık Sayıyı Yüzdeye Çevirme | Ondalık Sayıyı Yüzdeye Çevirme | Ondalığı % Yapın | Ücretsiz ondalık sayıdan yüzdeye çevirme aracı. Herhangi bir ondalık değeri girin, yüzdeye anında dönüştürün — okul, iş veya finans için doğru sonuçlar. |
| `depreciation-calculator` | Amortisman Hesaplama | Amortisman Hesaplama | Doğrusal Amortisman Yöntemi | Doğrusal amortisman yöntemini kullanan ücretsiz amortisman hesaplama aracı. Varlık maliyetini, hurda değerini ve faydalı ömrü girerek yıllık amortismanı hesaplayın. |
| `food-cost-percentage-calculator` | Gıda Maliyeti Yüzdesi Hesaplama | Gıda Maliyeti Yüzdesi Hesaplama | Menü Maliyeti % | Ücretsiz gıda maliyeti yüzdesi hesaplama aracı. Malzeme maliyetini ve menü fiyatını girin, bir menü ögesinin gıda maliyeti yüzdesini anında hesaplayın. |
| `fraction-to-percentage-calculator` | Kesri Yüzdeye Çevirme | Kesri Yüzdeye Çevirme | Kesri % Olarak Yazın | Ücretsiz kesirden yüzdeye çevirme aracı. Herhangi bir kesri anında yüzdeye dönüştürün — sınav notları, oranlar ve orantılar için ideal. |
| `gpa-to-percentage-calculator` | GPA Yüzdeye Çevirme Hesaplayıcı | GPA Yüzdeye Çevirme | 4.0 Ölçeğinde GPA’yı % Yap | Ücretsiz GPA yüzdeye çevirme aracı. 4.0 ölçeğindeki GPA’nızı anında karşılık gelen yüzdeye dönüştürün. Doğru, basit, üyelik gerektirmez. |
| `gross-margin-calculator` | Brüt Marj Hesaplama | Brüt Marj Hesaplama | Brüt Kâr Marjı Yüzdesi | Ücretsiz brüt marj hesaplama aracı. Gelir ve satılan malın maliyetini (SMM) girerek brüt kârı ve brüt marj yüzdesini anında hesaplayın. |
| `loan-interest-calculator` | Kredi Faizi Hesaplama | Kredi Faizi Hesaplama | Aylık Taksit ve Toplam Faiz | Ücretsiz kredi faizi hesaplama aracı. Kredi tutarı, yıllık faiz oranı ve vadeyi girerek aylık taksiti ve ödenecek toplam faizi anında hesaplayın. |
| `marks-percentage-calculator` | Not Yüzdesi Hesaplama | Not Yüzdesi Hesaplama | Sınav Yüzdesi Hesaplayıcı | Ücretsiz not yüzdesi hesaplama aracı. Aldığınız notu ve toplam puanı girerek sınav veya test yüzdenizi anında hesaplayın. |
| `markup-calculator` | Maliyet Üzeri Kâr (Markup) Hesaplama | Maliyet Üzeri Kâr Hesaplama | Maliyet + Kâr % ile Satış Fiyatı | Ücretsiz maliyet üzeri kâr (markup) hesaplama aracı. Maliyet fiyatını ve istediğiniz kâr yüzdesini girerek uygulamanız gereken satış fiyatını hesaplayın. |
| `percent-solution-calculator` | Yüzde Çözelti Hesaplama | Yüzde Çözelti Hesaplama | Kütle/Hacim Derişimi | Ücretsiz yüzde çözelti hesaplama aracı. Çözünen maddenin kütlesini ve çözeltinin hacmini girerek yüzde derişimi (% a/h) anında hesaplayın. |
| `percentage-calculator` | Yüzde Hesaplama | Yüzde Hesaplama | Yüzdeleri Hızlıca Hesaplayın | Ücretsiz çevrimiçi yüzde hesaplama araçlarıyla yüzdeleri anında hesaplayın. Yüzde artış, azalış, fark ve değişim için kolay araçlar. |
| `percentage-change-calculator` | Yüzde Değişim Hesaplama | Yüzde Değişim Hesaplama | Yüzde Artış/Azalış | Ücretsiz yüzde değişim hesaplama aracı. İki değer arasındaki yüzde artışı veya azalışı hesaplayın — hisse ve fiyat değişimlerini takip edin. |
| `percentage-decrease-calculator` | Yüzde Azalış Hesaplama | Yüzde Azalış Hesaplama | Bir Sayıdan Yüzde Çıkarma | Ücretsiz yüzde azalış hesaplama aracı. Bir sayıdan istediğiniz yüzdeyi anında çıkarın — amortisman, kilo kaybı ve bütçe kesintilerini hesaplayın. |
| `percentage-difference-calculator` | Yüzde Fark Hesaplama | Yüzde Fark Hesaplama | İki Değeri Karşılaştırın | Ücretsiz yüzde fark hesaplama aracı. İki sayıyı karşılaştırıp yüzde farkı bulun. Ortalamayı taban alarak simetrik, tarafsız bir karşılaştırma yapar. |
| `percentage-error-calculator` | Yüzde Hata Hesaplama | Yüzde Hata Hesaplama | Laboratuvar için Yüzde Hata | Ücretsiz yüzde hata hesaplama aracı. Fizik, kimya ve biyoloji laboratuvarları için deneysel ve kuramsal değerler arasındaki yüzde hatayı hesaplayın. |
| `percentage-growth-calculator` | Yüzde Büyüme Hesaplama | Yüzde Büyüme Hesaplama | İşletme Büyüme Oranı | Ücretsiz yüzde büyüme hesaplama aracı. Gelir, müşteri, satış ve KPI büyüme oranlarını hesaplayın. İşletme performansını doğru metriklerle izleyin. |
| `percentage-increase-calculator` | Yüzde Artış Hesaplama | Yüzde Artış Hesaplama | Sayıya Yüzde Ekleme | Ücretsiz yüzde artış hesaplama aracı. Bir sayıya istediğiniz yüzdeyi anında ekleyin. Maaş zammı, fiyat artışı, yatırım getirisi ve daha fazlasını hesaplayın. |
| `percentage-of-a-percentage-calculator` | Yüzdenin Yüzdesi Hesaplama | Yüzdenin Yüzdesi Hesaplama | İki Yüzdeyi Birleştirin | Ücretsiz yüzdenin yüzdesi hesaplama aracı. Üst üste gelen iki yüzdeyi çarpın, birleşik oranı vergi veya indirim zincirleme uygulamasında bir değere uygulayın. |
| `percentage-off-calculator` | Yüzde İndirim Hesaplama | Yüzde İndirim Hesaplama | İndirimli Fiyat Hesaplayıcı | Ücretsiz yüzde indirim hesaplama aracı. İndirimli fiyatı ve tasarrufunuzu anında hesaplayın. Her indirim sonrası ödeyeceğiniz son fiyatı bulun. |
| `percentage-point-calculator` | Yüzde Puanı Hesaplama | Yüzde Puanı Hesaplama | Puan Farkı Hesaplayıcı | Ücretsiz yüzde puanı hesaplama aracı. İki yüzde girin, yüzde puanı farkını ve göreli yüzde değişimini anında görün. |
| `percentile-to-percentage-calculator` | Yüzdelik Dilimden Yüzdeye Hesaplama | Yüzdelik Dilimden Yüzdeye Hesaplama | Yüzde Tahmini | Ücretsiz yüzdelik dilimden yüzdeye hesaplama aracı. Sınav yüzdelik dilim puanınızdan yaygın bir yaklaşık formülle hızlı bir yüzde tahmini alın. |
| `ppm-to-percentage-calculator` | PPM’den Yüzdeye Çevirme | PPM’den Yüzdeye Çevirme | Milyonda Bir Parça Hesaplama | Ücretsiz PPM’den yüzdeye çevirme aracı. Milyonda bir parça (ppm) değerini girin, yüzdeye anında dönüştürün; kimya ve mühendislik için doğru sonuç. |
| `profit-margin-calculator` | Kâr Marjı Hesaplama | Kâr Marjı Hesaplama | Kâr Marjı Yüzdesi Hesaplayıcı | Ücretsiz kâr marjı hesaplama aracı. Maliyet fiyatını ve satış fiyatını girin; kârınızı ve satış fiyatı üzerinden kâr marjı yüzdenizi anında hesaplayın. |
| `profit-percentage-calculator` | Kâr Yüzdesi Hesaplama | Kâr Yüzdesi Hesaplama | Maliyet Üzerinden Kâr % Hesaplayıcı | Ücretsiz kâr yüzdesi hesaplama aracı. Maliyet fiyatını ve satış fiyatını girin; kâr tutarınızı ve kâr yüzdenizi anında hesaplayın. |
| `ratio-to-percentage-calculator` | Orandan Yüzdeye Çevirme | Orandan Yüzdeye Çevirme | Oranı % Olarak Hesaplama | Ücretsiz orandan yüzdeye çevirme aracı. Bir oranın iki parçasını girin; toplamı ve ilk parçanın yüzde kaç olduğunu anında görün. |
| `reverse-percentage-calculator` | Ters Yüzde Hesaplama | Ters Yüzde Hesaplama | Orijinal Sayıyı Bulma | Ücretsiz ters yüzde hesaplama aracı. Bir değeri ve yüzdesini biliyorsanız orijinal sayıyı bulun; indirim öncesi fiyatı ve daha fazlasını hesaplayın. |
| `salary-increase-calculator` | Maaş Zammı Hesaplama | Maaş Zammı Hesaplama | Yeni Maaşınızı Hesaplayın | Ücretsiz maaş zammı hesaplama aracı. Mevcut maaşınızı ve zam yüzdesini girin; zam tutarını ve yeni maaşınızı anında hesaplayın. |
| `sgpa-to-percentage-calculator` | SGPA’dan Yüzdeye Çevirme | SGPA’dan Yüzdeye Çevirme | SGPA’yı Yüzdeye Dönüştürme | Standart SGPA × 9.5 formülünü kullanan ücretsiz SGPA’dan yüzdeye çevirme aracı. Dönem ortalamanızı (SGPA) eşdeğer yüzdeye anında dönüştürün. |
| `simple-interest-calculator` | Basit Faiz Hesaplama | Basit Faiz Hesaplama | Faiz ve Toplam Tutar | Ücretsiz basit faiz hesaplama aracı. Anapara, yıllık faiz oranı ve süreyi girin; kazanılan faizi ve toplam tutarı anında hesaplayın. |
| `slope-percentage-calculator` | Yüzde Eğim Hesaplama | Yüzde Eğim Hesaplama | Yükseliş/Mesafeyi Eğim %’sine Çevirme | Ücretsiz yüzde eğim hesaplama aracı. Yükseliş ve yatay mesafeyi girin; yüzde eğimi ve derece cinsinden eşdeğer açıyı anında hesaplayın. |
| `tip-calculator` | Bahşiş Hesaplama | Bahşiş Hesaplama | Bahşiş ve Hesap Bölüşme | Ücretsiz bahşiş hesaplama aracı. Hesap tutarını, bahşiş yüzdesini ve kişi sayısını girin; bahşişi, toplamı ve kişi başı tutarı anında hesaplayın. |
| `win-loss-percentage-calculator` | Galibiyet/Mağlubiyet Oranı Hesaplama | Galibiyet/Mağlubiyet Oranı Hesaplama | Kazanma Oranı | Ücretsiz galibiyet/mağlubiyet yüzdesi hesaplama aracı. Galibiyet, mağlubiyet ve beraberlik sayısını girin; her spor, oyun veya yarışma için kazanma yüzdenizi hesaplayın. |
