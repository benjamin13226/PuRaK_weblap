# Import Wagtail core blocks, image blocks, and document chooser blocks
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock


# Shared color choices matching the club and department visual themes
ACCENT_COLOR_CHOICES = [
    ("#800000", "Club Maroon (#800000)"),
    ("#1b5e20", "ARDF Green (#1b5e20)"),
    ("#4e342e", "Constructor Brown (#4e342e)"),
    ("#1e1e1e", "Dark Charcoal (#1e1e1e)"),
]

# Shared section background choices for alternating visual bands
SECTION_BG_CHOICES = [
    ("transparent", "Default Page Background"),
    ("#ffffff", "White Section (#ffffff)"),
    ("#f3f4f6", "Light Gray Section (#f3f4f6)"),
]


# Versatile hero and page header banner block supporting full, compact, and CTA modes
class HeroBlock(blocks.StructBlock):
    # Hungarian main heading text
    title = blocks.CharBlock(required=True, label="Title (HU)")
    # Optional English main heading text
    title_en = blocks.CharBlock(required=False, label="Title (EN)")
    # Optional Hungarian subtitle text
    subtitle = blocks.CharBlock(required=False, label="Subtitle (HU)")
    # Optional English subtitle text
    subtitle_en = blocks.CharBlock(required=False, label="Subtitle (EN)")
    # Optional background image for full hero display
    background_image = ImageChooserBlock(required=False, label="Background Image")
    # Solid fallback background color when no background image is set
    background_color = blocks.ChoiceBlock(
        choices=[
            ("#181818", "Deep Black (#181818)"),
            ("#2b2b2b", "Charcoal Gray (#2b2b2b)"),
            ("#800000", "Club Maroon (#800000)"),
        ],
        default="#181818",
        label="Fallback Background Color",
    )
    # Toggle between full-height banner and compact subpage or CTA header
    is_compact = blocks.BooleanBlock(required=False, default=False, label="Compact Height")
    # Toggle for bottom accent border line
    show_bottom_border = blocks.BooleanBlock(required=False, default=True, label="Show Bottom Accent Border")
    # Bottom border and button theme color
    accent_color = blocks.ChoiceBlock(choices=ACCENT_COLOR_CHOICES, default="#800000", label="Accent Color")
    # Button color scheme selection
    button_style = blocks.ChoiceBlock(
        choices=[
            ("accent", "Accent Color Button"),
            ("white", "White Button with Dark Text"),
        ],
        default="accent",
        label="Button Style",
    )
    # Optional Hungarian call-to-action button label
    button_text = blocks.CharBlock(required=False, label="Button Text (HU)")
    # Optional English call-to-action button label
    button_text_en = blocks.CharBlock(required=False, label="Button Text (EN)")
    # Optional internal page destination for the button
    button_page = blocks.PageChooserBlock(required=False, label="Button Target Page")

    class Meta:
        template = "home/blocks/hero_block.html"
        icon = "image"
        label = "Hero / Banner / CTA"


# Section heading block with optional underline bar and lead paragraph
class SectionHeaderBlock(blocks.StructBlock):
    # Hungarian section title
    heading = blocks.CharBlock(required=True, label="Heading (HU)")
    # Optional English section title
    heading_en = blocks.CharBlock(required=False, label="Heading (EN)")
    # Optional Hungarian introductory paragraph
    lead_text = blocks.TextBlock(required=False, label="Intro Text (HU)")
    # Optional English introductory paragraph
    lead_text_en = blocks.TextBlock(required=False, label="Intro Text (EN)")
    # Horizontal text alignment option
    alignment = blocks.ChoiceBlock(
        choices=[("center", "Center"), ("left", "Left")],
        default="center",
        label="Alignment",
    )
    # Toggle for decorative accent underline below heading
    show_underline = blocks.BooleanBlock(required=False, default=True, label="Show Accent Underline")
    # Accent color for the underline bar
    accent_color = blocks.ChoiceBlock(choices=ACCENT_COLOR_CHOICES, default="#800000", label="Underline Color")
    # Full-width section background color
    section_bg = blocks.ChoiceBlock(choices=SECTION_BG_CHOICES, default="transparent", label="Section Background")

    class Meta:
        template = "home/blocks/section_header_block.html"
        icon = "title"
        label = "Section Heading"


# Bilingual rich text content block with optional card container styling
class BilingualRichTextBlock(blocks.StructBlock):
    # Hungarian formatted text content
    content = blocks.RichTextBlock(required=True, label="Content (HU)")
    # Optional English formatted text content
    content_en = blocks.RichTextBlock(required=False, label="Content (EN)")
    # Toggle to wrap text inside a white elevated card
    boxed = blocks.BooleanBlock(required=False, default=False, label="Display Inside White Card")

    class Meta:
        template = "home/blocks/bilingual_richtext_block.html"
        icon = "doc-full"
        label = "Formatted Text (HU/EN)"


