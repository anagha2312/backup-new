# -*- coding: utf-8 -*-
from abase import *

# ===================== 2 =====================
F += [H1('2&nbsp;&nbsp;What each part does')]
F += [P('The same picture, one block at a time. Read the middle column if you only want to know '
        'what it is for; read the right one if you want to know what it actually is.', 'big')]

F += TBL(['The block', 'What it is for', 'What it actually is'], [
    ['<b>What it notices</b><br/><font size=8 color="#5A6772">the four boxes at the top</font>',
     'Tells the app what kind of moment this is. Four readings, refreshed every few seconds.',
     'A small background job reading things the phone already reports &mdash; connectivity state, '
     'battery level and drain rate, the GVB arrival estimate, and a count of how much history we '
     'hold for this person. Nothing new is collected.'],
    ['<b>The switcher</b><br/><font size=8 color="#5A6772">the amber box in the middle</font>',
     'Turns those four readings into a decision: which level each job should use right now.',
     'Six ordered if-then rules, a minimum dwell time before it is allowed to change its mind '
     'again, and a hard floor that guarantees Light is always a legal answer. A few hundred lines '
     'of ordinary code &mdash; no model involved in the switching itself.'],
    ['<b>The shelf</b><br/><font size=8 color="#5A6772">the nine coloured chips</font>',
     'Holds every model the app might want, already downloaded, ready to run.',
     'Three model files per job, bundled with the app and refreshed from the cloud. Under 2 MB '
     'for the whole offer ladder. They are loaded lazily and the unused ones are dropped from '
     'memory.'],
    ['<b>The notebook</b><br/><font size=8 color="#5A6772">the small box on the right</font>',
     'Makes the switching explainable. If we cannot say why a switch happened, we treat that as a '
     'bug.',
     'A local append-only log: timestamp, job, level before, level after, the rule that fired, '
     'and the four readings at that instant. Uploaded in aggregate, kept on the phone in full.'],
    ['<b>The floor</b><br/><font size=8 color="#5A6772">the green box, bottom right</font>',
     'The promise that the screen is never empty.',
     'Not really a component &mdash; it is a constraint the switcher is written to obey and the '
     'tests check. The Light models are built to need nothing: no network, no history, no '
     'meaningful battery, no modern chip.'],
    ['<b>The cloud</b><br/><font size=8 color="#5A6772">the dashed box at the top</font>',
     'Makes the models better over time using what everyone did, without knowing what any one '
     'person did.',
     'A daily batch job. It aggregates events into counts, retrains the three levels, and ships a '
     'bundle. It is never called during a decision, so its latency and availability do not affect '
     'the commuter at all.'],
], [36*mm, 52*mm, CW-88*mm], fs=9.2,
  caption='Note which way the arrows run. Nothing in the bottom half of the picture ever waits on '
          'anything in the top half.')

F += [PageBreak()]

# ===================== 3 =====================
F += [H1('3&nbsp;&nbsp;What comes from the cloud')]
F += [P('This is the part people ask about most, so it is worth being precise. The cloud '
        'contributes real value, and it does so without ever needing to know who anybody is.',
        'big')]

F += [H2('Going up: what the phone sends')]
F += TBL(['What is sent', 'What it looks like', 'What it is used for'], [
    ['<b>Offer outcome counts</b>',
     'Bucketed tallies: <i>time-of-day band &times; area &times; offer category &rarr; shown '
     '1,412, taken 61.</i> No user identifier, no journey, no exact location.',
     'Rebuilding the popularity table that the <b>Light</b> models read from. This is what lets '
     'the simplest model still be sensible in a tunnel.'],
    ['<b>Content engagement counts</b>',
     'Same shape: <i>topic &times; article length band &times; time-of-day &rarr; opened, '
     'finished, skipped.</i>',
     'Retraining the Standard and Strong feed models.'],
    ['<b>The switch log, aggregated</b>',
     '<i>Rule 2 fired 18,004 times yesterday; median time spent at Light was 4m 10s; 0.3% of '
     'switches were reversed within a minute.</i>',
     'Checking the rules behave, and tuning the thresholds. This is about <b>our software</b>, '
     'not about people.'],
    ['<b>Health counters</b>',
     'Crashes, model load failures, decisions that timed out, blank-screen seconds.',
     'Catching problems. Also feeds directly into the metrics in Section 6.'],
], [38*mm, 58*mm, CW-96*mm], fs=9.2)

F += [H2('Coming down: what the phone receives')]
F += TBL(['What arrives', 'How big', 'How often'], [
    ['<b>The popularity table</b> &mdash; what people broadly like, by hour and area. The Light '
     'models are a lookup into this.', 'about 60 KB', 'Nightly'],
    ['<b>Refreshed model files</b> &mdash; new Light, Standard and Strong for both jobs.',
     'about 2 MB for offers; the Strong feed model is larger and only downloads on wifi',
     'Weekly, or when a retrain is worth shipping'],
    ['<b>Threshold updates</b> &mdash; the numbers inside the six rules.', 'well under 1 KB',
     'Rarely, and never mid-journey'],
], [CW-70*mm, 36*mm, 34*mm], fs=9.2,
  caption='All three arrive as one bundle, applied when the app is idle. A phone that has been '
          'offline for a fortnight runs on the bundle it already has, at slightly stale quality. '
          'Nothing breaks.')

