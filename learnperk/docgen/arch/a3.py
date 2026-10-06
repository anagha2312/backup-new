# -*- coding: utf-8 -*-
from abase import *

# ===================== 5 =====================
F += [H1('5&nbsp;&nbsp;How we will compare it')]
F += [P('To say switching is better we have to say <b>better than what</b>. So we build four '
        'versions of the app and run them over the same journeys. Three of them never switch.',
        'big')]


def arms_diagram(cv):
    lab_w, bar_x, bar_w = 40, 44, DW - 46
    rows = [
        ('Arm A  ·  Always Light', 'never switches',
         [(0.22, L_BASIC, E_BASIC, 'Light', NAVY), (0.53, L_BASIC, E_BASIC, 'Light', NAVY),
          (0.25, L_BASIC, E_BASIC, 'Light', NAVY)],
         'Cheapest possible. The quality floor.'),
        ('Arm B  ·  Always Standard', 'never switches',
         [(0.22, L_STD, E_STD, 'Standard', NAVY), (0.53, L_STD, E_STD, 'Standard', NAVY),
          (0.25, L_STD, E_STD, 'Standard', NAVY)],
         'What we would ship if we did nothing. THE BASELINE THAT MATTERS.'),
        ('Arm C  ·  Always Strong', 'never switches',
         [(0.22, L_SMART, E_SMART, 'Strong', NAVY), (0.53, L_OFF, E_OFF, 'NOTHING AT ALL', MUTED),
          (0.25, L_SMART, E_SMART, 'Strong', NAVY)],
         'The quality ceiling — for the part of the journey it survives.'),
        ('Arm D  ·  Switching', 'the thing we are testing',
         [(0.22, L_STD, E_STD, 'Standard', NAVY), (0.53, L_BASIC, E_BASIC, 'Light', NAVY),
          (0.15, L_STD, E_STD, 'Standard', NAVY), (0.10, L_BASIC, E_BASIC, 'Light', NAVY)],
         'Steps down for the tunnel, back up after, down again near the end.'),
    ]
    # journey ruler
    label(cv, bar_x, 74.5, 'ONE 14-MINUTE JOURNEY  —  the same recorded conditions for all four arms',
          fs=6.6, col=TEAL)
    cv.saveState(); cv.setFillColor(colors.HexColor('#E9EEF2'))
    cv.rect((bar_x + bar_w*0.22)*mm, 4*mm, (bar_w*0.53)*mm, 68*mm, stroke=0, fill=1)
    cv.restoreState()
    label(cv, bar_x + bar_w*0.485, 69.5, 'IN THE TUNNEL — no signal', fs=6.4, col=MUTED,
          font=HEAD, align='c')

    y = 57
    for name, sub, segs, foot in rows:
        note(cv, 0, y + 8.6, lab_w, name, fs=7.4, col=NAVY, font=HEAD)
        note(cv, 0, y + 5.2, lab_w, sub, fs=6.1, col=MUTED)
        segbar(cv, bar_x, y + 3, bar_w, 9, segs, fs=6.4)
        note(cv, bar_x, y + 0.6, bar_w, foot, fs=6.0, col=MUTED)
        y -= 16

    label(cv, bar_x + bar_w/2, 0.5,
          'Same route, same time of day, same phone model, same starting battery.',
          fs=6.4, col=MUTED, font=SANS, align='c')


F += [Dia(78, arms_diagram)]
F += [Paragraph('Arm B is the one that decides the project. Arm A tells us how much quality '
                'switching actually buys over doing the cheapest thing always; Arm C tells us how '
                'much quality we gave up against a ceiling that cannot actually be reached on a '
                'metro.', S['cap'])]

