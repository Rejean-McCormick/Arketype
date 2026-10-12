"""Build an A4 PDF edition from Arketype JSON (offline, noncanonical)."""
from __future__ import annotations
from pathlib import Path
import json
import sys
from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
import cairosvg

ROOT = Path(__file__).resolve().parent.parent
W,H=A4
BRAND=HexColor('#1E6864')
DARK=HexColor('#172B29')
MUTED=HexColor('#55736E')
PALE=HexColor('#E8F4F0')
BORDER=HexColor('#CFDFDB')

font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('ArketypeRegular',font))
pdfmetrics.registerFont(TTFont('ArketypeBold',bold))


def lines(text:str, maxw:float, size:float, is_bold=False):
    face='ArketypeBold' if is_bold else 'ArketypeRegular'
    res=[]; cur=''
    for word in text.split():
        test=(cur+' '+word).strip()
        if pdfmetrics.stringWidth(test,face,size)>maxw and cur:
            res.append(cur);cur=word
        else:cur=test
    if cur:res.append(cur)
    return res


def print_text(c,text,x,y,maxw,size=8.2,dy=12,color=DARK,maxlines=8,bold=False):
    face='ArketypeBold' if bold else 'ArketypeRegular'
    c.setFont(face,size);c.setFillColor(color)
    li=lines(text,maxw,size,bold)
    for idx,line in enumerate(li[:maxlines]):
        if idx==maxlines-1 and idx<len(li)-1:line=line[:-1]+'…'
        c.drawString(x,y,line);y-=dy
    return y


def logo(c,x,y,w=76):
    png=cairosvg.svg2png(bytestring=(ROOT/'assets/logo-k.svg').read_bytes(),output_width=420)
    image=ImageReader(BytesIO(png))
    c.drawImage(image,x,y,w,w*92/209,mask='auto')


def topbar(c,title='Arketype / Visual catalogue'):
    c.setFillColor(BRAND); c.roundRect(34,H-60,51,43,8,fill=0,stroke=0)
    logo(c,40,H-55,44)
    c.setFillColor(BRAND);c.setFont('ArketypeBold',10);c.drawString(99,H-39,'ARKETYPE')
    c.setFillColor(MUTED);c.setFont('ArketypeRegular',8);c.drawRightString(W-36,H-39,title)
    c.setStrokeColor(BORDER);c.line(38,H-65,W-38,H-65)


def footer(c,page):
    c.setFillColor(MUTED);c.setFont('ArketypeRegular',7)
    c.drawString(40,35,'Non-normative diagrams · no real domain data')
    c.drawRightString(W-40,35,f'Arketype 1.4.0  ·  {page}')


def draw_diagram(c,diag,x,y,scale=0.56):
    node_by={n['id']:n for n in diag['nodes']}
    ox=x+((W-80)-660*scale)/2
    oy=y
    def coord(n):return ox+n['x']*scale,oy+(244-n['y'])*scale
    c.setLineWidth(1.25);c.setStrokeColor(HexColor('#89B2AC'))
    for edge in diag['edges']:
        u=node_by[edge['from']];v=node_by[edge['to']];x1,y1=coord(u);x2,y2=coord(v)
        c.line(x1,y1,x2,y2)
    if diag['pattern']=='matrix':
        c.setStrokeColor(BORDER)
        for col in range(3):
            for row in range(2):
                px=ox+(37+col*195)*scale; py=oy+(244-27-row*97-94)*scale
                c.roundRect(px,py,192*scale,94*scale,3,stroke=1,fill=0)
    for i,n in enumerate(diag['nodes']):
        xx,yy=coord(n)
        bw=(154 if diag['pattern'] in ('casefile','multilayer') else 142)*scale
        bh=44*scale
        fill_anchor=i==0 and diag['pattern'] in ('hub','casefile','network','tree')
        c.setFillColor(BRAND if fill_anchor else HexColor('#F0F8F5'))
        c.setStrokeColor(BRAND)
        c.roundRect(xx-bw/2,yy-bh/2,bw,bh,5,stroke=1,fill=1)
        c.setFont('ArketypeBold',7.0);c.setFillColor(white if fill_anchor else DARK)
        label=n['label']
        lns=lines(label,bw-9,7.0,True)
        if len(lns)>1:
            c.drawCentredString(xx,yy+2.5,lns[0]);c.drawCentredString(xx,yy-6.5,lns[1])
        else:c.drawCentredString(xx,yy-2.7,label)


