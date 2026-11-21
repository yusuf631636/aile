"""Generates the chat-style promo pages (v6, v10, v11) from their scripts below.
Edit the messages here, run `python3 gen_chats.py`, then build with build2.py.
Message fields: s (L incoming / R sent), t (time it appears), ty (R: when typing starts),
text, typed (what is typed in the input box, if different), img + h + cap, zoom [from, to], link, from (group sender).
"""
from pathlib import Path

HEAD = Path(__file__).with_name("chat_template.html").read_text(encoding="utf-8")

PAGES = {
    "v6-esnaf-sohbeti.html": dict(
        title="getirtrend – Esnaf Sohbeti", music="chill", line1="Sen de hemen", line2="restoranını ekle",
        p1="pide", p2="durum", p3="kebap", btn="Ücretsiz Başvur →", chat="""{
  name: 'Hasan Usta · Pideci', sub: 'çevrimiçi', avatar: 'assets/pide2.jpg', clockStart: 20 * 60 + 41, end: 24.6,
  msgs: [
    { s: 'L', t: 1.2, text: 'Selamün aleyküm Mehmet abi 👋' },
    { s: 'L', t: 2.6, text: 'Dükkân nasıl, işler ne âlemde?' },
    { s: 'R', t: 4.3, ty: 3.1, text: 'Aleyküm selam Hasan 😊' },
    { s: 'R', t: 6.3, ty: 4.7, text: 'Maşallah bu ara siparişe yetişemiyoruz 😅' },
    { s: 'L', t: 7.7, text: 'Hayırdır abi, sırrın ne? 😄' },
    { s: 'R', t: 9.4, ty: 8.1, text: "getirtrend'e restoranı ekledim 👍" },
    { s: 'R', t: 10.4, img: 'assets/ui/demo-top.jpg', h: 620, cap: 'Müşteri bizi böyle görüyor 👇', zoom: [10.9, 12.9] },
    { s: 'R', t: 15.6, ty: 14.6, text: 'Bak yine sipariş geldi 😄' },
    { s: 'L', t: 17.0, text: 'Abi ben nasıl eklerim? 🙏' },
    { s: 'R', t: 18.8, ty: 17.6, link: true, text: 'Buradan başvur, ücretsiz 👇', typed: 'getirtrend.com/restoran-ol' },
    { s: 'L', t: 20.6, text: 'Hemen ekliyorum abi, Allah razı olsun 🤲' },
    { s: 'R', t: 22.4, ty: 21.2, text: 'Hayırlı işler kardeşim 🤝' },
  ],
  notifs: [{ t: 13.3, d: 1.9, title: '🔔 Yeni sipariş · 360 TL', body: '2× Lahmacun, 1× Ayran · Kapıda nakit' }],
}"""),
    "v10-esnaf-grubu.html": dict(
        title="getirtrend – Esnaf Grubu", music="acoustic", line1="Çarşıda herkes", line2="getirtrend'de",
        p1="lahmacun", p2="adana", p3="baklava", btn="Restoranını Ekle →", chat="""{
  name: 'Çarşı Esnafları 🤝', sub: 'Ahmet, Kemal, Selim, Siz', avatar: 'assets/lahmacun3.jpg', clockStart: 20 * 60 + 52, end: 25.2, group: true,
  members: { 'Ahmet · Kebapçı': '#c2410c', 'Kemal · Tatlıcı': '#7c3aed', 'Selim · Dönerci': '#0369a1' },
  msgs: [
    { s: 'L', from: 'Ahmet · Kebapçı', t: 1.1, text: 'Arkadaşlar bu akşam durum nasıl? Bizde sinek avlıyoruz 😅' },
    { s: 'L', from: 'Kemal · Tatlıcı', t: 2.7, text: 'Bizde de sessiz valla' },
    { s: 'R', t: 4.5, ty: 3.3, text: 'Bizde telefon susmuyor çok şükür 🙏' },
    { s: 'L', from: 'Selim · Dönerci', t: 5.9, text: 'Nasıl yani? 😮' },
    { s: 'R', t: 7.6, ty: 6.4, text: "getirtrend'e geçtim, siparişler oradan geliyor" },
    { s: 'R', t: 8.6, img: 'assets/ui/lock.jpg', h: 760, cap: 'Son yarım saat 👇', zoom: [9.1, 11.3] },
    { s: 'L', from: 'Ahmet · Kebapçı', t: 12.6, text: 'Maşallah! Kurulumu zor mu?' },
    { s: 'R', t: 14.4, ty: 13.2, text: 'Hiç zor değil, menüyü resimleriyle onlar yüklüyor' },
    { s: 'R', t: 16.0, ty: 14.8, text: 'Siparişler AlfaPOS kasaya düşüyor, fiş yazıcıdan çıkıyor 👌' },
    { s: 'L', from: 'Kemal · Tatlıcı', t: 17.4, text: 'Başvuru nereden?' },
    { s: 'R', t: 19.0, ty: 17.9, link: true, typed: 'getirtrend.com/restoran-ol' },
    { s: 'L', from: 'Selim · Dönerci', t: 20.5, text: 'Ben başvurdum bile 👍' },
    { s: 'L', from: 'Ahmet · Kebapçı', t: 21.8, text: 'Ben de! Hayırlı olsun 🤝' },
    { s: 'L', from: 'Kemal · Tatlıcı', t: 23.0, text: '👏👏👏' },
  ],
}"""),
    "v11-basvuru-yazismasi.html": dict(
        title="getirtrend – Başvuru Yazışması", music="chill", line1="Sorunuz mu var?", line2="Yazın, yardımcı olalım",
        p1="lahmacun2", p2="pide", p3="cigkofte", btn="Hemen Başvur →", chat="""{
  name: 'getirtrend Restoran', sub: 'işletme hesabı', avatar: 'assets/logo-mark.svg', clockStart: 11 * 60 + 5, end: 25.6,
  msgs: [
    { s: 'R', t: 1.7, ty: 0.3, text: "Merhaba, restoranımı getirtrend'e eklemek istiyorum 🙂" },
    { s: 'L', t: 3.2, text: 'Merhaba, hoş geldiniz! 🙌 Başvuru ücretsiz, birkaç dakika sürüyor.' },
    { s: 'L', t: 4.7, text: '1️⃣ Hesabınızı ve restoranınızı tek formda açın\\n2️⃣ Onay beklerken menünüzü ve bölgelerinizi hazırlayın\\n3️⃣ Onaylanınca siparişler başlasın' },
    { s: 'R', t: 7.1, ty: 6.0, text: 'Menüyü ben mi yükleyeceğim?' },
    { s: 'L', t: 8.5, text: 'Menünüz resimleriyle sizin yerinize yüklenir 📸' },
    { s: 'R', t: 10.0, ty: 9.0, text: 'Siparişler bana nasıl gelecek?' },
    { s: 'L', t: 11.5, text: 'Sesli uyarıyla panelinize, telefonunuza ve AlfaPOS kasanıza düşer. Kilit ekranında bile zil çalar 🔔' },
    { s: 'L', t: 12.6, img: 'assets/ui/lock.jpg', h: 700, zoom: [13.0, 15.0] },
    { s: 'R', t: 16.6, ty: 15.5, text: 'Ödemeyi kim alıyor?' },
    { s: 'L', t: 18.0, text: 'Ödemeyi kapıda siz alırsınız; nakit ya da kendi POS’unuzla 👍' },
    { s: 'L', t: 19.3, link: true, text: 'Başvuru formu burada 👇' },
    { s: 'R', t: 21.6, ty: 20.4, text: 'Harika, hemen başvuruyorum 🙏' },
    { s: 'L', t: 23.0, text: 'Hayırlı işler dileriz! 🤝' },
  ],
}"""),
}

if __name__ == "__main__":
    here = Path(__file__).parent
    for fn, d in PAGES.items():
        html = HEAD
        for k, v in d.items():
            html = html.replace("{{" + k + "}}", v)
        (here / fn).write_text(html, encoding="utf-8")
        print("wrote", fn)
