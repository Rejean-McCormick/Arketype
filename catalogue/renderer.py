"""Offline, deterministic HTML catalogue projection. Reads Arketype JSON; never writes canon."""
from __future__ import annotations
from pathlib import Path
from html import escape
import json


def svg(diagram: dict, decorative: bool = False) -> str:
    nodes=diagram['nodes']; edges=diagram['edges']; pattern=diagram['pattern']
    positions={n['id']:n for n in nodes}
    parts=['<svg class="diagram" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 244" role="img" aria-label="Situated diagram: '+escape(diagram['caption'],quote=True)+'">']
    if pattern == 'matrix':
        for x in (37,232,427):
            for y in (27,124):
                parts.append(f'<rect class="grid-cell" fill="none" stroke="#bad4ce" stroke-width="2" x="{x}" y="{y}" width="192" height="94" rx="8"/>')
    if pattern == 'multilayer':
        parts.append('<path class="layer-guide" fill="none" stroke="#ccdcd8" stroke-width="2" stroke-dasharray="5 8" d="M96 59 H564 M96 118 H564 M96 178 H564"/>')
    for e in edges:
        a=positions[e['from']]; b=positions[e['to']]
        parts.append(f'<path class="connector" fill="none" stroke="#8cadab" stroke-width="3.5" stroke-linecap="round" d="M{a["x"]} {a["y"]} L{b["x"]} {b["y"]}"/>')
    for i,n in enumerate(nodes):
        x=n['x'];y=n['y']
        width=150 if pattern in ('casefile','multilayer') else 138
        height=44 if pattern not in ('casefile','matrix') else 40
        # the first node is the anchor in hub/casefile/network
        role=' anchor' if i==0 and pattern in ('hub','casefile','network','tree') else ''
        parts.append(f'<rect class="graph-node{role}" x="{x-width/2:g}" y="{y-height/2:g}" width="{width}" height="{height}" fill="{'#1e6864' if role else '#f4faf8'}" stroke="{'#1e6864' if role else '#42847e'}" stroke-width="2.5" rx="11"/>')
        lbl=n['label']
        if len(lbl)>15 and ' ' in lbl:
            chunks=lbl.split(' ')
            line1=''; line2=''
            for word in chunks:
                if not line1 or len(line1)+len(word)+1<15:line1=(line1+' '+word).strip()
                else: line2=(line2+' '+word).strip()
            if line2:
                parts.append(f'<text class="node-label" font-size="15" font-family="sans-serif" font-weight="600" fill="{'#ffffff' if role else '#104c49'}" x="{x}" y="{y-4}" text-anchor="middle"><tspan x="{x}">{escape(line1)}</tspan><tspan x="{x}" dy="15">{escape(line2)}</tspan></text>')
            else:
                parts.append(f'<text class="node-label" font-size="15" font-family="sans-serif" font-weight="600" fill="{'#ffffff' if role else '#104c49'}" x="{x}" y="{y+4}" text-anchor="middle">{escape(lbl)}</text>')
        else:
            parts.append(f'<text class="node-label" font-size="15" font-family="sans-serif" font-weight="600" fill="{'#ffffff' if role else '#104c49'}" x="{x}" y="{y+4}" text-anchor="middle">{escape(lbl)}</text>')
    parts.append('</svg>')
    return ''.join(parts)


def build(root: Path, output: Path | None = None) -> Path:
    root=Path(root).resolve()
    output=Path(output) if output else root/'catalogue/index.html'
    cat=json.loads((root/'catalogue.json').read_text(encoding='utf-8'))
    index=json.loads((root/'inventaires/archetypes-visuels.json').read_text(encoding='utf-8'))['archetypes']
    profiles=json.loads((root/'inventaires/profils-usage.json').read_text(encoding='utf-8'))['profiles']
    patterns=json.loads((root/'inventaires/grammaire-visuelle.json').read_text(encoding='utf-8'))['patterns']
    diagrams=json.loads((root/'inventaires/diagrammes-situes.json').read_text(encoding='utf-8'))['diagrams']
    dmap={(d['kind'],d['slug']):d for d in diagrams}
    pmap={p['id']:p for p in patterns}
    arch_cards=[]; profile_cards=[]
    def tx(v): return escape(str(v),quote=True)
    def dots(items):return ''.join('<span class="token">'+tx(v)+'</span>' for v in items)
    def arch_card(a):
        slug=a['slug'];detail=json.loads((root/a['file']).read_text(encoding='utf-8'))
        d=dmap[('archetype',slug)]
        pat=pmap[a['visual_pattern']]
        return f'''<article class="card arch-card" data-family="{tx(a['family'])}" data-pattern="{tx(a['visual_pattern'])}" data-search="{tx(' '.join(map(str,[a['id'],a['slug'],a['name'],a['family'],a['situational_schema'],*a['canonical_use_cases'],*detail.get('primitive_labels_en',detail['primitive_candidates'])])).casefold())}">
          <div class="card-top"><span class="entry-id">{tx(a['id'])}</span><span class="entry-family">{tx(a['family'])}</span></div>
          <h3>{tx(a['name'])}</h3>
          <figure class="diagram-panel">{svg(d)}<figcaption>{tx(pat['label'])} · {tx(a['structure_label'])}</figcaption></figure>
          <p class="card-description">{tx(detail['description'])}</p>
          <div class="structure-caption"><span class="field-title">Structural interpretation</span>{tx(a['situational_schema'])}</div>
          <div class="card-examples"><span class="field-title">Use cases</span><div class="tokens">{dots(a['canonical_use_cases'])}</div></div>
          <details><summary>Primitives and integrity</summary><p><b>Candidate primitives:</b> {tx(', '.join(detail.get('primitive_labels_en',detail['primitive_candidates'])))}</p><p><b>Rule:</b> {tx(detail['integrity_rule'])}</p><p><b>Avoid:</b> {tx(detail['antipattern'])}</p></details>
          <a class="file-link" href="../{tx(a['file'])}" title="Descriptive JSON record">JSON record <span aria-hidden="true">↗</span></a>
        </article>'''
    for a in index:
        arch_cards.append(arch_card(a))
    for p in profiles:
        d=dmap[('profile',p['slug'])]
        pat=pmap[p['visual_pattern']]
        profile_cards.append(f'''<article class="card profile-card" data-pattern="{tx(p['visual_pattern'])}" data-search="{tx(' '.join(map(str,[p['slug'],p['name'],p['summary'],p['situational_schema'],*p['use_cases'],*p['supporting_archetypes']])).casefold())}">
          <div class="card-top"><span class="entry-id">{tx(p['id'])}</span><span class="entry-family">Use-case profile</span></div>
          <h3>{tx(p['name'])}</h3><figure class="diagram-panel">{svg(d)}<figcaption>{tx(pat['label'])}</figcaption></figure>
          <p class="card-description">{tx(p['summary'])}</p>
          <div class="structure-caption"><span class="field-title">Scenario</span>{tx(p['situational_schema'])}</div>
          <div class="card-examples"><span class="field-title">Combined with</span><div class="tokens">{dots([p['primary_archetype'],*p['supporting_archetypes']])}</div></div>
          <details><summary>Usage and boundaries</summary><p><b>Inputs:</b> {tx(', '.join(p['inputs']))}</p><p><b>Candidate outputs:</b> {tx(', '.join(p['outputs']))}</p><p><b>Boundaries:</b> {tx('; '.join(p['boundaries']))}</p></details>
          <a class="file-link" href="../assemblages/{tx(p['assemblage_reference'])}.json">Assembly JSON <span aria-hidden="true">↗</span></a>
        </article>''')
    motif_cells=[]
    for p in patterns:
        d=next(x for x in diagrams if x['pattern']==p['id'])
        motif_cells.append(f'''<div class="motif"><div class="motif-meta"><b>{tx(p['label'])}</b><span>{tx(p['id'])}</span></div>{svg(d,decorative=True)}</div>''')

    html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#1e6864"><meta name="description" content="Arketype visual catalogue of Kristal structures, use cases, diagrams, and linked JSON inventories.">
<title>Arketype · Visual Kristal Catalogue</title>
<style>
:root{{--brand:#1e6864;--brand-dark:#104c49;--brand-wash:#e8f4f0;--ink:#172b29;--muted:#607875;--canvas:#f5f8f7;--paper:#fff;--line:#d9e5e2;--shadow:0 8px 30px rgba(10,59,55,.055)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--canvas);color:var(--ink);font:15px/1.58 system-ui,-apple-system,Segoe UI,Arial,sans-serif}}a{{color:var(--brand);text-decoration:none}}a:hover{{text-decoration:underline}}
.shell{{max-width:1300px;margin:0 auto;padding:0 30px}}.hero{{background:linear-gradient(120deg,#f0faf6 0%,#fff 66%);border-bottom:1px solid var(--line)}}.hero-inner{{padding:42px 0 32px}}.brandline{{display:flex;align-items:center;gap:20px;margin-bottom:30px}}.logo-wrap{{width:118px;height:66px;display:flex;justify-content:center;align-items:center;padding:8px 12px;border:1px solid #d2e6e0;border-radius:16px;background:#fff}}.logo-wrap img{{width:100%;height:100%;object-fit:contain}}.brand-word{{font-size:20px;font-weight:800;letter-spacing:-.05em;color:var(--brand)}}.brand-subtitle{{font-size:12px;color:var(--muted);letter-spacing:.11em;text-transform:uppercase}}.eyebrow{{display:block;text-transform:uppercase;letter-spacing:.15em;font-size:11px;font-weight:800;color:var(--brand);margin-bottom:12px}}h1{{font-size:clamp(34px,4.7vw,64px);line-height:1.09;max-width:900px;margin:0 0 19px;letter-spacing:-.045em}}.hero-intro{{max-width:770px;color:#4f6964;font-size:17px;margin:0 0 22px}}.statline{{display:flex;gap:10px;flex-wrap:wrap}}.stat{{border:1px solid #c8dfd9;background:#fff;border-radius:9px;padding:9px 13px;font-size:13px}}.stat b{{color:var(--brand);font-size:17px;margin-right:6px}}
.navbar{{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}}.navinner{{display:flex;gap:22px;align-items:center;min-height:52px;flex-wrap:wrap}}.navinner a{{font-size:13px;font-weight:750}}.navright{{margin-left:auto;font-size:12px;color:var(--muted)}}section{{padding-top:48px}}.section-head{{display:flex;align-items:end;justify-content:space-between;gap:16px;margin:0 0 20px}}h2{{font-size:28px;letter-spacing:-.035em;line-height:1.2;margin:0 0 5px}}.section-desc{{margin:0;color:var(--muted);max-width:690px}}.disclaimer{{border-left:3px solid var(--brand);background:#fff;border-radius:0 11px 11px 0;padding:18px 22px;margin-top:35px;font-size:14px;color:#4b6763}}.disclaimer strong{{color:var(--brand)}}
.motif-grid{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}}.motif{{background:#fff;border:1px solid var(--line);padding:12px 12px 4px;border-radius:12px;min-width:0}}.motif-meta{{display:flex;align-items:center;justify-content:space-between;gap:6px;font-size:12px;line-height:1.3}}.motif-meta span{{font:10px ui-monospace,monospace;color:var(--muted)}}.motif .diagram{{height:76px;width:100%;max-width:220px;margin:5px 0}}
.filters{{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:16px 0 22px}}.filters input,.filters select{{background:#fff;border:1px solid #b9ceca;color:var(--ink);border-radius:9px;padding:10px 12px;min-height:41px;font:inherit;font-size:14px}}.filters input{{min-width:240px;flex:1}}.filters select{{min-width:160px}}.filter-count{{font-size:13px;color:var(--muted)}}.reset{{cursor:pointer;color:var(--brand);border:1px solid #c5dbd5;background:#fff;border-radius:9px;padding:10px 13px;font-size:13px;font-weight:700}}
.card-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.card{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:19px;min-width:0;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:0}}.card[hidden]{{display:none!important}}.card-top{{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:10px}}.entry-id{{font-size:12px;font-weight:850;letter-spacing:.04em;color:var(--brand)}}.entry-family{{font-size:11px;color:var(--muted);padding:3px 8px;background:#f0f5f3;border-radius:30px}}h3{{font-size:20px;line-height:1.24;letter-spacing:-.025em;margin:0 0 14px;min-height:49px}}.diagram-panel{{border:1px solid #dbe8e4;border-radius:12px;padding:12px 8px 6px;background:linear-gradient(180deg,#f7fbfa,#fff);margin:0 0 16px}}.diagram{{display:block;width:100%;height:auto;max-height:155px;overflow:visible}}.diagram .connector{{stroke:#8cadab;stroke-width:3.5;stroke-linecap:round;fill:none}}.diagram .graph-node{{fill:#f4faf8;stroke:#42847e;stroke-width:2.5}}.diagram .graph-node.anchor{{fill:var(--brand);stroke:var(--brand)}}.diagram .node-label{{fill:var(--brand-dark);font:600 15px system-ui,sans-serif;pointer-events:none}}.diagram .graph-node.anchor + .node-label{{fill:white}}.diagram .grid-cell{{fill:none;stroke:#bad4ce;stroke-width:2}}.diagram .layer-guide{{stroke:#ccdcd8;stroke-dasharray:5 8;stroke-width:2}}.diagram-panel figcaption{{font-size:11px;color:var(--muted);text-align:center;margin-top:2px}}.card-description{{font-size:14px;margin:0 0 12px;min-height:45px}}.structure-caption{{background:var(--brand-wash);border-radius:9px;padding:10px 12px;font-size:13px;line-height:1.55}}.field-title{{display:block;color:var(--brand);font-size:10px;font-weight:850;text-transform:uppercase;letter-spacing:.12em;margin-bottom:4px}}.card-examples{{margin:13px 0}}.tokens{{display:flex;gap:5px;flex-wrap:wrap}}.token{{background:#f2f5f4;border:1px solid #e2eae7;border-radius:6px;color:#4d6862;padding:3px 7px;font-size:11px}}details{{border-top:1px solid var(--line);padding-top:10px;margin-top:auto;font-size:12px}}details summary{{cursor:pointer;color:var(--brand);font-weight:750}}details p{{margin:8px 0}}.file-link{{font-size:12px;font-weight:700;display:inline-block;margin-top:14px}}.resources{{margin:45px 0 62px;padding:24px;background:#eaf3f0;border-radius:14px}}.resource-links{{display:flex;gap:16px;flex-wrap:wrap}}.resource-links a{{font-size:13px;font-weight:700}}.footer{{text-align:center;color:#69857e;padding:12px 0 35px;font-size:12px}}.empty{{display:none;color:var(--muted);padding:32px 0}}
@media(max-width:1080px){{.card-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.motif-grid{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}@media(max-width:650px){{.shell{{padding:0 17px}}.hero-inner{{padding:26px 0}}.navinner{{gap:14px}}.navright{{display:none}}.motif-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.card-grid{{grid-template-columns:1fr}}.card h3{{min-height:0}}.section-head{{display:block}}.filters input{{width:100%}}h1{{font-size:38px}}}}
@page{{size:A4;margin:13mm 11mm}}@media print{{:root{{--canvas:#fff;--shadow:none}}body{{font-size:11px!important;background:#fff}}.shell{{padding:0}}.hero-inner{{padding:4mm 0 6mm}}h1{{font-size:27px}}.brandline{{margin-bottom:9px}}.logo-wrap{{width:80px;height:48px}}.hero-intro{{font-size:11px;margin:0 0 12px}}.navbar,.filters,.reset{{display:none!important}}.disclaimer{{margin-top:12px;padding:9px;font-size:10px}}.stat{{font-size:10px;padding:4px 8px}}section{{padding-top:14px}}.section-head{{margin-bottom:11px}}h2{{font-size:18px}}.section-desc{{font-size:10px}}.motif-grid{{grid-template-columns:repeat(5,1fr);gap:5px}}.motif{{padding:6px;border-radius:5px;break-inside:avoid}}.motif .diagram{{height:53px}}.motif-meta b{{font-size:9px}}.motif-meta span{{display:none}}.card-grid{{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}}.card{{padding:10px;border-radius:8px;box-shadow:none;break-inside:avoid;page-break-inside:avoid}}.card h3{{font-size:14px;min-height:0;margin-bottom:6px}}.card-top{{margin-bottom:3px}}.entry-id,.entry-family{{font-size:9px}}.diagram-panel{{padding:4px;margin-bottom:5px}}.diagram{{max-height:75px}}.diagram-panel figcaption{{font-size:8px}}.card-description{{font-size:9px;min-height:0;margin-bottom:5px}}.structure-caption{{font-size:9px;padding:6px 7px}}.field-title{{font-size:8px;margin-bottom:2px}}.card-examples{{margin:6px 0}}.token{{font-size:8px;padding:1px 4px}}details{{font-size:9px;padding-top:5px}}details summary{{list-style:none;color:var(--brand)}}details summary::-webkit-details-marker{{display:none}}details>p,details>ul{{display:block!important}}.file-link{{font-size:8px;margin-top:5px}}.resources{{padding:12px;margin:18px 0 0}}.footer{{padding:10px}}.profile-card,.arch-card{{break-inside:avoid}}.diagram .node-label{{font-size:16px}}}}
</style></head>
<body><header class="hero" id="accueil"><div class="shell hero-inner"><div class="brandline"><span class="logo-wrap"><img src="../assets/logo-k.svg" alt="Supplied K brand mark" width="108" height="52"></span><span><span class="brand-word">ARKETYPE</span><br><span class="brand-subtitle">Kristal · structure library</span></span></div><span class="eyebrow">Structural archetypes · English edition 1.3.0</span><h1>A structure for every kind of knowledge.</h1><p class="hero-intro">Explore linear, branching, clustered, layered and casefile Kristal structures with situated diagrams, practical use cases, and neutral templates linked to the JSON inventory.</p><div class="statline"><span class="stat"><b>{len(index)}</b>archetypes</span><span class="stat"><b>{len(profiles)}</b>use-case profiles</span><span class="stat"><b>{len(patterns)}</b>visual patterns</span><span class="stat"><b>14</b>assemblies</span></div></div></header>
<nav class="navbar"><div class="shell navinner"><a href="#motifs">Patterns</a><a href="#archetypes">Archetypes</a><a href="#profils">Use cases</a><a href="#inventaires">JSON inventories</a><span class="navright">Offline local catalogue</span></div></nav><main class="shell">
<div class="disclaimer"><strong>A visualization is not canon.</strong> These diagrams are <em>fictional design examples</em>, not Logical Contracts, factual evidence, or authorized procedures. Real domains must define their sources, ownership boundaries, access rights, and qualification.</div>
<section id="motifs"><div class="section-head"><div><h2>10 structural patterns</h2><p class="section-desc">One consistent visual grammar applied across archetypes and situated use-case profiles.</p></div></div><div class="motif-grid">{''.join(motif_cells)}</div></section>
<section id="archetypes"><div class="section-head"><div><h2>Archetypes</h2><p class="section-desc">Fundamental structures, each with a labeled fictional example and no real domain data.</p></div></div><div class="filters"><label for="search-arch">Search</label><input id="search-arch" type="search" placeholder="e.g., diagnosis, timeline, taxonomy…"><label for="family-filter">Family</label><select id="family-filter"><option value="">All families</option>{''.join('<option value="'+tx(f)+'">'+tx(f)+'</option>' for f in sorted({x['family'] for x in index}))}</select><label for="pattern-filter">Motif</label><select id="pattern-filter"><option value="">All patterns</option>{''.join('<option value="'+tx(p['id'])+'">'+tx(p['label'])+'</option>' for p in patterns)}</select><button type="button" class="reset" id="reset-filters">Reset</button><span class="filter-count" id="arch-count" aria-live="polite">{len(index)} results</span></div><div class="card-grid" id="arch-grid">{''.join(arch_cards)}</div><p class="empty" id="arch-empty">No archetypes match the current filters.</p></section>
<section id="profils"><div class="section-head"><div><h2>Situated use cases</h2><p class="section-desc">Five illustrative compositions connecting abstract structures to practical scenarios.</p></div></div><div class="card-grid" id="profile-grid">{''.join(profile_cards)}</div></section>
<section id="inventaires" class="resources"><h2>JSON remains the source</h2><p class="section-desc">This offline catalogue is generated from the linked JSON inventories. Run <code>python arketype.py build-html</code> after editing a source file.</p><div class="resource-links"><a href="../catalogue.json">Catalogue index ↗</a><a href="../inventaires/archetypes-visuels.json">Visual archetype index ↗</a><a href="../inventaires/profils-usage.json">Profiles ↗</a><a href="../inventaires/grammaire-visuelle.json">Grammar ↗</a><a href="../inventaires/diagrammes-situes.json">Situated diagrams ↗</a></div></section><footer class="footer">Arketype 1.3.0 · Fictional diagrams, neutral templates · Brand #1E6864 · User-supplied logo</footer></main>
<script>
(()=>{{const a=document.querySelectorAll('.arch-card'),s=document.getElementById('search-arch'),f=document.getElementById('family-filter'),p=document.getElementById('pattern-filter'),c=document.getElementById('arch-count'),empty=document.getElementById('arch-empty');
function norm(t){{return (t||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase()}}function update(){{let n=0;for(const card of a){{const visible=(!s.value||norm(card.dataset.search).includes(norm(s.value)))&&(!f.value||card.dataset.family===f.value)&&(!p.value||card.dataset.pattern===p.value);card.hidden=!visible;if(visible)n++}}c.textContent=n+' result'+(n>1?'s':'');empty.style.display=n?'none':'block'}}
[s,f,p].forEach(e=>e.addEventListener('input',update));document.getElementById('reset-filters').addEventListener('click',()=>{{s.value='';f.value='';p.value='';update();s.focus()}});window.addEventListener('beforeprint',()=>{{for(const card of a)card.hidden=false;document.querySelectorAll('details').forEach(d=>d.open=true)}});window.addEventListener('afterprint',()=>{{document.querySelectorAll('details').forEach(d=>d.open=false);update()}});}})();
</script></body></html>'''
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(html,encoding='utf-8')
    return output
