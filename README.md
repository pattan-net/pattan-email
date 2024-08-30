============
pattan-email
============

pattan-email module and cli application to send emails via sendgrid.


Install
----
```python
pip install pattan-email
```

Configuration
-------------
Configuration file .pattan-email.json pattan-email will look for this file in your homedirectory 
```json
{
  "api_key": "{YOUR SENDGRID API KEY}",
  "senders": {
    "{Name of Sender}": {
      "from_address": {
        "email": "no-reply@example.com"
      },
      "nickname": "no-reply@example.com",
      "reply_to": "no-reply@example.com",
      "address": "1 main st",
      "city": "Harrisburg",
      "state": "Pennsylvania",
      "zip": "17112"
    },
    ...
  },
  "unsubscribe_groups": {
    "{Group Name}": {
      "group_id": {Sendgrid Group ID}
    },
    ...
  },
  "email_templates": {
    "{Template name}": {
      "id": "{Sendgrid template id}"
    },
    ...
  }
}
```

Usage
-------
## cli
pattanemail send --sender senders_dict_key --template template_dict_key

## as a module
```python
from pattan_email import Config, PattanEmail
config = Config(api_key=api_key, senders=senders, unsubscribe_groups=unsubscribe_groups, email_templates=templates)
emailer = PattanEmail(config)

```

Resources
---------
1. https://docs.djangoproject.com/en/5.0/intro/reusable-apps/
2. https://pypi.org/project/sendgrid/


