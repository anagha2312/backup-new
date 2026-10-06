# -*- coding: utf-8 -*-
from abase import *

# ===================== COVER =====================
F += [SP(40)]
F += [P('How It All Fits Together', 'title')]
F += [P('The shape of the LearnPerk system, and how we will know model switching '
        'was worth building', 'sub')]
F += [RULEF(TEAL, 1.8)]
F += [SP(14)]
F += [P('Prepared by Anagha', 'big')]

F += [NextPageTemplate('body'), PageBreak()]

# ===================== CONTENTS =====================
F += [H1('What is in this document')]
F += [P('Two halves. The first draws the system. The second says how we will judge it.', 'big')]

for n, t, d in [
    ('1', 'The whole system on one page',
     'One picture: the phone, the cloud, and what travels between them.'),
    ('2', 'What each part does',
     'The same picture, walked through block by block.'),
    ('3', 'What comes from the cloud',
     'Aggregated, anonymous information &mdash; and what is deliberately not sent.'),
    ('4', 'One decision, end to end',
     'The train enters a tunnel. What happens in the next fifth of a second.'),
    ('5', 'How we will compare it',
     'Four versions of the app, run against the same journeys.'),
    ('6', 'The metrics',
     'Six families of measurement: energy, quality, never-blank, the switching '
     'itself, the person, and fairness.'),
    ('7', 'What a result looks like',
     'The four conditions that have to hold before we call switching a win.'),
    ('8', 'Five ways to get this measurement wrong',
     'Including the one that would make our numbers look great and be untrue.'),
    ('9', 'Words we used',
     'A short glossary.'),
]:
    F.append(Paragraph('%s&nbsp;&nbsp;&nbsp;%s' % (n, t), S['toc1']))
    F.append(Paragraph('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + d, S['tiny']))
    F.append(SP(4))

F += [SP(6)]
F += BOX('The short version, if you read nothing else',
    'Three models of each kind sit <b>on the phone</b>. A small piece of software watches four '
    'simple things &mdash; signal, battery, time left, how well we know the person &mdash; and '
    'picks which model to use, changing its mind a few times per journey. The <b>cloud</b> is not '
    'in the loop: once a day it sends down fresh model files and a popularity table built from '
    'everybody&rsquo;s behaviour with the names stripped out, and that is the whole of its '
    'involvement.<br/><br/>'
    'To prove it was worth doing we run the same journeys four ways &mdash; always Light, always '
    'Standard, always Strong, and switching &mdash; and compare them on <b>energy</b>, '
    '<b>quality</b>, <b>how often the screen had something on it</b>, and <b>what the switching '
    'itself cost</b>.',
    accent=TEAL)

F += [PageBreak()]

# ===================== 1  THE BIG DIAGRAM =====================
F += [H1('1&nbsp;&nbsp;The whole system on one page')]
F += [P('Everything inside the big box happens on the commuter&rsquo;s phone, with no internet '
        'needed. The cloud sits above it and is only involved once a day.', 'big')]


def main_diagram(cv):
    W = DW

    # ---------- cloud ----------
    box(cv, 0, 168, W, 34, None, None, fill=CLOUDBG, edge=E_SMART, lw=0.9,
        r=2.5, dash=(2.4, 1.8))
    label(cv, 6, 196.4,
          'THE CLOUD  —  a few minutes a day, on wifi, usually overnight while the phone charges',
          fs=7.2, col=E_SMART)
    cbx = [(6, 'Everybody’s totals',
            'Counts only. "At 8am near Zuid, offers like this got taken." Millions of people, '
            'added up, no individuals.'),
           (59, 'Fresh model files',
            'Light, Standard and Strong rebuilt on last week’s totals, then shipped down as '
            'one small bundle.'),
           (112, 'Better starting numbers',
            'What counts as "low battery" or "nearly there", nudged based on what we saw last '
            'week.')]
    for x, t, b in cbx:
        box(cv, x, 171, 48, 20, t, b, fill=colors.white, edge=E_SMART, tfs=7.2, bfs=5.9)

    # ---------- the two links ----------
    arrow(cv, 28, 167, 28, 150, col=E_SMART, lw=1.4, head=2.6)
    label(cv, 32, 162.5, 'COMES DOWN  —  once a day', fs=6.4, col=E_SMART)
    note(cv, 32, 159, 46, 'New model files and a fresh popularity table. A few megabytes. '
                          'The phone works perfectly well if it never arrives.', fs=6.0)

    arrow(cv, 138, 150, 138, 167, col=TEAL, lw=1.4, head=2.6)
    label(cv, 134, 162.5, 'GOES UP  —  once a day', fs=6.4, col=TEAL, align='r')
    note(cv, 88, 159, 46, 'Counters and the switch log. Which model ran, which rule fired. '
                          'Nothing that identifies a person.', fs=6.0, align='r')

    # ---------- phone ----------
    box(cv, 0, 0, W, 148, None, None, fill=PHONEBG, edge=NAVY, lw=1.3, r=2.5)
    cv.saveState(); cv.setFillColor(NAVY)
    cv.roundRect(0, 140*mm, W*mm, 8*mm, 2.5*mm, stroke=0, fill=1)
    cv.rect(0, 140*mm, W*mm, 4*mm, stroke=0, fill=1)
    cv.setFont(HEAD, 7.6); cv.setFillColor(colors.white)
    cv.drawString(4*mm, 142.6*mm,
                  'THE PHONE  —  everything below this line runs here, offline, in a tunnel, '
                  'on a five-year-old handset')
    cv.restoreState()

    # row A - the senses
    label(cv, 6, 136, 'WHAT IT NOTICES  —  re-checked every few seconds', fs=6.8, col=TEAL)
    senses = [('Signal', 'Internet, patchy, or a tunnel?'),
              ('Battery', 'How much is left, and how fast is it going?'),
              ('Time left', 'Minutes until they get off.'),
              ('How well we know them', 'A regular, or signed up on Tuesday?')]
    for i, (t, b) in enumerate(senses):
        box(cv, 6 + i*37, 112, 32, 22, t, b, fill=colors.white, edge=RULE, tfs=7.4, bfs=5.9)

    arrow(cv, 83, 111, 83, 104, col=NAVY)

    # row B - the switcher + the notebook
    box(cv, 6, 82, 106, 20, 'THE SWITCHER',
        'Six rules, checked in order; the first that applies wins. A cool-down stops it flipping '
        'back and forth. If everything else is ruled out it falls back to Light, so it can never '
        'end up with nothing.',
        fill=L_STD, edge=E_STD, lw=1.2, tfs=8.4, bfs=6.2)
    box(cv, 118, 82, 42, 20, 'THE NOTEBOOK',
        'Every switch written down: when, from what to what, and which rule caused it.',
        fill=colors.white, edge=TEAL, tfs=7.4, bfs=5.9)
    arrow(cv, 112, 92, 117, 92, col=TEAL, lw=0.9, head=1.6)

    arrow(cv, 83, 81, 83, 74, col=NAVY)
    label(cv, 86, 76.8, 'picks one level for each job', fs=6.2, col=MUTED, font=SANS)

    # row C - the shelf
    label(cv, 6, 75.5, 'THE SHELF  —  three of each, all already downloaded', fs=6.8, col=TEAL)
    cols = [
        (6, 'CHOOSING OFFERS', False,
         [('Strong', 'the Smart Picker', 'needs internet, history and a decent phone'),
          ('Standard', 'the Everyday Picker', 'the normal one. Works offline.'),
          ('Light', 'the Simple Picker', 'needs nothing at all. Always available.')]),
        (59, 'CHOOSING CONTENT', False,
         [('Strong', 'the Smart Feed', 'reads the articles themselves'),
          ('Standard', 'the Everyday Feed', 'learns from what they opened'),
          ('Light', 'the Simple Feed', 'sorts what is already on the phone')]),
        (112, 'ANSWERING QUESTIONS', True,
         [('Strong', '', 'not in the first build'),
          ('Standard', '', 'not in the first build'),
          ('Light', '', 'not in the first build')]),
    ]
    for x, head, off, chips in cols:
        box(cv, x, 64, 48, 8, head, None, fill=NAVY if not off else E_OFF,
            edge=NAVY if not off else E_OFF, tfs=7.0, tcol=colors.white)
        fills = [L_SMART, L_STD, L_BASIC]
        edges = [E_SMART, E_STD, E_BASIC]
        for i, (lvl, nm, sub) in enumerate(chips):
            yy = 50 - i*14
            f = L_OFF if off else fills[i]
            e = E_OFF if off else edges[i]
            ttl = lvl if not nm else '%s  ·  %s' % (lvl, nm)
            box(cv, x, yy, 48, 12, ttl, sub, fill=f, edge=e, tfs=7.0, bfs=5.8,
                tcol=MUTED if off else NAVY)

    arrow(cv, 30, 21, 30, 14, col=NAVY)
    label(cv, 33, 16.8, 'the chosen one runs — a few milliseconds', fs=6.2, col=MUTED,
          font=SANS)

    # row D - what the person sees
    box(cv, 6, 2, 102, 11, 'WHAT THE COMMUTER SEES',
        'An offer still looks like an offer. Nothing on the screen says which model chose it.',
        fill=BAND, edge=NAVY, lw=1.1, tfs=7.6, bfs=6.1)
    box(cv, 118, 2, 42, 11, 'THE FLOOR',
        'Light can never be ruled out. The screen is never allowed to be empty.',
        fill=L_BASIC, edge=E_BASIC, tfs=7.4, bfs=5.8)


F += [Dia(202, main_diagram)]
F += [Paragraph('The four boxes at the top feed the switcher; the switcher picks one row off each '
                'shelf; the picked model produces what the commuter sees. The cloud never sits in '
                'the middle of a decision &mdash; if it vanished for a week, everything below the '
                'navy line would carry on working.', S['cap'])]
F += [PageBreak()]
