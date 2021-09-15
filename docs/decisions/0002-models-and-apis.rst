2. Models and API design
========================

Status
------

Under Review

Context
-------

We had a few guidelines we wanted to stick close to:
1. The addition, removal, disablement, or updating of notices should be done easily outside of any code deployment.
2. If a user hasn't logged in for a while, we wanted to be able to keep track of all notices they still need to acknowledge.
3. Client side implementation should be simple, leaving the heavy lifting to this server side application.

Decision
--------

With this in mind, we've decided to make a new plugin for edx-platform to keep track of these notices and acknowledgments. The sole purpose of this repo currently is to store notices, provide an API for a frontend client to know which notices the user hasn't acknowledgement yet, and provide an API to let the user acknowledge a notice.

The notices model will house the full notice that will be displayed to the user. It will display the notice in a way that it can be redirected to or iframed into an existing page or app. All administration of the notice content will be done via Django Admin.

Rejected Alternatives
---------------------

External tools
~~~~~~~~~~~~~~
We looked into taking care of this via external tools, but we also wanted to keep the data close to the rest of our data for reporting purposes.

Other IDA plugin
~~~~~~~~~~~~~~~~
This data is not *necessarily* related to the LMS in anyway, so it didn't necessarily need to be a platform plugin versus a plugin in any of our other IDAs. This functionality didn't necessarily align with any of our other services any better, nor was it large enough to warrant it's own service, so it was decided to be an isolated platform plugin. If, in the future, a *user* service exists, this could probably be installed there instead with the necessary plugin code changes.
