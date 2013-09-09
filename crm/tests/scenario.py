from crm.models import (
    Contact,
    Note,
    Ticket,
)
from crm.tests.model_maker import (
    make_contact,
    make_note,
    make_priority,
    make_ticket,
    make_user_contact,
)
from login.tests.scenario import (
    get_user_fred,
    get_user_sara,
    get_user_staff,
)


def contact_contractor():
    staff = get_user_staff()
    # fred has a farm
    fred = get_user_fred()
    farm = make_contact(
        'farm',
        "Fred's Farm",
    )
    make_user_contact(fred, farm)
    fence = make_ticket(
        farm, fred, 'Fence the orchard', make_priority('High', 1)
    )
    make_note(
        fence,
        staff,
        'Forgot to order fence posts',
    )
    # sara has a smallholding
    sara = get_user_sara()
    smallholding = make_contact(
        'smallholding',
        "Sara's Smallholding",
    )
    make_user_contact(sara, smallholding)


def get_contact_smallholding():
    return Contact.objects.get(slug='smallholder')


def get_contact_farm():
    return Contact.objects.get(slug='farm')


def get_note_fence_forgot():
    fence = get_ticket_fence()
    staff = get_user_staff()
    return Note.objects.get(ticket=fence, user=staff)


def get_ticket_fence():
    fred = get_user_fred()
    farm = get_contact_farm()
    return Ticket.objects.get(contact=farm, user=fred)
