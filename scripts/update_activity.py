#!/usr/bin/env python3
"""Render the public GitHub contribution calendar, without a PAT or dependencies.

Read only the public contributions page. A source/schema failure exits before
touching the last good assets. Counts come from GitHub's accessibility tooltips;
colors come from GitHub's contribution levels. Never substitute sample data.
"""
import argparse
from collections import defaultdict
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

from build_visuals import BLUE, CYAN, PURPLE, MUTED, WHITE, OUT, start, finish, text


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = []
        self.tips = {}
        self.tip_id = None
        self.tip_parts = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and 'data-date' in a and 'data-level' in a:
            self.cells.append(a)
        elif tag == 'tool-tip' and a.get('for', '').startswith('contribution-day-component-'):
            self.tip_id = a['for']
            self.tip_parts = []

    def handle_data(self, data):
        if self.tip_id is not None:
            self.tip_parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.tip_id is not None:
            self.tips[self.tip_id] = ''.join(self.tip_parts).strip()
            self.tip_id = None


def parse_calendar(html):
    parser = CalendarParser()
    parser.feed(html)
    days = []
    for cell in parser.cells:
        tip = parser.tips.get(cell.get('id', ''), '')
        match = re.match(r'^(No|[\d,]+) contributions?\b', tip)
        if not match:
            raise ValueError(f"Missing or changed contribution count for {cell.get('data-date')}")
        count = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
        day = date.fromisoformat(cell['data-date'])
        level = int(cell['data-level'])
        if not 0 <= level <= 4 or (count == 0) != (level == 0):
            raise ValueError('Contribution count/level mismatch')
        days.append({'date': day.isoformat(), 'count': count, 'level': level})
    days.sort(key=lambda d: d['date'])
    dates = [date.fromisoformat(d['date']) for d in days]
    if not 365 <= len(dates) <= 378 or len(set(dates)) != len(dates):
        raise ValueError('Expected one complete, unique annual calendar')
    if any(b - a != timedelta(days=1) for a, b in zip(dates, dates[1:])):
        raise ValueError('Contribution calendar has missing days')
    return days


def fetch_calendar(username):
    url = f'https://github.com/users/{username}/contributions'
    request = Request(url, headers={'User-Agent': 'Dinesh-757-profile-visuals', 'Accept': 'text/html', 'Accept-Language': 'en-US,en;q=0.9'})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                return parse_calendar(response.read().decode('utf-8'))
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def contribution_svg(username, days):
    first = date.fromisoformat(days[0]['date'])
    origin = first - timedelta(days=(first.weekday() + 1) % 7)
    total = sum(d['count'] for d in days)
    active = sum(d['count'] > 0 for d in days)
    colors = ['#132440', '#214586', '#396ac7', '#6d72e4', '#98dcff']
    desc = f'{username}: {total} contributions on {active} active days in GitHub’s displayed calendar, {days[0]["date"]} to {days[-1]["date"]}. A decorative scan moves over the real, unchanged calendar cells.'
    s = start(1200,347,'Contribution Current — '+username,desc,defs='<linearGradient id="sweep"><stop stop-color="#77e7ff" stop-opacity="0"/><stop offset="1" stop-color="#77e7ff" stop-opacity=".14"/></linearGradient><clipPath id="calendar"><rect x="102" y="130" width="1000" height="130"/></clipPath>')
    s += text(30,36,'PUBLIC TELEMETRY  /  CONTRIBUTION CURRENT',14,CYAN,'class="mono" letter-spacing="1"')
    s += text(31,84,f'{total:,}',42,WHITE,'font-weight="700"')
    s += text(167,80,'CONTRIBUTIONS',12,MUTED,'class="mono" letter-spacing="1"')
    s += text(378,80,str(active),30,PURPLE,'font-weight="700"')
    s += text(441,80,'ACTIVE DAYS',12,MUTED,'class="mono" letter-spacing="1"')
    s += text(1167,77,f'AS OF {days[-1]["date"]}',12,MUTED,'class="mono" text-anchor="end"')
    s += '<path d="M30 99H1170" stroke="#293d60"/>'
    months = set()
    coords = []
    for d in days:
        dt = date.fromisoformat(d['date'])
        index = (dt - origin).days
        week, weekday = divmod(index, 7)
        x, y = 106 + week * 18.4, 139 + weekday * 17
        key = (dt.year, dt.month)
        # Label only the first available date in each month and avoid clipping.
        if key not in months:
            months.add(key)
            if week < 51:
                s += text(round(x,1),126,dt.strftime('%b'),11,MUTED,'class="mono"')
        s += f'<rect x="{x:.1f}" y="{y}" width="14" height="13" rx="2.5" fill="{colors[d["level"]]}"><title>{d["date"]}: {d["count"]} contributions</title></rect>'
        if d['count']:
            coords.append((x+7,y+6.5))
    for i,label in [(1,'Mon'),(3,'Wed'),(5,'Fri')]:
        s += text(56,149+i*17,label,11,MUTED,'class="mono"')
    s += '<g clip-path="url(#calendar)"><rect class="scan" x="0" y="135" width="64" height="126" fill="url(#sweep)"/></g>'
    # A small orbiting spark above the grid does not alter the data encoding.
    s += '<path d="M108 269H1077" stroke="#2b4169"/><path class="current" d="M108 269H1077" stroke="#77e7ff" stroke-width="2"/>'
    s += text(106,302,f'{days[0]["date"]}  —  {days[-1]["date"]}',12,MUTED,'class="mono"')
    s += text(835,302,'LESS',10,MUTED,'class="mono"')
    for i,c in enumerate(colors): s += f'<rect x="{877+i*22}" y="290" width="16" height="14" rx="3" fill="{c}"/>'
    s += text(997,302,'MORE',10,MUTED,'class="mono"')
    s += text(600,331,'GITHUB PUBLIC PROFILE CALENDAR  /  REFRESHED DAILY',10,MUTED,'class="mono" text-anchor="middle" letter-spacing="1"')
    return s+finish(1200,347)


