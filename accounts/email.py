from django.contrib.auth.tokens import default_token_generator
from djoser.email import ActivationEmail as InbuiltActivationEmail

from djoser.conf import settings
from djoser import utils

class ActivationEmail(InbuiltActivationEmail):
    template_name = "email/activation.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")

        if user.is_kalafex_admin:
            role = 'kalafex_admin'
        if user.is_artist:
            role = 'artist'
        if user.is_customer:
            role = 'customer'

        context["url"] = settings.ACTIVATION_URL.format(role=role, **context)
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        return context
