from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField

from shared.models import OrderedModel


STATES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)


class Page(OrderedModel):
    """
    Abstract Model for holding Holds all shared page metadata
    """
    # Data Fields
    title = models.CharField(max_length=150)
    url = models.SlugField(max_length=150, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    published = models.BooleanField(default=False)    
    placement = models.PositiveSmallIntegerField(blank=True, null=True)
    pagetype = models.CharField(max_length=50, default="Regular")

    # Ordering info
    ordering_field = 'placement'
    
    def get_ordering_queryset(self):
        return self.__class__.objects.all()

    def save(self, *args, **kwargs):
        self.url = slugify(self.title)

        super(Page, self).save(*args, **kwargs)

    class Meta:
        ordering = ('placement', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/{}/'.format(self.url)


class StatePage(Page):
    """
    Specifies a page for a particular State
    """
    state = models.CharField(
        max_length=2,
        choices=STATES,
        blank=False,
        unique=True
    )

    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='states')

    def save(self, *args, **kwargs):
        self.pagetype = 'State'
        self.title = self.get_state_display()

        super(StatePage, self).save(*args, **kwargs)


class PageRevision(models.Model):
    """
    Holds serialized page data.  For when data is saved by and editor without publishing priveleges
    """
    page = models.OneToOneField(Page, related_name="revision")
    data = JSONField()

    updated = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def __str__(self):
        return "{}: {}".format(self.page, self.updated)
