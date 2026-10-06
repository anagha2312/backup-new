# -*- coding: utf-8 -*-
from common import *

def CARD(profile, engagement):
    left = [Paragraph('User profile', S['calloutb']), Spacer(1, 2)]
    left += [Paragraph('<bullet>&bull;</bullet>' + x, S['bullet']) for x in profile]
    right = [Paragraph('LearnPerk engagement', S['calloutb']), Spacer(1, 2)]
    right += [Paragraph('<bullet>&bull;</bullet>' + x, S['bullet']) for x in engagement]
    t = Table([[left, right]], colWidths=[CW*0.5, CW*0.5], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BAND),
        ('LINEBEFORE', (0, 0), (0, -1), 2.6, TEAL),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
    return [t, SP(9)]

def READINGS(rows, cap):
    return TBL(['Metric', 'Reading at the moment', 'Boundary', 'Verdict'], rows,
               [30*mm, 52*mm, 40*mm, CW - 122*mm], caption=cap, fs=7.7)

def SWITCHES(rows, cap):
    return TBL(['Task', 'Switch', 'Trigger', 'Why this model, on these metrics'], rows,
               [16*mm, 34*mm, 34*mm, CW - 84*mm], caption=cap, fs=7.7)

def TEST(items, label='How we test this case'):
    return CALLOUT(label, [Paragraph('<bullet>&bull;</bullet>' + i, S['bullet']) for i in items],
                   accent=NAVY, bg=colors.HexColor('#F0F3F6'))

F += [H1('7&nbsp;&nbsp;Five use cases')]
F += [P('Each case below is one traversal of the decision table in &sect;4.6. The structure is the '
        'same throughout: who the commuter is, what they do in LearnPerk, what happens at a '
        'specific moment, which metrics read what, which model each task moves to and why, what the '
        'efficiency argument is in numbers, and how we would test that the engine actually did it. '
        'The personas are constructed, but every profile attribute and every metric value is drawn '
        'from a real range in the dataset.')]
F += [P('The five are chosen to exercise different arms of the decision table deliberately. Two '
        'switch down, one switches up, one switches sideways, and one is mostly about a switch '
        'correctly <i>refused</i>. A set of five cases that all switch down would demonstrate a '
        'throttle, not an adaptation loop.')]

# ============== UC1 ==============
F += [H2('7.1&nbsp;&nbsp;UC-1 &nbsp;Lisa &mdash; the tunnel')]
F += [P('<b>The switching arm: <font face="Courier" size="8.5">CONNECTIVITY_LOSS</font>. '
        'Direction: down and sideways, immediately, with no dwell-time grace.</b>')]
F += CARD(
    ['<b>Lisa Bakker</b>, 34. <font face="Courier" size="7.6">age_cell</font> A4, Established '
     'professional, couple no kids.',
     'Home zone <b>West</b>, work zone <b>Zuid</b>. Habitual commuter, 640 days tenure.',
     'Device: <b>Mid-tier</b>. Consent opted-in, no accessibility flag.',
     'Declared interests at onboarding, in her own words: <i>&ldquo;I travel to Zuid most days for '
     'work, I like trying new coffee places and I&rsquo;m trying to eat healthier.&rdquo;</i>'],
    ['27 offers seen, 6 accepted &mdash; an accept rate of 22%, comfortably above the 15.5% dataset '
     'mean.',
     'Top content category: Local News &amp; Current Affairs. Has asked for GVB service updates '
     'specifically.',
     'Has said she wants <b>variety</b>: <i>&ldquo;still my thing, but I&rsquo;d like more variety, '
     'not always the same chain.&rdquo;</i>',
     'Tier Gold, <font face="Courier" size="7.6">tier_progress</font> 0.88 &mdash; close enough to '
     'the next reward that the goal-gradient term is strongly active.'])
F += [P('<b>The moment.</b> 08:18 on a Tuesday, metro M52 from Zuid towards Centraal. The leg is '
        'scheduled at 14 minutes and she boarded at the origin, so the window is long. Three minutes '
        'in, the train enters the tunnel under the IJ. Connectivity goes from '
        '<font face="Courier" size="8.5">Online</font> to '
        '<font face="Courier" size="8.5">Offline</font> between one tick and the next. This is not a '
        'rare event: it is 22.9% of metro-leg impressions in our own data.')]
F += READINGS([
    ['<b>N</b> connectivity', '<font face="Courier" size="7.6">Online &rarr; Offline</font> at '
     't&nbsp;=&nbsp;185&nbsp;s', 'Gate G3, instantaneous, unsmoothed', '<b>Gate fails</b> for every '
     'network-touching model'],
    ['<b>K</b> cache state', '<font face="Courier" size="7.6">fresh &rarr; stale</font> 40&nbsp;s '
     'later, once the catalogue refresh times out', 'B3 requires '
     '<font face="Courier" size="7.6">fresh</font>', '<b>Gate fails</b> for B3'],
    ['<b>&Phi;</b> coverage', 'B3 drops from 0.94 to 0.61 as live merchant and crowding fields go '
     'stale', 'B3 minimum 0.90; B2 minimum 0.70', 'B3 infeasible, B2 feasible at 0.78'],
    ['<b>W</b> remaining window', '~660&nbsp;s', '&mdash;', 'Ample. Latency is not the constraint '
     'here.'],
    ['<b>B</b> battery', '56%', 'Her personal threshold, learned from past disengagement: 31%',
     'No resource pressure. Mode stays <b>Balanced</b>, overlaid by <b>M5 Offline</b>.'],
    ['<b>U</b> CPU', '11% smoothed', 'Balanced ceiling 35%', 'Comfortable'],
], 'Table 7.1 &mdash; UC-1 readings. Note that only two metrics moved, and both are gates. No score '
   'comparison was needed to make the first three switches &mdash; the gate decided them.')
