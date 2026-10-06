# -*- coding: utf-8 -*-
from base import *

# ===================== 4 =====================
F += [H1('4&nbsp;&nbsp;The four things the phone looks at')]
F += [P('To switch sensibly the app has to notice what is going on. It checks four things, every '
        'few seconds, and all four are things the phone already knows &mdash; we are not asking '
        'the commuter anything or collecting anything new.', 'big')]

F += TBL(['', 'What it is', 'What it tells us'], [
    ['<b>1.&nbsp;&nbsp;Signal</b>',
     'Is there internet right now? Full, patchy, or none at all.',
     'This is the big one on the metro. Underground there is often no signal, so anything that '
     'needs the internet simply cannot run.'],
    ['<b>2.&nbsp;&nbsp;Battery</b>',
     'How much charge is left, and how fast it is draining.',
     'Below roughly a quarter charge, people start closing apps to save their phone. We would '
     'rather step down and stay useful than run hot and get shut off.'],
    ['<b>3.&nbsp;&nbsp;Time left</b>',
     'Roughly how many minutes until they get off this train.',
     'A typical leg is about twelve minutes. With two minutes to go there is no point loading a '
     'long article or spending time picking the perfect offer.'],
    ['<b>4.&nbsp;&nbsp;How well we know them</b>',
     'Are they a regular with months of history, or did they sign up on Tuesday?',
     'The Strong models need history to be any good. For a brand-new user there is nothing to work '
     'from, so a simpler model is genuinely the better answer.'],
], [40*mm, 54*mm, CW-94*mm], fs=9.6,
  caption='Four checks. The app also keeps an eye on how hard the phone is working and how old the '
          'phone is, but those mostly just rule out the Strong level on older devices.')

F += BOX('Nothing new is being collected',
    'All four of these already exist. Signal strength, battery level and journey time are things '
    'the phone and the GVB feed report anyway. &ldquo;How well we know them&rdquo; is just a count '
    'of things that already happened. The only genuinely new record is a small note saying '
    '<i>which model was used, and why we switched</i> &mdash; and that is information about our '
    'software, not about the person.',
    accent=TEAL)
F += [PageBreak()]

# ===================== 5 =====================
F += [H1('5&nbsp;&nbsp;The switching rules')]
F += [P('This is the heart of the document. Six rules, in plain if-this-then-that form. They are '
        'checked in the order below, and the first one that applies wins.', 'big')]

F += TBL(['#', 'If this is true…', '…then use', 'The plain reason'], [
    ['1', '<b>No signal.</b> The phone has lost the internet &mdash; usually a tunnel.',
     '<b>Light</b> for offers.<br/><b>Light</b> for content.',
     'Anything that reaches out to the internet cannot work. The Light models were built to run '
     'entirely on the phone, so they carry on as normal.'],
    ['2', '<b>Battery is low.</b> Under about a quarter, or draining unusually fast.',
     '<b>Light</b> for offers.<br/><b>Light</b> for content.<br/>Stop loading content in advance.',
     'People close apps that eat their battery. Stepping down keeps the app alive for the rest of '
     'the journey instead of being shut off halfway.'],
    ['3', '<b>Almost there.</b> Less than about two minutes of journey left.',
     '<b>Light</b> for offers.<br/><b>Content switched off.</b>',
     'Nobody starts a five-minute article with two minutes to go. Offers still make sense if they '
     'can be used quickly, so those keep running.'],
    ['4', '<b>We hardly know them.</b> New account, or almost no history yet.',
     '<b>Light</b> for offers.<br/><b>Light</b> for content.',
     'The stronger models work by spotting patterns in what someone has done before. With nothing '
     'to look at they do not give a careful answer, they give a random one. The simple one is '
     'honestly better here.'],
    ['5', '<b>Old or slow phone.</b> Lower-end device.',
     '<b>Never Strong.</b> Light or Standard only.',
     'The Strong models run badly on older hardware &mdash; slow enough that the commuter would '
     'notice. Roughly three in ten phones are in this group, so this is not an edge case.'],
    ['6', '<b>Everything is fine, and there is time.</b> Good signal, healthy battery, decent '
     'phone, more than ten minutes left, screen actually on.',
     '<b>Strong</b> for offers.<br/><b>Strong</b> for content.',
     'This is the moment worth spending on. Often it is a delayed train: the person is stuck, '
     'looking at their phone, with time to act on a good offer.'],
], [7*mm, 46*mm, 34*mm, CW-87*mm], fs=9.2,
  bg=[L_BASIC, L_BASIC, L_BASIC, L_BASIC, L_OFF, L_SMART],
  caption='Six rules, colour-coded by where they land: green steps down to Light, grey rules out '
          'the top level, blue steps up to Strong. If none of them applies, the app uses '
          '<b>Standard</b>, which is the normal state and where it spends most of its time.')

