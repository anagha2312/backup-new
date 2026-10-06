# -*- coding: utf-8 -*-
"""Styles, diagram primitives and page furniture for the architecture +
metrics guide. Same visual language as the plain-English switching guide."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, Flowable,
                                NextPageTemplate, HRFlowable, KeepTogether)

INK   = colors.HexColor('#1C1C1C')
NAVY  = colors.HexColor('#12324A')
TEAL  = colors.HexColor('#0E6E6E')
AMBER = colors.HexColor('#B06A00')
MUTED = colors.HexColor('#5A6772')
RULE  = colors.HexColor('#CBD3D8')
BAND  = colors.HexColor('#EDF2F4')
BAND2 = colors.HexColor('#F8FAFB')

L_BASIC = colors.HexColor('#E8F1DE')
L_STD   = colors.HexColor('#FDF3DC')
L_SMART = colors.HexColor('#E4EDF6')
L_OFF   = colors.HexColor('#F0F0F0')

# strong edge colours for the three levels (used on diagrams)
E_BASIC = colors.HexColor('#4E7A33')
E_STD   = colors.HexColor('#A8761B')
E_SMART = colors.HexColor('#2E5F8A')
E_OFF   = colors.HexColor('#9AA3AA')

# validated 2-series categorical pair for the trade-off chart
# (blue vs orange: OKLab dE 33.6 normal / 24.7 protan / 31.7 deutan)
SER1 = colors.HexColor('#2a78d6')   # switching  - the subject
SER2 = colors.HexColor('#eb6834')   # the fixed single-model baselines

CLOUDBG = colors.HexColor('#EEF3F8')
PHONEBG = colors.HexColor('#FAFBFC')

BODY = 'Times-Roman'; BOLD = 'Times-Bold'; ITAL = 'Times-Italic'
HEAD = 'Helvetica-Bold'; SANS = 'Helvetica'

S = {}
S['title']  = ParagraphStyle('t', fontName=HEAD, fontSize=25, leading=29, textColor=NAVY)
S['sub']    = ParagraphStyle('s', fontName=ITAL, fontSize=13.5, leading=18, textColor=TEAL,
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
DW = CW / mm                      # usable width in millimetres (~166)


def P(t, s='p'):  return Paragraph(t, S[s])
def H1(t): return Paragraph(t, S['h1'])
def H2(t): return Paragraph(t, S['h2'])
def SP(h=6): return Spacer(1, h)
def UL(items, st='bul'):
    return [Paragraph('<bullet>&bull;</bullet>' + i, S[st]) for i in items]
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


# ======================================================================
#  Diagram primitives.  Everything below works in millimetres, with the
#  origin at the bottom-left of the drawing area.
# ======================================================================

class Dia(Flowable):
    """A hand-drawn diagram. `fn(cv)` draws it; all helpers take mm."""
    def __init__(self, h_mm, fn, w_mm=None):
        Flowable.__init__(self)
        self.width = (w_mm or DW) * mm
        self.height = h_mm * mm
        self.fn = fn

    def draw(self):
        self.fn(self.canv)


def wrap(cv, text, font, size, maxw_mm):
    """Greedy wrap. maxw in mm, returns a list of lines."""
    maxw = maxw_mm * mm
    out = []
    for para in text.split('\n'):
        words, cur = para.split(), ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if cv.stringWidth(t, font, size) <= maxw or not cur:
                cur = t
            else:
                out.append(cur); cur = w
        out.append(cur)
    return out


def _text_block(cv, x, y, w, lines, font, size, lead, col, align):
    cv.setFont(font, size); cv.setFillColor(col)
    for i, ln in enumerate(lines):
        yy = (y - i * lead) * mm
        if align == 'c':
            cv.drawCentredString((x + w / 2) * mm, yy, ln)
        elif align == 'r':
            cv.drawRightString((x + w) * mm, yy, ln)
        else:
            cv.drawString(x * mm, yy, ln)


def box(cv, x, y, w, h, title=None, body=None, fill=colors.white, edge=RULE,
        tfs=7.4, bfs=6.3, tcol=NAVY, bcol=MUTED, lw=0.8, r=1.5, align='c',
        pad=2.4, dash=None, tfont=HEAD, bfont=SANS):
    """Rounded box with an optional bold title and wrapped body text."""
    cv.saveState()
    if dash:
        cv.setDash(dash)
    cv.setLineWidth(lw); cv.setStrokeColor(edge); cv.setFillColor(fill)
    cv.roundRect(x*mm, y*mm, w*mm, h*mm, r*mm, stroke=1, fill=1)
    cv.setDash()
    inner = w - 2 * pad
    tl = wrap(cv, title, tfont, tfs, inner) if title else []
    bl = wrap(cv, body, bfont, bfs, inner) if body else []
    tlead, blead = tfs * 1.22 / mm, bfs * 1.24 / mm
    total = len(tl) * tlead + (1.1 if tl and bl else 0) + len(bl) * blead
    cur = y + h / 2 + total / 2 - tfs * 0.78 / mm
    if tl:
        _text_block(cv, x + pad, cur, inner, tl, tfont, tfs, tlead, tcol, align)
        cur -= len(tl) * tlead + (1.1 if bl else 0)
        cur += (tfs * 0.78 - bfs * 0.78) / mm
    if bl:
        _text_block(cv, x + pad, cur, inner, bl, bfont, bfs, blead, bcol, align)
    cv.restoreState()


def label(cv, x, y, text, fs=6.8, col=TEAL, font=HEAD, align='l'):
    cv.saveState(); cv.setFont(font, fs); cv.setFillColor(col)
    if align == 'c':
        cv.drawCentredString(x*mm, y*mm, text)
    elif align == 'r':
        cv.drawRightString(x*mm, y*mm, text)
    else:
        cv.drawString(x*mm, y*mm, text)
    cv.restoreState()


def note(cv, x, y, w, text, fs=6.2, col=MUTED, font=SANS, align='l', lead=None):
    """Wrapped small text starting at the given baseline, running downward."""
    cv.saveState()
    lines = wrap(cv, text, font, fs, w)
    _text_block(cv, x, y, w, lines, font, fs, lead or fs * 1.3 / mm, col, align)
    cv.restoreState()
    return len(lines)


def arrow(cv, x1, y1, x2, y2, col=NAVY, lw=1.1, head=2.0, dash=None):
    import math
    cv.saveState()
    cv.setLineWidth(lw); cv.setStrokeColor(col); cv.setFillColor(col)
    if dash:
        cv.setDash(dash)
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * 0.92 * math.cos(ang), y2 - head * 0.92 * math.sin(ang)
    cv.line(x1*mm, y1*mm, bx*mm, by*mm)
    cv.setDash()
    p = cv.beginPath()
    p.moveTo(x2*mm, y2*mm)
    for s in (+1, -1):
        p.lineTo((x2 - head*math.cos(ang) + s*head*0.42*math.sin(ang))*mm,
                 (y2 - head*math.sin(ang) - s*head*0.42*math.cos(ang))*mm)
    p.close()
    cv.drawPath(p, stroke=0, fill=1)
    cv.restoreState()


def segbar(cv, x, y, w, h, segs, r=1.0, fs=6.0):
    """segs = [(fraction, fill, edge, text, textcolour), ...] summing to 1."""
    cx = x
    for frac, fill, edge, txt, tc in segs:
        sw = w * frac
        cv.saveState()
        cv.setLineWidth(0.7); cv.setStrokeColor(edge); cv.setFillColor(fill)
        cv.roundRect(cx*mm, y*mm, sw*mm, h*mm, r*mm, stroke=1, fill=1)
        if txt:
            cv.setFont(HEAD, fs); cv.setFillColor(tc)
            if cv.stringWidth(txt, HEAD, fs) < (sw - 1.5) * mm:
                cv.drawCentredString((cx + sw/2)*mm, (y + h/2)*mm - fs*0.36, txt)
        cv.restoreState()
        cx += sw


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
        cv.setFont(HEAD, 8.5); cv.drawString(LM, PH-9.2*mm, 'LEARNPERK')
        cv.setFont(SANS, 8.5)
        cv.drawRightString(PW-RM, PH-9.2*mm, 'ARCHITECTURE  ·  HOW WE MEASURE IT')
        cv.setFont(SANS, 7.4)
        cv.drawCentredString(PW/2, 3.4*mm, 'INTERNAL — FOR EVERYONE ON THE TEAM')
        cv.restoreState()

    def _body(self, cv, doc):
        cv.saveState()
        cv.setStrokeColor(RULE); cv.setLineWidth(0.5)
        cv.line(LM, PH-TM+6.5*mm, PW-RM, PH-TM+6.5*mm)
        cv.setFont(SANS, 7.6); cv.setFillColor(MUTED)
        cv.drawString(LM, PH-TM+8.8*mm, 'LearnPerk — How it fits together, and how we will know it works')
        cv.drawRightString(PW-RM, PH-TM+8.8*mm, 'v1.0')
        cv.line(LM, BM-6*mm, PW-RM, BM-6*mm)
        cv.setFont(SANS, 7.6); cv.drawString(LM, BM-10.4*mm, 'Internal')
        cv.setFont(HEAD, 8.5); cv.setFillColor(NAVY)
        cv.drawRightString(PW-RM, BM-10.4*mm, str(doc.page))
        cv.restoreState()

F = []
