# Module pattan_sendgrid.models
Pydantic-derived data models representing the information used by the [PattanEmail](PattanEmail.md) class.

## Classes

### Config

Gathers the other models described below, and defines validation on those populated by querying the SendGrid API.
    
#### Class variables
*api_key*: string

*email_templates*: dictionary[string, EmailTemplate]

*ip_pools*: dictionary[string, IpPool]

*senders*: dictionary[string, Sender]

*unsubscribe_groups*: dictionary[string, UnSubscribeGroup]

### EmailTemplate
Represents a SendGrid dynamic template.
    
#### Class variables

*id*: string

*name*: string

### From

#### Class variables

*email*: string

*name*: string

### IpPool

#### Class variables

*name*: string

### Sender

#### Class variables

*address*: string

*address_2*: string

*city*: string

*from_address*: From

*nickname*: string

*reply_to*: From

*state*: string

*zip*: string

### UnSubscribeGroup

#### Class variables

*id*: integer