F += SWITCHES([
    ['<b>B</b> offers', 'B3 &rarr; <b>B2</b>', 'G3 then G4', 'B2 is the heaviest model in the '
     'spectrum that is both offline-capable and satisfied at 0.78 coverage. This is a sideways move '
     'for an epistemic reason and a downward move for a resource reason at the same time, and B2 is '
     'the answer to both. The goal-gradient feature that matters most for Lisa &mdash; '
     '<font face="Courier" size="7.5">tier_progress</font> at 0.88 &mdash; is local and survives the '
     'outage, so the ranking stays personal.'],
    ['<b>C</b> content', 'C2 &rarr; <b>C1</b>', 'G3', 'C2 needs the live catalogue. C1 runs a cosine '
     'over the taste vector against the <i>cached</i> pool and adjusts for remaining window. This is '
     'the switch that closes the hole in Table&nbsp;1.1 row&nbsp;2: today Lisa would see <b>nothing</b> '
     'for eleven minutes, because zero content views in the dataset occur offline.'],
    ['<b>E</b> language', 'E4 &rarr; <b>E0&nbsp;+&nbsp;E1</b>', 'G3', 'Cloud assist is gone. The GVB '
     'bulletin she cares about is formulaic Dutch &mdash; <i>signaalstoring, vertraging van circa 10 '
     'minuten, lijn 24</i> &mdash; and E0&rsquo;s phrase table extracts line, cause and delay from it '
     'without any neural model. E1 stays resident on mid-tier and handles intent routing at '
     '~34&nbsp;ms.'],
    ['<b>A</b> journey state', 'A1 &rarr; <b>A1</b> (hold)', '&mdash;', 'A1 needs nothing the outage '
     'removed. Holding is the correct decision and the score produces it without a special case.'],
    ['<b>D</b> incentive', 'D1 &rarr; <b>D1</b> (hold)', '&mdash;', 'The LinUCB posterior is local. '
     'Nothing about being offline makes it worse.'],
], 'Table 7.2 &mdash; UC-1 switches. Three of five tasks move; two correctly hold.')
F += CALLOUT('Why this is efficient',
    'The efficiency argument here is not primarily about energy &mdash; it is about <b>availability</b>, '
    'which is the goal the decision map calls <i>never go dark</i>. Without switching, Lisa gets a '
    'blank content feed and a dead assistant for eleven minutes of a fourteen-minute leg, and we '
    'record nothing, so the failure is invisible. With switching she gets a cached, taste-ranked feed '
    'and a structured answer about her delay. The secondary gain is real but smaller: B2 at '
    '~180&nbsp;KB and 4&nbsp;ms replaces B3 at ~1.4&nbsp;MB and 14&nbsp;ms, roughly a <b>3.5&times; '
    'cut in per-call inference cost</b>, and dropping the cloud round trip removes a '
    '400&ndash;900&nbsp;ms wait that would in any case have failed. Switching costs are negligible: '
    'B2 and C1 are already resident, so &kappa; is near zero and the gate bypasses dwell time '
    'legitimately.',
    accent=TEAL)
F += TEST([
    '<b>Trigger test.</b> Replay a metro leg from '
    '<font face="Courier" size="7.6">event_stream.csv</font> with connectivity forced to Offline at '
    't&nbsp;=&nbsp;185&nbsp;s. Assert that gate&nbsp;G3 fires on the <i>same tick</i>, not the next, '
    'and that dwell time is bypassed.',
    '<b>Selection test.</b> Assert the chosen model is B2, not B1. A down-switch that overshoots to '
    'the cheapest available model is the most likely implementation bug, and it costs accuracy for '
    'no reason, since there was no resource pressure at all.',
    '<b>Availability test.</b> Assert content items are returned for every tick of the outage. The '
    'pass condition is a non-empty feed, measured against a baseline of zero.',
    '<b>Recovery test.</b> On exiting the tunnel, assert that the engine does <i>not</i> immediately '
    'restore B3: the cache is still stale, and the dwell timer on B2 has not expired. Restoring '
    'early is the second most likely bug.',
])
F += [PageBreak()]

# ============== UC2 ==============
F += [H2('7.2&nbsp;&nbsp;UC-2 &nbsp;John &mdash; the failing battery')]
F += [P('<b>The switching arm: <font face="Courier" size="8.5">RESOURCE_PRESSURE</font>. '
        'Direction: down, progressively, one tier per tick.</b>')]
F += CARD(
    ['<b>John de Vries</b>, 51. <font face="Courier" size="7.6">age_cell</font> A7, Established '
     'professional, solo household.',
     'Home zone <b>Noord</b>, work zone <b>Centrum</b>. Habitual commuter, metro every day, 410 days '
     'tenure.',
     'Device: <b>Low-tier</b> &mdash; the 30% of the fleet whose cache is evicted more often.',
     '<font face="Courier" size="7.6">accessibility_flag = hearing_impairment</font>. In his own '
     'words: <i>&ldquo;please make sure alerts are visual, not just audio.&rdquo;</i>'],
    ['Low-volume, high-signal: 21 offers seen, 3 accepted. Explicitly asked for <b>minimal offers</b>.',
     'Stated preferences: <i>&ldquo;quick useful info, not too many offers&rdquo;</i>; '
     '<i>&ldquo;don&rsquo;t send me food offers before 9am&rdquo;</i>.',
     'Declined a 5% discount and said why: <i>&ldquo;I&rsquo;d redeem this if the discount was '
     'bigger &mdash; 5% isn&rsquo;t enough to change my mind.&rdquo;</i> That is a labelled '
     'counterfactual for Task&nbsp;D.',
     'Estimated <font face="Courier" size="7.6">battery_anxiety</font> 0.61, putting his personal '
     'disengagement threshold at <b>24%</b> within the documented 20&ndash;40% band.'])