F += [H2('How the four arms get run')]
F += TBL(['Stage', 'What happens', 'What it is good for'], [
    ['<b>1. Replay</b>',
     'We take thousands of real recorded journeys &mdash; the signal, battery and timing traces, '
     'with the content of them stripped &mdash; and play the same trace through all four arms on '
     'the same bench phone.',
     'Perfectly paired comparison. Every arm faces the identical fourteen minutes, so any '
     'difference in energy or coverage is caused by the arm and nothing else.'],
    ['<b>2. Watch-only on our own phones</b>',
     'Switching runs for real but changes nothing: the app records what it <i>would</i> have '
     'switched to, and keeps using Standard.',
     'Every number about the switching behaviour itself &mdash; how often, which rules, whether it '
     'flaps &mdash; at zero risk to any commuter.'],
    ['<b>3. A live split</b>',
     'A small slice of real users, randomly assigned to an arm, for a few weeks.',
     'The only way to get the numbers that involve human behaviour: redemptions, reading time, '
     'whether people come back.'],
], [34*mm, 60*mm, CW-94*mm], fs=9.2,
  caption='Stages 1 and 2 give almost all of the energy and coverage evidence and cost nobody '
          'anything. Only stage 3 needs real users, and by then we already know the rules behave.')

F += [PageBreak()]

# ===================== 6 =====================
F += [H1('6&nbsp;&nbsp;The metrics')]
F += [P('Six families. The first two are the classic trade-off &mdash; did we spend less, did we '
        'lose quality. The third is the one only switching can win. The fourth asks whether the '
        'switching machinery paid for itself. The last two ask whether it helped a person, and '
        'whether it hurt anybody.', 'big')]

F += [H2('Family 1 &mdash; Energy and the phone')]
F += [P('<i>The &ldquo;it cost less&rdquo; claim. Measured on a bench phone with fixed screen '
        'brightness, so we are measuring the app and not the display.</i>', 'p')]
F += TBL(['Metric', 'Unit', 'Why it matters', 'What a win looks like'], [
    ['<b>Battery used per journey</b>', 'mAh per 14-min journey',
     'The headline. What the commuter would actually feel.',
     'Meaningfully below Arm B. We are aiming for at least 15&ndash;20% lower.'],
    ['<b>Energy per decision</b>', 'millijoules per inference',
     'Separates &ldquo;cheaper model&rdquo; from &ldquo;we simply made fewer decisions&rdquo;.',
     'Lower than Arm B, and the gap should track how much time was spent at Light.'],
    ['<b>Decision time</b>', 'milliseconds, median <b>and</b> worst 5%',
     'A good median with a terrible tail is a bad app. The tail is what people notice.',
     'Both at or below Arm B. The worst 5% matters more than the median.'],
    ['<b>Peak memory</b>', 'MB resident',
     'Three models on the shelf could mean three models in memory, which would be a real cost.',
     'No higher than Arm B &mdash; only the chosen model should be resident.'],
    ['<b>Thermal pressure</b>', '&deg;C peak, and seconds spent throttled',
     'A hot phone gets slowed down by the operating system, which makes everything worse.',
     'Lower than Arm C. Ideally indistinguishable from Arm A.'],
    ['<b>Mobile data used</b>', 'KB per journey',
     'Strong models reach out to the network. Data costs the commuter money.',
     'Well below Arm C. Close to Arm A.'],
], [34*mm, 30*mm, 48*mm, CW-112*mm], fs=8.8)

F += [PageBreak()]

F += [H2('Family 2 &mdash; Quality of what was shown')]
F += [P('<i>The &ldquo;we did not lose anything&rdquo; claim. This is the side we expect to be '
        'slightly worse, so the target is not &ldquo;better&rdquo; &mdash; it is &ldquo;not '
        'meaningfully worse&rdquo;.</i>', 'p')]
