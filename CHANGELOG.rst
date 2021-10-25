Change Log
----------

..
   All enhancements and patches to notices will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~

[0.9.0] - 2021-10-25
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Add in a snooze limit feature that will only allow a notice to be snoozed a number of times

[0.8.2] - 2021-10-21
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Update requirements

[0.8.1] - 2021-10-21
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Add ability to reshow notice after a snooze period via setting

[0.7.3] - 2021-10-20
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Make AcknowledgedNotice user editable in the admin for testing purposes

[0.7.2] - 2021-10-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Make AcknowledgedNotice user readonly in the admin for performance

[0.7.1] - 2021-10-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Add Waffle Flag to enable and disable the feature for rollout

[0.6.1] - 2021-10-7
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Add Python API for retrieving unack'd and active notice data
* Add Plugin Context API for notice data to support redirects on the LMS Course Dashboard

[0.5.1] - 2021-10-7
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Disallow dismissal after confirmation of notice

[0.4.1] - 2021-10-7
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Allow inactive (non-email-verified) users to call APIs

[0.3.1] - 2021-10-1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Add mobile calls so notice code can deep link

[0.2.2] - 2021-09-24
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Add fallback language on render view
* Add Bearer auth to APIs for mobile
* Add login requirement to render view
* Add first edx-platform dependency

[0.2.1] - 2021-09-22
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Utility functions for custom notice code to use to call APIs

[0.1.1] - 2021-09-16
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Moved to server rendered notice model
* Add mandatory types to acknowledgement to track more states

[0.1.0] - 2021-08-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* First release on PyPI.
