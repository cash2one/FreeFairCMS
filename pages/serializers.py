from rest_framework import serializers

from shared.serializers import LocalDateTimeField
from .models.pages import Page, StatePage
from .models.blocks import Block, TextBlock, AccordionBlock, Accordion, ContactBlock, \
        InfoBlock, InfoCategory, InfoContent, CheckboxBlock, CheckboxItem
from editors.models import Editor


SHARED_BLOCK_FIELDS = ['page', 'placement', 'title', 'blocktype', 'id', 'help_text']


class UpdateRelatedMixin:
    def update_related(self, data):
        """
        Allows updating nested serializer relations.  Should be called
        during to_internal_value, and expects:
            - full data from request, before validation
            - the dictionary key that contains the data for the related objects
            - the serializer for the nested relation
        returns the data with the nested relation data removed
        """
        serializer = self.Meta.update_related_serializer

        field_data = data.pop(self.Meta.update_related_field)
        field_ids = [c['id'] for c in field_data]
        objs = serializer.Meta.model.objects.filter(id__in=field_ids)

        for obj in objs:
            obj_data = [x for x in field_data if x['id'] == obj.id][0]
            s = serializer(obj, data=obj_data, context=self.context)
            s.is_valid(raise_exception=True)

            s.save()

        return data

    def process_related_data(self, related_data):
        """
        Overwrite this function if the related data needs any specific processing
        before being serialized
        """
        return related_data

    def to_internal_value(self, data):
        assert self.Meta.update_related_field is not None, (
            "The {} class requires a value for the `update_related_field` in "
            "its Meta class".format(self.__class__)
        )

        assert self.Meta.update_related_serializer is not None, (
            "The {} class requires a value for the `update_related_serializer` in "
            "its Meta class".format(self.__class__)
        )

        data = self.update_related(data)
        return super(UpdateRelatedMixin, self).to_internal_value(data)


class TextBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBlock 
        fields = SHARED_BLOCK_FIELDS + ['text']


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class AccordionSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Accordion
        fields = ['text', 'placement', 'children', 'id', 'parent', 'block']


class AccordionBlockSerializer(serializers.ModelSerializer):
    accordions = AccordionSerializer(many=True, read_only=True, source='root_nodes')

    def to_internal_value(self, data):
        """
        If it's an update (ie. self.instance exists),
        update the accordions as well
        """
        if self.instance is not None:
            accordion_data = data.pop('accordions')
            accordion_data = self.flatten_accordion_data(accordion_data)

            accordion_ids = [a['id'] for a in accordion_data]
            accordions = Accordion.objects.filter(id__in=accordion_ids)

            for accordion in accordions:
                single_accordion = [a for a in accordion_data if a['id'] == accordion.id][0]
                s = AccordionSerializer(accordion, data=single_accordion, context=self.context)
                s.is_valid(raise_exception=True)

                s.save()

        return super(AccordionBlockSerializer, self).to_internal_value(data)

    def flatten_accordion_data(self, accordion_data):
        accordions = []

        for accordion in accordion_data:
            children = accordion.pop('children')
            accordions.append(accordion)

            accordions += self.flatten_accordion_data(children)

        return accordions
    
    
    class Meta:
        model = AccordionBlock 
        fields = SHARED_BLOCK_FIELDS + ['accordions'] 


class ContactBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactBlock
        fields = SHARED_BLOCK_FIELDS


class InfoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoContent
        fields = [
                'name',
                'description',
                'address',
                'templates',
                'groups',
                'reading',
                'id',
                'category',
                'placement',
        ]


class InfoCategorySerializer(serializers.ModelSerializer):
    contents = InfoContentSerializer(read_only=True, many=True)

    def to_internal_value(self, data):
        """
        If it's an update (ie. self.instance exists),
        update the categories and contents as well
        """
        if self.instance is not None:
            content_data = data.pop('contents')
            content_ids = [c['id'] for c in content_data]
            contents = InfoContent.objects.filter(id__in=content_ids)

            for content in contents:
                single_content = [c for c in content_data if c['id'] == content.id][0]
                s = InfoContentSerializer(content, data=single_content, context=self.context)
                s.is_valid(raise_exception=True)

                s.save()

        return super(InfoCategorySerializer, self).to_internal_value(data)

    class Meta:
        model = InfoCategory
        fields = ['name', 'contents', 'block', 'id', 'placement']


class InfoBlockSerializer(UpdateRelatedMixin, serializers.ModelSerializer):
    categories = InfoCategorySerializer(read_only=True, many=True)

    class Meta:
        model = InfoBlock
        fields = SHARED_BLOCK_FIELDS + ['categories']
        update_related_field = 'categories'
        update_related_serializer = InfoCategorySerializer


class CheckboxItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckboxItem
        fields = ['id', 'name', 'value', 'block', 'placement']


class CheckboxBlockSerializer(UpdateRelatedMixin, serializers.ModelSerializer):
    checkboxes = CheckboxItemSerializer(many=True, read_only=True)

    class Meta:
        model = CheckboxBlock
        fields = SHARED_BLOCK_FIELDS + ['checkboxes']
        update_related_field = 'checkboxes'
        update_related_serializer = CheckboxItemSerializer


BLOCKTYPES = {
    Block.TEXT: {
        "queryset": TextBlock.objects.all(),
        "serializer_class": TextBlockSerializer
    },
    Block.ACCORDION: {
        "queryset": AccordionBlock.objects.all(),
        "serializer_class": AccordionBlockSerializer
    },
    Block.CONTACT: {
        "queryset": ContactBlock.objects.all(),
        "serializer_class": ContactBlockSerializer 
    },
    Block.INFO: {
        "queryset": InfoBlock.objects.all(),
        "serializer_class": InfoBlockSerializer
    },
    Block.CHECKBOX: {
        "queryset": CheckboxBlock.objects.all(),
        "serializer_class": CheckboxBlockSerializer
    }
}


class BlockSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        return BLOCKTYPES[obj.blocktype]["serializer_class"](obj.content_model, context=self.context).to_representation(obj.content_model)

    class Meta:
        model = TextBlock
        fields = SHARED_BLOCK_FIELDS


class PageListSerializer(serializers.ModelSerializer):
    def save(self):
        self.validated_data['edited_by'] = self.context.get('request').user
        return super(PageListSerializer, self).save()

    class Meta:
        model = Page
        fields = ('title', 'id', 'published', 'placement')


class PageFullSerializer(serializers.ModelSerializer):
    def save(self):
        self.validated_data['edited_by'] = self.context.get('request').user
        return super(PageFullSerializer, self).save()

    edited_by = serializers.SlugRelatedField(
        slug_field='email', queryset=Editor.objects.all()
    )
    edited = LocalDateTimeField(format='%B %-d, %Y, %-I:%M%p', read_only=True)
    blocks = BlockSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = (
            'title', 
            'id', 
            'published',
            'edited_by',
            'edited',
            'url',
            'blocks',
        )


class StatePageListSerializer(serializers.ModelSerializer):
    state_display = serializers.SerializerMethodField(read_only=True)

    def get_state_display(self, obj):
        return obj.get_state_display()

    class Meta:
        model = StatePage
        fields = ('title', 'id', 'published', 'placement', 'state', 'state_display')


class StatePageFullSerializer(PageFullSerializer, StatePageListSerializer):
    class Meta:
        model = StatePage
        fields = (
            'title', 
            'id', 
            'published',
            'edited_by',
            'edited',
            'url',
            'blocks',
            'state',
            'state_display'
        )
