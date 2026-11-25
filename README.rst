platform-plugin-notices
=============================

|pypi-badge| |ci-badge| |codecov-badge| |doc-badge| |pyversions-badge| |license-badge|

**This repo is not currently accepting open source contributions**

Overview
--------

This plugin for edx-platform manages notices that a user must acknowledge. It only stores the content of the notices and whether a user has acknowledged them. Presentation and other client side decisions will be left to the frontends that utilize these APIs.

This Django app contains notices that a user must acknowledge before continuing to use the site. This app will have two API endpoints to facilitate that:
1. An endpoint to return links to all notices that the user hasn't acknowledged.
2. An endpoint to acknowledge that a user has seen the notice. This endpoint's URL will be passed to the client via the first endpoint.

Two ways to show a notice
~~~~~~~~~~~~~~~~~~~~~~~~~

Notices are created and edited in Django Admin (``Notice`` with one ``TranslatedNoticeContent`` per language, an ``en`` row is required as the fallback). No deploy is needed to add, change or switch off a notice (untick ``active``).

* **Full-page notices (default).** ``GET /notices/api/v1/unacknowledged`` returns links to the rendered notice pages. Frontends such as the Learning MFE redirect the learner to the page, which acknowledges through ``POST /notices/api/v1/acknowledge``. The global flag ``notices.enable_notices`` turns this on.
* **Refund policy modal.** ``GET /notices/api/v1/refund-policy`` returns ``{"show", "notice_id", "body", "language"}`` as JSON so an MFE can show the notice in a modal (see ``@edx/refund-policy-notice-plugin`` in ``frontend-plugins``, mounted in the ``header_notice_slot`` of ``frontend-component-header-edx``). It is served for the ``Notice`` whose name equals the ``NOTICES_REFUND_POLICY_NOTICE_NAME`` setting (default ``Refund Policy Change``) and is controlled by the waffle flag ``commerce.show_refund_policy_change_notice``. It ignores ``launch_date`` and snoozing, strips HTML from the body, and the modal acknowledges with ``POST /notices/api/v1/acknowledge`` (``confirmed``). That notice is excluded from the ``unacknowledged`` list, so it never redirects to a full page.

Refund policy modal notes:

* The ``Notice`` name must match ``NOTICES_REFUND_POLICY_NOTICE_NAME`` exactly and must not be renamed afterwards. The name decides how the notice is shown: if it no longer matches, the notice becomes a full-page notice and appears in ``unacknowledged`` (when ``notices.enable_notices`` is on), and learners are redirected to a page with no confirm button.
* The body is converted from HTML to plain text: paragraphs are separated by one blank line, ``<br>`` becomes a line break, links keep only their text (the URL is dropped), and the contents of ``<style>``, ``<script>`` or ``<button>`` show up as text, so keep the HTML to simple paragraphs.
* The notice is web only. Mobile apps calling ``unacknowledged?mobile=true`` do not receive it.
* ``edx.bi.user.displayed_notice`` and ``edx.bi.user.acknowledged_notice`` are emitted server side with ``tracker.emit``, so they always reach the tracking log. They reach Segment only if both names are in ``EVENT_TRACKING_SEGMENTIO_EMIT_WHITELIST`` in the LMS config. Full-page notices send the acknowledgement event to Segment from the browser, so add both names to the whitelist to keep the two in one place.

Documentation
-------------

(TODO: `Set up documentation <https://openedx.atlassian.net/wiki/spaces/DOC/pages/21627535/Publish+Documentation+on+Read+the+Docs>`_)

Developing in Devstack
~~~~~~~~~~~~~~~~~~~~~~
Make sure the LMS container is running in Devstack, then

.. code-block::

  git clone git@github.com:edx/platform-plugin-notices.git <devstack_folder>/src
  cd <devstack_folder>/devstack
  make dev.shell.lms
  pip install -e /edx/src/platform-plugin-notices
  cd /edx/app/edxapp/edx-platform
  ./manage.py lms migrate

Once that is done, LMS will pickup the plugin and saves to existing files should cause a devserver restart with your changes. Occasionally when adding a new file, you may need to restart the LMS container in order for it to pickup the changes.

Enabling the Notices Plugin in the LMS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Notices plugin functionality is enabled via use of a waffle flag. After installation of the plugin you need to do the following in devstack:

#. Log into the LMS Django Admin (http://localhost:18000/admin/)
#. Add a new waffle flag (http://localhost:18000/admin/waffle/flag/add/)
#. Name the waffle flag ``notices.enable_notices``
#. Set `Everyone` to `Yes`
#. Save the waffle flag.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

This repo is not currently accepting open source contributions

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Support
-------

If you're having trouble, we have discussion forums at https://discuss.openedx.org where you can connect with others in the community.

Our real-time conversations are on Slack. You can request a `Slack invitation`_, then join our `community Slack workspace`_.

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx-slack-invite.herokuapp.com/
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help

.. |pypi-badge| image:: https://img.shields.io/pypi/v/edx-notices.svg
    :target: https://pypi.python.org/pypi/edx-notices/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/edx/platform-plugin-notices/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/edx/platform-plugin-notices/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/edx/platform-plugin-notices/coverage.svg?branch=main
    :target: https://codecov.io/github/edx/platform-plugin-notices?branch=main
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/platform-plugin-notices/badge/?version=latest
    :target: https://platform-plugin-notices.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/edx-notices.svg
    :target: https://pypi.python.org/pypi/platform-plugin-notices/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/edx/platform-plugin-notices.svg
    :target: https://github.com/edx/platform-plugin-notices/blob/main/LICENSE.txt
    :alt: License
