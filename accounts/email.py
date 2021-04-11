from djoser.email import ActivationEmail as InbuiltActivationEmail

class ActivationEmail(InbuiltActivationEmail):
    template_name = 'email/activation.html'
