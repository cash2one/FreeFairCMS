from rest_framework import generics

from .models import Editor
from .serializers import EditorDetailsSerializer


class AllEditorsView(generics.ListAPIView):
    queryset = Editor.objects.prefetch_related('states')
    serializer_class = EditorDetailsSerializer
