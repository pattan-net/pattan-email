# pe

  CLI utility for querying the SendGrid API  
  Expects to find the SendGrid API key as the **SENDGRID_API_KEY** environment variable.

## Usage:
`pe [OPTIONS] COMMAND [ARGS]`

## Options:
  **--help**  Show this message and exit.

## Commands:

  **ga**  - Get SendGrid ASMs (unsubscribe groups)
    
  **gc**  - Get and format configuration for [PattanEmail](../pattan_sendgrid/PattanEmail.md) class
  
  **gi**  - Get SendGrid ip pools
  
  **gs**  - Get SendGrid approved senders
  
  **gt**  - Get SendGrid dynamic templates
  
  **gtd** - Get details for a specific template
  
  **gtv** - Get the variables defined in a specific template
