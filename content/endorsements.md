---
title: "Endorsements"
description: "Endorsements for Michael Turon, candidate for SFUSD Board of Education November 3, 2026."
summary: "Coalition, labor, parent, and community endorsements for Michael Turon's SFUSD Board of Education campaign."
date: 2026-05-12
lastmod: 2026-05-12
translationKey: "endorsements"
layout: "endorsements"
schema_type: "WebPage"
inLanguage: "en"
canonical_language: "en"
canonical_path: "/endorsements/"
translation_status: "live"
include_in_llms: true
is_active: false
images:
  - "/img/endorsements/og.png"
---

{{< endorsements-renderer
  data_source="endorsements"
  active_field="is_active"
  inactive_state="dormant"
>}}

<!--
  Activation logic (Architecture Decision 10.C):

    is_active: false (default)
      -> Render "We are collecting endorsements." dormant state.
      -> Show the Individual Endorsement form.
      -> Show the Organization Endorsement form.
      -> Do NOT render any endorser list, even if data/endorsements.yaml has entries.
         (Disagreement is a preflight failure — see Phase1_Preflight_Checklist.md §1.)

    is_active: true
      -> Render the endorser list above the forms.
      -> Sort: featured first, then category order
         (labor, educator, parent, community, elected, organization, newspaper, other),
         then quote_date descending, then name.
      -> If data/endorsements.yaml is empty: render the
         "endorsements coming soon" state and fail preflight §1.

  First endorsement activation procedure (no code changes required):

    1. Add the endorsement record to data/endorsements.yaml.
    2. Flip is_active: true in this file (and in the six translated scaffolds).
    3. Run AI translation of the quote per Phase1_Translation_Workflow.md.
    4. Set per-language translation_status to live in
       data/translation_status.yaml only after Sam Ray sign-off on labor
       references and Lauren sign-off on financial references.
    5. hugo --minify; Cloudflare Pages preview; merge to main.
-->

## We are collecting endorsements

This page lights up the moment the first endorsement lands. Until then, we are talking to coalitions, listening, and answering questions on the record.

If you want to endorse, or if you represent an organization that wants to evaluate the campaign:

- **Individuals** can endorse using the form below.
- **Organizations** can request the campaign questionnaire using the form below or by emailing [info@turonsf.com](mailto:info@turonsf.com).
- **UESF members** can also email [info@turonsf.com](mailto:info@turonsf.com) to set up a direct conversation with Michael.

{{< endorsement-form
  kind="individual"
  fields="name,email,city,why"
  submit_action="action_network"
  thank_you_message="form_success"
>}}

{{< endorsement-form
  kind="organization"
  fields="organization_name,contact_name,email,role,why,logo_upload"
  submit_action="action_network"
  thank_you_message="form_success"
>}}