F += BOX('What the cloud is deliberately not',
    'It is <b>not in the decision loop</b>. When the app picks an offer, it does not ask a server '
    '&mdash; that would defeat the whole point, because the moment we care most about is the one '
    'where there is no signal.<br/><br/>'
    'It does <b>not receive a per-person profile</b>. What goes up are counts that have already '
    'had the individual removed. Two people who did the same thing are indistinguishable in what '
    'we send, and a count of one is not sent at all.<br/><br/>'
    'It does <b>not send anything person-specific down</b>. The bundle that arrives on Lisa&rsquo;s '
    'phone is byte-for-byte the same one that arrives on John&rsquo;s. Everything personal about '
    'her recommendations is computed on her phone, from history that never left it.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))

# ===================== 4 =====================
F += [H1('4&nbsp;&nbsp;One decision, end to end')]
F += [P('Lisa&rsquo;s train enters the tunnel at 3:10. Here is the whole chain of events that '
        'follows, drawn to scale in time. It finishes before she could notice anything had '
        'happened.', 'big')]


def decision_timeline(cv):
    xs = [2, 35, 68, 101, 134]
    w = 30
    steps = [
        ('The train enters\nthe tunnel', 'The phone loses its data connection.', RULE, colors.white),
        ('The senses notice', 'Signal reading goes from "good" to "none".', RULE, colors.white),
        ('The switcher decides', 'Rule 1 fires. Cool-down checked: last switch was minutes ago, '
         'so the change is allowed.', E_STD, L_STD),
        ('The model swaps', 'Standard is unloaded, Light is loaded. This is the only cost that '
         'switching adds.', E_SMART, L_SMART),
        ('The feed refreshes', 'The Simple Feed sorts what is already on the phone. Lisa keeps '
         'scrolling.', E_BASIC, L_BASIC),
    ]
    for i, (t, b, e, f) in enumerate(steps):
        box(cv, xs[i], 22, w, 28, t.replace('\n', ' '), b, fill=f, edge=e, lw=1.0,
            tfs=7.4, bfs=6.0)
        if i:
            arrow(cv, xs[i]-3, 36, xs[i]-0.8, 36, col=NAVY, lw=1.0, head=1.8)

    # the time ruler
    cv.saveState()
    cv.setStrokeColor(RULE); cv.setLineWidth(0.6)
    cv.line(2*mm, 16*mm, 164*mm, 16*mm)
    cv.restoreState()
    ticks = [(17, 'about 2 seconds'), (50, 'under 1 ms'), (83, 'under 1 ms'),
             (116, 'about 40 ms'), (149, 'about 8 ms')]
    for x, t in ticks:
        cv.saveState(); cv.setStrokeColor(RULE); cv.setLineWidth(0.6)
        cv.line(x*mm, 16*mm, x*mm, 19*mm); cv.restoreState()
        label(cv, x, 12.2, t, fs=6.4, col=NAVY, align='c')
    note(cv, 2, 7.4, DW, 'The two-second wait at the start is deliberate: the app does not react to '
                        'a single missed packet, it waits to be sure the signal is really gone. '
                        'Everything after that is faster than a blink.',
         fs=6.4, col=MUTED, align='c')
    cv.saveState()
    cv.setStrokeColor(E_SMART); cv.setLineWidth(0.9); cv.setDash(2, 2)
    cv.line(101*mm, 52*mm, 131*mm, 52*mm); cv.restoreState()
    label(cv, 116, 53.6, 'THE ONLY STEP A SINGLE-MODEL APP DOES NOT HAVE', fs=6.2,
          col=E_SMART, align='c')


F += [Dia(60, decision_timeline)]
F += [Paragraph('Total, from losing signal to a working feed: roughly two seconds, almost all of '
                'it the deliberate wait. The actual switching work is about fifty milliseconds.',
                S['cap'])]

F += BOX('The step that costs us something',
    'Everything in this chain except the fourth box also happens in an app with one fixed model. '
    'The swap &mdash; unloading one model and loading another &mdash; is the <b>extra</b> work '
    'that switching introduces, and it is the thing that could in principle make switching a bad '
    'deal. If we swap a handful of times a journey it is trivially worth it. If the rules were '
    'badly tuned and it swapped every few seconds, the swapping could easily cost more energy '
    'than the cheaper models save.<br/><br/>'
    'That is why <b>switch overhead as a share of the energy saved</b> is one of the headline '
    'numbers in Section 6, and not an afterthought.',
    accent=TEAL)

F += [PageBreak()]
