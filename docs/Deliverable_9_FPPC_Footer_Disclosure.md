# Deliverable 9: FPPC §84305 Standard Footer Disclosure

**Status:** SAM RAY REVIEW REQUIRED — FPPC §84305 disclosure ENGLISH SOURCE
locked from v1.2.0; per-language translation REQUIRES SAM RAY REVIEW BEFORE
PUBLICATION; financial figures REQUIRE LAUREN TURON REVIEW BEFORE PUBLICATION.

**Sam Ray sign-off (English source unchanged from v1.2.0):** _________________
Date: _________________

**Lauren Turon sign-off (treasurer identity unchanged from v1.2.0):** _________________
Date: _________________

---

## 9.1 English source (LOCKED — unchanged from v1.2.0)

The FPPC §84305 footer disclosure renders in the footer partial of every
page in every language. The English source is locked from v1.2.0 and is
**not edited in v1.3.0**:

> **Paid for by Michael Turon for SFUSD Board of Education 2026.
> FPPC ID 1482971.
> Treasurer: Lauren Turon.**

Encoded in `i18n/en.toml` under the key `fppc_disclaimer`:

```toml
[fppc_disclaimer]
other = "Paid for by Michael Turon for SFUSD Board of Education 2026. FPPC ID 1482971. Treasurer: Lauren Turon."
```

**Legal basis:** Cal. Gov. Code §84305(c)(1) for mass electronic
communications; the same `Paid for by [committee name]` pattern is the
established norm for candidate-controlled websites per FPPC Regulation 18435
and Campaign Manuals 1 and 4 (Research §2.1, §2.3). FPPC ID 1482971 is
the committee's registered identifier and must appear (Research §2.3).

---

## 9.2 Per-language footer translation contract

Per Research §2.2 and §2.8, FPPC Regulation 18435 requires "same-language"
disclosures when a communication is produced in a language other than
English. The campaign's compliance approach for v1.3.0 is:

- The footer translates into each target language.
- **Proper nouns stay English:** `Michael Turon`, `Lauren Turon`, `SFUSD`,
  `FPPC`, `FPPC ID 1482971` (literal numeric string). These do not
  transliterate or localize.
- **Surrounding clauses translate:** "Paid for by ... 2026.", "Treasurer:".

The six non-English string tables in `i18n/{es,zh-Hant,zh-Hans,tl,vi,ar}.toml`
ship with the `fppc_disclaimer` key carrying the English text plus an
`# AWAITING TRANSLATION` marker. The translation workflow
(`Phase1_Translation_Workflow.md`) routes every footer translation through
Sam Ray review (FPPC-sensitive) and Lauren review (treasurer identity)
before publication.

### Reference translations (PRE-REVIEW — NOT FOR PUBLICATION)

Reference renderings the workflow can start from. Each requires Sam Ray
review before merge. Operator does not commit these unedited.

