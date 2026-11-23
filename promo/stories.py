"""25 photo-real ad scenarios built from AI-generated stills.

Workflow: the user generates the images from the English prompts below (Gemini / Kling / Midjourney,
vertical 9:16, no text in the image), saves them as assets/ai/sNN/1.jpg, 2.jpg ... and runs
    python3 gen_stories.py            # writes ai-senaryolar.md (prompt pack) and sNN-*.html pages
    python3 build2.py <work> sNN-*.html
Each scene = (image prompt, Turkish on-screen caption: light line, bold line).
"""

STYLE = ("photorealistic, cinematic commercial photography, natural warm light, shallow depth of field, "
         "35mm, authentic Turkish setting, vertical 9:16, no text, no logos, no watermark")

STORIES = [
    # ---------------- A · Sipariş akışı ----------------
    ("s01", "Akşam Yemeği", "restoran", "corporate", [
        ("Turkish family on a sofa at home in the evening, father holding a smartphone, deciding what to order, cozy living room", "Akşam oldu,", "karnımız acıktı."),
        ("Close-up of a hand tapping a food ordering app on a smartphone, warm home lighting, bokeh", "Üç dokunuşla", "sipariş verildi."),
        ("Turkish restaurant kitchen at night, chef glancing at a phone on the counter lighting up with a notification", "Restoranda", "zil çaldı."),
        ("Family happily opening warm food containers of lahmacun and pide on a dining table", "Afiyet", "olsun!"),
    ]),
    ("s02", "Mutfakta Bir Sipariş", "restoran", "groove", [
        ("Thermal receipt printer in a busy Turkish restaurant kitchen printing an order ticket, close-up", "Sipariş geldi,", "fiş çıktı."),
        ("Turkish chef spreading minced meat topping on thin dough for lahmacun, flour on the counter, action shot", "Usta", "işbaşında."),
        ("Lahmacun being pulled out of a wood-fired stone oven on a wooden peel, flames, steam", "Fırından", "sıcacık."),
        ("Hands packing food containers into a brown paper delivery bag on a stainless counter", "Paketlendi,", "yola hazır."),
    ]),
    ("s03", "Paket Servis Hızı", "restoran", "house", [
        ("Kebab master grilling adana skewers over charcoal, sparks and smoke, dramatic light", "Ocak", "yanıyor."),
        ("Chef wrapping a dürüm in paper with fast hands, close-up, motion blur", "Hızlı", "hazırlık."),
        ("Delivery courier taking a paper food bag from a restaurant counter, smiling, night", "Kurye", "teslim aldı."),
        ("Scooter courier riding through a lit Turkish city street at night, motion blur", "Siparişin", "yolda."),
    ]),
    ("s04", "Kapıda Ödeme", "restoran", "chill", [
        ("Delivery courier ringing an apartment doorbell holding a warm food bag, hallway light", "Ding dong,", "sipariş geldi."),
        ("Customer paying a courier at the door with a card on a portable POS terminal, close-up of hands", "Kapıda", "kartla öde."),
        ("Customer handing cash to a courier at an apartment door, friendly, warm light", "İstersen", "nakit."),
        ("Smiling young couple at the door holding a food bag, waving goodbye to the courier", "Mutlu", "müşteri."),
    ]),
    ("s05", "Öğle Arası", "restoran", "groove", [
        ("Busy office workers at desks at lunchtime, one looking at a food app on her phone", "Öğle", "arası."),
        ("Steaming bowl of lentil soup and pide on a restaurant pass, ready for delivery", "Sıcak", "çorba hazır."),
        ("Courier walking into a modern office lobby with food bags", "Ofise", "teslimat."),
        ("Coworkers eating together at an office table, laughing", "Tok karnına", "mesai."),
    ]),
    # ---------------- B · Kurye ----------------
    ("s06", "Kuryenin Günü", "restoran", "corporate", [
        ("Delivery courier putting on a helmet next to a scooter in the morning, Turkish street", "Güne", "başlarken."),
        ("Courier checking a delivery route on a phone mounted on scooter handlebars", "Rota", "hazır."),
        ("Courier riding past historic mosque and Bursa green mountains, golden hour", "Şehrin", "her köşesine."),
        ("Courier handing a food bag to a smiling elderly man at a garden gate", "Güler yüzle", "teslim."),
    ]),
    ("s07", "Yağmurda Teslimat", "restoran", "chill", [
        ("Rainy night street in a Turkish city, neon reflections on wet asphalt, a courier in rain gear on a scooter", "Yağmur", "çamur."),
        ("Close-up of an insulated delivery box with raindrops, steam rising when opened", "Sipariş", "sıcacık kaldı."),
        ("Courier under an apartment awning handing a dry food bag to a customer", "Kuru ve", "zamanında."),
        ("Family eating soup by a rainy window, cozy", "İçimiz", "ısındı."),
    ]),
    ("s08", "Canlı Takip", "restoran", "house", [
        ("Woman on a balcony looking at her phone with a map tracking a delivery, evening city lights", "Siparişim", "nerede?"),
        ("Overhead drone shot of a scooter courier on a city avenue at dusk", "Canlı", "takipte."),
        ("Courier parking a scooter in front of an apartment building", "Kapıya", "geldi."),
        ("Woman opening the door smiling, taking the food bag", "Tam", "zamanında."),
    ]),
    # ---------------- C · Kargo (mağaza siparişi) ----------------
    ("s09", "İlk Online Satış", "magaza", "corporate", [
        ("Small shop owner in a Turkish electronics store looking surprised and happy at a phone notification", "İlk online", "satış!"),
        ("Hands placing a product into a cardboard box with bubble wrap on a shop counter", "Özenle", "paketlendi."),
        ("Shop owner printing a shipping label from a small label printer, close-up", "Kargo etiketi", "hazır."),
        ("Cargo courier picking up boxes from the shop door", "Kargoya", "verildi."),
    ]),
    ("s10", "Kutu Açılışı", "magaza", "groove", [
        ("Cargo delivery man handing a cardboard box to a young woman at her apartment door", "Kargon", "geldi."),
        ("Young woman cutting the tape of a cardboard box on a living room table, excited", "Heyecanla", "açılıyor."),
        ("Close-up of a new kitchen kettle being lifted out of the box, soft light", "Tam", "istediğim gibi."),
        ("Woman giving five stars on her phone, smiling", "Beş", "yıldız."),
    ]),
    ("s11", "Depodan Kapıya", "magaza", "house", [
        ("Small warehouse with shelves of boxed products, shop owner scanning a barcode", "Stok", "kontrol."),
        ("Packing table with several boxes being taped, top-down view", "Siparişler", "paketleniyor."),
        ("Cargo van being loaded with parcels at dusk", "Yola", "çıktı."),
        ("Parcel left on a doormat in front of an apartment door", "Kapına", "teslim."),
    ]),
    ("s12", "Çiçekçi", "magaza", "chill", [
        ("Turkish florist arranging a bouquet of pink roses in a flower shop, morning light", "Çiçekçi", "Oğuz usta."),
        ("Florist reading an order on a phone, smiling, flowers around", "Online", "sipariş geldi."),
        ("Beautiful bouquet wrapped in paper with a small card on the counter", "Özenle", "hazırlandı."),
        ("Woman at her door receiving a bouquet, surprised and happy", "Mutlu", "sürpriz."),
    ]),
    # ---------------- D · Mağaza yönetimi ----------------
    ("s13", "Ürününü Listele", "magaza", "corporate", [
        ("Shop owner photographing a product on a white backdrop with a smartphone in a small studio corner", "Fotoğrafını", "çek."),
        ("Hands typing a product description and price on a laptop in a shop", "Fiyatını", "gir."),
        ("Shop owner tapping publish on a tablet, satisfied", "Yayınla,", "satışta."),
        ("Many products displayed on shelves in a tidy modern shop", "Vitrin", "büyüdü."),
    ]),
    ("s14", "Tek Panelde Mağaza", "magaza", "house", [
        ("Shop owner at a counter checking a sales dashboard on a tablet, charts", "Sipariş,", "stok, soru."),
        ("Phone on a counter showing a new order notification, shop in the background", "Anında", "bildirim."),
        ("Shop owner answering a customer question on a phone, friendly", "Sorulara", "hızlı cevap."),
        ("Shop owner smiling with arms crossed in front of his store", "Hepsi", "tek panelde."),
    ]),
    ("s15", "Hakediş Günü", "magaza", "chill", [
        ("Shop owner at a desk reviewing sales on a laptop in the evening", "Satışlar", "teslim edildi."),
        ("Close-up of a banking app notification of an incoming transfer on a phone", "Hakediş", "IBAN'ında."),
        ("Shop owner shaking hands with his employee in the shop, cheerful", "Şeffaf", "ve net."),
        ("Shop sign lit up at dusk on a Turkish shopping street", "Büyüyen", "mağaza."),
    ]),
    ("s16", "POS ve Barkod Mağazası", "magaza", "groove", [
        ("POS terminals and receipt printers neatly displayed in a technology shop", "Barkod", "dünyası."),
        ("Shop owner packing a receipt printer into a box", "Siparişi", "hazırla."),
        ("Cargo van driving through Bursa streets", "Türkiye'nin", "her yerine."),
        ("Restaurant owner unboxing a new POS terminal at his counter", "Yeni", "müşterin."),
    ]),
    # ---------------- E · Restoran yönetimi ----------------
    ("s17", "AlfaPOS Kasa", "restoran", "corporate", [
        ("Modern touchscreen POS cash register on a restaurant counter, warm light", "Siparişler", "kasaya düşer."),
        ("Cashier tapping accept on a POS screen, close-up", "Tek dokunuşla", "onayla."),
        ("Kitchen printer printing a ticket with a chef waiting", "Mutfak", "yazıcısı çalışır."),
        ("Restaurant owner relaxed behind the counter, smiling at camera", "Adisyon", "düzenli."),
    ]),
    ("s18", "Teslimat Bölgeni Seç", "restoran", "house", [
        ("Restaurant owner looking at a city map on a tablet, pointing at neighborhoods", "Bölgeni", "seç."),
        ("Aerial view of Bursa neighborhoods at sunset", "Mahalle", "mahalle."),
        ("Restaurant owner adjusting prices on a tablet in the kitchen", "Ücreti", "sen belirle."),
        ("Couriers leaving the restaurant in different directions", "Siparişler", "her yöne."),
    ]),
    ("s19", "Menün Resimli", "restoran", "chill", [
        ("Professional food photographer shooting a plate of pide in a restaurant", "Menünün", "fotoğrafları."),
        ("Beautiful top-down shot of a Turkish table spread: lahmacun, pide, salad, ayran", "İştah", "açan menü."),
        ("Customer scrolling a food menu with photos on a phone", "Müşteri", "görünce seçer."),
        ("Restaurant owner giving a thumbs up in his kitchen", "Menüyü", "biz yükleriz."),
    ]),
    ("s20", "Şubeler Tek Panelde", "restoran", "groove", [
        ("Owner of a restaurant chain in an office looking at a monitor with several restaurant locations", "Birden çok", "şube mi?"),
        ("Three restaurant storefronts in a Turkish city at night collage-like composition", "Hepsi", "tek panelde."),
        ("Phone on a desk receiving multiple order notifications", "Sesli", "bildirim."),
        ("Restaurant manager meeting with staff, positive mood", "Kontrol", "sende."),
    ]),
    # ---------------- F · Reklam / kampanya ----------------
    ("s21", "Esnafın Tavsiyesi", "restoran", "corporate", [
        ("Portrait of a mature Turkish kebab master in his restaurant looking confidently at the camera", "Otuz yıllık", "usta."),
        ("Kebab master showing his phone with a new order to a younger chef", "Siparişler", "getirtrend'den."),
        ("Kebab master and his son working together in the kitchen", "Esnaf", "esnafa tavsiye."),
        ("The master smiling with his hand on his heart", "Hayırlı", "işler."),
    ]),
    ("s22", "Önce / Sonra", "restoran", "drama", [
        ("Empty restaurant at night, chairs on tables, owner sitting alone, cold blue light", "Önce:", "boş masalar."),
        ("Silent phone on a dusty counter", "Sessiz", "telefon."),
        ("Same restaurant busy, kitchen full of action, warm light", "Sonra:", "mutfak tam gaz."),
        ("Owner laughing while several couriers wait at the counter", "Siparişler", "peş peşe."),
    ]),
    ("s23", "Mahallenin Lezzetleri", "restoran", "house", [
        ("Macro shot of crispy lahmacun with parsley and lemon", "Lahmacun", ""),
        ("Kıymalı pide with butter melting, steam", "Pide", ""),
        ("Adana kebab on a plate with grilled peppers and tomatoes", "Kebap", ""),
        ("Pistachio baklava with syrup glistening", "ve", "tatlısı."),
    ]),
    ("s24", "Bursa'nın Lezzeti", "restoran", "corporate", [
        ("Bursa skyline with Uludağ mountain at sunset", "Bursa'nın", "lezzeti,"),
        ("Iskender kebab being served with melted butter poured on top", "tek uygulamada.", ""),
        ("Historic Bursa bazaar street with small restaurants at evening", "Mahallendeki", "restoranlar."),
        ("Family enjoying dinner on a balcony overlooking Bursa", "Kapına", "gelsin."),
    ]),
    ("s25", "Herkes Kazanır", "restoran", "groove", [
        ("Restaurant owner smiling behind his counter", "Restoran", "kazanır."),
        ("Courier giving a thumbs up next to his scooter", "Kurye", "kazanır."),
        ("Customer family eating happily at home", "Müşteri", "kazanır."),
        ("Shop owner packing an order in his small store", "Mağaza", "kazanır."),
    ]),
]
