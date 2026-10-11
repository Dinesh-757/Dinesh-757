#!/usr/bin/env python3
"""Build Dilli Dinesh's original, self-contained README artwork (stdlib only)."""
from html import escape
from pathlib import Path
import math
import random

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
BLUE, CYAN, PURPLE, WHITE, MUTED = "#448aff", "#77e7ff", "#a78bfa", "#edf5ff", "#a6b8d6"

STYLE = """
text{font-family:Arial,Helvetica,sans-serif} .mono{font-family:'DejaVu Sans Mono',Consolas,monospace}
.orbit{transform-box:fill-box;transform-origin:center;animation:orbit 32s linear infinite}
.reverse{animation-direction:reverse;animation-duration:45s}
.current{stroke-dasharray:95 1100;animation:current 9s linear infinite}
.spark{animation:spark 7s ease-in-out infinite}
.glitch{opacity:0;animation:glitch 9s steps(1,end) infinite}
.glitch2{animation-delay:-4.5s}
.pulse{animation:pulse 5s ease-in-out infinite}
.scan{animation:scan 12s linear infinite}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes current{to{stroke-dashoffset:-1195}}
@keyframes spark{0%,35%,54%,100%{opacity:.25}40%,48%{opacity:1}44%{opacity:.6}}
@keyframes glitch{0%,88%,94%,100%{opacity:0;transform:translateX(0)}89%,92%{opacity:.7;transform:translateX(4px)}90%,93%{opacity:.45;transform:translateX(-3px)}}
@keyframes pulse{0%,100%{opacity:.45}50%{opacity:1}}
@keyframes scan{0%{transform:translateX(-100px);opacity:0}10%,90%{opacity:.65}100%{transform:translateX(1200px);opacity:0}}
@keyframes rain{from{transform:translateY(-240px)}to{transform:translateY(240px)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.glitch,.scan{display:none}.type-animated{display:none}.type-static{display:block!important}}
"""

def text(x, y, value, size=18, color=WHITE, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(value)}</text>'

