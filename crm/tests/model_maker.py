from base.tests.model_maker import clean_and_save

from crm.models import Contact


def make_contact(slug, name, **kwargs):
    return clean_and_save(
        Contact(
            slug=slug,
            name=name,
            **kwargs
        )
    )
