from operator import attrgetter

from django.db import models


class OrderedModel(models.Model):
    """
    Mixin for supplying ordable, semi-automatically populated fields for models
    """

    ordering_field = None
    ordering_queryset = None

    def get_ordering_queryset(self):
        assert self.ordering_queryset is not None, (
            "'%s' should either include a `ordering_queryset` attribute, "
            "or override the `get_ordering_queryset` method."
            % self.__class__.__name__
        )

    def save(self, *args, **kwargs):
        assert self.ordering_field is not None, (
            "'%s' must specify an `ordering_field`" % self.__class__.__name__
        )

        if getattr(self, self.ordering_field) is None:
            try:
                instances = self.get_ordering_queryset().all()
                last = sorted(instances, key=attrgetter(self.ordering_field))[::-1][0]
                ordering_value = getattr(last, self.ordering_field) + 1
            except IndexError:
                ordering_value = 0
           
            setattr(self, self.ordering_field, ordering_value)

        super(OrderedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
