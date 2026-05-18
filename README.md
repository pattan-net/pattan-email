# pattan-sendgrid

**pattan-sendgrid** is a Python package that wraps the **sendgrid** package
with PaTTAN-specific configurations.

## Quick start
1. Installation (bash):  
    `pip install pattan-sendgrid`
2. Create an environment variable **SENDGRID_API_KEY** and set its value to your SendGrid API key:  
    `export SENDGRID_API_KEY={your SENDGRID_API_KEY}`
3. Generate the config the package uses by redirecting the output of the **gc** command to a file or copy/paste to a file.  Keep this file out of version control as it will include your SendGrid API key (bash):  
    `pe gc >{your filename}`  
    If you are using Django, the project's **.env** is a good place for this value.
4. Use the output from the command in step **3** to initialize the **PattanEmail** class (bash): 
    ```
    from pattan_sendgrid import PattanEmail
     ...
    emailer = PattanEmail({command output from step 3})
   ```

## Resources
1. https://docs.djangoproject.com/en/5.0/intro/reusable-apps/
2. https://pypi.org/project/sendgrid/