def start(w, h, title, desc, css="", defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs>
<linearGradient id="bg" x2="1" y2="1"><stop stop-color="#040b19"/><stop offset=".55" stop-color="#0b1432"/><stop offset="1" stop-color="#190f36"/></linearGradient>
<linearGradient id="edge"><stop stop-color="{CYAN}"/><stop offset=".52" stop-color="{BLUE}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#4358f6" stop-opacity=".35"/><stop offset="1" stop-color="#6754fb" stop-opacity="0"/></radialGradient>
<linearGradient id="shade"><stop stop-color="#050c1c"/><stop offset=".62" stop-color="#050c1c" stop-opacity=".93"/><stop offset="1" stop-color="#050c1c" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-60%" y="-80%" width="220%" height="260%"><feGaussianBlur stdDeviation="4"/></filter>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#7f9bdf" stroke-opacity=".055"/></pattern>
<clipPath id="bounds"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18"/></clipPath>{defs}
</defs><style>{STYLE}{css}</style>
<g clip-path="url(#bounds)"><rect width="{w}" height="{h}" fill="url(#bg)"/><rect width="{w}" height="{h}" fill="url(#grid)"/>
'''

def finish(w, h):
    return f'</g><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" stroke="#31466c" stroke-opacity=".8"/></svg>\n'

def rain(w, h, seed=757, spacing=33, opacity=.34):
    rng = random.Random(seed)
    s = f'<g class="mono" font-size="13" opacity="{opacity}" aria-hidden="true">'
    for x in range(20, w, spacing):
        offset = rng.randint(-100, 100)
        dur = rng.uniform(9, 17)
        s += f'<g style="animation:rain {dur:.2f}s linear infinite;animation-delay:-{rng.uniform(0,dur):.2f}s">'
        for j in range(-15, h//18+15):
            col = CYAN if j % 9 == 0 else (PURPLE if x % 3 == 0 else BLUE)
            s += f'<text x="{x}" y="{j*18+offset}" fill="{col}" opacity="{.95 if j%9==0 else .32}">{rng.choice("01ABCDEF<>/") .replace("<","&lt;").replace(">","&gt;")}</text>'
        s += '</g>'
    return s + '</g>'

def bolt(d, color=CYAN, delay=0):
    return f'<g fill="none" stroke-linejoin="round" stroke-linecap="round"><path d="{d}" stroke="{color}" stroke-width="9" opacity=".3" filter="url(#glow)"/><path d="{d}" stroke="{color}" stroke-width="1.6" opacity=".35"/><g class="spark" style="animation-delay:-{delay}s"><path d="{d}" stroke="{color}" stroke-width="2.4"/><path d="{d}" stroke="#e6faff" stroke-width=".75"/></g></g>'

def ring(cx, cy, r, color=BLUE):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-opacity=".2"/><circle class="orbit" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="70 40 4 38 18 80"/><circle class="orbit reverse" cx="{cx}" cy="{cy}" r="{r-15}" fill="none" stroke="{PURPLE}" stroke-opacity=".45" stroke-dasharray="2 12"/>'

def write(name, content):
    OUT.mkdir(exist_ok=True)
    (OUT/name).write_text(content, encoding="utf-8")

def hero():
    s = start(1200, 420, "Dilli Dinesh — Electric Defense", "Original blue and purple lightning, orbiting signal rings, falling code and brief sliced-text glitch effects. All essential text remains visible without animation.", defs='<clipPath id="slice"><path d="M44 133h660v7H44zM44 165h660v5H44z"/></clipPath>')
    s += '<ellipse cx="945" cy="200" rx="300" ry="300" fill="url(#halo)"/>' + rain(1200, 420, spacing=47, opacity=.45)
    s += '<rect width="780" height="420" fill="url(#shade)"/>'
    s += ring(959,207,137) + ring(959,207,106,CYAN)
    s += '<circle cx="959" cy="207" r="78" fill="#090e27" stroke="#48428a"/>'
    s += bolt('M1032 -20L1009 26 1030 39 989 72 1008 98 958 132 987 155 921 215 947 233 903 295 951 258 936 241 1000 188 973 169 1025 132 1006 110 1077 48 1051 36 1089 -10')
    s += bolt('M1200 127L1152 139 1141 168 1096 163 1062 192 1023 193 1000 218',PURPLE,2)
    s += bolt('M1195 339L1152 314 1127 324 1082 293 1056 306 1019 282',BLUE,3.1)
    s += bolt('M835 63L817 87 838 98 790 144 810 165 764 199',PURPLE,1.5)
    s += '<path d="M46 43H656L677 64H725" fill="none" stroke="url(#edge)" stroke-opacity=".7"/><path class="current" d="M46 43H656L677 64H725" fill="none" stroke="#bcf4ff" stroke-width="2"/>'
    s += text(48,88,'ELECTRIC DEFENSE  /  GLITCH PROTOCOL',16,CYAN,'class="mono" letter-spacing="2"')
    name = text(44,179,'DILLI DINESH',82,WHITE,'font-weight="800" letter-spacing="-2"')
    s += name + f'<g class="glitch" clip-path="url(#slice)">{name.replace(WHITE,CYAN)}</g><g class="glitch glitch2" clip-path="url(#slice)">{name.replace(WHITE,PURPLE)}</g>'
    s += text(48,236,'DETECT. INVESTIGATE. DEFEND.',27,'#c0d8ff','font-weight="700" letter-spacing=".5"')
    s += text(49,275,'SOC  /  BLUE TEAM  /  SECURITY ENGINEERING',16,MUTED,'class="mono"')
    for x,label,width in [(48,'SIGNALS',111),(174,'EVIDENCE',129),(318,'DEFENSE',124)]:
        s += f'<rect x="{x}" y="310" width="{width}" height="30" rx="5" fill="#101d37" stroke="#294263"/>' + text(x+15,330,label,12,CYAN,'class="mono" letter-spacing="1"')
    s += '<path d="M48 373H700" stroke="#293c60"/><circle class="pulse" cx="54" cy="390" r="3" fill="#77e7ff"/>'
    s += text(68,395,'GITHUB.COM/DINESH-757  ::  SIGNAL ACTIVE',12,MUTED,'class="mono" letter-spacing="1"')
    s += text(959,387,'01 / ELECTRIC DEFENSE',11,PURPLE,'class="mono" text-anchor="middle" letter-spacing="1"')
    write('electric-defense-banner.svg',s+finish(1200,420))

def typing():
    # CSS animates the clipping rectangle in discrete character-sized steps.
    css='''
.typing-window{animation:typing 7s steps(71,end) infinite}
.cursor{animation:cursor 1.1s steps(1,end) infinite}
@keyframes typing{0%,7%{width:0}62%,92%{width:1090px}100%{width:0}}
@keyframes cursor{0%,55%{opacity:1}56%,100%{opacity:0}}
@media(prefers-reduced-motion:reduce){.typing-window{width:1090px}}
'''
    s=start(1200,82,'Dilli Dinesh — current focus','Typing animation: Cybersecurity student · SOC / Blue Team track · Security product builder.',css, '<clipPath id="typing"><rect class="typing-window" x="58" y="21" width="1090" height="42"/></clipPath>')
    s+=text(25,50,'›',28,CYAN,'class="mono"')
    s+='<g clip-path="url(#typing)">'+text(59,48,'Cybersecurity student · SOC / Blue Team track · Security product builder',22,'#c5d9ff','class="mono"')+'</g>'
    s+='<rect class="cursor" x="1163" y="30" width="3" height="24" fill="#a78bfa"/>'
    write('focus-typing.svg',s+finish(1200,82))

def stream():
    s=start(1200,120,'Signals in motion','Decorative blue and purple Matrix-style falling hexadecimal code with a lightning conduit.')
    s+=rain(1200,120,spacing=27,opacity=.64)
    s+='<rect x="310" y="22" width="580" height="76" rx="10" fill="#060e23" fill-opacity=".93" stroke="#284263"/>'
    s+=text(600,53,'SYSTEM ONLINE  //  SIGNALS IN MOTION',16,CYAN,'class="mono" text-anchor="middle" letter-spacing="1"')
    s+=text(600,79,'BLUE TEAM  /  TRACE  /  TRIAGE  /  DEFEND',12,MUTED,'class="mono" text-anchor="middle" letter-spacing="1"')
    s+=bolt('M0 69L52 66 69 49 86 73 127 60 150 71 209 47 232 65 305 60',CYAN)
    s+=bolt('M895 60L948 61 963 40 981 79 1004 52 1026 66 1079 51 1106 64 1200 49',PURPLE,2)
    write('electric-matrix-stream.svg',s+finish(1200,120))

def divider():
    # Transparent outer region keeps the transition compact on light and dark GitHub.
    s=start(1200,48,'Electric transition','A compact electric-blue and purple animated lightning divider.')
    d='M14 24H380L397 17 413 31 431 14 448 32 466 24H728L745 16 763 31 781 22H1186'
    s+=f'<path d="{d}" fill="none" stroke="url(#edge)" opacity=".45"/><path class="current" d="{d}" fill="none" stroke="{CYAN}" stroke-width="2"/>'
    s+=bolt('M544 24L565 17 584 31 599 9 612 36 631 19 650 24',PURPLE)
    write('electric-conduit.svg',s+finish(1200,48))

def projects():
    projects=[('cybershield','01','CYBERSHIELD AI','SECURITY OPERATIONS','Real-time IDS • threat signals • security incident workflows',CYAN),('codeguard','02','CODEGUARD AI','DEVELOPER SECURITY','Local code monitoring • secrets • MCP security • alerts',PURPLE),('memforensix','03','MEMFORENSIX','DIGITAL FORENSICS','Memory artifacts • Volatility 3 • YARA • anomaly analysis','#82aaff')]
    for slug,n,title,category,subtitle,color in projects:
        s=start(1200,228,title,f'Original {category.lower()} project artwork. The entire card links to the {title} source repository. Illustrative graphics are not live measurements.')
        s+='<ellipse cx="960" cy="125" rx="235" ry="210" fill="url(#halo)"/>'
        s+=rain(1200,228,seed=int(n),spacing=55,opacity=.18)+'<rect width="785" height="228" fill="url(#shade)"/>'
        s+=f'<path d="M2 30V198" stroke="{color}" stroke-width="4"/>'
        s+=text(38,37,f'OPERATION {n}  /  {category}',13,color,'class="mono" letter-spacing="1.5"')
        s+=text(35,99,title,47,WHITE,'font-weight="800" letter-spacing="-1"')
        s+=text(39,135,subtitle,17,MUTED)
        s+='<rect x="38" y="166" width="203" height="35" rx="5" fill="#132541" stroke="#3d6590"/>'
        s+=text(54,188,'EXPLORE SOURCE  ↗',13,color,'class="mono" font-weight="bold"')
        s+=text(268,188,'VIEW MISSION DOSSIER BELOW',11,MUTED,'class="mono" letter-spacing="1"')
        s+=f'<path d="M775 1L734 53V175L780 227" fill="none" stroke="{color}" stroke-opacity=".28"/>'
        if slug=='cybershield':
            s+=ring(958,113,87,color)
            s+='<path d="M958 55L1009 74V112Q1009 155 958 177Q907 155 907 112V74Z" fill="#0c1b35" stroke="#77e7ff" stroke-width="2"/>'
            s+=bolt('M976 81L944 115 966 115 941 149',color)
            s+='<path class="current" d="M823 119H888L903 99 917 141 932 119H1090" fill="none" stroke="#77e7ff" stroke-width="2"/>'
        elif slug=='codeguard':
            s+='<rect x="843" y="42" width="231" height="148" rx="12" fill="#0a132b" stroke="#625198"/><path d="M843 70H1074" stroke="#3a365e"/>'
            for x,c in [(858,BLUE),(870,PURPLE),(882,CYAN)]: s+=f'<circle cx="{x}" cy="56" r="3" fill="{c}"/>'
            s+=text(874,145,'{',67,PURPLE,'class="mono"')+text(1000,145,'}',67,PURPLE,'class="mono"')
            s+='<rect x="936" y="115" width="42" height="36" rx="7" fill="#182648" stroke="#a78bfa"/><path d="M944 115V105a13 13 0 0 1 26 0V115" fill="none" stroke="#77e7ff" stroke-width="3"/><circle class="pulse" cx="957" cy="132" r="3" fill="#77e7ff"/>'
            s+=bolt('M1100 16L1070 29 1090 39 1065 66',color,1)
        else:
            for i in range(3):
                y=58+i*42
                s+=f'<rect x="855" y="{y}" width="209" height="30" rx="5" fill="#10213c" stroke="#354f80"/>'
                for j in range(8): s+=f'<rect x="{868+j*24}" y="{y+10}" width="12" height="10" rx="2" fill="{color if (i+j)%3==0 else "#203859"}" opacity=".8"/>'
            s+='<circle cx="975" cy="110" r="36" fill="#0a132b" fill-opacity=".7" stroke="#77e7ff" stroke-width="3"/><path d="M1000 137L1026 164" stroke="#a78bfa" stroke-width="9" stroke-linecap="round"/>'
            s+=f'<circle class="pulse" cx="975" cy="110" r="23" fill="none" stroke="{color}" stroke-dasharray="3 6"/>'
        s+=f'<path class="current" d="M20 226H1180" fill="none" stroke="{color}" stroke-width="2"/>'
        write(f'operation-{slug}.svg',s+finish(1200,228))

def signal_path():
    s=start(1200,200,'Signal Path — Dilli Dinesh’s security engineering workflow','Capture packets and file events; detect with models, rules and IOCs; investigate context and triage; respond by documenting and improving.')
    s+=text(28,35,'SIGNAL PATH  //  FROM OBSERVATION TO ACTION',14,CYAN,'class="mono" letter-spacing="1"')
    labels=[('CAPTURE','Packets · File events'),('DETECT','Models · Rules · IOCs'),('INVESTIGATE','Context · Triage'),('RESPOND','Document · Improve')]
    for i,(title,sub) in enumerate(labels):
        x=28+i*294
        s+=f'<rect x="{x}" y="58" width="260" height="91" rx="9" fill="#0c1930" stroke="#2c4365"/>'
        s+=text(x+18,81,f'STAGE 0{i+1}',10,PURPLE,'class="mono" letter-spacing="1"')
        s+=text(x+18,109,title,23,WHITE,'font-weight="700"')+text(x+18,133,sub,13,MUTED)
        if i<3: s+=f'<path d="M{x+264} 104H{x+289}m-6-5 6 5-6 5" fill="none" stroke="#6385ba"/>'
    s+='<path d="M32 159H1168" stroke="#21385c"/><path class="current" d="M32 159H1168" stroke="#77e7ff" stroke-width="2"/>'
    s+=text(600,183,'EVIDENCE > ASSUMPTIONS  //  SECURITY WORKFLOW',11,MUTED,'class="mono" text-anchor="middle" letter-spacing="1"')
    write('signal-path.svg',s+finish(1200,200))

def footer():
    s=start(1200,158,'Stay curious. Defend relentlessly.','Electric-blue and purple lightning outro for Dilli Dinesh.')
    s+=rain(1200,158,spacing=59,opacity=.18)
    s+=bolt('M0 69L62 51 85 70 109 41 129 69 151 61 181 76 210 64',CYAN)
    s+=bolt('M985 89L1015 76 1034 94 1056 65 1074 82 1102 70 1138 79 1200 56',PURPLE,3)
    s+=text(600,74,'STAY CURIOUS. DEFEND RELENTLESSLY.',29,WHITE,'font-weight="700" text-anchor="middle" letter-spacing="1"')
    s+=text(600,111,'DILLI DINESH  //  END TRANSMISSION',12,CYAN,'class="mono" text-anchor="middle" letter-spacing="2"')
    write('electric-defense-footer.svg',s+finish(1200,158))

if __name__ == '__main__':
    hero(); typing(); stream(); divider(); projects(); signal_path(); footer()
    print('Built 9 original profile SVG assets.')
