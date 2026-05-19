# Module pattan_sendgrid.exceptions
All classes can accept an optional message string as an argument to the constructor.

## Classes

### MailSendFailure
Raise this to indicate a failure to transmit to the SendGrid API, or an error returned from the API.

### MalformedConfiguration
Raise this to indicate an error in parsing the configuration data passed to the [PattanEmail](PattanEmail.md) constructor.

### MissingAPIKey
Raise this when the environment variable **SENDGRID_API_KEY** is not found.
