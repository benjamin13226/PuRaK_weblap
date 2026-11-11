# Import Django and Wagtail model components
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.snippets.models import register_snippet

# Import custom content blocks
from home.blocks import HeroBlock, CardGridBlock


# Base HomePage model
class HomePage(Page):
    # StreamField container for homepage dynamic content
    body = StreamField(
        [
            ('hero', HeroBlock()),
            ('rich_text', blocks.RichTextBlock()),
            ('card_grid', CardGridBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


# Flexible modular page for dynamic user creation
class FlexPage(Page):
    # Dynamic streamfield for creating custom layouts block by block
    body = StreamField(
        [
            ('hero', HeroBlock()),
            ('rich_text', blocks.RichTextBlock(label="Formatted Text")),
            ('card_grid', CardGridBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


# Clean snippet model for menu items and submenus with English translation support
@register_snippet
class MenuItem(models.Model):
    # Hungarian title displayed in navigation
    title = models.CharField(max_length=100, help_text="Hungarian menu title")
    # English title displayed in navigation
    title_en = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="English menu title (optional, falls back to Hungarian)"
    )
    
    # Destination page linked to this menu item
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Leave empty if this item is only a group header/dropdown"
    )
    # Optional parent menu item to create dropdown levels
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        help_text="Select a parent item to place this under a dropdown group"
    )
    # Ordering index for top navigation
    sort_order = models.IntegerField(default=0, help_text="Order in menu bar (e.g. 1, 2, 3)")

    panels = [
        FieldPanel('title'),
        FieldPanel('title_en'),
        FieldPanel('link_page'),
        FieldPanel('parent'),
        FieldPanel('sort_order'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"


# Editable footer settings configuration snippet with translation fields
@register_snippet
class FooterSettings(models.Model):
    # Announcement bar text
    top_bar_text = models.CharField(max_length=255, default="Kérjük, támogassa a Puskás Rádióklubot adója 1%-ával! Adószám: 19005560-1-43")
    top_bar_text_en = models.CharField(max_length=255, blank=True, null=True, default="Please support Puskás Radio Club with 1% of your tax! Tax ID: 19005560-1-43")

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
    copyright_text = models.CharField(max_length=255, default="© 2026 HA5KHC Puskás Tivadar rádióklub. Minden jog fenntartva.")
    copyright_text_en = models.CharField(max_length=255, default="© 2026 HA5KHC Puskás Tivadar Radio Club. All rights reserved.")

    panels = [
        FieldPanel('top_bar_text'),
        FieldPanel('top_bar_text_en'),
        FieldPanel('col1_title'),
        FieldPanel('col1_title_en'),
        FieldPanel('col1_text'),
        FieldPanel('col1_text_en'),
        FieldPanel('col1_address'),
        FieldPanel('col1_clubdays'),
        FieldPanel('col1_clubdays_en'),
        FieldPanel('col2_title'),
        FieldPanel('col2_title_en'),
        FieldPanel('col2_links_text'),
        FieldPanel('col2_links_text_en'),
        FieldPanel('col3_title'),
        FieldPanel('col3_title_en'),
        FieldPanel('col3_text'),
        FieldPanel('col3_text_en'),
        FieldPanel('col3_tax_number'),
        FieldPanel('copyright_text'),
        FieldPanel('copyright_text_en'),
    ]

    def get_col2_links(self, current_lang='hu'):
        links = []
        raw_text = self.col2_links_text_en if (current_lang == 'en' and self.col2_links_text_en) else self.col2_links_text
        if raw_text:
            lines = raw_text.strip().split('\n')
            for line in lines:
                if '|' in line:
                    title, url = line.split('|', 1)
                    links.append({'title': title.strip(), 'url': url.strip()})
        return links

    def __str__(self):
        return "Footer Settings"

    class Meta:
        verbose_name = "Footer Settings"
        verbose_name_plural = "Footer Settings"