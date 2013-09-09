from crm.models import (
    Contact,
)
from crm.tests.model_maker import (
    make_contact,
    make_user_contact,
)
from login.tests.scenario import (
    get_fred,
    get_sara,
)


def contact_contractor():
    farm = make_contact(
        'farm',
        "Fred's Farm",
    )
    make_user_contact(get_fred(), farm)
    smallholding = make_contact(
        'smallholding',
        "Sara's Smallholding",
    )
    make_user_contact(get_sara(), smallholding)


def get_smallholding():
    return Contact.objects.get(slug='smallholder')


def get_farm():
    return Contact.objects.get(slug='farm')