def card(c,a,d,y_top,profile=False):
    x=40;width=W-80;height=323;y=y_top-height
    c.setFillColor(white);c.setStrokeColor(BORDER)
    c.roundRect(x,y,width,height,10,stroke=1,fill=1)
    c.setFillColor(BRAND);c.setFont('ArketypeBold',8);c.drawString(x+15,y_top-23,a['id'])
    title=a['name']
    print_text(c,title,x+75,y_top-23,width-100,12,14,DARK,2,True)
    desc=a['summary'] if profile else a['description']
    print_text(c,desc,x+15,y_top-45,width-30,8,11,MUTED,2)
    c.setFillColor(HexColor('#F8FBFA'));c.roundRect(x+13,y_top-198,width-26,126,8,fill=1,stroke=0)
    draw_diagram(c,d,x+15,y_top-202,scale=.49)
    c.setFont('ArketypeBold',8);c.setFillColor(BRAND);c.drawString(x+15,y_top-219,'STRUCTURE')
    sit=a['situational_schema']
    print_text(c,sit,x+82,y_top-219,width-99,7.5,10,DARK,3)
    c.setFont('ArketypeBold',8);c.setFillColor(BRAND);c.drawString(x+15,y_top-261,'USE CASES')
    uses=a['use_cases'] if profile else a['canonical_use_cases']
    print_text(c,' · '.join(uses),x+82,y_top-261,width-99,7.3,10,DARK,2)
    c.setFont('ArketypeRegular',7.1);c.setFillColor(MUTED)
    rule='Assembly: '+', '.join([a['primary_archetype'],*a['supporting_archetypes']]) if profile else 'Pattern: '+a['structure_label']
    print_text(c,rule,x+15,y_top-296,width-30,7.1,9,MUTED,2)


def cover(c,patterns,arch_count,profile_count):
    topbar(c,'Structures · patterns · use cases')
    c.setFillColor(BRAND);c.setFont('ArketypeBold',30);c.drawString(40,H-118,'Visual catalogue')
    c.setFont('ArketypeBold',18);c.drawString(40,H-146,'of Kristals')
    print_text(c,'Different knowledge structures deserve distinct shapes. Explore archetypes, situated examples, and one common visual grammar.',40,H-174,W-80,10.6,16,MUTED,3)
    c.setFillColor(PALE);c.roundRect(40,H-247,W-80,47,8,fill=1,stroke=0)
    print_text(c,f'{arch_count} archetypes    ·    {profile_count} profiles    ·    {len(patterns)} visual patterns    ·    14 assemblies',55,H-226,W-100,11,16,BRAND,2,True)
    c.setFont('ArketypeBold',14);c.setFillColor(DARK);c.drawString(40,H-276,'The visual grammar')
    y=H-303
    for i,p in enumerate(patterns):
        if i%2==0:
            c.setFillColor(HexColor('#F3F7F5'));c.roundRect(40,y-10,W-80,35,5,fill=1,stroke=0)
        c.setFillColor(BRAND);c.setFont('ArketypeBold',10);c.drawString(53,y+7,p['label'])
        print_text(c,p['description'],255,y+7,W-305,8.1,11,MUTED,2)
        y-=42
    c.setFillColor(BRAND);c.setFont('ArketypeBold',9);c.drawString(40,96,'Reading / integrity')
    print_text(c,'The diagrams are fictional specimens, not evidence, Logical Contracts, or authorized decisions. Sources, access rights, and ownership boundaries belong to real Kristal instances.',40,78,W-80,8.5,12,MUTED,3)
    footer(c,1);c.showPage()


def main():
    index=json.loads((ROOT/'inventaires/archetypes-visuels.json').read_text())['archetypes']
    profiles=json.loads((ROOT/'inventaires/profils-usage.json').read_text())['profiles']
    patterns=json.loads((ROOT/'inventaires/grammaire-visuelle.json').read_text())['patterns']
    diagrams=json.loads((ROOT/'inventaires/diagrammes-situes.json').read_text())['diagrams']
    dmap={(d['kind'],d['slug']):d for d in diagrams}
    a=sorted([{**x,**json.loads((ROOT/x['file']).read_text())} for x in index],key=lambda x:int(x['id'].split('-')[1]))
    objects=[('archetype',v) for v in a]+[('profile',v) for v in profiles]
    target=ROOT/'catalogue/Arketype_Visual_Catalogue_v1.4.0.pdf'
    c=Canvas(str(target),pagesize=A4,pageCompression=1)
    c.setTitle('Arketype — Visual Kristal Catalogue v1.4.0')
    c.setAuthor('Arketype')
    cover(c,patterns,len(a),len(profiles))
    page=2
    for i in range(0,len(objects),2):
        topbar(c,'Archetypes' if i<len(a) else 'Situated profiles')
        for j,(kind,d) in enumerate(objects[i:i+2]):
            diagram=dmap[(kind,d['slug'])]
            card(c,d,diagram,H-88-j*348,profile=kind=='profile')
        footer(c,page);c.showPage();page+=1
    c.save()
    print(target, page-1)

if __name__=='__main__':main()
