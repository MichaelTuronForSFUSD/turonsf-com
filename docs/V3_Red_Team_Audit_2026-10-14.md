# v3 hub — red-team audit of the English copy, 2026-10-14

**Scope:** every English string in `data/hub_copy.json` and every outbound link in the built site, all 8 languages.  
**Method:** each factual sentence was checked against its primary source, downloaded and read on 2026-10-14. Sources: the six Mission Local articles, the four SF Parents Action questionnaires, the August 31 voter guide (English, Chinese, Spanish, Filipino, Vietnamese editions), SF.gov's candidate and election pages, the Voter Portal, and the three ActBlue pages. The copy was then edited for AI writing patterns using the humanizer checklist.  
**Who did this:** Claude, in the same session that built v3. It is not an independent human review.

## Factual errors found and fixed

| # | Was | Source says | Now |
|---|---|---|---|
| 1 | Ryan "backs the school plan now in place." | The Board voted for zones in 2020, but as of Aug. 21 the district "has yet to present a plan" (Mission Local). Michael's questionnaire says it was pushed to 2028–29. | The page says the zones haven't been presented and that Ryan wants them delivered "without further delay." |
| 2 | Ryan "says do not delay when it can be avoided." | "The superintendent must deliver it without further delay," on the condition that "integration goals must be built into the zone design from the start." | Both points, stated accurately. |
| 3 | Phil "calls for data and a careful plan." | Phil answered **yes** and "led the board in naming zone-based enrollment as a Superintendent priority." | Phil said yes and led the Board in making it a priority, with data and careful planning. |
| 4 | Alida's position was described without her answer. | Alida's short answer: **"it depends."** | "Alida said it depends," followed by her conditions. |
| 5 | "This does not show that Phil or Alida oppose change." | Staging (a contrast that answers a claim nobody made). | Cut. The answers speak for themselves. |
| 6 | Alida "says it may not save money." | "Let's be clear: Closing schools won't save money." | "won't save money." |
| 7 | Only Ryan's forum lightning-round answer was given. | "Garibay, Fisher, Kim and Tung said they supported school closures and Cheung, Hazelton, Lee and Tello said they did not." | All three answers: Phil and Alida yes, Ryan no. |
| 8 | Ryan's written answer "leaves this choice open until the district acts on school assignment and enrollment." | "Consolidation may be necessary at some point... but it is not the only solution"; first steps are absenteeism and lottery reform. | Paraphrased from his own words. |
| 9 | Link label: "the three candidates' August 21 answers." | The article covers all eight candidates. | "Candidates on school assignment, Aug. 21." |
| 10 | "Read or listen to the voter guide" linked `sfelections.gov/vip`. | That URL redirects to the same English PDF. There is no audio there. | Audio link now goes to the official MP3 ZIP (English, 73 MB) listed on SF.gov. |
| 11 | "Check your ballot in the Voter Portal." | The guide says the portal is for registration, ballot tracking, polling place, and districts, not for viewing ballot contents. | Label lists what the portal does. The status box points to the sample ballot every voter is mailed. |
| 12 | Shared answers: "fairness, student results, reading and math, the Board's role, and school budgets." | Item 2 is a twice-yearly school-level math and reading dashboard. Item 5 protects the most vulnerable students in budget fixes. | Each of the five statements is described as written. |
| 13 | "The voter guide... came before my October 3 decision." | Withdrawal was July 20 (corrected earlier today). | Removed. |

## Facts checked and kept

- SF.gov lists 8 Board of Education filers; Michael is not among them (Oct. 14). No reason is given.
- All four questionnaires (Kim, Fisher, Hazelton, Turon) score 4 = "Strongly Agree" on all five opening statements. None is dated.
- Phil's teaching answer covers data, coaching, early intervention, and aligning the budget to outcomes. His fiscal answer covers forecasting and spending within means.
- Alida's voter-guide statement: "early intervention, inclusion, and meaningful support." Her retention answer covers pay and benefits, "grow your own" credential programs, and special education caseloads.
- Ryan's voter-guide statement covers lottery reform, paying educators "fairly and on-time," and absenteeism. His retention answer covers fixing payroll. He runs Mariposa Kids (after-school programs, Mission and Bernal Heights).
- Phil and Alida each cite about 14,000 empty seats.
- The voter guide is dated August 31 and says no official agency checks candidate statements for accuracy.
- November 3, 2026 is a Tuesday.
- The ActBlue pages are headed "Phil Kim for School Board November 2026," "Reelect Alida Fisher to the San Francisco School Board," and "Donate to Ryan Hazelton for SF Board of Education."

## Link changes

- Each language links its own official voter guide: Spanish (SP), Chinese for Cantonese and both Chinese routes (CH, Traditional script), Filipino (FI), Vietnamese (VI). English and Arabic link the English guide. The Arabic copy says no Arabic edition exists.
- Alida's and Ryan's cards now link their voter-guide statements at the right PDF page: p. 31 in English; p. 23 (Alida) and p. 24 (Ryan) in the translated guides. Ryan's card previously linked the assignment article instead of anything about his own reasons.
- Source links say "(Mission Local)" and, in translations, that the source is in English.

**Link QC:** all 25 unique URLs return 200/206. The Voter Portal blocks curl (403) but loads in a browser.

## Writing changes (humanizer pass)

- Removed the repeated card closers ("These are his plans. They are not proof of results."), plus the "Three candidates. Three reasons." heading and the self-describing "Each card has a site link..." line. Positions are attributed in the sentence itself ("In his published answers, he says...").
- Replaced the choppy short sentences (written for a Flesch score) with normal sentences, kept short enough to read on a phone.
- Gave each card a different opening, so the three no longer start "I endorse X for...".
- Added one sentence in Michael's voice, supported by his questionnaire ("What I will not do: Accept one more delay."): "My own questionnaire answer is closest to Ryan's: no more delays." Also added "and so did I" to the shared-answers paragraph, since his questionnaire matches.
- No em or en dashes, no stock AI vocabulary (scripted scan of all 8 languages).

## Translations

All seven were rewritten from the new English as fresh copy, not adapted from the October 4 drafts:

- Spanish uses *usted*.
- Cantonese is written Cantonese (嘅/係/佢).
- Traditional and Simplified Chinese are standard written Chinese, using SFUSD's own terms (教育總監 for superintendent, 選務處 for the Department of Elections).
- Filipino uses everyday Filipino with the English terms Filipino-Americans actually use (school board, special education, lottery).
- Vietnamese uses formal ông/bà.
- Arabic is Modern Standard Arabic, with candidate names in Latin script.

Each route still shows the AI-translation notice and stays `ai_translated` (noindex) in `data/translation_status.yaml`. **No human native speaker has reviewed them.** That review is still required before they are indexed or presented as reviewed.

## Still open

1. Human native-speaker review of the seven translations.
2. Michael's approval of the rewritten first-person copy, especially the new "closest to Ryan's" sentence.
3. Recheck SF.gov's candidate list and all links on release day.
