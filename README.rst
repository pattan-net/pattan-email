============
pattan-email
============

pattan-email is a python package that combines the sendgrid package
with PaTTAN specific configurations.


Quick start
-----------
1. Add pattan-email the following line to your requirements.txt
    pattan-email @ git+ssh://git@github.com/pattan-net/pattan-email.git

2. Usage
    from pattan_email.PattanEmail import PattanEmail
    ....
    mailer = PattanEmail( api_key={SENDGRID API KEY}, [purpose='transactional' or 'marketing'])


Details
-------
1. When testing you can specify a specific commit in your requirements.text
    pattan-email @ git+ssh://git@github.com/pattan-net/pattan-email.git@6c5043126464a2034b402f59b0c382469801ef5e
2. The pattan-email package defines the sendgrid package as a dependency.  Therefore the sendgrid
package does not need to be defined in the requirements.txt file of the application using this package
3. If you made a change to this repo, you can not deploy on top of an already running instance. You 
should provision one from scratch. 



Resources
---------
1. https://docs.djangoproject.com/en/5.0/intro/reusable-apps/
2. https://pypi.org/project/sendgrid/