> **Spanish (`es`)** — REFERENCE, REQUIRES SAM RAY REVIEW:
> *Pagado por Michael Turon for SFUSD Board of Education 2026.
> FPPC ID 1482971.
> Tesorera: Lauren Turon.*
>
> Note: The committee name itself ("Michael Turon for SFUSD Board of
> Education") stays English because that is the formal committee name
> registered with FPPC (Research §2.4 — "obscuring identity" is the
> enforcement risk). "Pagado por" is the conventional Spanish rendering
> of "Paid for by." "Tesorera" uses the feminine form per Lauren's role.

> **Traditional Chinese (`zh-Hant`)** — REFERENCE, REQUIRES SAM RAY REVIEW:
> *本訊息由 Michael Turon for SFUSD Board of Education 2026 委員會支付。
> FPPC 註冊編號 1482971。
> 司庫：Lauren Turon。*

> **Simplified Chinese (`zh-Hans`)** — REFERENCE, REQUIRES SAM RAY REVIEW:
> *本信息由 Michael Turon for SFUSD Board of Education 2026 委员会支付。
> FPPC 注册编号 1482971。
> 司库：Lauren Turon。*

> **Tagalog (`tl`)** — REFERENCE, REQUIRES SAM RAY REVIEW:
> *Binayaran ng Michael Turon for SFUSD Board of Education 2026.
> FPPC ID 1482971.
> Ingat-yaman: Lauren Turon.*

> **Vietnamese (`vi`)** — REFERENCE, REQUIRES SAM RAY REVIEW:
> *Trả tiền bởi Michael Turon for SFUSD Board of Education 2026.
> FPPC ID 1482971.
> Thủ quỹ: Lauren Turon.*

> **Arabic (`ar`)** — REFERENCE, REQUIRES SAM RAY REVIEW:
> *دفعت من قبل Michael Turon for SFUSD Board of Education 2026.
> FPPC ID 1482971.
> أمينة الصندوق: Lauren Turon.*
>
> RTL note: Proper nouns and `FPPC ID 1482971` carry bidi isolation
> (`unicode-bidi: isolate; direction: ltr;` per Deliverable 5) so they
> read left-to-right inside the right-to-left Arabic body.

---

## 9.3 D8 vs D9 separation contract (re-stated)

Deliverable 8 (AI translation transparency disclosure) and Deliverable 9
(this FPPC §84305 footer) are **separate disclosures, separate surfaces,
separate i18n keys, separate review channels.**

| Dimension                    | Deliverable 8 (AI disclosure)              | Deliverable 9 (FPPC footer)              |
|------------------------------|--------------------------------------------|------------------------------------------|
| Speaks to                    | Translation method                         | Payment / committee identity             |
| Surface placement            | Top of page (below header, above content)  | Bottom of page (footer)                  |
| Legal basis                  | Research §2.8 / §2.9 best practice         | Cal. Gov. Code §84305 + FPPC Reg. 18435  |
| Required by law              | No (best practice)                         | Yes (mass electronic comms)              |
| Renders on English page      | No                                         | Yes                                      |
| Renders on translated page   | Yes (when status ≠ placeholder)            | Yes                                      |
| Renders on placeholder       | Translation-pending notice instead         | Yes                                      |
| i18n key (English source)    | `ai_translation_disclosure_body` + `_link_text` | `fppc_disclaimer`                  |
| Hugo partial                 | `ai-translation-disclosure.html`           | `footer.html` (existing v1.2.0)          |
| Dismissible                  | NO (OIL Decision 2 contract)               | NO (FPPC compliance)                     |
| Review channel               | Sam Ray (D8 source) + workflow per-language| Sam Ray + Lauren per-language            |

Neither replaces the other. Both render. The preflight checklist
(Deliverable 12 §5, §6) gates this contract.

---

## 9.4 Acceptance gates

- [ ] English `fppc_disclaimer` i18n key is unchanged from v1.2.0:
      "Paid for by Michael Turon for SFUSD Board of Education 2026.
       FPPC ID 1482971. Treasurer: Lauren Turon."
- [ ] FPPC ID `1482971` appears as the literal numeric string in every
      language's footer.
- [ ] Committee name `Michael Turon for SFUSD Board of Education` appears
      in Latin script (English) in every language's footer.
- [ ] Lauren Turon's name appears in Latin script in every language's footer.
- [ ] Sam Ray sign-off recorded for each of the six target-language
      translations before publication.
- [ ] Lauren Turon sign-off recorded for each of the six target-language
      translations before publication.
- [ ] D8 disclosure renders separately from D9 footer; both visible on every
      translated page (Preflight §5, §6).
- [ ] Arabic footer renders with bidi isolation on proper nouns and FPPC ID
      so `Michael Turon`, `Lauren Turon`, and `1482971` read LTR inside the
      RTL body (Preflight §3).
- [ ] No translated footer drops, paraphrases, obscures, or restates any
      financial claim. The footer carries no financial figures by design;
      financial figures live in the trust strip and content body, both
      under separate gates.


## D9 Amendment — 2026-05-13

Treasurer line removed per Sam Ray written sign-off. §84305(c)(1) requires 'Paid for by [committee name]' only for mass electronic mailings (>200/month). Website footer amended accordingly.
