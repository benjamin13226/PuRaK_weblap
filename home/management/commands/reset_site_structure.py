# Import Django management command utilities and project models
from django.core.management.base import BaseCommand
from home.models import HomePage, FlexPage, MenuItem, SubMenu, SubMenuItem


class Command(BaseCommand):
    # CLI command description
    help = "Deletes existing FlexPage instances, MenuItems, and SubMenus, then builds a clean site structure."

    def create_page(self, parent, title, slug, theme_color="", sub_menu=None, body=None):
        # Instantiate, attach, and publish a FlexPage with optional theme, submenu, and StreamField blocks
        page = FlexPage(
            title=title,
            slug=slug,
            theme_color=theme_color,
            sub_menu=sub_menu,
            body=body or [],
        )
        parent.add_child(instance=page)
        page.save_revision().publish()
        return page

    def build_header_blocks(self, title_hu, title_en, subtitle_hu, subtitle_en, accent_color="#800000"):
        # Generate standard compact page header and section intro blocks
        return [
            (
                "hero",
                {
                    "title": title_hu,
                    "title_en": title_en,
                    "subtitle": subtitle_hu,
                    "subtitle_en": subtitle_en,
                    "background_color": "#181818",
                    "is_compact": True,
                    "show_bottom_border": True,
                    "accent_color": accent_color,
                },
            ),
        ]

    def handle(self, *args, **options):
        # Retrieve the root HomePage instance
        home_page = HomePage.objects.first()
        if not home_page:
            self.stdout.write(self.style.ERROR("HomePage not found in database."))
            return

        # Clear existing navigation snippets and submenus
        MenuItem.objects.all().delete()
        SubMenu.objects.all().delete()

        # Delete all existing FlexPage trees under HomePage
        for child in home_page.get_children().specific():
            if isinstance(child, FlexPage):
                child.delete()

        # Refresh HomePage tree pointers from database
        home_page = HomePage.objects.get(pk=home_page.pk)

        # 1. Create Főoldal menu item
        MenuItem.objects.create(
            title="Főoldal",
            title_en="Home",
            link_page=home_page,
            parent=None,
            sort_order=1,
        )

        # 2. Create Szakosztályok container and dropdown menu
        departments_root = self.create_page(
            home_page,
            "Szakosztályok",
            "szakosztalyok",
            body=self.build_header_blocks(
                "Szakosztályok",
                "Departments",
                "A HA5KHC Puskás Tivadar Rádióklub szakmai műhelyei és sportágai",
                "Technical workshops and radio sport divisions of HA5KHC",
            ),
        )
        departments_menu = MenuItem.objects.create(
            title="Szakosztályok",
            title_en="Departments",
            link_page=None,
            parent=None,
            sort_order=2,
        )

        # Define departments with tailored themes and starter blocks
        departments_spec = [
            (
                "Gyorstávirász",
                "High-Speed Telegraphy (HST)",
                "gyorstavirasz",
                "#800000",
                self.build_header_blocks(
                    "Gyorstávirász szakosztály",
                    "High-Speed Telegraphy Department",
                    "Morze vétel, adás és számítógépes gyorstávírász felkészítés",
                    "Morse reception, transmission, and HST training",
                    "#800000",
                )
                + [
                    (
                        "rich_text",
                        {
                            "content": "<p>A gyorstávírász szakosztályban a klasszikus morze billentyűzés és a nagy sebességű távíró vétel alapjaitól a nemzetközi versenyfelkészítésig foglalkozunk az utánpótlással és a felnőtt versenyzőkkel.</p>",
                            "content_en": "<p>Our High-Speed Telegraphy division trains both youth and adult competitors from basic Morse keying to international contest preparation.</p>",
                            "boxed": True,
                        },
                    ),
                ],
            ),
            (
                "Rádió iránymérés",
                "Radio Direction Finding (ARDF)",
                "radio-iranymeres",
                "#1b5e20",
                self.build_header_blocks(
                    "Rádió iránymérő (ARDF) szakosztály",
                    "Amateur Radio Direction Finding (ARDF)",
                    "Tájfutás és rádiótechnika találkozása terepen, 80 m-es és 2 m-es sávon",
                    "Orienteering meets radio engineering on 80m and 2m bands",
                    "#1b5e20",
                )
                + [
                    (
                        "highlight_card",
                        {
                            "title": "Mi az a rádiós tájfutás?",
                            "title_en": "What is Amateur Radio Direction Finding?",
                            "meta_info": "ARDF Szakosztály • Terepi edzések",
                            "meta_info_en": "ARDF Division • Field Training",
                            "body": "<p>A versenyzők térkép, tájoló és speciális iránymérő vevőkészülék segítségével keresik meg az erdőben elrejtett rókaadókat a lehető legrövidebb idő alatt.</p>",
                            "body_en": "<p>Competitors use a map, compass, and direction-finding receiver to locate hidden fox transmitters in the forest in the shortest possible time.</p>",
                            "accent_color": "#1b5e20",
                        },
                    ),
                ],
            ),
            (
                "Forgalmazás",
                "Radio Operating",
                "forgalmazas",
                "#1e1e1e",
                self.build_header_blocks(
                    "Forgalmazási szakosztály",
                    "Radio Operating Department",
                    "Rövidhullámú, URH és digitális üzemmódú összeköttetések a klubállomásról",
                    "HF, VHF/UHF, and digital mode operations from the club station",
                    "#1e1e1e",
                )
                + [
                    (
                        "rich_text",
                        {
                            "content": "<p>A HA5KHC klubállomásán lehetőség van rövidhullámú (HF), ultrarövidhullámú (VHF/UHF) és műholdas összeköttetések létesítésére, valamint QSL-lapok kezelésére és kitelepülések szervezésére.</p>",
                            "content_en": "<p>At the HA5KHC club station, members operate HF, VHF/UHF, and satellite communications, manage QSL cards, and organize portable field days.</p>",
                            "boxed": True,
                        },
                    ),
                ],
            ),
            (
                "Konstruktőr",
                "Construction & Homebrew",
                "konstruktor",
                "#4e342e",
                self.build_header_blocks(
                    "Konstruktőri szakosztály",
                    "Construction & Homebrew Department",
                    "Antennák, adó-vevők, mérőműszerek tervezése és építése a klub műhelyében",
                    "Designing and building antennas, transceivers, and test gear",
                    "#4e342e",
                )
                + [
                    (
                        "project_item",
                        {
                            "title": "80m-es ARDF Rókaadó és Vevő fejlesztés",
                            "title_en": "80m ARDF Fox Transmitter & Receiver Build",
                            "year_or_author": "HA5KHC Műhely",
                            "description": "<p>Saját tervezésű, terepi körülményekre optimalizált iránymérő vevők és automatikus vezérlésű rókaadók építése klubtagok részvételével.</p>",
                            "description_en": "<p>Custom-designed field-ready direction finding receivers and automated fox transmitters built by club members.</p>",
                            "photos": [],
                            "attachments": [],
                            "accent_color": "#4e342e",
                        },
                    ),
                ],
            ),
        ]

        for idx, (title_hu, title_en, slug, theme_color, body_blocks) in enumerate(departments_spec, start=1):
            dept_page = self.create_page(
                departments_root,
                title_hu,
                slug,
                theme_color=theme_color,
                body=body_blocks,
            )
            MenuItem.objects.create(
                title=title_hu,
                title_en=title_en,
                link_page=dept_page,
                parent=departments_menu,
                sort_order=idx,
            )

        # 3. Create Versenyek container and dropdown menu
        competitions_root = self.create_page(
            home_page,
            "Versenyek",
            "versenyek",
            body=self.build_header_blocks(
                "Versenyek",
                "Competitions",
                "A Puskás Tivadar Rádióklub által rendezett kupák és versenyek",
                "Cups and radio sport competitions organized by Puskás Radio Club",
            ),
        )
        competitions_menu = MenuItem.objects.create(
            title="Versenyek",
            title_en="Competitions",
            link_page=None,
            parent=None,
            sort_order=3,
        )

        # Define the four competitions and their five individual subpages
        competitions_spec = [
            ("HST Puskás Kupa", "HST Puskás Cup", "hst-puskas-kupa", "#800000"),
            ("RTF Puskás Kupa", "ARDF Puskás Cup", "rtf-puskas-kupa", "#1b5e20"),
            ("URH Puskás Kupa", "VHF/UHF Puskás Cup", "urh-puskas-kupa", "#800000"),
            ("RH Puskás Kupa", "HF Puskás Cup", "rh-puskas-kupa", "#800000"),
        ]
        subpage_templates = [
            (
                "Versenykiírás",
                "Rules & Announcement",
                "versenykiiras",
                "<p>A verseny hivatalos kiírása, nevezési feltételei, időpontja és kategóriái itt szerkeszthetők.</p>",
                "<p>Official competition rules, entry requirements, schedule, and categories can be edited here.</p>",
            ),
            (
                "Eredmények",
                "Results",
                "eredmenyek",
                "<p>Az aktuális verseny hivatalos eredménylistája és kategóriánkénti helyezései.</p>",
                "<p>Official results and category standings for the current competition.</p>",
            ),
            (
                "Képek",
                "Photos",
                "kepek",
                "<p>A versenyen készült fotók és galériák gyűjteménye.</p>",
                "<p>Photo albums and event pictures from the competition.</p>",
            ),
            (
                "Rendezők",
                "Organizers",
                "rendezok",
                "<p>A verseny rendezőbizottsága, versenybírósága és elérhetőségei.</p>",
                "<p>Organizing committee, jury members, and contact details.</p>",
            ),
            (
                "Archívum",
                "Archive",
                "archivum",
                "<p>Korábbi évek versenykiírásai, jegyzőkönyvei és eredménylistái.</p>",
                "<p>Announcements, logs, and results from previous years.</p>",
            ),
        ]

        # Generate each competition with its dedicated SubMenu and 5 separate subpages
        for comp_idx, (comp_hu, comp_en, comp_slug, comp_color) in enumerate(competitions_spec, start=1):
            comp_submenu = SubMenu.objects.create(name=f"{comp_hu} almenü")
            comp_page = self.create_page(
                competitions_root,
                comp_hu,
                comp_slug,
                theme_color=comp_color,
                sub_menu=comp_submenu,
                body=self.build_header_blocks(
                    comp_hu,
                    comp_en,
                    "Válassz a fenti almenüpontok közül (Versenykiírás, Eredmények, Képek, Rendezők, Archívum)",
                    "Select from the submenu above (Rules, Results, Photos, Organizers, Archive)",
                    comp_color,
                ),
            )
            comp_menu = MenuItem.objects.create(
                title=comp_hu,
                title_en=comp_en,
                link_page=comp_page,
                parent=competitions_menu,
                sort_order=comp_idx,
            )

            for sub_idx, (sub_hu, sub_en, sub_slug, text_hu, text_en) in enumerate(subpage_templates, start=1):
                sub_body = self.build_header_blocks(
                    f"{comp_hu} – {sub_hu}",
                    f"{comp_en} – {sub_en}",
                    comp_hu,
                    comp_en,
                    comp_color,
                )
                if sub_slug == "kepek":
                    sub_body.append(
                        (
                            "gallery",
                            {
                                "album_title": f"{comp_hu} galéria",
                                "album_title_en": f"{comp_en} Gallery",
                                "display_mode": "photo_grid",
                                "images": [],
                            },
                        )
                    )
                else:
                    sub_body.append(
                        (
                            "rich_text",
                            {
                                "content": text_hu,
                                "content_en": text_en,
                                "boxed": True,
                            },
                        )
                    )

                # Subpages inherit theme_color and sub_menu automatically from comp_page
                sub_page = self.create_page(
                    comp_page,
                    sub_hu,
                    sub_slug,
                    body=sub_body,
                )
                SubMenuItem.objects.create(
                    menu=comp_submenu,
                    title=sub_hu,
                    title_en=sub_en,
                    link_page=sub_page,
                    sort_order=sub_idx,
                )
                MenuItem.objects.create(
                    title=sub_hu,
                    title_en=sub_en,
                    link_page=sub_page,
                    parent=comp_menu,
                    sort_order=sub_idx,
                )

        # 4. Create BURABU as a plain, unconfigured page without extra settings
        burabu_page = self.create_page(home_page, "BURABU", "burabu")
        MenuItem.objects.create(
            title="BURABU",
            title_en="BURABU",
            link_page=burabu_page,
            parent=None,
            sort_order=4,
        )

        # 5. Create Galéria standalone page
        gallery_page = self.create_page(
            home_page,
            "Galéria",
            "galeria",
            body=self.build_header_blocks(
                "Galéria",
                "Gallery",
                "Képek a klub életéből, kitelepülésekről és rendezvényekről",
                "Photos from club life, field days, and events",
            )
            + [
                (
                    "gallery",
                    {
                        "album_title": "Klubélet és események",
                        "album_title_en": "Club Life & Events",
                        "display_mode": "photo_grid",
                        "images": [],
                    },
                )
            ],
        )
        MenuItem.objects.create(
            title="Galéria",
            title_en="Gallery",
            link_page=gallery_page,
            parent=None,
            sort_order=5,
        )

        # 6. Create Dokumentumok standalone page
        documents_page = self.create_page(
            home_page,
            "Dokumentumok",
            "dokumentumok",
            body=self.build_header_blocks(
                "Dokumentumok",
                "Documents",
                "Hivatalos klubdokumentumok, alapszabály és közgyűlési jegyzőkönyvek",
                "Official club documents, statutes, and meeting minutes",
            )
            + [
                (
                    "documents",
                    {
                        "categories": [
                            {
                                "category_title": "Alapszabály és Szervezeti dokumentumok",
                                "category_title_en": "Statutes & Organizational Documents",
                                "documents": [],
                            },
                            {
                                "category_title": "Közgyűlési jegyzőkönyvek és beszámolók",
                                "category_title_en": "Assembly Minutes & Reports",
                                "documents": [],
                            },
                        ]
                    },
                )
            ],
        )
        MenuItem.objects.create(
            title="Dokumentumok",
            title_en="Documents",
            link_page=documents_page,
            parent=None,
            sort_order=6,
        )

        # 7. Create Kapcsolat standalone page
        contact_page = self.create_page(
            home_page,
            "Kapcsolat",
            "kapcsolat",
            body=self.build_header_blocks(
                "Kapcsolat",
                "Contact",
                "Elérhetőségeink, klubnapok és megközelítés",
                "Contact details, club days, and location",
            )
            + [
                (
                    "two_column",
                    {
                        "ratio": "1fr 1fr",
                        "card_wrapper": True,
                        "left_column": [
                            (
                                "rich_text",
                                {
                                    "content": "<h3>HA5KHC Puskás Tivadar Rádióklub</h3><p><strong>Cím:</strong> 1097 Budapest, Gyáli út 22.</p><p><strong>Klubnap:</strong> Hétfő / Péntek: 16:00 - 19:00</p><p><strong>Adószám:</strong> 19005560-1-43</p>",
                                    "content_en": "<h3>HA5KHC Puskás Tivadar Radio Club</h3><p><strong>Address:</strong> 1097 Budapest, Gyáli út 22.</p><p><strong>Club Days:</strong> Monday / Friday: 16:00 - 19:00</p><p><strong>Tax ID:</strong> 19005560-1-43</p>",
                                    "boxed": False,
                                },
                            )
                        ],
                        "right_column": [
                            (
                                "map_embed",
                                {
                                    "embed_url": "https://www.google.com/maps?q=1097+Budapest,+Gy%C3%A1li+%C3%BAt+22.&output=embed",
                                    "height": 320,
                                },
                            )
                        ],
                    },
                )
            ],
        )
        MenuItem.objects.create(
            title="Kapcsolat",
            title_en="Contact",
            link_page=contact_page,
            parent=None,
            sort_order=7,
        )

        self.stdout.write(self.style.SUCCESS("Site pages, submenus, and navigation menu successfully reset and regenerated."))