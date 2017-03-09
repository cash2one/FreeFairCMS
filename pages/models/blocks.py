from django.db import models
from django.utils.functional import cached_property
from mptt.models import MPTTModel, TreeForeignKey

from shared.models import OrderedModel
from .pages import Page


class Block(OrderedModel):
    """
    Blocks are elements attached to pages that describe layout features.
    A Page is made up of blocks that are then rendered in order to create a page
    """
    TEXT = "T"
    ACCORDION = "A"
    CONTACT = "C"
    INFO = "I"        
    CHECKBOX = "H"
    TYPES = [
        (TEXT, "Text"), 
        (ACCORDION, "Accordion"),
        (CONTACT, 'Contact'),
        (INFO, "Info"),
        (CHECKBOX, "Checkbox"),
    ]

    page = models.ForeignKey(Page, related_name="blocks")
    title = models.CharField(max_length=250, blank=True)
    help_text = models.TextField(blank=True)

    blocktype = models.CharField(max_length=50, choices=TYPES, blank=True)
    placement = models.PositiveSmallIntegerField(blank=True)

    class Meta:
        ordering = ('placement', )

    ordering_field = 'placement'
    
    def get_ordering_queryset(self):
        return self.page.blocks.all()

    @property
    def content_model(self):
        return getattr(self, [t[1] for t in self.TYPES if t[0] == self.blocktype][0].lower() + 'block')

    def __str__(self):
        return self.title


class TextBlock(Block):
    """
    Normal Paragraph-based text block
    """
    text = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.blocktype = Block.TEXT
        super(TextBlock, self).save(*args, **kwargs)


class AccordionBlock(Block):
    """
    Block with recursively structure accordion blocks
    """
    def save(self, *args, **kwargs):
        self.blocktype = Block.ACCORDION
        super(AccordionBlock, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def root_nodes(self):
        return self.accordions.model.objects.root_nodes().filter(block=self)


class Accordion(MPTTModel):
    """
    Accordion item for displaying information in recursive, collapseable panels
    """
    block = models.ForeignKey(AccordionBlock, related_name="accordions")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    placement = models.SmallIntegerField()
    text = models.TextField(default="")

    class MPTTMeta:
        order_insertion_by = ['placement']


class ContactBlock(Block):
    """
    Stand in for Contact Form
    """
    def __str__(self):
        return "Contact Block"

    def save(self, *args, **kwargs):
        self.blocktype = Block.CONTACT
        super(ContactBlock, self).save(*args, **kwargs)


class InfoBlock(Block):
    """
    Block for containg the multilevel sections of:
    - Overall Category (e.g. Free, Fair, and Unfettered)
        - Subcategory (e.g. Gerrymandering)
            - How To Adress It
            - Templates for Action
            - Groups & Organizations Working on This
            - Reading & Watching List
    """
    def __str__(self):
        return "Action Block"

    def save(self, *args, **kwargs):
        self.blocktype = Block.INFO
        super(InfoBlock, self).save(*args, **kwargs)


class InfoCategory(OrderedModel):
    """
    Main Category for an InfoBlock
    """
    name = models.CharField(max_length=255)

    block = models.ForeignKey(InfoBlock, related_name="categories", on_delete=models.CASCADE)
    placement = models.PositiveSmallIntegerField(blank=True)

    class Meta:
        ordering = ('placement', )

    ordering_field = 'placement'
    
    def get_ordering_queryset(self):
        return self.block.categories.all()

    def __str__(self):
        return self.name


class InfoContent(OrderedModel):
    """
    Main Structure of an info Block
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    address = models.TextField(blank=True)
    templates = models.TextField(blank=True)
    groups = models.TextField(blank=True)
    reading = models.TextField(blank=True)

    category = models.ForeignKey(InfoCategory, related_name="contents", on_delete=models.CASCADE)
    placement = models.PositiveSmallIntegerField(blank=True)

    class Meta:
        ordering = ('placement', )

    ordering_field = 'placement'
    
    def get_ordering_queryset(self):
        return self.category.contents.all()

    def __str__(self):
        return self.name


class CheckboxBlock(Block):
    """
    Configurable Checkbox block
    """
    empty_text = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.blocktype = Block.CHECKBOX
        super(CheckboxBlock, self).save(*args, **kwargs)

    @cached_property
    def active(self):
        return self.checkboxes.filter(value=True)


class CheckboxItem(OrderedModel):
    """
    Checkbox item
    """
    name = models.CharField(max_length=100)
    value = models.BooleanField(default=False)

    block = models.ForeignKey(CheckboxBlock, related_name="checkboxes", on_delete=models.CASCADE)
    placement = models.PositiveSmallIntegerField(blank=True)

    class Meta:
        ordering = ('placement', )

    ordering_field = 'placement'
    
    def get_ordering_queryset(self):
        return self.block.checkboxes.all()

    def __str__(self):
        return self.name
