"""A fake SendGrid client, so the CLI and library can be tested without a
network connection or an API key.

The real client is reached as ``ctx.obj['sg_client']`` in the CLI and as
``PattanEmail.sg`` in the library; both are duck-typed, so these stand-ins only
need the attribute chains and the ``.body`` bytes that the code actually reads.
"""
import json


class _Response:
    """Mimics the SendGrid response object, which exposes an encoded body."""

    def __init__(self, payload):
        self.body = json.dumps(payload).encode('utf-8')


def make_sender(nickname):
    """Build a sender in the shape the senders endpoint returns.

    ``gc`` deletes the bookkeeping keys and renames ``from``, so all of them
    have to be present for the test to exercise the real code path.
    """
    contact = {'email': f'{nickname}@pattan.net', 'name': nickname}
    return {
        'nickname': nickname,
        'from': contact,
        'reply_to': contact,
        'address': '6340 Flank Dr',
        'address_2': '',
        'city': 'Harrisburg',
        'state': 'PA',
        'zip': '17112',
        # deleted by gc, but the endpoint always returns them
        'updated_at': 1,
        'created_at': 1,
        'locked': False,
        'id': 7,
        'verified': True,
        'country': 'US',
    }


class FakeSendGridClient:
    """Serves canned senders, IP pools, unsubscribe groups and templates."""

    def __init__(self, senders=(), ip_pools=(), unsubscribe_groups=(), templates=()):
        self._senders = [make_sender(n) for n in senders]
        self._ip_pools = [{'name': n} for n in ip_pools]
        self._groups = [{'name': n, 'id': i} for i, n in enumerate(unsubscribe_groups, 1)]
        self._templates = [{'id': f'd-{i}', 'name': n} for i, n in enumerate(templates, 1)]

        outer = self

        class _Senders:
            @staticmethod
            def get():
                return _Response(outer._senders)

        class _Pools:
            @staticmethod
            def get():
                return _Response(outer._ip_pools)

        class _Ips:
            pools = _Pools()

        class _Groups:
            @staticmethod
            def get(query_params=None):
                return _Response(outer._groups)

        class _Asm:
            groups = _Groups()

        class _Templates:
            @staticmethod
            def get(query_params=None):
                return _Response({'templates': outer._templates})

            @staticmethod
            def _(template_id):
                class _One:
                    @staticmethod
                    def get():
                        return _Response({
                            'name': template_id,
                            'versions': [{
                                'active': 1,
                                'plain_content': 'Hi {{first_name}} {{unsubscribe}}',
                                'subject': 'Re: {{topic}}',
                            }],
                        })
                return _One()

        self.senders = _Senders()
        self.ips = _Ips()
        self.asm = _Asm()
        self.templates = _Templates()