F += [P('<b>The moment.</b> 18:40, the evening leg home on M52. He has been navigating on a low-tier '
        'phone all afternoon. Charge is 18% and falling at 4.6% per hour, the thermal status has '
        'reached <font face="Courier" size="8.5">LIGHT</font>, and the leg has 14 minutes to run. '
        'This combination &mdash; low-tier and under 30% charge &mdash; is 5.8% of impressions in '
        'our data, which is roughly one commuting session in seventeen.')]
F += READINGS([
    ['<b>B</b> battery', '18%', 'His personal threshold: 24%. Global Survival floor: 12%',
     '<b>Below personal threshold.</b> Mode Balanced &rarr; <b>Frugal</b>, &alpha; 0.55 &rarr; 0.35'],
    ['<b>&Delta;B</b> drain rate', '4.6%/hr, near the top of the measured 1.06&ndash;5.02 band',
     'Dynamic boundary &theta;, currently tightened to 3.9%/hr after two sustained overspend windows',
     '<b>Boundary exceeded.</b> &theta; tightens again on the next update'],
    ['<b>T</b> thermal', '1 (<font face="Courier" size="7.6">LIGHT</font>)',
     'Tier&nbsp;3+ blocked at 2', 'Not yet gating, but one step away'],
    ['<b>D</b> device class', 'Low-tier', 'Memory ceiling 160&nbsp;MB; no language tier above E1',
     'E2 and E3 were never feasible on this device'],
    ['<b>U</b> CPU', '29% smoothed, against a 22% baseline for this device',
     'Frugal ceiling 25%', '<b>Exceeded</b>'],
    ['<b>W</b> remaining window', '~840&nbsp;s', '&mdash;', 'Long. Latency is not the constraint; '
     'energy is.'],
], 'Table 7.3 &mdash; UC-2 readings. Three separate resource signals agree, which is what '
   'distinguishes a genuine regime change from the noise that EMA smoothing exists to absorb.')
F += SWITCHES([
    ['<b>B</b> offers', 'B2 &rarr; <b>B1</b>', 'Frugal mode; U above ceiling',
     'At &alpha;&nbsp;=&nbsp;0.35 the cost term dominates. B1 is ~25&nbsp;KB against B2&rsquo;s '
     '~180&nbsp;KB and under 2&nbsp;ms against 7&nbsp;ms on this device class. The expected '
     'acceptance loss is small for John specifically, because his own free text says depth of '
     'discount &mdash; a feature B1 carries directly &mdash; is what moves him, not the subtle '
     'interactions B2 adds.'],
    ['<b>C</b> content', 'C2 &rarr; <b>C1</b>', 'Frugal mode', 'C1 is a dot product over a vector '
     'he has been building for 410 days, so the ranking stays genuinely personal at almost no cost. '
     'Content prefetch is suspended, which is where most of the saving actually comes from.'],
    ['<b>E</b> language', 'E1 &rarr; <b>E0</b>, slot unloaded', 'Frugal; memory ceiling',
     'E1&rsquo;s ~23&nbsp;MB is unloaded, freeing the largest single block on a 160&nbsp;MB ceiling. '
     'E0 still parses the GVB bulletin John actually wants, and &mdash; because of his '
     'accessibility flag &mdash; renders it <b>visually</b>. The flag changes rendering, never '
     'which model runs.'],
    ['<b>D</b> incentive', 'D1 &rarr; <b>D1</b> (hold)', '&mdash;',
     '<b>The instructive non-switch.</b> D1 is ~50&nbsp;KB and about 2&nbsp;ms. Dropping it to D0 '
     'would save an amount of energy indistinguishable from measurement noise and would cost the one '
     'thing John has told us matters &mdash; getting the discount depth right. The score sees this '
     'because D1&rsquo;s cost term is near zero, so even at &alpha;&nbsp;=&nbsp;0.35 its utility '
     'still wins. A rule-based throttle would have dropped it.'],
    ['<b>A</b> journey state', 'A1 &rarr; <b>A0</b>', 'U above ceiling',
     'On a familiar daily route the threshold table is very nearly as good as A1, and it costs '
     'nothing. This is the one place where EdgeMLBalancer&rsquo;s naive baseline is genuinely the '
     'right answer, and the score says so.'],
], 'Table 7.4 &mdash; UC-2 switches. Four tasks move down; D holds. The held task is the point of '
   'the case.')
F += CALLOUT('Why this is efficient',
    'Summed across the five tasks, resident model memory falls from roughly 24&nbsp;MB to under '
    '300&nbsp;KB, which on a 160&nbsp;MB ceiling removes essentially all of the model-attributable '
    'pressure. Per-surface inference cost falls from about 16&nbsp;ms to about 3&nbsp;ms on this '
    'device class. EdgeMLBalancer measured 2.10&nbsp;mAh for its adaptive policy against '
    '5.25&nbsp;mAh for a naive threshold policy over an identical 30-minute workload &mdash; a '
    '<b>60% reduction</b> &mdash; and our structure is the same, so a comparable order of saving is '
    'the hypothesis &sect;9 is designed to test. The argument that matters for John, though, is '
    'behavioural rather than electrical: his personal disengagement threshold is 24%, and he is at '
    '18%. Every mJ LearnPerk does not spend is charge that keeps him in the session at all.',
    accent=TEAL)