# Highlighted post or featured event card with colored left border
class HighlightCardBlock(blocks.StructBlock):
    # Hungarian card title
    title = blocks.CharBlock(required=True, label="Title (HU)")
    # Optional English card title
    title_en = blocks.CharBlock(required=False, label="Title (EN)")
    # Optional metadata line such as author or date
    meta_info = blocks.CharBlock(required=False, label="Author / Date Meta (HU)")
    # Optional English metadata line
    meta_info_en = blocks.CharBlock(required=False, label="Author / Date Meta (EN)")
    # Hungarian card body text
    body = blocks.RichTextBlock(required=True, label="Body Text (HU)")
    # Optional English card body text
    body_en = blocks.RichTextBlock(required=False, label="Body Text (EN)")
    # Left border and button accent color
    accent_color = blocks.ChoiceBlock(choices=ACCENT_COLOR_CHOICES, default="#800000", label="Accent Color")
    # Full-width section background color
    section_bg = blocks.ChoiceBlock(choices=SECTION_BG_CHOICES, default="transparent", label="Section Background")
    # Optional Hungarian action button text
    button_text = blocks.CharBlock(required=False, label="Button Text (HU)")
    # Optional English action button text
    button_text_en = blocks.CharBlock(required=False, label="Button Text (EN)")
    # Optional target page for action button
    button_page = blocks.PageChooserBlock(required=False, label="Button Target Page")

    class Meta:
        template = "home/blocks/highlight_card_block.html"
        icon = "pick"
        label = "Highlight / Announcement Card"


# Individual card item used inside the card grid block
class CardBlock(blocks.StructBlock):
    # Hungarian card title
    title = blocks.CharBlock(required=True, label="Title (HU)")
    # Optional English card title
    title_en = blocks.CharBlock(required=False, label="Title (EN)")
    # Optional emoji or short icon symbol displayed above the title
    icon = blocks.CharBlock(required=False, max_length=16, label="Emoji / Icon (e.g. 🎓, 📡, 🏆)")
    # Optional card thumbnail or icon image
    image = ImageChooserBlock(required=False, label="Image (Optional)")
    # Hungarian short card description
    text = blocks.TextBlock(required=False, label="Description (HU)")
    # Optional English short card description
    text_en = blocks.TextBlock(required=False, label="Description (EN)")
    # Optional internal link page
    link_page = blocks.PageChooserBlock(required=False, label="Target Page")

    class Meta:
        icon = "snippet"
        label = "Card Item"


# Responsive grid container for multiple content cards
class CardGridBlock(blocks.StructBlock):
    # Optional Hungarian section title above the grid
    section_title = blocks.CharBlock(required=False, label="Section Title (HU)")
    # Optional English section title above the grid
    section_title_en = blocks.CharBlock(required=False, label="Section Title (EN)")
    # Visual presentation mode for cards
    card_style = blocks.ChoiceBlock(
        choices=[
            ("bordered", "Standard Photo Card (Left Aligned)"),
            ("feature_icon", "Feature Icon Card (Centered)"),
        ],
        default="bordered",
        label="Card Layout Style",
    )
    # Full-width section background color
    section_bg = blocks.ChoiceBlock(choices=SECTION_BG_CHOICES, default="transparent", label="Section Background")
    # Dynamic list of card items
    cards = blocks.ListBlock(CardBlock(), label="Cards")

    class Meta:
        template = "home/blocks/card_grid_block.html"
        icon = "group"
        label = "Card Grid"


# Single downloadable document entry with bilingual labels
class DocumentItemBlock(blocks.StructBlock):
    # Hungarian document display title
    title = blocks.CharBlock(required=True, label="Document Title (HU)")
    # Optional English document display title
    title_en = blocks.CharBlock(required=False, label="Document Title (EN)")
    # Uploaded Wagtail document file
    document = DocumentChooserBlock(required=True, label="File")

    class Meta:
        icon = "doc-empty"
        label = "Document File"


# Category column holding multiple downloadable documents
class DocumentCategoryBlock(blocks.StructBlock):
    # Hungarian category heading
    category_title = blocks.CharBlock(required=True, label="Category Title (HU)")
    # Optional English category heading
    category_title_en = blocks.CharBlock(required=False, label="Category Title (EN)")
    # Hungarian empty state message when no documents are attached
    empty_text = blocks.CharBlock(
        required=False,
        default="Jelenleg nincs feltöltött dokumentum.",
        label="Empty State Text (HU)",
    )
    # Optional English empty state message
    empty_text_en = blocks.CharBlock(
        required=False,
        default="No documents uploaded yet.",
        label="Empty State Text (EN)",
    )
    # List of document items in this category
    documents = blocks.ListBlock(DocumentItemBlock(), required=False, label="Documents")

    class Meta:
        icon = "folder-open-inverse"
        label = "Document Category"


