# Import Django and Wagtail model, panel, and snippet viewset components
from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

# Import custom modular content blocks
from home.blocks import (
    HeroBlock,
    SectionHeaderBlock,
    BilingualRichTextBlock,
    HighlightCardBlock,
    NewsFeedBlock,
    CardGridBlock,
    TwoColumnLayoutBlock,
    DocumentListBlock,
    GalleryBlock,
    MapEmbedBlock,
    ProjectItemBlock,
)


# Shared block definitions available on both HomePage and FlexPage
PAGE_STREAM_BLOCKS = [
    ("hero", HeroBlock()),
    ("section_header", SectionHeaderBlock()),
    ("rich_text", BilingualRichTextBlock()),
    ("highlight_card", HighlightCardBlock()),
    ("news_feed", NewsFeedBlock()),
    ("two_column", TwoColumnLayoutBlock()),
    ("card_grid", CardGridBlock()),
    ("documents", DocumentListBlock()),
    ("gallery", GalleryBlock()),
    ("map_embed", MapEmbedBlock()),
    ("project_item", ProjectItemBlock()),
]

# Theme color choices for subpage navigation bars and accents
PAGE_THEME_CHOICES = [
    ("", "Inherit from Parent (Default Maroon #800000)"),
    ("#800000", "Club Maroon (#800000)"),
    ("#1b5e20", "ARDF Green (#1b5e20)"),
    ("#4e342e", "Constructor Brown (#4e342e)"),
    ("#0d47a1", "BURABU Blue (#0d47a1)"),
    ("#1e1e1e", "Dark Charcoal (#1e1e1e)"),
]


# Reusable subpage navigation menu snippet managed per department or competition
@register_snippet
class SubMenu(ClusterableModel):
    # Descriptive internal name for the submenu group
    name = models.CharField(max_length=100, help_text="Internal name (e.g. HST Puskás Kupa almenü)")

    panels = [
        FieldPanel("name"),
        InlinePanel("items", label="Submenu Links"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subpage Menu"
        verbose_name_plural = "Subpage Menus"


# Individual link item belonging to a SubMenu snippet
class SubMenuItem(Orderable):
    # Parent submenu container
    menu = ParentalKey(SubMenu, on_delete=models.CASCADE, related_name="items")
    # Hungarian link label
    title = models.CharField(max_length=100)
    # Optional English link label
    title_en = models.CharField(max_length=100, blank=True, null=True)
    # Target internal Wagtail page
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    # Optional section anchor ID on target page
    anchor = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional anchor ID without # (e.g. results-2026)",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("title_en"),
        FieldPanel("link_page"),
        FieldPanel("anchor"),
    ]


# Base HomePage model
class HomePage(Page):
    # StreamField container for homepage dynamic content
    body = StreamField(
        PAGE_STREAM_BLOCKS,
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


# Flexible modular page with inheritable theme colors and subpage menus
class FlexPage(Page):
    # Optional theme color override for subpage bar and visual accents
    theme_color = models.CharField(
        max_length=20,
        choices=PAGE_THEME_CHOICES,
        blank=True,
        default="",
        help_text="Select a theme color or leave empty to inherit from parent page",
    )
    # Optional subpage navigation menu displayed below main header
    sub_menu = models.ForeignKey(
        SubMenu,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pages",
        help_text="Select a subpage menu or leave empty to inherit from parent page",
    )
    # Dynamic streamfield for creating custom layouts block by block
    body = StreamField(
        PAGE_STREAM_BLOCKS,
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("theme_color"),
                FieldPanel("sub_menu"),
            ],
            heading="Subpage Theme & Navigation",
        ),
        FieldPanel("body"),
    ]

    # Resolve theme color from current page or nearest ancestor FlexPage
    def get_effective_theme_color(self):
        if self.theme_color:
            return self.theme_color
        for ancestor in self.get_ancestors().specific().reverse():
            if hasattr(ancestor, "theme_color") and ancestor.theme_color:
                return ancestor.theme_color
        return "#800000"

    # Resolve submenu from current page or nearest ancestor FlexPage
    def get_effective_sub_menu(self):
        if self.sub_menu:
            return self.sub_menu
        for ancestor in self.get_ancestors().specific().reverse():
            if hasattr(ancestor, "sub_menu") and ancestor.sub_menu:
                return ancestor.sub_menu
        return None


