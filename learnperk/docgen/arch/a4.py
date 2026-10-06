# -*- coding: utf-8 -*-
from abase import *

# ===================== 7 =====================
F += [H1('7&nbsp;&nbsp;What a result looks like')]
F += [P('Sixty metrics do not make a decision. Four of them do. Everything else is there to '
        'explain the four, or to catch the case where one of them is lying.', 'big')]

F += TBL(['', 'The condition', 'Measured as', 'Against'], [
    ['<b>1</b>', '<b>It genuinely costs less.</b>',
     'Battery used per journey, at least 15% lower.', 'Arm B &mdash; always Standard'],
    ['<b>2</b>', '<b>It is not meaningfully worse.</b>',
     'Offer redemption rate within 2% relative, with the margin fixed in advance.',
     'Arm B &mdash; always Standard'],
    ['<b>3</b>', '<b>It is available far more often.</b>',
     'Blank-screen seconds per journey at or near zero.',
     'Arm C &mdash; always Strong'],
    ['<b>4</b>', '<b>The mechanism paid for itself.</b>',
     'Energy spent switching under 10% of the energy saved.', 'Itself'],
], [8*mm, 48*mm, CW-104*mm, 48*mm], fs=9.4,
  bg=[L_BASIC, L_STD, L_SMART, colors.HexColor('#F3EDF7')],
  caption='All four have to hold. Three out of four is not a pass — it is a specific, informative '
          'failure, and each one points at a different fix.')

F += [PageBreak()]
F += [H2('The picture we expect to end up with')]
F += [P('Two of those conditions can be drawn together. Energy along the bottom, quality up the '
        'side. Every arm is one point, and the corner we want is <b>up and to the left</b>: as '
        'good, for less.')]


def tradeoff(cv):
    x0, y0, w, h = 26, 20, 104, 62
    # the target region
    cv.saveState()
    cv.setFillColor(colors.HexColor('#EAF1FA'))
    cv.rect(x0*mm, (y0+h*0.52)*mm, (w*0.46)*mm, (h*0.48)*mm, stroke=0, fill=1)
    cv.restoreState()
    label(cv, x0 + w*0.23, y0 + h - 5.5, 'WHERE WE WANT TO LAND', fs=6.4, col=SER1, align='c')

    # axes
    cv.saveState(); cv.setStrokeColor(MUTED); cv.setLineWidth(0.8)
    cv.line(x0*mm, y0*mm, (x0+w)*mm, y0*mm)
    cv.line(x0*mm, y0*mm, x0*mm, (y0+h)*mm)
    cv.restoreState()
    arrow(cv, x0+w-6, y0, x0+w, y0, col=MUTED, lw=0.8, head=1.6)
    arrow(cv, x0, y0+h-6, x0, y0+h, col=MUTED, lw=0.8, head=1.6)
    label(cv, x0 + w/2, y0 - 6.5, 'ENERGY USED PER JOURNEY   →   more', fs=6.8, col=MUTED,
          font=HEAD, align='c')
    cv.saveState(); cv.translate((x0-5.5)*mm, (y0 + h/2)*mm); cv.rotate(90)
    cv.setFont(HEAD, 6.8); cv.setFillColor(MUTED)
    cv.drawCentredString(0, 0, 'QUALITY OF WHAT WAS SHOWN   →   better')
    cv.restoreState()

    # the four arms: (x frac, y frac, label, filled?, label side)
    pts = [(0.16, 0.24, 'Arm A\nalways Light', False, 'r'),
           (0.52, 0.60, 'Arm B\nalways Standard', False, 'r'),
           (0.88, 0.86, 'Arm C\nalways Strong', False, 'l'),
           (0.34, 0.72, 'Arm D\nswitching', True, 'l')]
    for fx, fy, txt, filled, side in pts:
        px, py = x0 + w*fx, y0 + h*fy
        col = SER1 if filled else SER2
        cv.saveState()
        cv.setLineWidth(1.6); cv.setStrokeColor(col)
        cv.setFillColor(col if filled else colors.white)
        cv.circle(px*mm, py*mm, 1.7*mm, stroke=1, fill=1)
        cv.restoreState()
        lines = txt.split('\n')
        lx = px + 3.2 if side == 'r' else px - 3.2
        al = 'l' if side == 'r' else 'r'
        label(cv, lx, py + 0.9, lines[0], fs=7.0, col=NAVY, font=HEAD, align=al)
        label(cv, lx, py - 2.4, lines[1], fs=6.3, col=MUTED, font=SANS, align=al)

    # the arrow that tells the story
    arrow(cv, 26 + 104*0.52 - 1.4, 20 + 62*0.60 + 2.2, 26 + 104*0.372, 20 + 62*0.695,
          col=SER1, lw=1.2, head=2.0, dash=(2, 1.6))

    # the caveat on Arm C
    cv.saveState(); cv.setStrokeColor(E_OFF); cv.setLineWidth(0.7); cv.setDash(1.8, 1.6)
    cv.line((x0 + w*0.88)*mm, (y0 + h*0.86 - 2.2)*mm, 140*mm, 34*mm)
    cv.restoreState()
    box(cv, 134, 14, 32, 19, 'But only 45% of the time',
        'Arm C answers nothing in a tunnel. Its quality score covers just the journeys it survived.',
        fill=L_OFF, edge=E_OFF, tfs=6.6, bfs=5.7)

    # legend
    cv.saveState()
    cv.setLineWidth(1.6); cv.setStrokeColor(SER1); cv.setFillColor(SER1)
    cv.circle(27*mm, 6*mm, 1.5*mm, stroke=1, fill=1)
    cv.setStrokeColor(SER2); cv.setFillColor(colors.white)
    cv.circle(62*mm, 6*mm, 1.5*mm, stroke=1, fill=1)
    cv.restoreState()
    label(cv, 30, 5, 'switching', fs=6.8, col=NAVY, font=SANS)
    label(cv, 65, 5, 'fixed single model (never switches)', fs=6.8, col=NAVY, font=SANS)


