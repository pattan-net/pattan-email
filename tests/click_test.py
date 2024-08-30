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

    templates = {
        'I14 Notify POCS - Post Survey Outreach': {'id': 'd-8442f605a9994111bb110712221dfb1b'},
        'Survey Confirmation': {'id': 'd-eea0f32d9ef143f48160100c363281af'},
        'Survey Request': {'id': 'd-66c5cd0a14224c4c9e3d52ac840486ff'},
        'Pattan Standard Template': {'id': 'd-3890a147fac341c187cc424b1b595c4c'},
        'myplan4success_pc_post_push2': {'id': 'd-c6160024a0ac418885290c907a228407'},
        'myplan4success_pc_post_push1': {'id': 'd-57db6c0d9c9041f1adc883c55e433738'},
        'myplan4success_leaver_post_push2': {'id': 'd-c28a6f977f424632b8ae7c780d66575c'},
        'myplan4success_leaver_post_push1': {'id': 'd-f72706b6ebda498f974f2bba048a6924'},
        'PaTTAN_Short_Critical': {'id': 'd-3e075978344e4465b5471954f7a63ba4'},
        'FAB_Facilitator_Password_Reset_Prod': {'id': 'd-29e0609ac04e4fff98d3c874b85c5d13'},
        'Workshop-Act48 Conference Email': {'id': 'd-d213862c949c445f8313008581707af1'},
        'PaTTAN Training Annoucement': {'id': 'd-dc480849a02e45418952c7363cffc8be'},
        'Email Account Verification': {'id': 'd-5fe4e5951a6f4644a3c7798dc87373f6'}
    }

    config = Config(api_key=api_key, senders=senders, unsubscribe_groups=unsubscribe_groups, email_templates=templates)

    print(config.model_dump())


if __name__ == '__main__':
    main()