def pulse_svg(days):
    months = defaultdict(int)
    for d in days:
        months[d['date'][:7]] += d['count']
    entries = list(months.items())
    peak = max(months.values(), default=0)
    scale_max = max(10, ((peak+9)//10)*10)
    s=start(1200,250,'Monthly contribution pulse','Monthly sums of the displayed GitHub calendar. The first and last month may be partial. Language use and contribution counts are not measures of skill.')
    s+=text(30,33,'ACTIVITY PULSE  /  MONTHLY CONTRIBUTIONS',13,CYAN,'class="mono" letter-spacing="1"')
    x0, y0, width, height = 90, 178, 1035, 112
    for fraction in (0,.5,1):
        y=y0-height*fraction
        s+=f'<path d="M{x0} {y}H1128" stroke="#233553" stroke-dasharray="3 6"/>'+text(76,y+4,str(int(scale_max*fraction)),10,MUTED,'class="mono" text-anchor="end"')
    pts=[]
    for i,(m,count) in enumerate(entries):
        x=x0+i*width/max(1,len(entries)-1);y=y0-count/scale_max*height
        pts.append((x,y))
        label=date.fromisoformat(m+'-01').strftime('%b')
        s+=text(round(x,1),201,label,11,MUTED,'class="mono" text-anchor="middle"')
        s+=text(round(x,1),round(y-10,1),str(count),11,'#c1cfff','class="mono" text-anchor="middle"')
    path='M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
    s+=f'<path d="{path} L1125 178 L90 178Z" fill="#4c53ac" opacity=".15"/><path d="{path}" fill="none" stroke="url(#edge)" stroke-width="2.5"/>'
    for x,y in pts:s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{CYAN}"/>'
    s+=text(600,231,'COUNTS FROM THE DISPLAYED CALENDAR  ·  FIRST / LAST MONTH MAY BE PARTIAL',10,MUTED,'class="mono" text-anchor="middle"')
    return s+finish(1200,250)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--username',default='Dinesh-757')
    parser.add_argument('--html',type=Path,help='Render a previously fetched GitHub HTML page for offline validation.')
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?',args.username):
        parser.error('Invalid GitHub username')
    days=parse_calendar(args.html.read_text()) if args.html else fetch_calendar(args.username)
    rendered={'contribution-current.svg':contribution_svg(args.username,days),'activity-pulse.svg':pulse_svg(days)}
    rendered['contribution-snapshot.json']=json.dumps({'username':args.username,'source':f'https://github.com/users/{args.username}/contributions','through':days[-1]['date'],'days':days},indent=2)+'\n'
    OUT.mkdir(exist_ok=True)
    for name,content in rendered.items():
        tmp=OUT/(name+'.tmp')
        tmp.write_text(content,encoding='utf-8')
        tmp.replace(OUT/name)
    print(f'Rendered {len(days)} real calendar days; {sum(d["count"] for d in days)} contributions.')


if __name__=='__main__':
    main()
