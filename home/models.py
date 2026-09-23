from django.db import models
from wagtail.models import Page, Site
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):
    """Root homepage model."""
    subpage_types = ['home.SectionIndexPage', 'home.StandardPage']

    def get_context(self, request):
        context = super().get_context(request)
        # Fetch direct children marked to appear in menus
        context['menu_items'] = self.get_children().live().in_menu()
        return context

    class Meta:
        verbose_name = "Kezdőlap"


class SectionIndexPage(Page):
    """
    Dropdown parent container for sections like Szakosztályok or Versenyek.
    It does not contain heavy text, only acts as a category.
    """
    subpage_types = ['home.StandardPage']

    intro = models.TextField(blank=True, verbose_name="Rövid bevezető leírás")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Safely find the current site root page
        current_site = Site.find_for_request(request)
        root_page = current_site.root_page if current_site else self.get_ancestors().type(HomePage).first()
        if root_page:
            context['menu_items'] = root_page.get_children().live().in_menu()
        else:
            context['menu_items'] = []
        return context

    class Meta:
        verbose_name = "Gyűjtőoldal (Menü kategória)"
        verbose_name_plural = "Gyűjtőoldalak (Menü kategóriák)"


class StandardPage(Page):
    """Subsite for competitions or club departments."""
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name="Alcím / Rövid szlogen")
    theme_color = models.CharField(max_length=7, default='#2e7d32', verbose_name="Témaszín (Hex kód)")
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
        verbose_name="Egyedi banner kép"
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        MultiFieldPanel([
            FieldPanel('theme_color'),
            FieldPanel('banner_image'),
        ], heading="Megjelenés és stílus"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Safely find root page for consistent navigation
        current_site = Site.find_for_request(request)
        root_page = current_site.root_page if current_site else self.get_ancestors().type(HomePage).first()
        if root_page:
            context['menu_items'] = root_page.get_children().live().in_menu()
        else:
            context['menu_items'] = []
        return context

    class Meta:
        verbose_name = "Tartalmi / Verseny aloldal"
        verbose_name_plural = "Tartalmi / Verseny aloldalak"