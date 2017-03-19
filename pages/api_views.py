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
from django.utils import timezone

from editors.models import Editor
from editors.permissions import IsAdminEditor
from .models.pages import Page, StatePage, STATES, PageRevision
from .models.blocks import Block, TextBlock, AccordionBlock, Accordion, InfoBlock, \
    InfoCategory, InfoContent, CheckboxBlock, CheckboxItem
from .serializers import PageListSerializer, PageFullSerializer, BlockSerializer, BLOCKTYPES, \
    AccordionSerializer, InfoCategorySerializer, InfoContentSerializer, StatePageListSerializer, \
    StatePageFullSerializer


class AllRegularPagesView(generics.ListCreateAPIView):
    queryset = Page.objects.filter(statepage__isnull=True).all()
    serializer_class = PageListSerializer


class SinglePageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.select_related('edited_by').all()
    serializer_class = PageFullSerializer


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


def get_state_page(state_code, editor):
    state, created = StatePage.objects.get_or_create(pagetype='State', state=state_code, edited_by=editor)

    if created:
        issues = CheckboxBlock.objects.create(
            title="Issues in This State",
            help_text="For this section, you’ll check a box next to each of the major issues in your state surrounding election and voter reform. Here you can just highlight the main issues.",
            page=state,
            empty_text="No issues For now. Keep up the good work!",
        )

        CheckboxItem.objects.create(name="Corporate and Private Money / Corruption", block=issues)
        CheckboxItem.objects.create(name="Lack of Public Funding", block=issues)
        CheckboxItem.objects.create(name="Voter Suppression", block=issues)
        CheckboxItem.objects.create(name="Gerrymandering", block=issues)
        CheckboxItem.objects.create(name="Primary Elections", block=issues)
        CheckboxItem.objects.create(name="Inconsistent Voting Methods", block=issues)
        CheckboxItem.objects.create(name="Ballot Design and Language", block=issues)

        achievements = CheckboxBlock.objects.create(
            title="Achievements in This State",
            help_text="For this section, you’ll check a box next to each of the things your state has already made major progress on. Here you can just highlight those achievements, if any apply.",
            page=state,
            empty_text="No achievements in this state yet. Better get to work!",
        )

        CheckboxItem.objects.create(name="Public Financing", block=achievements)
        CheckboxItem.objects.create(name="Early Voting", block=achievements)
        CheckboxItem.objects.create(name="Vote-By-Mail", block=achievements)
        CheckboxItem.objects.create(name="Automatic Voter Registration", block=achievements)
        CheckboxItem.objects.create(name="Open Primaries", block=achievements)
        CheckboxItem.objects.create(name="Ranked Choice Voting", block=achievements)
        CheckboxItem.objects.create(name="Anti-Corruption Legislation", block=achievements)
        CheckboxItem.objects.create(name="Non-Partisan Redistricting", block=achievements)

        TextBlock.objects.create(
                page=state,
                title="How You Can Get Involved",
                help_text="Here use a bulleted list to let people know what groups, lawmakers, public officials, etc are working on these issues and how people can get in touch with them to support or join those efforts."
        )

        TextBlock.objects.create(
                page=state,
                title="Recent Legislation",
                help_text="If there has been any recent legislation proposed at the local or state level, list it here in a bulleted list, so that people can learn more. You can include legislation that wasn’t successful, because sometimes those laws can be re-proposed under new administrations or with changes."
        )

        TextBlock.objects.create(
                page=state,
                title="Reading & Watching on State Issues",
                help_text="Here you can include a bulleted lists of relevant articles, summaries, or information pages focused on election and voter reform in your state. The goal here is to post information specifically about election and voter reform efforts, not to post general articles about politics or parties in your local area or state."
        )

    return state


class AllStatePagesView(generics.ListAPIView):
    queryset = StatePage.objects.all()
    serializer_class = StatePageListSerializer


class SingleStatePagesView(SinglePageView):
    queryset = StatePage.objects.all()
    serializer_class = StatePageFullSerializer
    lookup_field = 'state'

    def put(self, request, *args, **kwargs):
        if request.user.role != Editor.ADMIN:
            page = self.get_object()

            data = request.data
            data['needs_approval'] = True
            data['edited_by'] = str(request.user)
            data['edited'] = timezone.localtime(timezone.now()).strftime('%B %-d, %Y, %-I:%M%p')

            revision, _ = PageRevision.objects.update_or_create(
                page=page, 
                defaults={ 
                    'edited_by':self.request.user, 'data': data,
                }
            )

            return Response(request.data)
        else:
            page = self.get_object()

            if hasattr(page, 'revision'):
                page.revision.delete()

            return super(SingleStatePagesView, self).put(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        page = self.get_object()

        if hasattr(page, 'revision'):
            data = page.revision.data

            return Response(data)
        else:
            return super(SingleStatePagesView, self).get(request, *args, **kwargs)


class UnusedStatesView(APIView):
    def get(self, request, *args, **kwargs):
        used = StatePage.objects.values_list('state', flat=True)
        
        unused = [state for state in STATES if state[0] not in used]

        return Response(unused)


class NewStatePageView(APIView):
    def post(self, request, *args, **kwargs):
        state_code = request.data.get('state', None)

        if state_code is None:
            return Response({ "state": ["This Field is Required"] }, status.HTTP_400_BAD_REQUEST)

        state = get_state_page(state_code, request.user)
        return Response(StatePageListSerializer(state).data)


class ApproveStatePageView(generics.GenericAPIView):
    permission_classes = [IsAdminEditor, ]
    queryset = StatePage.objects.all()
    lookup_field = 'state'
    serializer_class = StatePageFullSerializer

    def put(self, request, *args, **kwargs):
        state_page = self.get_object();
        
        if not hasattr(state_page, 'revision'):
            return Response(StatePagueFullSerializer(state_page).data)

        approved = request.data.get('approved', None)

        if approved == True:
            data = state_page.revision.data
            state_page.revision.delete()
            state_page = StatePage.objects.get(id=state_page.id)
            data.pop('edited', None)
            serializer = self.get_serializer(state_page, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        elif approved == False:
            state_page.revision.delete()
            state_page = StatePage.objects.get(id=state_page.id)
            serializer = self.get_serializer(state_page)
        else:
            return Response({"approved": ["Approved must be True or False"]}, status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.data)


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
