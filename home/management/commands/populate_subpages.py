# Import Django management command base and Wagtail models
from django.core.management.base import BaseCommand
from home.models import HomePage, FlexPage, MenuItem, SubMenu, SubMenuItem


# Create or update a FlexPage child under a given parent page
def get_or_create_flex_page(parent, slug, title, theme_color="", sub_menu=None, body_data=None):
    existing = FlexPage.objects.child_of(parent).filter(slug=slug).first()
    if existing:
        page = existing
        page.title = title
        page.theme_color = theme_color
        page.sub_menu = sub_menu
        if body_data is not None:
            page.body = body_data
        revision = page.save_revision()
        revision.publish()
        return page

    page = FlexPage(
        title=title,
        slug=slug,
        theme_color=theme_color,
        sub_menu=sub_menu,
        body=body_data or [],
    )
    parent.add_child(instance=page)
    revision = page.save_revision()
    revision.publish()
    return page


# Populate subpages, submenus, main navigation order, and homepage news anchor link
class Command(BaseCommand):
    help = "Populates all club subpages, department submenus, main navigation order, and news anchor links."

    def handle(self, *args, **options):
        homepage = HomePage.objects.first()
        if not homepage:
            self.stdout.write(self.style.ERROR("No HomePage instance found in database."))
            return

        # Create reusable SubMenu snippets for subpage navigation bars
        verseny_submenu, _ = SubMenu.objects.get_or_create(name="Versenyek almenü")
        ardf_submenu, _ = SubMenu.objects.get_or_create(name="Rádiós Tájfutás (ARDF) almenü")
        konstruktor_submenu, _ = SubMenu.objects.get_or_create(name="Konstruktőri almenü")
        burabu_submenu, _ = SubMenu.objects.get_or_create(name="BURABU almenü")

        # Create Department pages under HomePage
        ardf_page = get_or_create_flex_page(
            homepage,
            slug="ardf",
            title="Rádiós Tájfutás (ARDF)",
            theme_color="#1b5e20",
            sub_menu=ardf_submenu,
            body_data=[
                (
                    "hero",
                    {
                        "title": "Rádiós Tájfutás (ARDF)",
                        "title_en": "Amateur Radio Direction Finding (ARDF)",
                        "subtitle": "Köszöntünk a Rádiós Tájfutók Birodalmában!",
                        "subtitle_en": "Welcome to the Realm of Radio Orienteering!",
                        "background_image": None,
                        "background_color": "#1b5e20",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#1b5e20",
                        "button_style": "white",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "two_column",
                    {
                        "ratio": "2fr 1fr",
                        "card_wrapper": False,
                        "left_column": [
                            (
                                "section_header",
                                {
                                    "anchor_id": "sportagrol",
                                    "heading": "A sportágról",
                                    "heading_en": "About the Sport",
                                    "lead_text": (
                                        "A rádiós tájékozódási futás (ARDF) egy olyan izgalmas sportág, amely ötvözi a "
                                        "hagyományos tájfutást a rádióirányméréssel. A versenyzőknek rejtett adóállomásokat "
                                        "kell megtalálniuk egy erdős területen, kizárólag egy iránymérő vevőkészülék és egy térkép segítségével."
                                    ),
                                    "lead_text_en": (
                                        "Amateur Radio Direction Finding (ARDF) combines traditional orienteering with radio direction finding."
                                    ),
                                    "alignment": "left",
                                    "show_underline": False,
                                    "accent_color": "#1b5e20",
                                    "section_bg": "transparent",
                                },
                            ),
                            (
                                "section_header",
                                {
                                    "anchor_id": "csapatrol",
                                    "heading": "A Csapatról (HA5KHC)",
                                    "heading_en": "About the Team (HA5KHC)",
                                    "lead_text": (
                                        "A Puskás Tivadar Rádióklub Szakosztálya évtizedek óta a hazai rádiós tájfutás "
                                        "meghatározó alakja. Célunk a sportág népszerűsítése, versenyek szervezése "
                                        "(mint a híres Puskás Kupa), és az utánpótlás nevelése."
                                    ),
                                    "lead_text_en": (
                                        "The Puskás Tivadar Radio Club department has been a leading force in Hungarian ARDF for decades."
                                    ),
                                    "alignment": "left",
                                    "show_underline": False,
                                    "accent_color": "#1b5e20",
                                    "section_bg": "transparent",
                                },
                            ),
                        ],
                        "right_column": [
                            (
                                "highlight_card",
                                {
                                    "anchor_id": "kiemelt-ardf",
                                    "title": "Kiemelt Esemény",
                                    "title_en": "Featured Event",
                                    "meta_info": "Nincs közelgő esemény",
                                    "meta_info_en": "No upcoming event",
                                    "body": "<p>Jelenleg nincs kiemelt versenyünk. Tekintsd meg a versenykiírásokat!</p>",
                                    "body_en": "<p>No featured competition right now. Check the competition notices!</p>",
                                    "accent_color": "#1b5e20",
                                    "section_bg": "transparent",
                                    "button_text": "Versenykiírás és Nevezés",
                                    "button_text_en": "Notices & Entry",
                                    "button_page": None,
                                    "button_anchor": "",
                                },
                            ),
                        ],
                    },
                ),
            ],
        )

        urh_page = get_or_create_flex_page(
            homepage,
            slug="urh-verseny",
            title="URH Verseny",
            theme_color="#800000",
            body_data=[
                (
                    "hero",
                    {
                        "title": "URH Verseny Szakosztály",
                        "title_en": "VHF/UHF Contest Department",
                        "subtitle": "Kitelepülések, magaslatok és távolsági összeköttetések VHF/UHF/SHF sávokon.",
                        "subtitle_en": "Portable activations, hilltops, and DX contacts on VHF/UHF/SHF bands.",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "rich_text",
                    {
                        "content": "<p>Klubunk rendszeresen részt vesz a hazai és nemzetközi URH versenyeken kitelepült állomásokkal.</p>",
                        "content_en": "<p>Our club regularly participates in national and international VHF/UHF contests.</p>",
                        "boxed": True,
                    },
                ),
            ],
        )

        hst_page = get_or_create_flex_page(
            homepage,
            slug="gyors-tavirazs-hst",
            title="Gyors Távírász (HST)",
            theme_color="#800000",
            body_data=[
                (
                    "hero",
                    {
                        "title": "Gyors Távírász (HST)",
                        "title_en": "High Speed Telegraphy (HST)",
                        "subtitle": "Morze vétel, adás és szimulációs versenyszámok felkészítése.",
                        "subtitle_en": "Morse reception, transmission, and radio simulation training.",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "rich_text",
                    {
                        "content": "<p>A gyors távírász szakosztályunk várja mind a kezdő morze tanulókat, mind a versenyzőket.</p>",
                        "content_en": "<p>Our High Speed Telegraphy section welcomes both beginners and experienced competitors.</p>",
                        "boxed": True,
                    },
                ),
            ],
        )

        konstruktor_page = get_or_create_flex_page(
            homepage,
            slug="konstruktori-projektek",
            title="Konstruktőri Projektek",
            theme_color="#4e342e",
            sub_menu=konstruktor_submenu,
            body_data=[
                (
                    "hero",
                    {
                        "title": "Konstruktőri Projektek",
                        "title_en": "Constructor Projects",
                        "subtitle": "Forrasztópáka, antennák, mikrokontrollerek és saját építésű rádiós berendezések.",
                        "subtitle_en": "Soldering irons, antennas, microcontrollers, and homebrew radio equipment.",
                        "background_image": None,
                        "background_color": "#4e342e",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#4e342e",
                        "button_style": "white",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "section_header",
                    {
                        "anchor_id": "muhely-titkai",
                        "heading": "A Műhely Titkai",
                        "heading_en": "Secrets of the Workshop",
                        "lead_text": (
                            "A Puskás Rádióklubban nem csak használjuk a rádiókat, hanem építjük és javítjuk is őket. "
                            "Ebben a rovatban a tagjaink által tervezett áramköröket, felújított készülékeket és saját "
                            "építésű antennákat mutatjuk be, részletes dokumentációval és letölthető segédanyagokkal."
                        ),
                        "lead_text_en": (
                            "At Puskás Radio Club we not only operate radios, we build and repair them too."
                        ),
                        "alignment": "center",
                        "show_underline": False,
                        "accent_color": "#4e342e",
                        "section_bg": "#ffffff",
                    },
                ),
                (
                    "project_item",
                    {
                        "anchor_id": "projekt-urh-antenna",
                        "title": "2m / 70cm Kétsávos Yagi Antenna",
                        "title_en": "2m / 70cm Dual-Band Yagi Antenna",
                        "year_or_author": "2026 | HA5KHC Műhely",
                        "description": "<p>Könnyű, terepi kitelepülésekhez és műholdas összeköttetésekhez optimalizált irányított antenna leírása.</p>",
                        "description_en": "<p>Lightweight directional antenna optimized for portable activations and satellite contacts.</p>",
                        "photos": [],
                        "attachments": [],
                        "accent_color": "#4e342e",
                    },
                ),
            ],
        )

        # Create Versenyek parent page and its 5 required child pages
        versenyek_page = get_or_create_flex_page(
            homepage,
            slug="versenyek",
            title="Versenyek",
            theme_color="#800000",
            sub_menu=verseny_submenu,
            body_data=[
                (
                    "hero",
                    {
                        "title": "Versenyek",
                        "title_en": "Competitions",
                        "subtitle": "Versenykiírások, friss eredmények, képtár, rendezők és korábbi versenyarchívum.",
                        "subtitle_en": "Competition notices, latest results, photos, organizers, and past archive.",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
            ],
        )

        versenykiiras_page = get_or_create_flex_page(
            versenyek_page,
            slug="versenykiiras",
            title="Versenykiírás",
            body_data=[
                (
                    "hero",
                    {
                        "title": "Versenykiírás",
                        "title_en": "Competition Notices",
                        "subtitle": "Aktuális versenykiírások, nevezési határidők és technikai feltételek.",
                        "subtitle_en": "Current competition notices, entry deadlines, and technical rules.",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "highlight_card",
                    {
                        "anchor_id": "kiiras-2026",
                        "title": "Puskás Kupa 2026 – Versenykiírás",
                        "title_en": "Puskás Cup 2026 – Competition Notice",
                        "meta_info": "Rendező: HA5KHC | Helyszín: Budai-hegység",
                        "meta_info_en": "Organizer: HA5KHC | Venue: Buda Hills",
                        "body": "<p>Nevezési határidő és kategóriák hamarosan elérhetőek a dokumentumok között.</p>",
                        "body_en": "<p>Entry deadline and categories will be available soon.</p>",
                        "accent_color": "#800000",
                        "section_bg": "transparent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
            ],
        )

        eredmenyek_page = get_or_create_flex_page(
            versenyek_page,
            slug="eredmenyek",
            title="Eredmények",
            body_data=[
                (
                    "hero",
                    {
                        "title": "Versenyeredmények",
                        "title_en": "Competition Results",
                        "subtitle": "Hivatalos eredménylisták és csapathelyezések.",
                        "subtitle_en": "Official result lists and team standings.",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "highlight_card",
                    {
                        "anchor_id": "puskas-kupa-2026",
                        "title": "Puskás Kupa 2026 – Hivatalos Végeredmény",
                        "title_en": "Puskás Cup 2026 – Official Final Results",
                        "meta_info": "2026-05-12 | Kategória: ARDF / Csapatverseny",
                        "meta_info_en": "2026-05-12 | Category: ARDF / Team Event",
                        "body": (
                            "<p><strong>1. helyezett:</strong> HA5KHC Puskás Rádióklub csapata<br>"
                            "<strong>2. helyezett:</strong> Vendég Csapat A<br>"
                            "<strong>3. helyezett:</strong> Vendég Csapat B</p>"
                        ),
                        "body_en": (
                            "<p><strong>1st Place:</strong> HA5KHC Puskás Radio Club Team<br>"
                            "<strong>2nd Place:</strong> Guest Team A<br>"
                            "<strong>3rd Place:</strong> Guest Team B</p>"
                        ),
                        "accent_color": "#800000",
                        "section_bg": "transparent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
            ],
        )

        verseny_kepek_page = get_or_create_flex_page(
            versenyek_page,
            slug="kepek",
            title="Képek",
            body_data=[
                (
                    "hero",
                    {
                        "title": "Verseny Képtár",
                        "title_en": "Competition Photos",
                        "subtitle": "Pillanatképek a versenyekről és az eredményhirdetésekről.",
                        "subtitle_en": "Snapshots from competitions and award ceremonies.",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "gallery",
                    {
                        "anchor_id": "verseny-album",
                        "album_title": "",
                        "album_title_en": "",
                        "description": "",
                        "description_en": "",
                        "display_mode": "photo_grid",
                        "section_bg": "transparent",
                        "images": [],
                    },
                ),
            ],
        )

        rendezok_page = get_or_create_flex_page(
            versenyek_page,
            slug="rendezok",
            title="Rendezők",
            body_data=[
                (
                    "hero",
                    {
                        "title": "Versenyrendezők",
                        "title_en": "Competition Organizers",
                        "subtitle": "A versenyek lebonyolításáért felelős bírói és szervezői stáb.",
                        "subtitle_en": "Referees and organizing staff responsible for our events.",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "rich_text",
                    {
                        "content": "<p><strong>Főrendező:</strong> HA5KHC Versenybizottság<br><strong>Kapcsolat:</strong> contact@ha5khc.hu</p>",
                        "content_en": "<p><strong>Chief Organizer:</strong> HA5KHC Contest Committee<br><strong>Contact:</strong> contact@ha5khc.hu</p>",
                        "boxed": True,
                    },
                ),
            ],
        )

        archivum_page = get_or_create_flex_page(
            versenyek_page,
            slug="archivum",
            title="Archívum",
            body_data=[
                (
                    "hero",
                    {
                        "title": "Verseny Archívum",
                        "title_en": "Competition Archive",
                        "subtitle": "Korábbi évek versenyeinek jegyzőkönyvei és eredménylistái.",
                        "subtitle_en": "Records and result lists from previous years.",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "documents",
                    {
                        "anchor_id": "archivum-dokumentumok",
                        "categories": [
                            {
                                "category_title": "2025-ös versenyek",
                                "category_title_en": "2025 Competitions",
                                "empty_text": "Még nincs feltöltött archív fájl.",
                                "empty_text_en": "No archived files uploaded yet.",
                                "documents": [],
                            },
                            {
                                "category_title": "2024 és korábbi évek",
                                "category_title_en": "2024 and Earlier",
                                "empty_text": "Még nincs feltöltött archív fájl.",
                                "empty_text_en": "No archived files uploaded yet.",
                                "documents": [],
                            },
                        ],
                    },
                ),
            ],
        )

        # Create BURABU, Galéria, Dokumentumok, and Kapcsolat top-level pages
        burabu_page = get_or_create_flex_page(
            homepage,
            slug="burabu",
            title="BURABU",
            theme_color="#0d47a1",
            sub_menu=burabu_submenu,
            body_data=[
                (
                    "hero",
                    {
                        "title": "BURABU – Budapesti Rádióamatőr Találkozó",
                        "title_en": "BURABU – Budapest Amateur Radio Meeting",
                        "subtitle": "Hagyományos rádióamatőr találkozó, börze és szakmai előadások.",
                        "subtitle_en": "Traditional amateur radio gathering, flea market, and technical talks.",
                        "background_image": None,
                        "background_color": "#0d47a1",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#0d47a1",
                        "button_style": "white",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "rich_text",
                    {
                        "content": "<p>A BURABU programjai és a gyakori kérdések hamarosan frissítésre kerülnek.</p>",
                        "content_en": "<p>BURABU programs and frequently asked questions will be updated soon.</p>",
                        "boxed": True,
                    },
                ),
            ],
        )

        galeria_page = get_or_create_flex_page(
            homepage,
            slug="galeria",
            title="Galéria",
            theme_color="#800000",
            body_data=[
                (
                    "hero",
                    {
                        "title": "Galéria",
                        "title_en": "Gallery",
                        "subtitle": "Klubunk eseményei, versenyei és mindennapjai képekben.",
                        "subtitle_en": "Our club's events, competitions, and daily life in pictures.",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "gallery",
                    {
                        "anchor_id": "klub-galeria",
                        "album_title": "",
                        "album_title_en": "",
                        "description": "",
                        "description_en": "",
                        "display_mode": "photo_grid",
                        "section_bg": "transparent",
                        "images": [],
                    },
                ),
            ],
        )

        dokumentumok_page = get_or_create_flex_page(
            homepage,
            slug="dokumentumok",
            title="Dokumentumok",
            theme_color="#800000",
            body_data=[
                (
                    "hero",
                    {
                        "title": "Hivatalos Dokumentumok",
                        "title_en": "Official Documents",
                        "subtitle": "A Puskás Tivadar Rádióklub hatályos alapszabálya és üléseinek jegyzőkönyvei.",
                        "subtitle_en": "Effective bylaws and meeting minutes of Puskás Tivadar Radio Club.",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "documents",
                    {
                        "anchor_id": "hivatalos-dokumentumok",
                        "categories": [
                            {
                                "category_title": "Hatályos Alapszabály",
                                "category_title_en": "Effective Bylaws",
                                "empty_text": "Jelenleg nincs feltöltve alapszabály.",
                                "empty_text_en": "No bylaws uploaded currently.",
                                "documents": [],
                            },
                            {
                                "category_title": "Közgyűlési Jegyzőkönyvek",
                                "category_title_en": "General Assembly Minutes",
                                "empty_text": "Még nincsenek feltöltött jegyzőkönyvek.",
                                "empty_text_en": "No meeting minutes uploaded yet.",
                                "documents": [],
                            },
                        ],
                    },
                ),
            ],
        )

        kapcsolat_page = get_or_create_flex_page(
            homepage,
            slug="kapcsolat",
            title="Kapcsolat",
            theme_color="#800000",
            body_data=[
                (
                    "hero",
                    {
                        "title": "Kapcsolat",
                        "title_en": "Contact",
                        "subtitle": "Keress minket bizalommal az alábbi elérhetőségeken, vagy látogass el hozzánk személyesen!",
                        "subtitle_en": "Feel free to contact us below or visit us in person!",
                        "background_image": None,
                        "background_color": "#181818",
                        "is_compact": True,
                        "show_bottom_border": True,
                        "accent_color": "#800000",
                        "button_style": "accent",
                        "button_text": "",
                        "button_text_en": "",
                        "button_page": None,
                        "button_anchor": "",
                    },
                ),
                (
                    "two_column",
                    {
                        "ratio": "1fr 1fr",
                        "card_wrapper": True,
                        "left_column": [
                            (
                                "rich_text",
                                {
                                    "content": (
                                        "<h3>Elérhetőségeink</h3>"
                                        "<p><strong>Cím:</strong><br>HA5KHC Puskás Tivadar Rádióamatőr Klub<br>H-1097 Budapest, Gyáli út 22.</p>"
                                        "<p><strong>E-mail:</strong><br><a href='mailto:contact@ha5khc.hu'>contact@ha5khc.hu</a></p>"
                                        "<h3>Klub Támogatása</h3>"
                                        "<p>Köszönjük, ha adód 1%-ával vagy egyéb módon támogatod a klub munkáját!</p>"
                                        "<p><strong>Adószám:</strong> 19005560-1-43<br>"
                                        "<strong>Számlaszám:</strong> 11996217-06207418-10000001</p>"
                                    ),
                                    "content_en": (
                                        "<h3>Contact Details</h3>"
                                        "<p><strong>Address:</strong><br>HA5KHC Puskás Tivadar Radio Amateur Club<br>H-1097 Budapest, Gyáli út 22.</p>"
                                        "<p><strong>E-mail:</strong><br><a href='mailto:contact@ha5khc.hu'>contact@ha5khc.hu</a></p>"
                                        "<h3>Support the Club</h3>"
                                        "<p>Thank you for supporting our club's work with 1% of your tax or other donations!</p>"
                                        "<p><strong>Tax ID:</strong> 19005560-1-43<br>"
                                        "<strong>Bank Account:</strong> 11996217-06207418-10000001</p>"
                                    ),
                                    "boxed": False,
                                },
                            ),
                        ],
                        "right_column": [
                            (
                                "map_embed",
                                {
                                    "embed_url": "https://www.google.com/maps?q=1097+Budapest,+Gy%C3%A1li+%C3%BAt+22.&output=embed",
                                    "height": 380,
                                },
                            ),
                        ],
                    },
                ),
            ],
        )

        # Populate SubMenu items for Versenyek, ARDF, Konstruktőr, and BURABU
        verseny_submenu.items.all().delete()
        for idx, (hu, en, pg) in enumerate(
            [
                ("Versenykiírás", "Notices", versenykiiras_page),
                ("Eredmények", "Results", eredmenyek_page),
                ("Képek", "Photos", verseny_kepek_page),
                ("Rendezők", "Organizers", rendezok_page),
                ("Archívum", "Archive", archivum_page),
            ]
        ):
            SubMenuItem.objects.create(menu=verseny_submenu, title=hu, title_en=en, link_page=pg, sort_order=idx)

        ardf_submenu.items.all().delete()
        for idx, (hu, en, pg, anc) in enumerate(
            [
                ("A sportágról", "About Sport", ardf_page, "sportagrol"),
                ("Versenyek", "Competitions", versenykiiras_page, ""),
                ("Eredmények", "Results", eredmenyek_page, ""),
                ("Képtár", "Gallery", verseny_kepek_page, ""),
            ]
        ):
            SubMenuItem.objects.create(
                menu=ardf_submenu, title=hu, title_en=en, link_page=pg, anchor=anc, sort_order=idx
            )

        konstruktor_submenu.items.all().delete()
        for idx, (hu, en, pg, anc) in enumerate(
            [
                ("Projektek és Leírások", "Projects & Docs", konstruktor_page, "projekt-urh-antenna"),
                ("Képtár", "Gallery", galeria_page, ""),
            ]
        ):
            SubMenuItem.objects.create(
                menu=konstruktor_submenu, title=hu, title_en=en, link_page=pg, anchor=anc, sort_order=idx
            )

        burabu_submenu.items.all().delete()
        SubMenuItem.objects.create(
            menu=burabu_submenu, title="Áttekintés", title_en="Overview", link_page=burabu_page, sort_order=0
        )

        # Rebuild top navigation MenuItems in the exact requested order
        MenuItem.objects.all().delete()

        MenuItem.objects.create(title="Főoldal", title_en="Home", link_page=homepage, sort_order=1)

        szakosztalyok_menu = MenuItem.objects.create(
            title="Szakosztályok", title_en="Departments", link_page=None, sort_order=2
        )
        MenuItem.objects.create(
            title="Rádiós Tájfutás (ARDF)",
            title_en="Radio Orienteering (ARDF)",
            link_page=ardf_page,
            parent=szakosztalyok_menu,
            sort_order=1,
        )
        MenuItem.objects.create(
            title="URH Verseny",
            title_en="VHF/UHF Contest",
            link_page=urh_page,
            parent=szakosztalyok_menu,
            sort_order=2,
        )
        MenuItem.objects.create(
            title="Gyors Távírász (HST)",
            title_en="High Speed Telegraphy (HST)",
            link_page=hst_page,
            parent=szakosztalyok_menu,
            sort_order=3,
        )
        MenuItem.objects.create(
            title="Konstruktőri Projektek",
            title_en="Constructor Projects",
            link_page=konstruktor_page,
            parent=szakosztalyok_menu,
            sort_order=4,
        )

        versenyek_menu = MenuItem.objects.create(
            title="Versenyek", title_en="Competitions", link_page=versenyek_page, sort_order=3
        )
        MenuItem.objects.create(
            title="Versenykiírás",
            title_en="Notices",
            link_page=versenykiiras_page,
            parent=versenyek_menu,
            sort_order=1,
        )
        MenuItem.objects.create(
            title="Eredmények",
            title_en="Results",
            link_page=eredmenyek_page,
            parent=versenyek_menu,
            sort_order=2,
        )
        MenuItem.objects.create(
            title="Képek",
            title_en="Photos",
            link_page=verseny_kepek_page,
            parent=versenyek_menu,
            sort_order=3,
        )
        MenuItem.objects.create(
            title="Rendezők",
            title_en="Organizers",
            link_page=rendezok_page,
            parent=versenyek_menu,
            sort_order=4,
        )
        MenuItem.objects.create(
            title="Archívum",
            title_en="Archive",
            link_page=archivum_page,
            parent=versenyek_menu,
            sort_order=5,
        )

        MenuItem.objects.create(title="BURABU", title_en="BURABU", link_page=burabu_page, sort_order=4)
        MenuItem.objects.create(title="Galéria", title_en="Gallery", link_page=galeria_page, sort_order=5)
        MenuItem.objects.create(title="Dokumentumok", title_en="Documents", link_page=dokumentumok_page, sort_order=6)
        MenuItem.objects.create(title="Kapcsolat", title_en="Contact", link_page=kapcsolat_page, sort_order=7)

        # Link HomePage news card button directly to the Puskás Kupa 2026 result anchor
        updated_body = []
        for block in homepage.body:
            if block.block_type == "highlight_card":
                val = dict(block.value)
                val["button_text"] = "Eredmények megtekintése →"
                val["button_text_en"] = "View Results →"
                val["button_page"] = eredmenyek_page
                val["button_anchor"] = "puskas-kupa-2026"
                updated_body.append(("highlight_card", val))
            elif block.block_type == "hero" and block.value.get("button_style") == "white":
                val = dict(block.value)
                val["button_page"] = kapcsolat_page
                updated_body.append(("hero", val))
            else:
                updated_body.append((block.block_type, block.value))

        homepage.body = updated_body
        rev = homepage.save_revision()
        rev.publish()

        self.stdout.write(self.style.SUCCESS("Subpages, submenus, main menu, and news anchor links populated!"))