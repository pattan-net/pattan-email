from pattan_email.models import Config


def main():
    api_key = 'lakjdsflkajsdfds'
    unsubscribe_groups = {
        'SendGrid Tech Test Group': {
            'group_id': 31335
        },
        'pattan unsubscribe': {
            'group_id': 32801
        }
    }
    senders = {
        "DEFAULT": {
            'from_address': {'email': 'no-reply@pattan.net'},
            'nickname': 'no-reply@pattan.net',
            'reply_to': 'no-reply@pattan.net',
            'address': '6340 Flank Drive',
            'city': 'Harrisburg',
            'state': 'Pennsylvania',
            'zip': '17112'
        }
    }

    config = Config(api_key=api_key, senders=senders, unsubscribe_groups=unsubscribe_groups)

    print(config.model_dump())


if __name__ == '__main__':
    main()
