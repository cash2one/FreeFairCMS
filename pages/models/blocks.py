from django.db import models
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
    TYPES = [
        (TEXT, "Text"), 
        (ACCORDION, "Accordion"),
        (CONTACT, 'Contact'),
    ]

    page = models.ForeignKey(Page, related_name="blocks")
    title = models.CharField(max_length=250, blank=True)

    placement = models.PositiveSmallIntegerField(blank=True)
    blocktype = models.CharField(max_length=50, choices=TYPES, blank=True)

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
    text = models.TextField(default="")

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
