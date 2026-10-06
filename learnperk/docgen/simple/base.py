# -*- coding: utf-8 -*-
"""Styles and helpers for the plain-English model switching doc."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak,
                                NextPageTemplate, HRFlowable, KeepTogether)

INK   = colors.HexColor('#1C1C1C')
NAVY  = colors.HexColor('#12324A')
TEAL  = colors.HexColor('#0E6E6E')
AMBER = colors.HexColor('#B06A00')
MUTED = colors.HexColor('#5A6772')
RULE  = colors.HexColor('#CBD3D8')
BAND  = colors.HexColor('#EDF2F4')
BAND2 = colors.HexColor('#F8FAFB')

# traffic-light colours for the three levels
L_BASIC = colors.HexColor('#E8F1DE')   # green-ish  = cheapest, always works
L_STD   = colors.HexColor('#FDF3DC')   # amber      = the normal one
L_SMART = colors.HexColor('#E4EDF6')   # blue       = the best one
L_OFF   = colors.HexColor('#F0F0F0')   # grey       = switched off

BODY = 'Times-Roman'; BOLD = 'Times-Bold'; ITAL = 'Times-Italic'
HEAD = 'Helvetica-Bold'; MONO = 'Courier'

S = {}
S['title']  = ParagraphStyle('t', fontName=HEAD, fontSize=27, leading=31, textColor=NAVY)
S['sub']    = ParagraphStyle('s', fontName=ITAL, fontSize=14, leading=18, textColor=TEAL,
                             spaceBefore=6)
S['h1']     = ParagraphStyle('h1', fontName=HEAD, fontSize=17, leading=21, textColor=NAVY,
                             spaceBefore=16, spaceAfter=9)
S['h2']     = ParagraphStyle('h2', fontName=HEAD, fontSize=12, leading=15, textColor=TEAL,
                             spaceBefore=13, spaceAfter=5)
S['p']      = ParagraphStyle('p', fontName=BODY, fontSize=11, leading=15.8, textColor=INK,
                             spaceAfter=8)
S['big']    = ParagraphStyle('big', fontName=BODY, fontSize=12.5, leading=18, textColor=INK,
                             spaceAfter=9)
S['bul']    = ParagraphStyle('b', parent=S['p'], leftIndent=13, bulletIndent=2, spaceAfter=5,
                             alignment=TA_LEFT)
S['cell']   = ParagraphStyle('c', fontName=BODY, fontSize=9.4, leading=12.4, textColor=INK)
S['cellb']  = ParagraphStyle('cb', parent=S['cell'], fontName=BOLD)
S['cellc']  = ParagraphStyle('cc', parent=S['cell'], alignment=TA_CENTER)
S['hdr']    = ParagraphStyle('h', fontName=HEAD, fontSize=9.4, leading=12.4,
                             textColor=colors.white)
S['cap']    = ParagraphStyle('cap', fontName=ITAL, fontSize=9, leading=12, textColor=MUTED,
                             spaceBefore=4, spaceAfter=11)
S['box']    = ParagraphStyle('bx', fontName=BODY, fontSize=10.5, leading=15, textColor=INK)
S['boxb']   = ParagraphStyle('bxb', parent=S['box'], fontName=BOLD, textColor=NAVY)
S['toc1']   = ParagraphStyle('t1', fontName=BOLD, fontSize=11, leading=17.5, textColor=NAVY)
S['tiny']   = ParagraphStyle('ty', fontName=BODY, fontSize=8.6, leading=11.4, textColor=MUTED)

PW, PH = A4
LM = RM = 22*mm; TM = 20*mm; BM = 19*mm
CW = PW - LM - RM


def P(t, s='p'):  return Paragraph(t, S[s])
def H1(t): return Paragraph(t, S['h1'])
def H2(t): return Paragraph(t, S['h2'])
def SP(h=6): return Spacer(1, h)
def UL(items, st='bul'):
    return [Paragraph('<bullet>&bull;</bullet>' + i, S[st]) for i in items]
def NL(items):
    return [Paragraph('<bullet>%d.</bullet>&nbsp;%s' % (n+1, i), S['bul'])
            for n, i in enumerate(items)]
def RULEF(col=RULE, w=0.8):
    return HRFlowable(width='100%', thickness=w, color=col, spaceBefore=5, spaceAfter=9)


def TBL(header, rows, widths, caption=None, fs=None, bg=None, hdr_bg=NAVY,
        zebra=True, centre=(), keep=False):
    cs = S['cell']
    if fs:
        cs = ParagraphStyle('x%s' % fs, parent=S['cell'], fontSize=fs, leading=fs*1.32)
    data = []
    if header:
        data.append([Paragraph(str(h), S['hdr']) for h in header])
    for r in rows:
        data.append([v if not isinstance(v, str) else Paragraph(v, cs) for v in r])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign='LEFT')
    off = 1 if header else 0
    st = [('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
          ('TOPPADDING', (0, 0), (-1, -1), 4.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
          ('GRID', (0, 0), (-1, -1), 0.4, RULE)]
    if header:
        st += [('BACKGROUND', (0, 0), (-1, 0), hdr_bg),
               ('TOPPADDING', (0, 0), (-1, 0), 5), ('BOTTOMPADDING', (0, 0), (-1, 0), 6)]
    if zebra and not bg:
        for i in range(len(rows)):
            if i % 2 == 1:
                st.append(('BACKGROUND', (0, i+off), (-1, i+off), BAND2))
    if bg:
        for i, col in enumerate(bg):
            if col is not None:
                st.append(('BACKGROUND', (0, i+off), (-1, i+off), col))
    for cidx in centre:
        st.append(('ALIGN', (cidx, off), (cidx, -1), 'CENTER'))
    t.setStyle(TableStyle(st))
    out = [t, Paragraph(caption, S['cap']) if caption else SP(11)]
    return [KeepTogether(out)] if keep else out


def BOX(title, body, accent=TEAL, bg=BAND, width=None):
    inner = []
    if title:
        inner += [Paragraph(title, S['boxb']), Spacer(1, 3)]
    if isinstance(body, str):
        body = [body]
    for b in body:
        inner.append(Paragraph(b, S['box']) if isinstance(b, str) else b)
    t = Table([[inner]], colWidths=[width or CW], hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), bg),
                           ('LINEBEFORE', (0, 0), (0, -1), 3, accent),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, -1), 9),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 9)]))
    return [t, SP(11)]


def LADDER(rows):
    """rows = [(colour, level, name, one-line description), ...] top = best."""
    data = []
    for col, lvl, name, desc in rows:
        cell = [Paragraph('<b>%s</b>' % name, S['cell']),
                Paragraph(desc, ParagraphStyle('ld', parent=S['cell'], fontSize=8.8,
                                               leading=11.6, textColor=MUTED))]
        data.append([Paragraph('<b>%s</b>' % lvl, S['cellc']), cell])
    t = Table(data, colWidths=[24*mm, CW-24*mm], hAlign='LEFT')
    st = [('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
          ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
          ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
          ('GRID', (0, 0), (-1, -1), 0.4, RULE)]
    for i, (col, _, _, _) in enumerate(rows):
        st.append(('BACKGROUND', (0, i), (-1, i), col))
    t.setStyle(TableStyle(st))
    return [t, SP(11)]


class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        BaseDocTemplate.__init__(self, fn, pagesize=A4, leftMargin=LM, rightMargin=RM,
                                 topMargin=TM, bottomMargin=BM, **kw)
        fr = Frame(LM, BM, CW, PH-TM-BM, id='n', leftPadding=0, rightPadding=0,
                   topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[fr], onPage=self._cover),
            PageTemplate(id='body', frames=[fr], onPage=self._body)])

    def _cover(self, cv, doc):
        cv.saveState()
        cv.setFillColor(NAVY); cv.rect(0, PH-14*mm, PW, 14*mm, stroke=0, fill=1)
        cv.setFillColor(TEAL); cv.rect(0, PH-16.6*mm, PW, 2.6*mm, stroke=0, fill=1)
        cv.setFillColor(NAVY); cv.rect(0, 0, PW, 9*mm, stroke=0, fill=1)
        cv.setFillColor(colors.white)
        cv.setFont('Helvetica-Bold', 8.5); cv.drawString(LM, PH-9.2*mm, 'LEARNPERK')
        cv.setFont('Helvetica', 8.5)
        cv.drawRightString(PW-RM, PH-9.2*mm, 'MODEL SWITCHING  ·  PLAIN-ENGLISH GUIDE')
        cv.setFont('Helvetica', 7.4)
        cv.drawCentredString(PW/2, 3.4*mm, 'INTERNAL — FOR EVERYONE ON THE TEAM')
        cv.restoreState()

    def _body(self, cv, doc):
        cv.saveState()
        cv.setStrokeColor(RULE); cv.setLineWidth(0.5)
        cv.line(LM, PH-TM+6.5*mm, PW-RM, PH-TM+6.5*mm)
        cv.setFont('Helvetica', 7.6); cv.setFillColor(MUTED)
        cv.drawString(LM, PH-TM+8.8*mm, 'LearnPerk — Model Switching on the Phone')
        cv.drawRightString(PW-RM, PH-TM+8.8*mm, 'Plain-English guide  ·  v1.0')
        cv.line(LM, BM-6*mm, PW-RM, BM-6*mm)
        cv.setFont('Helvetica', 7.6); cv.drawString(LM, BM-10.4*mm, 'Internal')
        cv.setFont('Helvetica-Bold', 8.5); cv.setFillColor(NAVY)
        cv.drawRightString(PW-RM, BM-10.4*mm, str(doc.page))
        cv.restoreState()

F = []