F += TEST([
    '<b>Personal-threshold test.</b> Two commuters at identical 22% charge, with anxiety-derived '
    'thresholds of 21% and 34%. Assert that only the second enters Frugal. A global constant would '
    'fail this, and it is the failure the dictionary explicitly warns about.',
    '<b>Non-switch test.</b> Assert D1 is still bound after ten ticks in Frugal mode. This is the '
    'regression test that catches a blanket throttle disguised as a switching engine.',
    '<b>Hysteresis test.</b> Oscillate charge across the threshold, 23%&ndash;25%, for two minutes. '
    'Assert at most one mode change, and that the dwell timer and the margin &delta; are both '
    'respected.',
    '<b>Accessibility invariance test.</b> Assert the rendering path for '
    '<font face="Courier" size="7.6">hearing_impairment</font> is identical across every tier from '
    'E0 to E4. Accessibility must never be a casualty of a down-switch.',
    '<b>Energy test.</b> On-device, two matched 30-minute runs, fixed workload, 30-minute cooldown '
    'between them, following the EdgeMLBalancer protocol. Compare mAh.',
])
F += [PageBreak()]

# ============== UC3 ==============
F += [H2('7.3&nbsp;&nbsp;UC-3 &nbsp;Sanne &mdash; the delayed, crowded train')]
F += [P('<b>The switching arm: <font face="Courier" size="8.5">OPPORTUNITY</font>. '
        'Direction: up. This is the case most resource-management designs forget.</b>')]
F += CARD(
    ['<b>Sanne Visser</b>, 27. <font face="Courier" size="7.6">age_cell</font> A3, Early-career '
     'professional, shared housing.',
     'Home zone <b>Oost</b>, work zone <b>Zuid</b>. Habitual commuter, 395 days tenure.',
     'Device: <b>High-tier</b>. Opted-in, no accessibility flag.',
     'Estimated novelty-seeking 0.71 and detour tolerance ~9 minutes &mdash; both well above median, '
     'so she is unusually open to an unfamiliar merchant slightly off her route.'],
    ['24 offers seen, 5 accepted. Mean discount seen 14%, mean detour seen 5.2 minutes.',
     'Content: high video share, strong appetite (multiplier 1.9), median dwell 41&nbsp;s.',
     'Tier Silver, <font face="Courier" size="7.6">tier_progress</font> 0.41.',
     'Asks the assistant questions when disrupted &mdash; her history shows three questions in the '
     'last month, all on delayed legs.'])
F += [P('<b>The moment.</b> 17:52, peak, Tram 12 towards Centraal. The GVB feed reports a signal '
        'problem: <font face="Courier" size="8.5">delay_minutes</font> is 11 and '
        '<font face="Courier" size="8.5">crowding_level</font> is '
        '<font face="Courier" size="8.5">High</font>. She is standing, screen active, phone at 74%. '
        'The delay has stretched the remaining window from 13 minutes to about 22. She is, for the '
        'next twenty minutes, a captive and attentive audience on a fast phone with plenty of charge.')]
F += READINGS([
    ['<b>&Delta;t</b> delay', '11 minutes', 'M6 requires &gt; 5 minutes. Only 12.6% of peak '
     'impressions clear this', '<b>Condition met</b>'],
    ['<b>W</b> remaining window', '~1,320&nbsp;s, against a median leg of 714&nbsp;s',
     'M6 requires &gt; 600&nbsp;s', '<b>Condition met</b>, and generously'],
    ['<b>B</b> battery', '74%', 'M6 requires &gt; 50%', '<b>Condition met</b>'],
    ['<b>&sigma;</b> screen / foreground', 'Active, foreground', 'M6 requires Active',
     '<b>Condition met.</b> The app is backgrounded on 51.6% of impressions, so this is the minority '
     'state that makes spending worthwhile'],
    ['<b>X</b> crowding', 'High', 'Not a gate; a utility signal',
     'In our data, acceptance under High crowding is <b>16.5%</b> against <b>14.8%</b> under Low '
     '&mdash; 1.7&nbsp;pp higher, small but real'],
    ['<b>T</b> / <b>U</b>', 'Thermal 0, CPU 14%', 'Full ceiling 45%', 'No pressure. Tier&nbsp;4 is '
     'available'],
    ['<b>&kappa;</b> switch charge', 'Loading B3 costs ~110&nbsp;mJ; amortised over 1,320&nbsp;s it '
     'is ~0.08&nbsp;mJ/s', 'Compared against the utility gain from &alpha;&nbsp;=&nbsp;0.85',
     '<b>Negligible.</b> The long window is precisely what makes the upgrade affordable'],
], 'Table 7.5 &mdash; UC-3 readings. Every M6 condition holds simultaneously, which is rare and is '
   'meant to be: M6 is capped at five minutes and then reverts.')
F += SWITCHES([
    ['<b>A</b> journey state', 'A1 &rarr; <b>A2</b>', 'M6', 'With 28 features including her own '
     'history on line 12, A2 can distinguish <i>this delay will clear</i> from <i>this delay will '
     'grow</i>, which determines how much window the other tasks can rely on.'],
    ['<b>B</b> offers', 'B2 &rarr; <b>B3</b>', 'M6', 'B3&rsquo;s depth-8 trees carry the explicit '
     'detour, goal-gradient and repeat-merchant interactions. Sanne has ~9 minutes of detour '
     'tolerance and high novelty-seeking, and the dictionary is explicit that detour enters as a '
     '<b>threshold rather than a slope</b> &mdash; the hardest trait to recover, and the shape that '
     'most needs depth. This is precisely the commuter and the moment where B3&rsquo;s extra '
     'capacity converts into an acceptance that B2 would miss.'],
    ['<b>B</b> (considered)', 'B3 &rarr; B4 <b>rejected</b>', 'Score, not gate',
     'B4 is feasible: high-tier, delegate present, tenure 395 days. It loses on score. Its '
     '~3.2&nbsp;MB load and 28&nbsp;ms p95 buy generalisation to unseen merchants, but Sanne has 24 '
     'prior impressions in familiar categories, so the embedding has little to add. The margin '
     '&delta; is not cleared. <b>Feasible is not the same as selected.</b>'],
    ['<b>D</b> incentive', 'D1 &rarr; <b>D2</b>', 'M6', 'At '
     '<font face="Courier" size="7.5">tier_progress</font> 0.41 she is mid-ladder, where the '
     'sequential question is live: a shallower discount now may be worth more if it preserves the '
     'pull toward the 500-point reward. A bandit optimises this impression; D2 optimises the '
     'sequence.'],
    ['<b>E</b> language', 'E1 &rarr; <b>E2 preloaded</b>', 'M6 + A2 prediction',
     'A2 predicts a high probability of a question on a delayed leg, and her history agrees. E2 is '
     'loaded into the single language slot <b>now</b>, while she is not waiting, so the answer to '
     '<i>&ldquo;will I make my connection at Zuid?&rdquo;</i> is warm when it is asked. This is the '
     'preload rule of &sect;5.7 doing its job.'],
], 'Table 7.6 &mdash; UC-3 switches. Four tasks move up; one candidate is feasible but correctly '
   'rejected on score.')
