# -*- coding: utf-8 -*-
"""Generates LearnPerk_Runtime_Model_Switching.pdf"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether,
                                NextPageTemplate, HRFlowable)
from reportlab.pdfbase import pdfmetrics

# ---------- palette ----------
INK    = colors.HexColor('#1A1A1A')
NAVY   = colors.HexColor('#12324A')
TEAL   = colors.HexColor('#0E6E6E')
AMBER  = colors.HexColor('#9A5B00')
RULE   = colors.HexColor('#C8CFD4')
BAND   = colors.HexColor('#EDF2F4')
BAND2  = colors.HexColor('#F7F9FA')
MUTED  = colors.HexColor('#5A6772')
CRIT   = colors.HexColor('#8A2A2A')

BODY_F = 'Times-Roman'; BODY_B = 'Times-Bold'; BODY_I = 'Times-Italic'
HEAD_F = 'Helvetica-Bold'; MONO_F = 'Courier'

S = {}
S['title'] = ParagraphStyle('title', fontName=HEAD_F, fontSize=25, leading=29,
                            textColor=NAVY, spaceAfter=4)
S['subtitle'] = ParagraphStyle('subtitle', fontName=BODY_I, fontSize=13.5, leading=17,
                               textColor=TEAL, spaceAfter=10)
S['meta'] = ParagraphStyle('meta', fontName=BODY_F, fontSize=9, leading=13,
                           textColor=MUTED)
S['h1'] = ParagraphStyle('h1', fontName=HEAD_F, fontSize=15.5, leading=19,
                         textColor=NAVY, spaceBefore=16, spaceAfter=7)
S['h2'] = ParagraphStyle('h2', fontName=HEAD_F, fontSize=11.5, leading=14.5,
                         textColor=TEAL, spaceBefore=12, spaceAfter=5)
S['h3'] = ParagraphStyle('h3', fontName=BODY_B, fontSize=10.5, leading=13.5,
                         textColor=INK, spaceBefore=9, spaceAfter=3)
S['p'] = ParagraphStyle('p', fontName=BODY_F, fontSize=9.7, leading=13.6,
                        textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
S['pt'] = ParagraphStyle('pt', parent=S['p'], spaceAfter=3)
S['bullet'] = ParagraphStyle('bullet', parent=S['p'], leftIndent=11, bulletIndent=2,
                             spaceAfter=3.5, alignment=TA_LEFT)
S['cell'] = ParagraphStyle('cell', fontName=BODY_F, fontSize=8.1, leading=10.4,
                           textColor=INK)
S['cellb'] = ParagraphStyle('cellb', parent=S['cell'], fontName=BODY_B)
S['cellm'] = ParagraphStyle('cellm', parent=S['cell'], fontName=MONO_F, fontSize=7.3,
                            leading=9.8)
S['hdr'] = ParagraphStyle('hdr', fontName=HEAD_F, fontSize=8.1, leading=10.4,
                          textColor=colors.white)
S['cap'] = ParagraphStyle('cap', fontName=BODY_I, fontSize=8.2, leading=11,
                          textColor=MUTED, spaceBefore=3, spaceAfter=9)
S['callout'] = ParagraphStyle('callout', fontName=BODY_F, fontSize=9.3, leading=12.8,
                              textColor=INK, alignment=TA_JUSTIFY)
S['calloutb'] = ParagraphStyle('calloutb', parent=S['callout'], fontName=BODY_B,
                               textColor=NAVY)
S['eq'] = ParagraphStyle('eq', fontName=MONO_F, fontSize=8.6, leading=12.6,
                         textColor=NAVY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4)
S['toc1'] = ParagraphStyle('toc1', fontName=BODY_B, fontSize=9.6, leading=13.6, textColor=NAVY, spaceBefore=3)
S['toc2'] = ParagraphStyle('toc2', fontName=BODY_F, fontSize=9.0, leading=12.1,
                           textColor=INK, leftIndent=13)

# ---------- helpers ----------
def P(t, s='p'): return Paragraph(t, S[s])
def H1(t): return Paragraph(t, S['h1'])
def H2(t): return Paragraph(t, S['h2'])
def H3(t): return Paragraph(t, S['h3'])
def SP(h=5): return Spacer(1, h)

def UL(items, style='bullet'):
    return [Paragraph(f'<bullet>&bull;</bullet>{i}', S[style]) for i in items]

def NL(items):
    return [Paragraph(f'<bullet>{n+1}.</bullet>&nbsp;{i}', S['bullet'])
            for n, i in enumerate(items)]

def c(t, st='cell'): return Paragraph(str(t), S[st])

def TBL(header, rows, widths, caption=None, hdr_bg=NAVY, zebra=True,
        align=None, fs=None, repeat=1):
    cs = S['cell']
    if fs:
        cs = ParagraphStyle('tmp%s' % fs, parent=S['cell'], fontSize=fs, leading=fs*1.28)
    data = []
    if header:
        data.append([Paragraph(str(h), S['hdr']) for h in header])
    for r in rows:
        row = []
        for v in r:
            if isinstance(v, Paragraph) or isinstance(v, Table):
                row.append(v)
            else:
                row.append(Paragraph(str(v), cs))
        data.append(row)
    t = Table(data, colWidths=widths, repeatRows=repeat if header else 0, hAlign='LEFT')
    st = [('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('LEFTPADDING', (0, 0), (-1, -1), 4.5),
          ('RIGHTPADDING', (0, 0), (-1, -1), 4.5),
          ('TOPPADDING', (0, 0), (-1, -1), 3.2),
          ('BOTTOMPADDING', (0, 0), (-1, -1), 3.6),
          ('GRID', (0, 0), (-1, -1), 0.3, RULE)]
    if header:
        st += [('BACKGROUND', (0, 0), (-1, 0), hdr_bg),
               ('TOPPADDING', (0, 0), (-1, 0), 4),
               ('BOTTOMPADDING', (0, 0), (-1, 0), 4.5)]
        off = 1
    else:
        off = 0
    if zebra:
        for i in range(len(rows)):
            if i % 2 == 1:
                st.append(('BACKGROUND', (0, i+off), (-1, i+off), BAND2))
    if align:
        for col, a in align.items():
            st.append(('ALIGN', (col, off), (col, -1), a))
    t.setStyle(TableStyle(st))
    out = [t]
    if caption:
        out.append(Paragraph(caption, S['cap']))
    else:
        out.append(SP(9))
    return out

def CALLOUT(title, body, accent=TEAL, bg=BAND):
    inner = []
    if title:
        inner.append(Paragraph(title, S['calloutb']))
        inner.append(Spacer(1, 2.5))
    if isinstance(body, str):
        body = [body]
    for b in body:
        if isinstance(b, str):
            inner.append(Paragraph(b, S['callout']))
        else:
            inner.append(b)
    t = Table([[inner]], colWidths=[168*mm], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('LINEBEFORE', (0, 0), (0, -1), 2.6, accent),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
    return [t, SP(9)]

def EQ(*lines):
    return [Paragraph(l, S['eq']) for l in lines]

def RULEF(col=RULE, w=0.8):
    return HRFlowable(width='100%', thickness=w, color=col,
                      spaceBefore=4, spaceAfter=8)

# ---------- document template ----------
PW, PH = A4
LM = RM = 21*mm; TM = 20*mm; BM = 19*mm
CW = PW - LM - RM

class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        BaseDocTemplate.__init__(self, fn, pagesize=A4,
                                 leftMargin=LM, rightMargin=RM,
                                 topMargin=TM, bottomMargin=BM, **kw)
        fr = Frame(LM, BM, CW, PH-TM-BM, id='n',
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[fr], onPage=self._cover),
            PageTemplate(id='body', frames=[fr], onPage=self._body)])

    def _cover(self, cv, doc):
        cv.saveState()
        cv.setFillColor(NAVY); cv.rect(0, PH-13*mm, PW, 13*mm, stroke=0, fill=1)
        cv.setFillColor(TEAL); cv.rect(0, PH-15.4*mm, PW, 2.4*mm, stroke=0, fill=1)
        cv.setFillColor(NAVY); cv.rect(0, 0, PW, 9*mm, stroke=0, fill=1)
        cv.setFillColor(colors.white); cv.setFont('Helvetica-Bold', 8)
        cv.drawString(LM, PH-8.6*mm, 'LEARNPERK')
        cv.setFont('Helvetica', 8)
        cv.drawRightString(PW-RM, PH-8.6*mm,
                           'EDGE AI  \u00b7  RUNTIME MODEL SWITCHING  \u00b7  V1.0')
        cv.setFont('Helvetica', 7.2)
        cv.drawCentredString(PW/2, 3.4*mm,
                             'INTERNAL \u2014 FOUNDERS, DEVELOPERS AND RESEARCH COLLABORATORS')
        cv.restoreState()

    def _body(self, cv, doc):
        cv.saveState()
        cv.setStrokeColor(RULE); cv.setLineWidth(0.5)
        cv.line(LM, PH-TM+6.5*mm, PW-RM, PH-TM+6.5*mm)
        cv.setFont('Helvetica', 7.3); cv.setFillColor(MUTED)
        cv.drawString(LM, PH-TM+8.6*mm, 'LearnPerk \u2014 Runtime Model Switching on the Edge Device')
        cv.drawRightString(PW-RM, PH-TM+8.6*mm, 'v1.0  \u00b7  September 2026')
        cv.line(LM, BM-6*mm, PW-RM, BM-6*mm)
        cv.setFont('Helvetica', 7.3)
        cv.drawString(LM, BM-10.4*mm, 'Internal')
        cv.setFont('Helvetica-Bold', 8)
        cv.setFillColor(NAVY)
        cv.drawRightString(PW-RM, BM-10.4*mm, str(doc.page))
        cv.restoreState()

F = []   # flowables
