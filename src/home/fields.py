from django.utils import translation


class TranslatedField:
    def __init__(self, sk_field, en_field):
        self.sk_field = sk_field
        self.en_field = en_field

    def __get__(self, instance, owner):
        if translation.get_language() == "en":
            field = getattr(instance, self.en_field)
            if field:
                return field
        return getattr(instance, self.sk_field)
