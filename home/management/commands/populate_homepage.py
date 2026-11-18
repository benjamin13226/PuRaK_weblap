# Import standard library and Django management command utilities
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.images import get_image_model

# Import HomePage model
from home.models import HomePage


# Create an in-memory PNG placeholder image in the Wagtail image library
def create_placeholder_image(title, width, height, bg_color, label_text):
    ImageModel = get_image_model()
    existing = ImageModel.objects.filter(title=title).first()
    if existing:
        return existing

    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, width - 10, height - 10], outline="#cccccc", width=2)
    draw.text((24, height // 2 - 8), label_text, fill="#ffffff")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    wagtail_image = ImageModel(
        title=title,
        file=ImageFile(buffer, name=f"{title.lower().replace(' ', '_')}.png"),
    )
    wagtail_image.save()
    return wagtail_image


# Populate HomePage StreamField with modular blocks matching the homepage layout
class Command(BaseCommand):
    help = "Populates the HomePage StreamField with reusable blocks matching the club homepage design."

    def handle(self, *args, **options):
        homepage = HomePage.objects.first()
        if not homepage:
            self.stdout.write(self.style.ERROR("No HomePage instance found in database."))
            return

        # Retrieve or create placeholder image instances for block fields
        hero_bg = create_placeholder_image("Hero Radio Station", 1920, 800, "#24292e", "HA5KHC Station Photo")
        icon_edu = create_placeholder_image("Icon Education", 128, 128, "#333333", "EDU")
        icon_qth = create_placeholder_image("Icon Repeater", 128, 128, "#333333", "QTH")
        icon_cup = create_placeholder_image("Icon Contest", 128, 128, "#d4af37", "CUP")
        logo_mrasz = create_placeholder_image("Logo MRASZ", 180, 90, "#666666", "MRASZ")
        logo_puskas = create_placeholder_image("Logo BMSZC Puskas", 220, 90, "#666666", "BMSZC PUSKAS")
        logo_viacom = create_placeholder_image("Logo VIACOM", 180, 90, "#666666", "VIACOM")

        # Assign StreamField block instances to HomePage body
        homepage.body = [
            (
                "hero",
                {
                    "title": "Üdvözlünk a Puskás Rádióklubban!",
                    "title_en": "Welcome to Puskás Radio Club!",
                    "subtitle": "Hagyomány, technika és közösség. Fedezd fel a rádióamatőr világot velünk.",
                    "subtitle_en": "Tradition, technology, and community. Explore the amateur radio world with us.",
                    "background_image": hero_bg,
                    "background_color": "#181818",
                    "is_compact": False,
                    "show_bottom_border": False,
                    "accent_color": "#800000",
                    "button_style": "accent",
                    "button_text": "Friss Hírek",
                    "button_text_en": "Latest News",
                    "button_page": None,
                },
            ),
            (
                "section_header",
                {
                    "heading": "A Puskás Tivadar Rádióklubról",
                    "heading_en": "About Puskás Tivadar Radio Club",
                    "lead_text": (
                        "Klubunk évtizedek óta a hazai rádióamatőr közösség egyik meghatározó bázisa. "
                        "Célunk az utánpótlás nevelése, a rádióamatőr hagyományok ápolása és a legmodernebb "
                        "digitális kommunikációs technikák elsajátítása. Akár a rövidhullámú DX-elés, akár a "
                        "műholdas kommunikáció érdekel, nálunk megtalálod a helyed."
                    ),
                    "lead_text_en": (
                        "Our club has been a cornerstone of the Hungarian amateur radio community for decades. "
                        "Our mission is youth mentoring, preserving radio traditions, and mastering modern "
                        "digital communication techniques."
                    ),
                    "alignment": "center",
                    "show_underline": True,
                    "accent_color": "#800000",
                    "section_bg": "#ffffff",
                },
            ),
            (
                "card_grid",
                {
                    "section_title": "",
                    "section_title_en": "",
                    "card_style": "feature_icon",
                    "section_bg": "#ffffff",
                    "cards": [
                        {
                            "title": "Oktatás és Vizsga",
                            "title_en": "Training & Exams",
                            "icon": "🎓",
                            "image": None,
                            "text": (
                                "Rendszeres tanfolyamokat indítunk kezdőknek, hogy sikeres rádióamatőr "
                                "vizsgát tehessenek és megszerezzék a hívójelet."
                            ),
                            "text_en": (
                                "We organize regular courses for beginners to pass the amateur radio exam "
                                "and earn their callsign."
                            ),
                            "link_page": None,
                        },
                        {
                            "title": "Átjátszók (QTH)",
                            "title_en": "Repeaters (QTH)",
                            "icon": "📡",
                            "image": None,
                            "text": (
                                "Klubunk több analóg és digitális átjátszó állomást is üzemeltet (pl. Nadap), "
                                "biztosítva a folyamatos összeköttetést."
                            ),
                            "text_en": (
                                "Our club operates several analog and digital repeater stations (e.g. Nadap), "
                                "ensuring continuous connectivity."
                            ),
                            "link_page": None,
                        },
                        {
                            "title": "Versenyek",
                            "title_en": "Contests",
                            "icon": "🏆",
                            "image": None,
                            "text": (
                                "Rendszeres résztvevői és szervezői vagyunk a hazai és nemzetközi "
                                "rádióiránymérő (ARDF) és RH/URH versenyeknek."
                            ),
                            "text_en": (
                                "We regularly participate in and organize national and international "
                                "ARDF and HF/VHF radio contests."
                            ),
                            "link_page": None,
                        },
                    ],
                },
            ),
            (
                "highlight_card",
                {
                    "title": "Új Weboldal!!",
                    "title_en": "New Website!!",
                    "meta_info": "Írta: admin | 2026-05-12",
                    "meta_info_en": "Posted by: admin | 2026-05-12",
                    "body": (
                        "<p>Üdvözlet kedves látogató! Az elmúlt hónapokban új weboldal fejlesztése zajlott, "
                        "aminek az átirányítása most zajlik. Hamarosan ismét minden információ megtalálható "
                        "lesz itt is, mint a régi oldalon. --Addig kérlek légy türelemmel!</p>"
                    ),
                    "body_en": (
                        "<p>Welcome dear visitor! Over the past months we have been developing a new website, "
                        "and migration is currently underway. All information from the old site will soon be "
                        "available here as well. --Thank you for your patience!</p>"
                    ),
                    "accent_color": "#800000",
                    "section_bg": "#f3f4f6",
                    "button_text": "",
                    "button_text_en": "",
                    "button_page": None,
                },
            ),
            (
                "gallery",
                {
                    "album_title": "",
                    "album_title_en": "",
                    "description": "",
                    "description_en": "",
                    "display_mode": "logo_strip",
                    "section_bg": "#ffffff",
                    "images": [logo_mrasz, logo_puskas, logo_viacom],
                },
            ),
            (
                "hero",
                {
                    "title": "Szeretnél a közösségünk tagja lenni?",
                    "title_en": "Would you like to join our community?",
                    "subtitle": (
                        "Gyere el a következő klubnapunkra, vagy vedd fel velünk a kapcsolatot, "
                        "és ismerd meg a rádióamatőrök világát!"
                    ),
                    "subtitle_en": (
                        "Visit our next club day or get in touch with us to discover the world of amateur radio!"
                    ),
                    "background_image": None,
                    "background_color": "#2b2b2b",
                    "is_compact": True,
                    "show_bottom_border": False,
                    "accent_color": "#800000",
                    "button_style": "white",
                    "button_text": "Kapcsolatfelvétel",
                    "button_text_en": "Contact Us",
                    "button_page": None,
                },
            ),
        ]

        # Save draft revision and publish HomePage
        revision = homepage.save_revision()
        revision.publish()
        self.stdout.write(self.style.SUCCESS("HomePage populated successfully."))