F += TBL(['Metric', 'Unit', 'Why it matters', 'What a win looks like'], [
    ['<b>Offer redemption rate</b>', '% of offers shown that get used',
     'The one that makes money. If this drops, nothing else rescues the project.',
     'Within a small, pre-declared margin of Arm B &mdash; we propose 2% relative.'],
    ['<b>Offer click rate</b>', '% of offers shown that get tapped',
     'A faster-moving signal than redemption, useful while redemptions are still sparse.',
     'Non-inferior to Arm B.'],
    ['<b>Agreement with Strong</b>', '% of decisions where the top pick was identical',
     'The cheap, high-volume proxy. For every decision we can also ask what Strong would have '
     'said, offline, for free.',
     'High &mdash; and crucially, high <i>in the moments we stepped down</i>. If Light disagrees '
     'with Strong 60% of the time in a tunnel, stepping down is expensive.'],
    ['<b>Regret</b>', 'average drop in predicted value when it disagrees',
     'Not all disagreements are equal. Picking the second-best offer is nearly free; picking the '
     'ninth is not.',
     'Small and, more importantly, bounded &mdash; no long tail of very bad picks.'],
    ['<b>Ranking quality, offline</b>', 'nDCG@5, Precision@3, AUC',
     'Scored against logged outcomes. Lets us compare arms on millions of decisions without '
     'showing anything to anybody.',
     'Arm D close to Arm C, clearly above Arm A.'],
    ['<b>Content engagement</b>', 'open rate, reading seconds, % finished',
     'The feed half of the story.',
     'Non-inferior to Arm B, and clearly better than Arm C <i>in tunnels</i>, where Arm C shows '
     'nothing.'],
], [34*mm, 34*mm, 46*mm, CW-114*mm], fs=8.8)