# Multi-column official documents container block
class DocumentListBlock(blocks.StructBlock):
    # List of document categories rendered side by side
    categories = blocks.ListBlock(DocumentCategoryBlock(), label="Document Categories")

    class Meta:
        template = "home/blocks/document_list_block.html"
        icon = "doc-empty-inverse"
        label = "Official Documents List"


# Gallery album and logo strip block with image grid and empty state handling
class GalleryBlock(blocks.StructBlock):
    # Optional Hungarian album title
    album_title = blocks.CharBlock(required=False, label="Album Title (HU)")
    # Optional English album title
    album_title_en = blocks.CharBlock(required=False, label="Album Title (EN)")
    # Optional Hungarian album description
    description = blocks.TextBlock(required=False, label="Description (HU)")
    # Optional English album description
    description_en = blocks.TextBlock(required=False, label="Description (EN)")
    # Display mode supporting full photo grids and compact partner logo rows
    display_mode = blocks.ChoiceBlock(
        choices=[
            ("photo_grid", "Photo Album Grid"),
            ("logo_strip", "Centered Logo Strip"),
        ],
        default="photo_grid",
        label="Display Mode",
    )
    # Full-width section background color
    section_bg = blocks.ChoiceBlock(choices=SECTION_BG_CHOICES, default="transparent", label="Section Background")
    # List of images included in the gallery
    images = blocks.ListBlock(ImageChooserBlock(), required=False, label="Images")

    class Meta:
        template = "home/blocks/gallery_block.html"
        icon = "image"
        label = "Photo Gallery / Logo Strip"


# Embedded map block for location display
class MapEmbedBlock(blocks.StructBlock):
    # Google Maps iframe embed URL
    embed_url = blocks.URLBlock(required=True, label="Google Maps Embed URL")
    # Frame height in pixels
    height = blocks.IntegerBlock(default=380, min_value=200, max_value=800, label="Map Height (px)")

    class Meta:
        template = "home/blocks/map_embed_block.html"
        icon = "site"
        label = "Embedded Map"


# Technical or constructor project showcase block with gallery and attachments
class ProjectItemBlock(blocks.StructBlock):
    # Hungarian project title
    title = blocks.CharBlock(required=True, label="Project Title (HU)")
    # Optional English project title
    title_en = blocks.CharBlock(required=False, label="Project Title (EN)")
    # Optional year or author tag
    year_or_author = blocks.CharBlock(required=False, label="Year / Author")
    # Hungarian detailed project description
    description = blocks.RichTextBlock(required=True, label="Description (HU)")
    # Optional English detailed project description
    description_en = blocks.RichTextBlock(required=False, label="Description (EN)")
    # Optional project photos
    photos = blocks.ListBlock(ImageChooserBlock(), required=False, label="Project Photos")
    # Optional downloadable schematics or project files
    attachments = blocks.ListBlock(DocumentItemBlock(), required=False, label="Project Files")
    # Left border accent color
    accent_color = blocks.ChoiceBlock(choices=ACCENT_COLOR_CHOICES, default="#4e342e", label="Accent Color")

    class Meta:
        template = "home/blocks/project_item_block.html"
        icon = "cogs"
        label = "Constructor Project"


# Nested StreamBlock available inside two-column layouts
class ColumnContentStreamBlock(blocks.StreamBlock):
    section_header = SectionHeaderBlock()
    rich_text = BilingualRichTextBlock()
    highlight_card = HighlightCardBlock()
    documents = DocumentListBlock()
    gallery = GalleryBlock()
    map_embed = MapEmbedBlock()
    card_grid = CardGridBlock()


# Flexible two-column split layout allowing arbitrary blocks in left and right columns
class TwoColumnLayoutBlock(blocks.StructBlock):
    # Column width distribution ratio
    ratio = blocks.ChoiceBlock(
        choices=[
            ("1fr 1fr", "Equal (50% / 50%)"),
            ("2fr 1fr", "Wide Left (66% / 33%)"),
            ("1fr 2fr", "Wide Right (33% / 66%)"),
        ],
        default="1fr 1fr",
        label="Column Ratio",
    )
    # Optional white card background wrapping the entire two-column container
    card_wrapper = blocks.BooleanBlock(required=False, default=False, label="Wrap Columns in White Card")
    # Blocks placed in the left column
    left_column = ColumnContentStreamBlock(required=False, label="Left Column Blocks")
    # Blocks placed in the right column
    right_column = ColumnContentStreamBlock(required=False, label="Right Column Blocks")

    class Meta:
        template = "home/blocks/two_column_block.html"
        icon = "placeholder"
        label = "Two-Column Split Layout"