# Snippet model for top navigation menu items and dropdown hierarchy
class MenuItem(models.Model):
    # Hungarian title displayed in navigation
    title = models.CharField(max_length=100, help_text="Hungarian menu title")
    # English title displayed in navigation
    title_en = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="English menu title (optional, falls back to Hungarian)",
    )
    # Destination page linked to this menu item
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Leave empty if this item is only a group header/dropdown",
    )
    # Optional parent menu item to create dropdown levels
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        help_text="Select a parent item to place this under a dropdown group",
    )
    # Ordering index for top navigation
    sort_order = models.IntegerField(default=0, help_text="Order in menu bar (e.g. 1, 2, 3)")

    panels = [
        FieldPanel("title"),
        FieldPanel("title_en"),
        FieldPanel("link_page"),
        FieldPanel("parent"),
        FieldPanel("sort_order"),
    ]

    # Display linked target page title in admin overview
    def link_page_display(self):
        return self.link_page.title if self.link_page else "-"

    link_page_display.short_description = "Link Page"

    # Display parent page of the linked target page in admin overview
    def parent_page_display(self):
        if self.link_page:
            parent_page = self.link_page.get_parent()
            if parent_page and parent_page.depth > 1:
                return parent_page.title
        return "-"

    parent_page_display.short_description = "Parent Page"

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"


# Custom SnippetViewSet exposing link_page and parent page columns in list view
class MenuItemViewSet(SnippetViewSet):
    model = MenuItem
    icon = "list-ul"
    list_display = ["title", "link_page_display", "parent_page_display", "sort_order"]
    list_filter = ["parent"]
    search_fields = ["title", "title_en"]


register_snippet(MenuItem, viewset=MenuItemViewSet)


# Standalone news post model managed through its own Wagtail Admin window
class NewsPost(ClusterableModel):
    # Hungarian post headline
    title = models.CharField(max_length=200, verbose_name="Title (HU)")
    # Optional English post headline
    title_en = models.CharField(max_length=200, blank=True, null=True, verbose_name="Title (EN)")
    # Publication date displayed on post card
    published_date = models.DateField(default=timezone.now, verbose_name="Publication Date")
    # Optional author or department attribution
    author = models.CharField(max_length=100, blank=True, default="HA5KHC", verbose_name="Author / Division")
    # Optional featured cover image
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Cover Image",
    )
    # Optional short lead summary in Hungarian
    summary = models.TextField(blank=True, verbose_name="Short Summary (HU)")
    # Optional short lead summary in English
    summary_en = models.TextField(blank=True, verbose_name="Short Summary (EN)")
    # Full rich text body supporting inline links to any subpage
    body = RichTextField(verbose_name="Post Content (HU)")
    # Optional English rich text body
    body_en = RichTextField(blank=True, verbose_name="Post Content (EN)")
    # Left border and button accent color
    accent_color = models.CharField(
        max_length=20,
        choices=[
            ("#800000", "Club Maroon (#800000)"),
            ("#1b5e20", "ARDF Green (#1b5e20)"),
            ("#4e342e", "Constructor Brown (#4e342e)"),
            ("#0d47a1", "BURABU Blue (#0d47a1)"),
            ("#1e1e1e", "Dark Charcoal (#1e1e1e)"),
        ],
        default="#800000",
        verbose_name="Accent Color",
    )
    # Toggle to pin important announcements to the top of the news feed
    is_pinned = models.BooleanField(default=False, verbose_name="Pin to Top")
    # Toggle to control public visibility
    is_published = models.BooleanField(default=True, verbose_name="Published")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("title_en"),
                FieldPanel("published_date"),
                FieldPanel("author"),
                FieldPanel("cover_image"),
            ],
            heading="Post Header & Metadata",
        ),
        MultiFieldPanel(
            [
                FieldPanel("summary"),
                FieldPanel("summary_en"),
                FieldPanel("body"),
                FieldPanel("body_en"),
            ],
            heading="Post Content",
        ),
        InlinePanel("subpage_links", label="Subpage Action Links (Results, Rules, Galleries, etc.)"),
        MultiFieldPanel(
            [
                FieldPanel("accent_color"),
                FieldPanel("is_pinned"),
                FieldPanel("is_published"),
            ],
            heading="Appearance & Publishing",
        ),
    ]

    # Display linked subpages summary in admin table
    def linked_subpages_display(self):
        links = [link.target_page.title for link in self.subpage_links.all() if link.target_page]
        return ", ".join(links) if links else "-"

    linked_subpages_display.short_description = "Linked Subpages"

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-is_pinned", "-published_date", "-id"]
        verbose_name = "News Post"
        verbose_name_plural = "News Posts"


# Action button link connecting a NewsPost to any internal subpage and optional anchor
class NewsPostLink(Orderable):
    # Parent news post
    post = ParentalKey(NewsPost, on_delete=models.CASCADE, related_name="subpage_links")
    # Hungarian button label
    label = models.CharField(max_length=100, help_text="Button text in Hungarian (e.g. Eredmények megtekintése)")
    # Optional English button label
    label_en = models.CharField(max_length=100, blank=True, null=True, help_text="Button text in English")
    # Target internal Wagtail subpage
    target_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Target Subpage",
    )
    # Optional section anchor on target subpage
    anchor = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional section anchor without #",
    )

    panels = [
        FieldPanel("label"),
        FieldPanel("label_en"),
        FieldPanel("target_page"),
        FieldPanel("anchor"),
    ]


