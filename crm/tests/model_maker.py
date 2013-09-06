from base.tests.model_maker import clean_and_save

from crm.models import (
    Contact,
    Industry,
    Note,
    Priority,
    Ticket,
    UserContact,
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


def make_note(ticket, user, name, **kwargs):
    return clean_and_save(
        Note(
            ticket=ticket,
            user=user,
            name=name,
            **kwargs
        )
    )


def make_priority(name, level):
    return clean_and_save(
        Priority(name=name, level=level)
    )


def make_ticket(contact, user, name, description, priority, **kwargs):
    return clean_and_save(
        Ticket(
            contact=contact,
            user=user,
            name=name,
            description=description,
            priority=priority,
            **kwargs
        )
    )


def make_user_contact(user, contact):
    return clean_and_save(
        UserContact(user=user, contact=contact)
    )
