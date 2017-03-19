from django.test import TestCase
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.test import force_authenticate, APIRequestFactory

from .permissions import IsAdminEditor
from .models import Editor

factory = APIRequestFactory()


class PermissionTestView(APIView):
    permission_classes = [IsAdminEditor, ] 

    def get(self, request, *args, **kwargs):
        return Response(status=HTTP_204_NO_CONTENT)


class EditorPermissionTests(TestCase):
    def setUp(self):
        self.view = PermissionTestView.as_view()

    def test_editor_with_access_view(self):
        """
        If the logged in editor is an ADMIN user, we should have proper access
        """
        editor = Editor.objects.create(email="test@test.com", role=Editor.ADMIN)

        request = factory.get('/editors/editor-test/')
        force_authenticate(request, editor)

        response = self.view(request)

        self.assertEqual(response.status_code, 204)

    def test_editor_without_access_view(self):
        """
        If the logged in editor is not ADMIN, we should return a 403
        """
        editor = Editor.objects.create(email="test@test.com", role=Editor.EDITOR)

        request = factory.get('/editors/editor-test/')
        force_authenticate(request, editor)

        response = self.view(request)

        self.assertEqual(response.status_code, 403)

    def test_anonymous_user(self):
        """
        If no user is logged in, we should return a 401 (not authenticated)
        """
        request = factory.get('/editors/editor-test/')

        response = self.view(request)

        self.assertEqual(response.status_code, 401)