F += [Dia(92, tradeoff)]
F += [Paragraph('<b>These positions are what we expect to find, not measurements &mdash; no data '
                'has been collected yet.</b> The diagram is here to make the shape of the argument '
                'clear: Arm D should sit up and to the left of Arm B, and the grey note is the '
                'reason Arm C sitting highest does not settle anything.', S['cap'])]

F += BOX('Reading the result honestly',
    'If Arm D lands where the dashed arrow points &mdash; clearly left of Arm B, at roughly the '
    'same height &mdash; switching worked, and the coverage numbers from Family 3 make the case '
    'stronger still.<br/><br/>'
    'If Arm D lands <b>below and left</b> of Arm B, we bought energy with quality. That is not '
    'automatically a failure, but it is a different, smaller claim and it has to be argued on its '
    'own terms.<br/><br/>'
    'If Arm D lands <b>right</b> of Arm B, the switching overhead ate the saving. Check Family 4 '
    'first &mdash; it is far more likely to be a flapping problem than a fundamental one.',
    accent=TEAL)

F += [PageBreak()]

# ===================== 8 =====================
F += [H1('8&nbsp;&nbsp;Five ways to get this measurement wrong')]
F += [P('These are the mistakes that produce a confident, well-presented, wrong answer. The first '
        'one is the one we are most likely to make.', 'big')]

F += TBL(['', 'The trap', 'What it does to the numbers', 'How we avoid it'], [
    ['<b>1</b>', '<b>Dropping the journeys where Strong could not answer.</b>',
     'It is the natural thing to do &mdash; you cannot score a recommendation that never happened. '
     'But it silently removes every tunnel from Arm C&rsquo;s results, so Arm C gets judged only '
     'on its easiest moments and comes out looking excellent. This single decision could make '
     'switching look unnecessary.',
     'A decision that produced nothing is scored as a <b>zero</b>, not as missing data. Every arm '
     'is scored over the same denominator: all decisions requested.'],
    ['<b>2</b>', '<b>Comparing different journeys.</b>',
     'Arm C happens to get more overground routes, or sunnier weeks, or newer phones, and the '
     'comparison measures that instead of the arm.',
     'Replay the identical recorded trace through all four arms on the same bench phone. For the '
     'live split, randomise per user and check the arms are balanced on route and device before '
     'reading anything.'],
    ['<b>3</b>', '<b>Letting the screen dominate the battery number.</b>',
     'The display uses far more power than any model on the phone. A small difference in screen-on '
     'time between arms would swamp the entire effect we are trying to measure.',
     'Fix screen brightness on the bench, and report the <i>app&rsquo;s share</i> of battery use '
     'rather than total drain. Report screen-on time separately as a check.'],
    ['<b>4</b>', '<b>Choosing the success margin after seeing the data.</b>',
     'Whatever the quality drop turns out to be, it will be possible to describe it as acceptable. '
     'This is how a project convinces itself.',
     'The 15% energy target and the 2% quality margin in Section 7 are written down now, before '
     'any measurement exists. If we later want to change them, we change them in writing and say '
     'why.'],
    ['<b>5</b>', '<b>Reporting only averages.</b>',
     'A median decision time of 20 ms with a worst-5% of 900 ms is a bad app that looks like a '
     'good one. Averages also hide the fairness problems in Family 6 completely.',
     'Every latency and energy metric is reported as median <b>and</b> worst 5%. Every headline is '
     'cut by phone tier, user age, and route before it is believed.'],
], [8*mm, 40*mm, CW-124*mm, 52*mm], fs=8.8)

