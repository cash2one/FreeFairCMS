import subprocess
import os
import zipfile
import requests
from shutil import make_archive

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.management import call_command
from django.conf import settings

from .models.pages import Page
from .models.blocks import Block, TextBlock, AccordionBlock, Accordion, InfoBlock, \
    InfoCategory, InfoContent
from .serializers import PageListSerializer, PageFullSerializer, BlockSerializer, BLOCKTYPES, \
    AccordionSerializer, InfoCategorySerializer, InfoContentSerializer


class AllRegularPagesView(generics.ListCreateAPIView):
    queryset = Page.objects.filter(statepage__isnull=True).all()
    serializer_class = PageListSerializer


class SinglePageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.select_related('edited_by').all()
    serializer_class = PageFullSerializer

    def put(self, request, *args, **kwargs):
        blocks_data = request.data.pop('blocks')
        block_ids = [block['id'] for block in blocks_data]
        blocks = Block.objects.filter(id__in=block_ids)

        for block_data in blocks_data:
            block = [b for b in blocks if b.id == block_data['id']][0]

            context = { request: 'request' }
            serializer = BLOCKTYPES[block.blocktype]["serializer_class"]
            b = serializer(block.content_model, data=block_data, context=context)
            b.is_valid()

            b.save()

        return super(SinglePageView, self).put(request, *args, **kwargs)


class BulkPageUpdateView(APIView):
    serializer_class = PageListSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class

        ids = [page['id'] for page in self.request.data]
        pages = Page.objects.filter(id__in=ids)
        updated_pages = []

        for page_data in self.request.data:
            page = [p for p in pages if p.id == page_data['id']][0]
           
            context = { 'request': request }
            s = serializer(page, data=page_data, context=context)
            s.is_valid(raise_exception=True)

            page = s.save()
            updated_pages.append(page)

        return Response(serializer(updated_pages, many=True).data)


class BlockTypeView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(Block.TYPES)


class NewBlockView(generics.CreateAPIView):
    def get_queryset(self):
        return BLOCKTYPES[self.request.data["blocktype"]]["queryset"]

    def get_serializer_class(self):
        return BLOCKTYPES[self.request.data["blocktype"]]["serializer_class"]


class BlockDeleteView(generics.DestroyAPIView):
    queryset = Block.objects.all()


class NewAccordionView(generics.CreateAPIView):
    queryset = Accordion.objects.all()
    serializer_class = AccordionSerializer


class DeleteAccordionView(generics.DestroyAPIView):
    queryset = Accordion.objects.all()


class NewInfoCategoryView(generics.CreateAPIView):
    queryset = InfoCategory.objects.all()
    serializer_class = InfoCategorySerializer


class DeleteInfoCategoryView(generics.DestroyAPIView):
    queryset = InfoCategory.objects.all()


class NewInfoContentView(generics.CreateAPIView):
    queryset = InfoContent.objects.all()
    serializer_class = InfoContentSerializer

    

class DeleteInfoContentView(generics.DestroyAPIView):
    queryset = InfoContent.objects.all()


def zipdir(path, ziph):
    """
    Zip code courtesy of:
    http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory/
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), path)
            )


class PublishView(APIView):
    def get(self, request, *args, **kwargs):
        call_command('build')

        buildzip = os.path.join(settings.BASE_DIR, 'output.zip')

        zipf = zipfile.ZipFile(buildzip, 'w', zipfile.ZIP_DEFLATED)
        zipdir(settings.BUILD_DIR, zipf)
        zipf.close()

        data = open(buildzip, 'rb').read()

        r = requests.post(
                url='https://api.netlify.com/api/v1/sites/{}/deploys'.format(settings.NETLIFY_SITE),
                data=data,
                headers={
                    'Content-Type': 'application/zip',
                    'Authorization': 'Bearer {}'.format(settings.NETLIFY_TOKEN)
                })

        if r.status_code >= 300:
            print(r.json())
            return Response({'error': 'Unable to publish site'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status.HTTP_204_NO_CONTENT)
