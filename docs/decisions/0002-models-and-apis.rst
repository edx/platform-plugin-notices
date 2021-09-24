2. Models and API design
========================

Status
------

Accepted

Context
-------

We had a few guidelines we wanted to stick close to:
1. The addition, removal, disablement, or updating of notices should be done easily outside of any code deployment.
2. If a user hasn't logged in for a while, we wanted to be able to keep track of all notices they still need to acknowledge.
3. Client side implementation should be simple, leaving the heavy lifting to this server side application.

Decision
--------

The notices model will house the full notice that will be displayed to the user. It will display the notice in a way that it can be redirected to or iframed into an existing page or app. All administration of the notice content will be done via Django Admin.