# Dedicated Wagtail Admin menu viewset for creating and managing NewsPost items
class NewsPostViewSet(SnippetViewSet):
    model = NewsPost
    icon = "doc-full-inverse"
    menu_label = "News Posts"
    menu_name = "news_posts"
    menu_order = 250
    add_to_admin_menu = True
    list_display = ["title", "published_date", "author", "linked_subpages_display", "is_pinned", "is_published"]
    list_filter = ["is_published", "is_pinned", "published_date"]
    search_fields = ["title", "title_en", "summary", "author"]


register_snippet(NewsPost, viewset=NewsPostViewSet)


# Editable footer settings configuration snippet with translation fields
@register_snippet
class FooterSettings(models.Model):
    # Announcement bar text
    top_bar_text = models.CharField(
        max_length=255,
        default="Kérjük, támogassa a Puskás Rádióklubot adója 1%-ával! Adószám: 19005560-1-43",
    )
    top_bar_text_en = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="Please support Puskás Radio Club with 1% of your tax! Tax ID: 19005560-1-43",
    )

    # Column 1 details
    col1_title = models.CharField(max_length=100, default="PUSKÁS TIVADAR RÁDIÓKLUB")
    col1_title_en = models.CharField(max_length=100, default="PUSKÁS TIVADAR RADIO CLUB")
    col1_text = models.TextField(default="Hagyomány és modern technika a rádióamatőr közösségért.")
    col1_text_en = models.TextField(default="Tradition and modern technology for the radio amateur community.")
    col1_address = models.CharField(max_length=255, default="1097 Budapest, Gyáli út 22.")
    col1_clubdays = models.CharField(max_length=255, default="Hétfő/Péntek: 16:00 - 19:00")
    col1_clubdays_en = models.CharField(max_length=255, default="Monday/Friday: 16:00 - 19:00")

    # Column 2 details
    col2_title = models.CharField(max_length=100, default="GYORSLINKEK")
    col2_title_en = models.CharField(max_length=100, default="QUICK LINKS")
    col2_links_text = models.TextField(default="MRASZ|https://mrasz.hu\nRégi Weboldal|#\nViacom Kft. (támogatónk)|#")
    col2_links_text_en = models.TextField(default="MRASZ|https://mrasz.hu\nOld Website|#\nViacom Kft. (sponsor)|#")

    # Column 3 details
    col3_title = models.CharField(max_length=100, default="TÁMOGASSON MINKET!")
    col3_title_en = models.CharField(max_length=100, default="SUPPORT US!")
    col3_text = models.TextField(default="Adója 1%-ával sokat segíthet az utánpótlás nevelésében és a klub fenntartásában.")
    col3_text_en = models.TextField(default="Your 1% tax donation helps youth training and club operations.")
    col3_tax_number = models.CharField(max_length=100, default="19005560-1-43")

    # Copyright info
    copyright_text = models.CharField(
        max_length=255,
        default="© 2026 HA5KHC Puskás Tivadar rádióklub. Minden jog fenntartva.",
    )
    copyright_text_en = models.CharField(
        max_length=255,
        default="© 2026 HA5KHC Puskás Tivadar Radio Club. All rights reserved.",
    )

    panels = [
        FieldPanel("top_bar_text"),
        FieldPanel("top_bar_text_en"),
        FieldPanel("col1_title"),
        FieldPanel("col1_title_en"),
        FieldPanel("col1_text"),
        FieldPanel("col1_text_en"),
        FieldPanel("col1_address"),
        FieldPanel("col1_clubdays"),
        FieldPanel("col1_clubdays_en"),
        FieldPanel("col2_title"),
        FieldPanel("col2_title_en"),
        FieldPanel("col2_links_text"),
        FieldPanel("col2_links_text_en"),
        FieldPanel("col3_title"),
        FieldPanel("col3_title_en"),
        FieldPanel("col3_text"),
        FieldPanel("col3_text_en"),
        FieldPanel("col3_tax_number"),
        FieldPanel("copyright_text"),
        FieldPanel("copyright_text_en"),
    ]

    def get_col2_links(self, current_lang="hu"):
        links = []
        raw_text = self.col2_links_text_en if (current_lang == "en" and self.col2_links_text_en) else self.col2_links_text
        if raw_text:
            lines = raw_text.strip().split("\n")
            for line in lines:
                if "|" in line:
                    title, url = line.split("|", 1)
                    links.append({"title": title.strip(), "url": url.strip()})
        return links

    def __str__(self):
        return "Footer Settings"

    class Meta:
        verbose_name = "Footer Settings"
        verbose_name_plural = "Footer Settings"