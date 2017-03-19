from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_auth.views import LoginView

from .models import Editor
from .serializers import EditorDetailsSerializer


class AllEditorsView(generics.ListCreateAPIView):
    queryset = Editor.objects.prefetch_related('states')
    serializer_class = EditorDetailsSerializer


class SingleEditorView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Editor.objects.all()
    serializer_class = EditorDetailsSerializer


class AllRolesView(APIView):
    def get(self, request, *args, **kwargs):
        return Response([[role[0], role[1]] for role in Editor.EDITOR_ROLES])


class EditorLoginView(LoginView):
    """
    Adapted from django-rest-auth's LoginView.  Allows profile information AND token to be 
    sent with successful login, cutting out the multiple roundtrips and making more
    complicated routing/validation based on user details possible
    """
    def get_response(self):
        data = {
            'editor': EditorDetailsSerializer(self.user).data,
            'token': self.get_response_serializer()(self.token).data
        }

        return Response(data, status=status.HTTP_200_OK)
