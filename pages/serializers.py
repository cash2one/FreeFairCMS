from rest_framework import serializers

from shared.serializers import LocalDateTimeField
from .models.pages import Page
from .models.blocks import Block, TextBlock, AccordionBlock, Accordion, ContactBlock
from editors.models import Editor


SHARED_BLOCK_FIELDS = ['page', 'placement', 'title', 'blocktype', 'id']


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
