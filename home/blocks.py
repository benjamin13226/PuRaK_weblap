# Import Wagtail core blocks and image chooser block
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


# Custom Hero block definition matching the design requirements
class HeroBlock(blocks.StructBlock):
    # Title displayed over the hero background image
    title = blocks.CharBlock(required=True, help_text="Main heading title")
    # Subtitle displayed under the main heading
    subtitle = blocks.CharBlock(required=False, help_text="Subtitle text")
    # Background image for the hero section
    background_image = ImageChooserBlock(required=True, help_text="Hero background image")
    # Optional button text for call to action
    button_text = blocks.CharBlock(required=False, help_text="Button text")
    # Optional page link for call to action button
    button_page = blocks.PageChooserBlock(required=False, help_text="Target page for button link")

    class Meta:
        template = "home/blocks/hero_block.html"
        icon = "image"
        label = "Hero Banner"


# Content card item for grid layout
class CardBlock(blocks.StructBlock):
    # Title of the individual card
    title = blocks.CharBlock(required=True)
    # Optional thumbnail image
    image = ImageChooserBlock(required=False)
    # Short body text inside the card
    text = blocks.TextBlock(required=False)
    # Optional destination link for the card
    link_page = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = "snippet"
        label = "Card Item"


# Container block for multiple cards displayed in a grid
class CardGridBlock(blocks.StructBlock):
    # Section title above cards
    section_title = blocks.CharBlock(required=False)
    # List of cards added dynamically
    cards = blocks.ListBlock(CardBlock())

    class Meta:
        template = "home/blocks/card_grid_block.html"
        icon = "group"
        label = "Card Grid"