F += CALLOUT('Why this is efficient',
    'Efficiency is a ratio, not a floor, and this case is the numerator. The inference spend rises '
    'roughly <b>4&times;</b> for the next five minutes &mdash; and this is the moment when a '
    'marginal accepted offer is worth most. The three conditions that make it affordable are all '
    'measured rather than assumed: the window is 85% longer than a median leg, so &kappa; amortises '
    'to almost nothing; the battery is 74%, so the energy has no behavioural cost; and the screen is '
    'active, which is the minority state. A design that only ever switches down would spend exactly '
    'the same at 17:52 as at 03:00, and would be leaving the entire upside on the table. M6 is '
    'capped at five minutes and reverts automatically, so the exposure is bounded by construction.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))
F += TEST([
    '<b>Composite-trigger test.</b> Assert M6 fires only when <i>all four</i> conditions hold. '
    'Negative cases: delay 11 min but battery 40%; delay 11 min but screen locked; delay 3 min with '
    'everything else true. None may fire.',
    '<b>Cap test.</b> Assert M6 reverts after 300&nbsp;s even if every condition still holds, and '
    'that it cannot immediately re-enter.',
    '<b>Rejection test.</b> Assert B4 is <i>scored</i> and <i>rejected</i>, not gated out. The log '
    'must show it in the feasible set with a score below B3&rsquo;s. Confusing the two makes the '
    'system untunable, because a gate cannot be re-weighted.',
    '<b>Value test.</b> Off-policy, using the <font face="Courier" size="7.6">propensity</font> '
    'column: estimate the acceptance lift of B3 over B2 restricted to impressions where the M6 '
    'condition holds. If the lift is not positive, M6 is not worth its cost and the mode should be '
    'retired.',
    '<b>Preload test.</b> Assert E2 is resident <i>before</i> the first question, and measure the '
    'saved cold-start latency &mdash; the whole justification for preloading.',
])
F += [PageBreak()]

# ============== UC4 ==============
F += [H2('7.4&nbsp;&nbsp;UC-4 &nbsp;Daan &mdash; the commuter we know nothing about')]
F += [P('<b>The switching arm: <font face="Courier" size="8.5">COVERAGE_LOSS</font>. '
        'Direction: sideways. Resources are plentiful; the constraint is evidence.</b>')]
F += CARD(
    ['<b>Daan Mulder</b>, 19. <font face="Courier" size="7.6">age_cell</font> A2, Student, shared '
     'housing.',
     'Home zone <b>Centrum</b>, university in <b>Nieuw-West</b>. Occasional/personal archetype.',
     'Device: <b>Mid-tier</b>. Battery 63%, thermal 0 &mdash; <b>no resource pressure whatsoever</b>.',
     'Tenure <b>9 days</b>. The dataset&rsquo;s 10th percentile is 26 days, so he is newer than 90% '
     'of impressions.'],
    ['<font face="Courier" size="7.6">offers_seen_before</font> = 1. '
     '<font face="Courier" size="7.6">accept_rate_before</font> = <b>null</b> &mdash; undefined, not '
     'zero, and null on 17% of all impressions.',
     '<font face="Courier" size="7.6">local_cache_state</font> = <b>empty</b>. No behavioural '
     'history has accumulated locally yet.',
     '4 content views, no reactions. Reaction rate across the whole dataset is only 3.6%, so this '
     'tells us almost nothing either way.',
     'One free-text statement at onboarding: <i>&ldquo;I&rsquo;m a student, budget offers are more '
     'useful to me than premium ones.&rdquo;</i> Right now this is the single most informative thing '
     'we hold about him.'])
F += [P('<b>The moment.</b> 14:20 on a Thursday, bus 21 towards Nieuw-West, a 16-minute leg, online '
        'throughout. Nothing is under pressure. The phone is fine, the network is fine, the window is '
        'long. The heavy models are all <i>feasible</i> &mdash; and all of them would be wrong, '
        'because there is nothing for them to condition on.')]
F += READINGS([
    ['<b>H</b> history depth', '<font face="Courier" size="7.6">offers_seen_before</font> = 1, '
     'tenure 9 days', 'B3 requires meaningful history; B4 requires 30 days and 20 impressions',
     '<b>B4 gated out.</b> B3 technically loads but conditions on near-empty features'],
    ['<b>K</b> cache state', '<font face="Courier" size="7.6">empty</font>',
     'B3 requires <font face="Courier" size="7.6">fresh</font>', '<b>Gate G4 fails</b> for B3'],
    ['<b>&Phi;</b> coverage', 'B3 at 0.44; B2 at 0.58; B1 at 0.71; B0 at 1.00',
     'Minimums: B3 0.90, B2 0.70, B1 0.60, B0 1.00', '<b>Only B1 and B0 are feasible</b>'],
    ['<b>B</b>, <b>U</b>, <b>T</b>, <b>N</b>', '63%, 12%, 0, Online', 'All comfortable',
     '<b>No resource pressure at all.</b> Mode stays Balanced'],
    ['<b>W</b> remaining window', '~900&nbsp;s', '&mdash;', 'Long'],
    ['<b>D1</b> posterior depth', '1 resolved impression', 'D1 requires ~20',
     '<b>D1 not yet usable.</b> Its uncertainty estimate would be all uncertainty'],
], 'Table 7.7 &mdash; UC-4 readings. Every resource metric is healthy. The constraint is entirely '
   'epistemic, which is why the coverage metric &Phi; has to exist separately from the cost terms.')
F += SWITCHES([
    ['<b>B</b> offers', 'B2 &rarr; <b>B0</b>, then B1 at ~impression 8', 'G4 coverage',
     'B0 is a segment-prior table: acceptance by age cell, merchant category, peak flag and discount '
     'band. For a 19-year-old student at 14:20 it returns the population&rsquo;s honest estimate '
     'rather than a personalised guess built from one data point. As impressions accumulate, '
     'coverage crosses B1&rsquo;s 0.60 minimum and the engine promotes him &mdash; a switch driven '
     'by <i>evidence arriving</i>, which is the reverse of every other case in this section.'],
    ['<b>C</b> content', 'C2 &rarr; <b>C0</b>, then C1 at ~view 12', 'G4 coverage',
     'C0 orders the cached pool by his declared onboarding interests, because declared interest is '
     'genuinely all we have. C1 takes over once the taste vector has enough mass to beat the '
     'declared prior &mdash; which is exactly the refinement loop the v3 document describes, where '
     'the system later asks <i>&ldquo;still your thing, or should we show you less of it?&rdquo;</i>'],
    ['<b>D</b> incentive', 'D1 &rarr; <b>D0</b>', 'Insufficient posterior',
     'With one resolved outcome, LinUCB would be exploring at full width and spending real margin to '
     'learn almost nothing. The merchant default ladder is the correct, honest floor, and it doubles '
     'as the control arm for measuring D1&rsquo;s value later.'],
    ['<b>E</b> language', 'E0 &rarr; <b>E1</b> <i>(a switch up)</i>', 'Sparse structured signal',
     '<b>The counter-intuitive move.</b> When structured history is empty, the free text is the '
     'richest thing we hold. E1 embeds <i>&ldquo;budget offers are more useful than premium '
     'ones&rdquo;</i> and seeds an initial taste and price-sensitivity prior. Spending 23&nbsp;MB '
     'and 34&nbsp;ms once, on the one signal that exists, is a far better use of the budget than '
     'running a heavy ranker over nothing.'],
], 'Table 7.8 &mdash; UC-4 switches. Three tasks move down in tier and one moves up, all from the '
   'same trigger. This is why coverage cannot be collapsed into cost.')
F += CALLOUT('Why this is efficient',
    'Two arguments, and the second is the important one. The narrow argument: B0 at ~60&nbsp;KB and '
    'under a millisecond replaces B2 at ~180&nbsp;KB and 4&nbsp;ms, for an expected accuracy '
    '<i>gain</i> rather than a loss, because B2 conditioned on empty features is worse than a '
    'well-estimated population prior. Spending less and getting more is the rare case, and cold '
    'start is where it occurs. The broader argument: the failure this avoids is not slowness, it is '
    'a <b>confident wrong answer</b>. A gradient-boosted model fed nulls for its top splits does not '
    'return a hedged answer; it returns an arbitrary one with a high confidence score attached, and '
    'that score then poisons the switching engine&rsquo;s own quality metric. For a nine-day-old '
    'account, an irrelevant offer shown confidently is the most expensive thing LearnPerk can do, '
    'because the cost is churn rather than milliamps.',
    accent=TEAL)
F += TEST([
    '<b>Null-handling test.</b> Assert that a null '
    '<font face="Courier" size="7.6">accept_rate_before</font> is never imputed as zero anywhere in '
    'the feature pipeline. Test the three distinct meanings the dictionary names &mdash; consent '
    'refused, event never happened, merchant did not disclose &mdash; and assert they route '
    'differently.',
    '<b>Direction test.</b> Assert the engine moves B down and E <i>up</i> from the same trigger on '
    'the same tick. A coverage handler that only moves down has conflated coverage with cost.',
    '<b>Promotion test.</b> Feed impressions one at a time and assert the promotion to B1 happens '
    'when &Phi; crosses 0.60, not on a fixed impression count and not on tenure.',
    '<b>Calibration test.</b> Compare B0&rsquo;s predicted acceptance against realised acceptance '
    'for all impressions with tenure under 14 days. A prior that is not calibrated is not a prior.',
    '<b>Counterfactual test.</b> Off-policy, estimate what B2 <i>would</i> have achieved on this '
    'cohort. If it beats B0, the coverage minimum is set too conservatively and should move.',
])
F += [PageBreak()]

# ============== UC5 ==============
F += [H2('7.5&nbsp;&nbsp;UC-5 &nbsp;Priya &mdash; four minutes to the interchange')]
F += [P('<b>The switching arm: <font face="Courier" size="8.5">WINDOW_CLOSING</font>. '
        'Direction: mostly refusal. The most important decision here is a switch not taken.</b>')]
F += CARD(
    ['<b>Priya Raman</b>, 41. <font face="Courier" size="7.6">age_cell</font> A5, Established '
     'professional, family with children.',
     'Home zone <b>IJburg</b>, work zone <b>Zuidas</b> &mdash; a thinly served origin, so her trips '
     'run to 3 legs with a last-mile hop.',
     'Device: <b>High-tier</b>. Battery 41%, thermal 0.',
     'Free text: <i>&ldquo;I travel with my child sometimes, so family-friendly offers matter&rdquo;</i>; '
     '<i>&ldquo;can you only show me offers that don&rsquo;t require detours from my route?&rdquo;</i>'],
    ['31 offers seen, 7 accepted. Mean detour seen 3.1 minutes &mdash; well below the 6.2-minute '
     'dataset mean, because she filters hard on detour.',
     'Estimated detour tolerance ~2.4 minutes, in the bottom quartile. Detour is the dominant '
     'negative term in her acceptance.',
     'Content: low appetite (0.6), bounce rate 21% &mdash; she screens out almost everything.',
     'Tier Platinum, <font face="Courier" size="7.6">points_balance</font> 1,240.'])
F += [P('<b>The moment.</b> 08:41. She is on the second leg of a three-leg trip, approaching the '
        'interchange at Zuid with about four minutes of in-vehicle time left, then a 90-second '
        'platform transfer. The journey-state classifier has moved to '
        '<font face="Courier" size="8.5">interchange-imminent</font>. She stands and starts walking '
        'towards the door, so <font face="Courier" size="8.5">motion_state</font> becomes '
        '<font face="Courier" size="8.5">Walking</font> and '
        '<font face="Courier" size="8.5">ambient_location_precision</font> degrades to '
        '<font face="Courier" size="8.5">Inferred</font>. The interchange is the highest-value '
        'moment the v3 document identifies for time-sensitive offers, and it is also the shortest.')]
F += READINGS([
    ['<b>W</b> remaining window', '240&nbsp;s in-vehicle, ~90&nbsp;s transfer',
     'Latency budget tightens from 120&nbsp;ms to 60&nbsp;ms below 120&nbsp;s',
     '<b>WINDOW_CLOSING raised.</b> All &kappa; charges roughly quintuple against a median leg'],
    ['<b>S</b> journey stage', '<font face="Courier" size="7.6">interchange-imminent</font>',
     'Selects the tight budget and the short-expiry offer filter', 'High value, low time'],
    ['<b>&rho;</b> location precision', '<font face="Courier" size="7.6">Inferred</font> (32.4% of '
     'impressions)', 'Not a gate; a discount on geographic models',
     '<b>Discounts B3</b>, whose leading features are detour and merchant zone'],
    ['<b>&kappa;</b> for a B2&nbsp;&rarr;&nbsp;B3 upgrade', '~110&nbsp;mJ load, amortised over 240&nbsp;s '
     '= ~0.46&nbsp;mJ/s', 'Against B3&rsquo;s utility gain, itself discounted by Inferred location',
     '<b>Upgrade rejected.</b> Same models, same scores, opposite decision to UC-3 &mdash; and the '
     'only thing that changed is W'],
    ['<b>B</b> battery / <b>N</b>', '41%, Online', 'No pressure', 'Resources are not the issue here'],
    ['Content appetite', 'Median content length 145 word-units; her bounce rate 21%',
     'Below 60&nbsp;s remaining, content is suppressed entirely',
     '<b>Task C suspended</b> rather than downgraded'],
], 'Table 7.9 &mdash; UC-5 readings. Compare row 4 directly against Table 7.5 row 7: identical '
   'models, identical switch cost, opposite outcome, because the window is 5.5&times; shorter.')
F += SWITCHES([
    ['<b>B</b> offers', 'B2 &rarr; <b>B2</b> (hold); B3 upgrade <b>refused</b>',
     'WINDOW_CLOSING + &rho;', '<b>The decision the case exists for.</b> B3 is feasible on latency '
     '&mdash; 9&nbsp;ms p95 on high-tier, well inside a 60&nbsp;ms budget &mdash; so a naive '
     'latency rule would have allowed it. The score refuses it on two grounds the rule cannot see: '
     '&kappa; amortised over 240&nbsp;s is five times its UC-3 value, and Inferred location '
     'discounts exactly the geographic features B3 exists to exploit. The incumbent is scored at '
     '&kappa;&nbsp;=&nbsp;0, so holding wins cleanly.'],
    ['<b>B</b> candidate filter', 'Unchanged model, <b>restricted candidates</b>',
     'Stage = interchange', 'Not a model switch but a constraint the stage imposes: only offers with '
     '<font face="Courier" size="7.5">detour_minutes</font> under 2 and an expiry window long enough '
     'to survive the transfer are eligible. Her own free text asked for precisely this, and her '
     '2.4-minute tolerance confirms it.'],
    ['<b>C</b> content', 'C1 &rarr; <b>suspended</b>', 'W below threshold',
     'A 145-word item cannot be read in the time available, and she screens out 21% of items in under '
     'two seconds at the best of times. Showing content here would spend energy to produce a '
     'guaranteed bounce. Suspension is a switching decision, and the floor model is <i>nothing</i>.'],
    ['<b>E</b> language', 'Slot <b>not loaded</b>; E0 only', '&kappa; over a small W',
     'Loading E2 would cost ~340&nbsp;ms and a large block of memory to serve a question that has '
     'about 240&nbsp;s to arrive. E0 still answers the one question this stage actually produces '
     '&mdash; <i>&ldquo;will I make my connection?&rdquo;</i> &mdash; from structured timetable and '
     'delay facts, with no generation at all.'],
    ['<b>D</b> incentive', 'D1 &rarr; <b>D1</b>, arms restricted', 'Stage',
     'The posterior is re-scored over short-expiry arms only. A 24-hour offer is worthless to '
     'someone who will act in the next four minutes or not at all.'],
], 'Table 7.10 &mdash; UC-5 switches. Only one task changes model. The engine&rsquo;s work here is '
   'refusing an upgrade, restricting candidates and suspending a surface.')
F += CALLOUT('Why this is efficient',
    'This case is the clearest demonstration that &kappa; belongs in the score rather than in a '
    'rule. UC-3 and UC-5 present the identical B2&nbsp;&rarr;&nbsp;B3 decision with identical model '
    'costs, and the engine reaches opposite conclusions purely because W is 1,320&nbsp;s in one and '
    '240&nbsp;s in the other. No threshold was tuned to produce that; it falls out of dividing the '
    'switch cost by the remaining window. The measurable saving is modest &mdash; one avoided model '
    'load, one avoided 200&nbsp;MB language load, and a suspended content surface, together perhaps '
    '450&nbsp;mJ &mdash; but the avoided <i>waste</i> is total: every one of those spends would have '
    'produced output arriving after Priya had already left the vehicle. The definition of efficiency '
    'that matters at an interchange is not energy per inference, it is the share of inference that '
    'reaches a commuter still present to receive it.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))
F += TEST([
    '<b>Symmetry test.</b> Run UC-3 and UC-5 with every input identical except W. Assert opposite '
    'decisions on the B2&nbsp;&rarr;&nbsp;B3 upgrade. This single test validates the entire '
    '&kappa;-amortisation mechanism, and it is the one to write first.',
    '<b>Refusal-is-logged test.</b> Assert the refused B3 upgrade appears in '
    '<font face="Courier" size="7.6">edge_switch_events</font> with '
    '<font face="Courier" size="7.6">decision_type = hold</font> and both scores recorded. An '
    'unlogged non-decision is indistinguishable from a bug.',
    '<b>Suspension test.</b> Assert Task C returns an empty result below the window threshold and '
    'that this is recorded as a decision, not as a serve failure. The two must not be conflated, '
    'because one of them triggers a blacklist.',
    '<b>Precision-discount test.</b> Two identical impressions differing only in '
    '<font face="Courier" size="7.6">ambient_location_precision</font>. Assert the geographic model '
    'scores lower under <font face="Courier" size="7.6">Inferred</font>.',
    '<b>Outcome test.</b> Off-policy, restricted to interchange-stage impressions: does restricting '
    'to sub-2-minute detours raise acceptance? Her stated preference and her 2.4-minute estimated '
    'tolerance both predict yes, and the data can settle it.',
])
F += [PageBreak()]

# ============== 7.6 ==============
F += [H2('7.6&nbsp;&nbsp;Cross-case summary')]
F += [P('Read together, the five cases show the engine moving in four different directions from one '
        'mechanism. The table below is the compressed argument of this whole document.')]
F += TBL(['', 'UC-1 Lisa', 'UC-2 John', 'UC-3 Sanne', 'UC-4 Daan', 'UC-5 Priya'], [
    ['<b>Trigger</b>', 'CONNECTIVITY<br/>_LOSS', 'RESOURCE<br/>_PRESSURE', 'OPPORTUNITY',
     'COVERAGE_LOSS', 'WINDOW<br/>_CLOSING'],
    ['<b>Direction</b>', 'Down + sideways', 'Down, stepwise', '<b>Up</b>', 'Sideways (both ways)',
     'Refusal + suspend'],
    ['<b>Binding metric</b>', 'N, then K and &Phi;', 'B vs personal threshold; &Delta;B; U',
     '&Delta;t, W, B, screen &mdash; all four', '&Phi; and H', 'W, via &kappa;'],
    ['<b>Mode</b>', 'Balanced + M5', 'Frugal', '<b>Opportunity</b>', 'Balanced', 'Balanced'],
    ['<b>Task A</b>', 'A1 hold', 'A1 &rarr; A0', 'A1 &rarr; <b>A2</b>', 'A1 hold', 'A1 hold'],
    ['<b>Task B</b>', 'B3 &rarr; B2', 'B2 &rarr; B1', 'B2 &rarr; <b>B3</b>; B4 rejected',
     'B2 &rarr; B0 &rarr; B1', 'B2 hold; B3 <b>refused</b>'],
    ['<b>Task C</b>', 'C2 &rarr; C1', 'C2 &rarr; C1', 'C2 hold', 'C2 &rarr; C0 &rarr; C1',
     '<b>suspended</b>'],
    ['<b>Task D</b>', 'D1 hold', 'D1 <b>hold</b>', 'D1 &rarr; <b>D2</b>', 'D1 &rarr; D0',
     'D1, arms restricted'],
    ['<b>Task E</b>', 'E4 &rarr; E0+E1', 'E1 &rarr; E0, unloaded', 'E1 &rarr; <b>E2 preloaded</b>',
     'E0 &rarr; <b>E1</b>', 'not loaded'],
    ['<b>Primary gain</b>', 'Availability: 11 minutes that are currently blank',
     'Charge retained below a 24% disengagement threshold',
     'Acceptance at the highest-value moment', 'Avoids a confident wrong answer to a new user',
     'Avoids spend that would arrive after she has gone'],
], [22*mm, (CW-22*mm)/5, (CW-22*mm)/5, (CW-22*mm)/5, (CW-22*mm)/5, (CW-22*mm)/5], fs=7.2,
  caption='Table 7.11 &mdash; The five cases side by side. Three observations are worth drawing out. '
          'First, <b>Task&nbsp;D holds in UC-2 and Task&nbsp;B holds in UC-5</b>: the engine leaves '
          'things alone when leaving them alone is right, which a rule-based throttle would not. '
          'Second, <b>UC-3 moves up and UC-4 moves in both directions at once</b>, so the loop is not '
          'a one-way ratchet. Third, <b>the primary gain is different in every column</b> &mdash; '
          'availability, charge, acceptance, correctness, avoided waste &mdash; which is why the '
          'evaluation in &sect;9 cannot be a single number.')
F += [PageBreak()]