F += BOX('The cheapest thing we can do, and we should do it first',
    'Watch-only mode. Switching runs, decides, and writes down what it <i>would</i> have done '
    '&mdash; and then does nothing. It gives us the whole of Family 4 (switches per journey, flap '
    'rate, time at each level, whether every switch is explainable) and a good estimate of Family '
    '1, on real journeys, with real conditions, and with literally zero risk to any commuter.'
    '<br/><br/>'
    'If the rules are badly tuned, we find out here, for free, before anybody is affected.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))

F += [PageBreak()]

# ===================== 9 =====================
F += [H1('9&nbsp;&nbsp;Words we used')]
F += [P('Mostly the measurement ones, since the architecture words are in the plain-English '
        'switching guide.', 'big')]
F += TBL(['Word', 'What it means here'], [
    ['<b>Arm</b>', 'One version of the app in the comparison. We have four: always Light, always '
     'Standard, always Strong, and switching.'],
    ['<b>Baseline</b>', 'The arm we are trying to beat. Ours is <b>always Standard</b>, because '
     'that is what we would ship if we did nothing at all.'],
    ['<b>Non-inferiority</b>', 'Testing that something is <i>not meaningfully worse</i>, rather '
     'than that it is better. The right test when you are trading quality for cost, and it needs '
     'its margin agreed in advance.'],
    ['<b>Coverage / answered rate</b>', 'The share of decisions that produced anything at all. A '
     'model that cannot run in a tunnel has poor coverage no matter how good its answers are.'],
    ['<b>Worst 5% (p95)</b>', 'The value that only one journey in twenty is worse than. It is what '
     'people actually complain about; the median is what looks good in a slide.'],
    ['<b>Flapping</b>', 'Switching back and forth because a reading is sitting right on a '
     'threshold. Burns energy and produces nothing.'],
    ['<b>Switch overhead</b>', 'The energy and time spent unloading one model and loading another. '
     'The price of the mechanism, and the thing that could sink the whole idea.'],
    ['<b>Regret</b>', 'How much worse the choice we made was than the choice the best available '
     'model would have made. Low regret means stepping down was nearly free.'],
    ['<b>Hindsight ceiling</b>', 'The best any rule set could have done on a journey, computed '
     'afterwards with full knowledge of what happened. Tells us whether to invest in better rules.'],
    ['<b>Watch-only mode</b>', 'The switcher decides and logs, but does not actually switch. Gives '
     'us most of the evidence at none of the risk.'],
    ['<b>Aggregated</b>', 'Added up across many people until no individual remains. What goes to '
     'the cloud is counts, not records.'],
    ['<b>Replay</b>', 'Playing a recorded journey &mdash; its signal, battery and timing trace '
     '&mdash; through each arm on a bench phone, so all four face identical conditions.'],
], [38*mm, CW-38*mm], fs=9.4)

F += [SP(6), RULEF(TEAL, 1.2)]
F += BOX('If you remember one thing',
    'The architecture is simple: <b>three models of each kind sit on the phone</b>, a small rule '
    'engine watches four readings and picks one, and the cloud only sends down fresh files once a '
    'day from everybody&rsquo;s behaviour added together.<br/><br/>'
    'The argument is equally simple, and it has three parts, not one: <b>less energy</b>, '
    '<b>about the same quality</b>, and <b>an answer in far more moments</b>. The third part is '
    'the one no single fixed model can match, and it is the part that is easiest to lose by '
    'measuring carelessly.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))
