import requests
import json

from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import ContactSerializer


class ContactFormView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        data = request.data

        email_serializer = ContactSerializer(data=data)

        if email_serializer.is_valid():
            email_data = email_serializer.data

            r = requests.post('https://www.google.com/recaptcha/api/siteverify', {
                    'secret': settings.RECAPTCHA_PRIVATE_KEY,
                    'response': email_data['recaptcha']
                })

            if not json.loads(r.content.decode())['success']:
                return Response({'non_field_errors': 'invalid reCaptcha. Please verify your identity'})

            email = EmailMessage(
                'Contact Form message from {}'.format(email_data['name']),
                email_data['message'],
                'info@freefairunfettered.org',
                ['info@freefairunfettered.org'],
                headers={'Reply-To':'{0} <{1}>'.format(email_data['name'], email_data['email'])}
            )

            try:
                email.send()

            except:
                return Response(
                    {'non_field_errors': ['There was a problem sending your email. Please try again later.']},
                    status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {'message': 'Thanks for your note! We hope to get back to you soon.'},
                status.HTTP_200_OK
            )

        else:
            return Response(email_serializer.errors, status.HTTP_400_BAD_REQUEST)
