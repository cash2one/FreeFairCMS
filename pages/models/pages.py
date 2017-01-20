from django.db import models
from django.conf import settings
from django.utils.text import slugify

from shared.models import OrderedModel


STATES = (
    ('AL', 'ALABAMA'),
    ('AK', 'ALASKA'),
    ('AZ', 'ARIZONA'),
    ('AR', 'ARKANSAS'),
    ('CA', 'CALIFORNIA'),
    ('CO', 'COLORADO'),
    ('CT', 'CONNECTICUT'),
    ('DE', 'DELAWARE'),
    ('FL', 'FLORIDA'),
    ('GA', 'GEORGIA'),
    ('HI', 'HAWAII'),
    ('ID', 'IDAHO'),
    ('IL', 'ILLINOIS'),
    ('IN', 'INDIANA'),
    ('IA', 'IOWA'),
    ('KS', 'KANSAS'),
    ('KY', 'KENTUCKY'),
    ('LA', 'LOUISIANA'),
    ('ME', 'MAINE'),
    ('MD', 'MARYLAND'),
    ('MA', 'MASSACHUSETTS'),
    ('MI', 'MICHIGAN'),
    ('MN', 'MINNESOTA'),
    ('MS', 'MISSISSIPPI'),
    ('MO', 'MISSOURI'),
    ('MT', 'MONTANA'),
    ('NE', 'NEBRASKA'),
    ('NV', 'NEVADA'),
    ('NH', 'HAMPSHIRE'),
    ('NJ', 'NEW JERSEY'),
    ('NM', 'NEW MEXICO'),
    ('NY', 'NEW YORK'),
    ('NC', 'NORTH CAROLINA'),
    ('ND', 'NORTH DAKOTA'),
    ('OH', 'OHIO'),
    ('OK', 'OKLAHOMA'),
    ('OR', 'OREGON'),
    ('PA', 'PENNSYLVANIA'),
    ('RI', 'RHODE ISLAND'),
    ('SC', 'CAROLINA'),
    ('SD', 'DAKOTA'),
    ('TN', 'TENNESSEE'),
    ('TX', 'TEXAS'),
    ('UT', 'UTAH'),
    ('VT', 'VERMONT'),
    ('VA', 'VIRGINIA'),
    ('WA', 'WASHINGTON'),
    ('WV', 'WEST VIRGINIA'),
    ('WI', 'WISCONSIN'),
    ('WY', 'WYOMING'),
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
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL)
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


class StatePage(Page):
    """
    Specifies a page for a particular State
    """
    state = models.CharField(
        max_length=1,
        choices=STATES,
        blank=False
    )

    def save(self, *args, **kwargs):
        self.pagetype = 'State'

        super(StatePage, self).save(*args, **kwargs)
