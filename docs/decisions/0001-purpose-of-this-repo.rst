1. Purpose of this Repo
=======================

Status
------

Accepted

Context
-------

We need to show notices (privacy policy updates, terms of service changes, etc) to the user with the ability for the user to confirm that they've seen the notice.

Decision
--------

With this in mind, we've decided to make a new plugin for edx-platform to keep track of these notices and acknowledgments. The sole purpose of this repo currently is to store notices, provide an API for a frontend client to know which notices the user hasn't acknowledgement yet, and provide an API to let the user acknowledge a notice.

Rejected Alternatives
---------------------

We looked into taking care of this via external tools, but we also wanted to keep the data close to the rest of our data and allow the rest of the Open edX platform to be able to easily customize the experience of what to show or block based on if a user acknowledged the notice or not.

Other IDA plugin
~~~~~~~~~~~~~~~~
This data is not *necessarily* related to the LMS in anyway, so it didn't necessarily need to be a platform plugin versus a plugin in any of our other IDAs. However we will allow use of imported edx-platform code, so if we install this elsewhere in the future, those imports will need to be moved to a common space.
