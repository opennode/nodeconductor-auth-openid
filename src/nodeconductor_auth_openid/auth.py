from __future__ import unicode_literals

from django.conf import settings
from django_openid_auth.auth import OpenIDBackend

from . import utils


class NodeConductorOpenIDBackend(OpenIDBackend):
    """ This backend sets user's full_name and email. """

    def update_user_details(self, user, details, openid_response):
        updated_fields = []

        # Don't update full_name if it is already set
        if not user.full_name:
            user.full_name = '{} {}'.format(details['first_name'], details['last_name']).strip()
            updated_fields.append('full_name')

        # Don't update email if it is already set
        if not user.email and details['email']:
            user.email = details['email']
            updated_fields.append('email')

        # Civil number should be updated after each login because it can be changed or
        # defined for user.
        if 'openid.identity' in details:
            civil_number = utils.get_civil_number(details['openid.identity'])
            if user.civil_number != civil_number:
                user.civil_number = civil_number
                updated_fields.append('civil_number')

        if updated_fields:
            user.save(update_fields=updated_fields)

    def create_user_from_openid(self, openid_response):
        user = super(NodeConductorOpenIDBackend, self).create_user_from_openid(openid_response)

        openid_identity = openid_response.getSigned('http://specs.openid.net/auth/2.0', 'identity')
        if openid_identity:
            user.civil_number = utils.get_civil_number(openid_identity)

        method_name = settings.NODECONDUCTOR_AUTH_OPENID.get('NAME', 'openid')
        user.registration_method = method_name

        user.save(update_fields=['civil_number', 'registration_method'])
        return user

    def _get_preferred_username(self, nickname, email):
        nickname = super(NodeConductorOpenIDBackend, self)._get_preferred_username(nickname, email)
        return nickname.replace(' ', '')
