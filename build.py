import re, html
lines = [l.rstrip('\n') for l in open('sources.txt', encoding='utf-8')]
DECADE = re.compile(r'^The 19\d0s$')
DYK = re.compile(r'^Did You Know\??$')
URL = re.compile(r'(https?://\S+)')
decades = []  # {name, cats:[{name, items:[], dyk:[]}]}
cur_cat = None; in_dyk = False
for l in lines[1:]:
    if not l.strip(): continue
    if DECADE.match(l):
        decades.append({'name': l, 'cats': []}); cur_cat = None; in_dyk = False; continue
    if DYK.match(l):
        in_dyk = True; continue
    m = URL.search(l)
    if not m:
        cur_cat = {'name': l, 'items': [], 'dyk': []}; decades[-1]['cats'].append(cur_cat); in_dyk = False; continue
    url = m.group(1).rstrip('›')
    text = l[:m.start()].strip()
    (cur_cat['dyk'] if in_dyk else cur_cat['items']).append((text, url))

def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def li(text, url):
    t = html.escape(text) if text else ''
    u = html.escape(url)
    shown = html.escape(re.sub(r'^https?://(www\.)?', '', url))
    return f'<li>{t + " " if t else ""}<a href="{u}" target="_blank" rel="noopener">{shown}</a></li>'

out = []
total = 0
for d in decades:
    did = slug(d['name'])
    out.append(f'<section class="decade" id="{did}"><h2>{html.escape(d["name"])}</h2>')
    for c in d['cats']:
        n = len(c['items']) + len(c['dyk']); total += n
        out.append(f'<details><summary><span>{html.escape(c["name"])}</span><span class="count">{n}</span></summary>')
        out.append('<ul>' + ''.join(li(t, u) for t, u in c['items']) + '</ul>')
        if c['dyk']:
            out.append('<h4>Did You Know?</h4><ul>' + ''.join(li(t, u) for t, u in c['dyk']) + '</ul>')
        out.append('</details>')
    out.append('</section>')
body = '\n'.join(out)
nav = ' '.join(f'<a href="#{slug(d["name"])}">{html.escape(d["name"].replace("The ", ""))}</a>' for d in decades)

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Totally Gen X! Sources</title>
<meta name="description" content="Sources and references for Totally Gen X!, the pop culture trivia book by Autumn Bridges.">
<style>
  :root {{
    --bg: #0f1020; --panel: #171a33; --ink: #f4f1ff; --muted: #b7b3d6;
    --neon: #ff5fa2; --neon2: #5ff2d0; --gold: #f6c860; --line: #2c3060;
  }}
  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink);
    font: 16px/1.5 -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
  main {{ max-width: 760px; margin: 0 auto; padding: 28px 16px 64px; }}
  header {{ text-align: center; padding: 16px 0 8px; }}
  .kicker {{ color: var(--neon2); letter-spacing: .25em; font-size: 12px; text-transform: uppercase; margin: 0 0 10px; }}
  h1 {{ font-size: clamp(30px, 8vw, 44px); line-height: 1.1; margin: 0 0 10px; text-shadow: 0 0 18px rgba(255,95,162,.35); }}
  .sub {{ color: var(--neon2); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 15px; margin: 0 0 6px; }}
  .byline {{ color: var(--muted); margin: 0 0 22px; font-size: 15px; }}
  .section-title {{ font-size: 20px; color: var(--ink); margin: 0 0 6px; letter-spacing: .04em; }}
  .lede {{ color: var(--muted); margin: 0 auto 18px; max-width: 520px; }}
  nav {{ display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin: 0 0 24px; position: sticky; top: 0;
    background: rgba(15,16,32,.92); padding: 10px 0; backdrop-filter: blur(6px); z-index: 2; }}
  nav a {{ border: 1px solid var(--line); border-radius: 999px; padding: 8px 16px; color: var(--ink); text-decoration: none; font-weight: 600; }}
  nav a:hover {{ border-color: var(--neon2); color: var(--neon2); }}
  .decade {{ margin: 28px 0 8px; }}
  h2 {{ font-size: 26px; margin: 0 0 12px; color: var(--gold); letter-spacing: .02em; }}
  details {{ background: var(--panel); border: 1px solid var(--line); border-radius: 14px; margin: 10px 0; overflow: hidden; }}
  summary {{ cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; gap: 12px;
    padding: 14px 18px; font-weight: 700; font-size: 17px; }}
  summary::-webkit-details-marker {{ display: none; }}
  summary::after {{ content: "+"; color: var(--neon2); font-size: 22px; line-height: 1; margin-left: 8px; }}
  details[open] summary::after {{ content: "\\2013"; }}
  summary span:first-child {{ flex: 1; }}
  .count {{ color: var(--muted); font-weight: 400; font-size: 13px; }}
  details ul {{ margin: 0; padding: 0 18px 16px 36px; }}
  details li {{ margin: 10px 0; word-break: break-word; }}
  details h4 {{ margin: 6px 18px 0; font-size: 12px; letter-spacing: .2em; text-transform: uppercase; color: var(--neon); }}
  a {{ color: var(--neon2); text-decoration: none; border-bottom: 1px solid rgba(95,242,208,.35); }}
  a:hover {{ border-bottom-color: var(--neon2); }}
  .mall {{ background: var(--panel); border: 1px solid var(--line); border-radius: 14px; padding: 20px; margin: 32px 0 0; text-align: center; }}
  .btn {{ display: inline-block; background: var(--neon); color: #1a0b14; font-weight: 700; padding: 12px 22px; border-radius: 999px; border: 0; margin-top: 10px; }}
  footer {{ text-align: center; color: var(--muted); font-size: 13px; margin-top: 32px; }}
</style>
</head>
<body>
<main>
  <header>
    <p class="kicker">Pop Culture Trivia Book</p>
    <h1>Totally Gen&nbsp;X!</h1>
    <p class="sub">70s, 80s &amp; 90s Throwback</p>
    <p class="byline">Autumn Bridges</p>
    <h2 class="section-title">Sources and References</h2>
    <p class="lede">Every source cited in the book, by decade and chapter. Tap a chapter to open its list.</p>
  </header>
  <nav>{nav}</nav>
{body}
  <div class="mall">
    <p>Trivia Night runs every Tuesday at 8pm ET at The Mall.</p>
    <a class="btn" href="https://genxtown.com">Visit The Mall at genxtown.com</a>
  </div>
  <footer><p>&copy; 2026 Autumn Bridges. All rights reserved.</p></footer>
</main>
</body>
</html>
'''
open('index.html', 'w', encoding='utf-8').write(page)
print('decades', len(decades), '| categories', sum(len(d['cats']) for d in decades), '| links', total)
for d in decades: print(' ', d['name'], [ (c['name'][:22], len(c['items']), len(c['dyk'])) for c in d['cats'] ])