F += BOX('Why &ldquo;non-inferior&rdquo; and not &ldquo;better&rdquo;',
    'The honest claim for model switching is not that it makes better recommendations. A smaller '
    'model is a smaller model. The claim is: <b>roughly the same quality, for meaningfully less '
    'energy, and available in far more moments</b>.<br/><br/>'
    'So the quality test has to be a <i>non-inferiority</i> test, with the acceptable margin '
    'written down <b>before</b> we look at any results. Deciding afterwards what counts as close '
    'enough is how projects talk themselves into shipping things that did not work.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))

F += [PageBreak()]

F += [H2('Family 3 &mdash; Never blank')]
F += [P('<i>The family where switching does not compete with the baselines &mdash; it beats them '
        'outright. A fixed Strong model cannot answer in a tunnel, and the metro is mostly '
        'tunnel.</i>', 'p')]
F += TBL(['Metric', 'Unit', 'Why it matters', 'What a win looks like'], [
    ['<b>Answered rate</b>', '% of decision requests that produced anything at all',
     'The single clearest argument for the whole project.',
     'Arm D at essentially 100%. Arm C will be far lower on a tunnel-heavy route.'],
    ['<b>Blank-screen seconds</b>', 'seconds per journey with nothing in the feed',
     'The commuter-facing version of the same thing. Seven blank minutes of a fourteen-minute trip '
     'is a broken app.',
     'Near zero for Arm D. This is the number to put in front of anyone who is not convinced.'],
    ['<b>Time to first result</b>', 'milliseconds, median and worst 5%',
     'A result that arrives after they have put the phone away is not a result.',
     'Better than Arm C, which has to wait on the network.'],
    ['<b>Timeout and error rate</b>', '% of decisions that failed or gave up',
     'Distinguishes &ldquo;could not answer&rdquo; from &ldquo;answered badly&rdquo;.',
     'Effectively zero for Arm D.'],
], [34*mm, 34*mm, 44*mm, CW-112*mm], fs=8.8,
  caption='This family is worth stating separately because averaging it into a quality score hides '
          'it. An arm that gives brilliant answers 45% of the time and nothing the rest of the '
          'time can look respectable on a mean.')

F += [PageBreak()]
F += [H2('Family 4 &mdash; Did the switching itself pay for itself')]
F += [P('<i>The machinery has a cost. These are the metrics that would tell us switching was a bad '
        'idea, and they are the ones a sceptical reviewer will go to first.</i>', 'p')]
F += TBL(['Metric', 'Unit', 'Why it matters', 'What a win looks like'], [
    ['<b>Switches per journey</b>', 'count',
     'Sanity. The design intends a handful.',
     'Roughly 2&ndash;8. Dozens would mean the thresholds are wrong.'],
    ['<b>Flap rate</b>', '% of switches reversed within 60 seconds',
     'Flapping is the classic failure of any rule-based switcher, and it burns energy for nothing.',
     'Under 1%. The cool-down exists to make this true.'],
    ['<b>Cost of one switch</b>', 'milliseconds and millijoules to unload and load',
     'The price of the mechanism, measured directly rather than assumed.',
     'Tens of milliseconds, and small enough that the next metric works out.'],
    ['<b>Switch overhead ratio</b>', 'energy spent switching &divide; energy saved',
     '<b>The make-or-break number.</b> If we spend more on swapping than we save by running '
     'smaller models, the entire idea is a loss regardless of every other metric.',
     'Under 10%. Above 50% and we should stop and redesign.'],
    ['<b>Time at each level</b>', '% of journey at Light / Standard / Strong',
     'Tells us whether the rules describe the world we thought they did.',
     'No surprises. If Strong is never reached, Rule 6 is dead code.'],
    ['<b>Explainable switches</b>', '% of switches attributable to a named rule',
     'If we cannot say why it switched, we cannot debug it or defend it.',
     'Exactly 100%. Anything else is a bug, not a metric.'],
    ['<b>Gap to hindsight</b>', 'quality vs a chooser that knew the future',
     'Replay the journey and compute the best possible sequence of levels with full knowledge. '
     'That is the ceiling any rule set could reach.',
     'A small gap means the rules are near-optimal; a large one means better rules exist and are '
     'worth finding.'],
], [34*mm, 34*mm, 46*mm, CW-114*mm], fs=8.8)

F += [PageBreak()]

F += [H2('Family 5 &mdash; Did it help a person')]
F += [P('<i>Everything above can look good while the app still gets deleted. These come from the '
        'live split only.</i>', 'p')]
F += TBL(['Metric', 'Unit', 'Why it matters', 'What a win looks like'], [
    ['<b>Session length and frequency</b>', 'minutes per journey; sessions per week',
     'The broadest signal that the app is more useful than it was.',
     'At or above Arm B.'],
    ['<b>Retention</b>', '% still active at day 7 and day 30',
     'Slow but decisive. A feed that works in tunnels should show up here.',
     'At or above Arm B, especially for tunnel-heavy routes.'],
    ['<b>App killed by the phone</b>', 'background terminations per 100 journeys',
     'The direct consequence of being a battery hog. It is also invisible unless you measure it.',
     'Below Arm B and far below Arm C.'],
    ['<b>Crash and freeze rate</b>', 'per 1,000 sessions',
     'Loading and unloading models is exactly the kind of thing that introduces crashes.',
     'No worse than Arm B. This is a gate, not a nice-to-have.'],
    ['<b>Battery complaints</b>', 'mentions per 1,000 reviews; uninstalls after a long journey',
     'Noisy, but it is the language real users actually use.',
     'No increase.'],
], [34*mm, 36*mm, 44*mm, CW-114*mm], fs=8.8)

F += [H2('Family 6 &mdash; Did it hurt anybody')]
F += [P('<i>Averages hide harm. Every metric above gets cut these four ways before we believe it.'
        '</i>', 'p')]
F += TBL(['Cut the results by…', 'The question it answers'], [
    ['<b>Phone age and tier</b>',
     'Switching should <i>narrow</i> the gap between a new phone and a five-year-old one, because '
     'the old phone gets a model it can actually run. If the gap widens instead, we have built '
     'something that quietly works better for people with money.'],
    ['<b>How new the user is</b>',
     'Rule 4 steps new users down deliberately. We need to confirm that this protects them from '
     'confident bad guesses rather than just giving them a worse app for a month.'],
    ['<b>Route type</b>',
     'Tunnel-heavy versus overground. Almost all of the coverage benefit lives in the first group; '
     'if there is a cost, it will show up in the second.'],
    ['<b>The worst 5% of journeys</b>',
     'Not the average journey &mdash; the bad one. Low battery, old phone, long tunnel, new user, '
     'all at once. If switching helps anywhere, it should help most here.'],
], [40*mm, CW-40*mm], fs=9.2,
  caption='If a headline number improves but one of these cuts gets worse, that is a finding, not '
          'a rounding error.')

F += [PageBreak()]
