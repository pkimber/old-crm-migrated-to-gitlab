from base.tests.model_maker import clean_and_save

from crm.models import (
    Contact,
    Industry,
    Priority,
    Ticket,
)


def make_contact(slug, name, **kwargs):
    return clean_and_save(
        Contact(
            slug=slug,
            name=name,
            **kwargs
        )
    )


def make_industry(name, **kwargs):
    return clean_and_save(
        Industry(
            name=name,
            **kwargs
        )
    )


def make_priority(name, level):
    return clean_and_save(
        Priority(name=name, level=level)
    )


def make_ticket(contact, name, description, priority):
    return clean_and_save(
        Ticket(
            contact=contact,
            name=name,
            description=description,
            priority=priority,
        )
    )