F += [H2('Two things the rules do on purpose')]
F += [P('<b>They do not only step down.</b> Rule 6 steps <i>up</i>. A switching system that only '
        'ever makes things smaller is just a brake, and it would miss the best moments. A delayed '
        'train with a charged phone is the most valuable situation LearnPerk gets, and the rules '
        'should spend more there, not less.')]
F += [P('<b>They do not flip back and forth.</b> If the battery hovers right on the line, we do '
        'not want the app switching every few seconds. So once a model is chosen it stays for a '
        'short minimum time, and the situation has to change clearly &mdash; not marginally &mdash; '
        'before we switch again. In practice this means a handful of switches per journey, not '
        'hundreds.')]

F += BOX('The one rule underneath all the others',
    'There must <b>always</b> be something that can run. Whatever the combination of no signal, '
    'low battery, old phone and new user, the Light model is built so that it can never be ruled '
    'out. The app is never allowed to end up with nothing to show.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))
F += [PageBreak()]

# ===================== 6 =====================
F += [H1('6&nbsp;&nbsp;One journey, start to finish')]
F += [P('Lisa takes the metro from Zuid to Centraal. Fourteen minutes, a normal Tuesday morning, '
        'phone at 56%. Here is what the app does, minute by minute. She notices none of it.', 'big')]

def leg(t, what, offers, content, why, col):
    return [t, what, offers, content, why]

F += TBL(['Time', 'What is happening', 'Offers', 'Content', 'Why it switched'], [
    ['<b>0:00</b>', 'On the platform, waiting. Good signal, plenty of battery, twelve-plus minutes '
     'ahead of her.', '<b>Standard</b>', '<b>Standard</b>',
     'Nothing unusual, so the app sits in its normal state.'],
    ['<b>3:10</b>', 'The train goes into the tunnel. <b>Signal drops to nothing.</b>',
     '<b>Light</b>', '<b>Light</b>',
     '<b>Rule 1.</b> No internet. Both jobs drop to the models that run entirely on the phone.'],
    ['<b>3:10</b>', 'Same moment, from Lisa&rsquo;s side: the feed keeps working and offers keep '
     'appearing.', '&mdash;', '&mdash;',
     'This is the point. Today she would see an empty feed for the whole tunnel. With switching, '
     'she does not.'],
    ['<b>10:40</b>', 'Out of the tunnel. <b>Signal comes back.</b>', '<b>Standard</b>',
     '<b>Standard</b>',
     'Conditions are normal again, so the app returns to its normal state. It waits a few seconds '
     'first to be sure the signal is really back.'],
    ['<b>12:30</b>', 'Approaching Centraal. Under two minutes left.', '<b>Light</b>',
     '<b>Off</b>',
     '<b>Rule 3.</b> No time to read anything, so content stops. A quick offer she could use at '
     'the station still makes sense.'],
    ['<b>14:00</b>', 'She gets off.', '&mdash;', '&mdash;', 'Journey over. Everything resets.'],
], [14*mm, 52*mm, 20*mm, 20*mm, CW-106*mm], fs=9.2,
  bg=[L_STD, L_BASIC, None, L_STD, L_BASIC, None],
  centre=(2, 3),
  caption='Three switching moments across a fourteen-minute journey. The commuter sees a working app '
          'throughout, which is the only thing she should notice.')

F += BOX('What to take from this one',
    'The interesting moment is 3:10. Today, going into that tunnel means the content feed goes '
    'blank until she comes out &mdash; roughly seven minutes of a fourteen-minute trip. The '
    'switching does not make the feed <i>better</i> there, it makes it <i>exist</i>. That is the '
    'clearest single thing this project does.',
    accent=TEAL)
F += [PageBreak()]

# ===================== 7 =====================
F += [H1('7&nbsp;&nbsp;Three more moments')]
F += [P('The same six rules, in three other situations, to show they pull in different directions.',
        'big')]

F += [H2('John, 18% battery, on his way home')]
F += TBL(None, [
    ['<b>The situation</b>', 'Evening metro. Older phone, 18% charge and dropping quickly. '
     'Fourteen minutes to go.'],
    ['<b>What switches</b>', 'Offers step down to <b>Light</b>. Content steps down to <b>Light</b>, '
     'and loading articles in advance stops.'],
    ['<b>Which rule</b>', '<b>Rule 2</b>, the battery rule. <b>Rule 5</b> had already ruled out the '
     'Strong level on his phone anyway.'],
    ['<b>The point</b>', 'John is close to the level where people start shutting apps down. The '
     'app spending less here is what keeps it open for the rest of his journey.'],
], [30*mm, CW-30*mm], zebra=False, fs=9.6, bg=[L_BASIC]*4)

F += [H2('Sanne, stuck on a delayed tram')]
F += TBL(None, [
    ['<b>The situation</b>', 'Peak hour. The tram is eleven minutes late and packed. She is '
     'standing, phone in hand, 74% battery, good phone, about twenty-two minutes still to go.'],
    ['<b>What switches</b>', 'Offers step <b>up</b> to <b>Strong</b>. Content steps <b>up</b> to '
     '<b>Strong</b>.'],
    ['<b>Which rule</b>', '<b>Rule 6.</b> Everything it asks for is true at once, which does not '
     'happen often.'],
    ['<b>The point</b>', 'This is the opposite of the other examples, and it is deliberate. She is '
     'stuck, attentive and has time to act. If we are ever going to use the best model, it is now. '
     'The app goes back to Standard after a few minutes so this does not run all day.'],
], [30*mm, CW-30*mm], zebra=False, fs=9.6, bg=[L_SMART]*4)

F += [H2('Daan, who signed up nine days ago')]
F += TBL(None, [
    ['<b>The situation</b>', 'Bus across town, sixteen minutes, good signal, 63% battery, decent '
     'phone. Nothing is under any pressure at all.'],
    ['<b>What switches</b>', 'Offers step down to <b>Light</b>. Content steps down to <b>Light</b>. '
     'As he uses the app more, they come back up on their own.'],
    ['<b>Which rule</b>', '<b>Rule 4.</b> Not because the phone cannot cope &mdash; it can &mdash; '
     'but because we do not know enough about him yet.'],
    ['<b>The point</b>', 'This is the example people find least obvious. Everything is fine and we '
     'still step down. A Strong model with nothing to learn from does not hedge; it makes a '
     'confident guess that happens to be wrong. For someone nine days in, one badly chosen offer '
     'is a good way to lose them.'],
], [30*mm, CW-30*mm], zebra=False, fs=9.6, bg=[L_BASIC]*4)

F += [SP(3)]
F += TBL(['', 'Lisa', 'John', 'Sanne', 'Daan'], [
    ['<b>What triggered it</b>', 'Tunnel', 'Low battery', 'Delay, and time to spare', 'Too new'],
    ['<b>Which way</b>', 'Down, then back up', 'Down', '<b>Up</b>', 'Down'],
    ['<b>Rule</b>', '1, then 3', '2 and 5', '6', '4'],
    ['<b>What it gets us</b>', 'A feed that is not blank', 'The app survives the trip',
     'The best answer at the best moment', 'No confident wrong guess'],
], [32*mm, (CW-32*mm)/4, (CW-32*mm)/4, (CW-32*mm)/4, (CW-32*mm)/4], fs=9.2,
  caption='Four people, four different outcomes, one set of rules. Three step down and one steps '
          'up &mdash; which is the balance we want.')
