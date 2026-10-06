# -*- coding: utf-8 -*-
from base import *

# ===================== COVER =====================
F += [SP(40)]
F += [P('Model Switching on the Phone', 'title')]
F += [P('What we are building, explained without jargon', 'sub')]
F += [RULEF(TEAL, 1.8)]
F += [SP(4)]

F += [SP(14)]
F += [P('Prepared by Anagha', 'big')]

F += [NextPageTemplate('body'), PageBreak()]

# ===================== CONTENTS =====================
F += [H1('What is in this document')]
for n, t, d in [
    ('1', 'The idea, using gears',
     'A car changes gear for the hill it is on. Same idea.'),
    ('2', 'What the app is deciding',
     'Three jobs the app does during a journey.'),
    ('3', 'The three levels',
     'Light, Standard and Strong &mdash; and what each one is good for.'),
    ('4', 'The four things the phone looks at',
     'Signal, battery, time left, and how well we know you.'),
    ('5', 'The switching rules',
     'Six plain if-this-then-that rules. This is the heart of it.'),
    ('6', 'One journey, start to finish',
     'Fourteen minutes on the metro, minute by minute.'),
    ('7', 'Three more moments',
     'A low battery, a delayed train, and a brand-new user.'),
]:
    F.append(Paragraph('%s&nbsp;&nbsp;&nbsp;%s' % (n, t), S['toc1']))
    F.append(Paragraph('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + d, S['tiny']))
    F.append(SP(4))

F += [SP(8)]
F += BOX('One thing to keep in mind while reading',
    'Nothing here changes what the commuter sees on screen. An offer still looks like an offer. '
    'All that changes is <b>which piece of software chose it</b>, and the app makes that choice '
    'sensibly instead of always using the same one.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))

F += [PageBreak()]

# ===================== 1 =====================
F += [H1('1&nbsp;&nbsp;The idea, using gears')]
F += [P('A car has more than one gear. Low gear for pulling away and climbing hills: lots of power, '
        'but noisy and thirsty. High gear for the motorway: quiet and efficient, but useless on a '
        'steep hill. Nobody thinks a car should have one gear and stay in it.', 'big')]
F += [P('A phone running an app is in the same situation, and the &ldquo;hill&rdquo; keeps '
        'changing during a single journey. The train goes into a tunnel and the internet '
        'disappears. The battery drops. The commuter is two minutes from getting off. Each of those '
        'calls for something different from the app.')]
F += [P('So instead of one model doing every job in every situation, we put a small set of models '
        'on the phone and let the app change gear.')]

F += [SP(3)]
F += TBL(['', 'A car', 'The LearnPerk app'], [
    ['<b>What changes around it</b>', 'Hills, traffic, motorway',
     'Signal, battery, how much journey is left'],
    ['<b>What it switches between</b>', 'Low gear, middle gears, top gear',
     'Light model, Standard model, Strong model'],
    ['<b>Who decides</b>', 'The driver, or the automatic gearbox',
     'The app decides by itself, a few times a minute'],
    ['<b>What the passenger notices</b>', 'Almost nothing. The car just keeps going.',
     'Almost nothing. The app just keeps working.'],
], [42*mm, (CW-42*mm)/2, (CW-42*mm)/2], fs=9.6,
  caption='The comparison is not perfect, but it holds where it matters: you switch because the '
          'situation changed, and the passenger should not have to think about it.')

F += BOX('Why not just always use the strongest model?',
    'Because the strongest model needs things that are not always there. Some need the internet, '
    'and the metro spends a lot of its time in tunnels. Some need a decent amount of battery. Some '
    'need to know quite a lot about the person, which we do not on their first day. When those '
    'things are missing, the strong model does not give a slightly worse answer &mdash; it gives '
    '<b>no answer at all</b>, and the commuter sees an empty screen.',
    accent=TEAL)
F += [PageBreak()]

# ===================== 2 =====================
F += [H1('2&nbsp;&nbsp;What the app is deciding')]
F += [P('During a journey the app is quietly making three kinds of decision. Each one is made by '
        'its own model, and each one can switch independently of the others.', 'big')]

F += TBL(['The job', 'The question it answers', 'How often'], [
    ['<b>1.&nbsp;&nbsp;Choosing offers</b>',
     'Of all the deals available near this person right now, which one do we show, and in what '
     'order? This is the one that makes money, so it is the one we care most about.',
     'A few times per journey'],
    ['<b>2.&nbsp;&nbsp;Choosing content</b>',
     'Which article or video goes at the top of the feed? Something short if the journey is nearly '
     'over, something in a topic they actually read.',
     'Every time the feed refreshes'],
    ['<b>3.&nbsp;&nbsp;Answering questions</b>',
     'The commuter types <i>&ldquo;why is my tram delayed?&rdquo;</i> and the app answers. This one '
     'is the most expensive to run, so it is the first thing we turn down.',
     'Only when someone asks'],
], [38*mm, CW-78*mm, 40*mm], fs=9.6,
  caption='Three jobs, three separate sets of models. The app can be running a Strong model for '
          'offers and a Light one for content at the same moment &mdash; that is fine and often '
          'correct.')

F += BOX('A note on scope',
    'For the first build we are doing switching on <b>jobs 1 and 2 only</b> &mdash; offers and '
    'content. Job 3, the question-answering, uses much bigger models and is a bigger piece of work. '
    'It comes after.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))
F += [PageBreak()]

# ===================== 3 =====================
F += [H1('3&nbsp;&nbsp;The three levels')]
F += [P('For each job we keep three models on the phone. They all do the same job. They differ in '
        'how much they need and how good they are.', 'big')]

F += [H2('Choosing offers')]
F += LADDER([
    (L_SMART, 'Strong', 'The Smart Picker',
     'Uses everything we know about this person, including how far they will walk out of their '
     'way and how close they are to their next reward. The best answers &mdash; when it can run.'),
    (L_STD, 'Standard', 'The Everyday Picker',
     'The one that runs most of the time. Knows this person reasonably well, works without the '
     'internet, and is quick on any phone. This is the default.'),
    (L_BASIC, 'Light', 'The Simple Picker',
     'A small lookup: people like you, at this time of day, tend to take offers like this. '
     'Barely personal, but it is instant, needs nothing, and always works.'),
])

F += [H2('Choosing content')]
F += LADDER([
    (L_SMART, 'Strong', 'The Smart Feed',
     'Reads the actual text of articles to find ones close to what this person likes, even for '
     'articles nobody has opened yet.'),
    (L_STD, 'Standard', 'The Everyday Feed',
     'Learns from what they have opened, how long they stayed, and what they skipped. The default '
     'when there is internet.'),
    (L_BASIC, 'Light', 'The Simple Feed',
     'Sorts whatever is already saved on the phone by the topics they chose when they signed up, '
     'and by whether it is short enough to finish before they get off.'),
])

F += BOX('The important one is the Light level',
    'It is tempting to think of the Light models as the sad fallback. They are the opposite: they '
    'are the reason the app never goes blank. They work in a tunnel, on a five-year-old phone, at '
    '9% battery, on someone&rsquo;s first day. Whatever else fails, one of these can always run, '
    'and that is a rule we are building in deliberately.',
    accent=TEAL)

F += [SP(2)]
F += [P('<b>For the developers reading this</b>, the plain names above map to real things:', 'p')]
F += TBL(['Plain name', 'What it actually is', 'Rough size'], [
    ['The Simple Picker', 'A pre-computed lookup table, refreshed overnight', 'about 60 KB'],
    ['The Everyday Picker', 'A small gradient-boosted model, quantised', 'about 180 KB'],
    ['The Smart Picker', 'A larger gradient-boosted model with more features', 'about 1.4 MB'],
    ['The Simple Feed', 'Sort by declared interest and article length', 'about 4 KB'],
    ['The Everyday Feed', 'A gradient-boosted model over reading history', 'about 220 KB'],
    ['The Smart Feed', 'Sentence embeddings plus nearest-neighbour search', 'about 23 MB'],
], [42*mm, CW-82*mm, 40*mm], fs=9.2, keep=True,
  caption='Sizes are rough targets to give a sense of scale, not measured figures. Note the whole '
          'offer ladder together is under 2 MB &mdash; smaller than a single photo.')
F += [PageBreak()]
