"""Animated learning diagrams. Standard library only; preserves original 01–07 SVGs."""
from pathlib import Path
from html import escape
import json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
C = dict(ink='#13263e', muted='#52677f', bg='#f3f7fc', line='#cad8e8',
         teal='#0d9488', blue='#2563eb', cyan='#0891b2', purple='#9333ea', gold='#d97706', green='#16805a')
ART = []

def text(x,y,label,size=18,weight=500,color=None,anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color or C["ink"]}" text-anchor="{anchor}">{escape(label)}</text>'

def rect(x,y,w,h,fill='#fff',stroke=None,r=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'

def path(d,color,width=3,arrow=False,dash=None):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"'+(' marker-end="url(#arrow)"' if arrow else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'

def flow(d,color,animated,duration=12,begin=0):
    # The route remains visible in static renders and with reduced motion.
    out=path(d,color,3,True)
    if animated:
        out+=f'<g class="motion"><circle r="6" fill="{color}" stroke="#fff" stroke-width="2"><animateMotion dur="{duration}s" begin="{begin}s" repeatCount="indefinite" path="{d}"/></circle></g>'
    return out

def icon(kind,x,y,color):
    start=f'<g transform="translate({x} {y})" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
    if kind==0:shape=''.join(f'<rect x="{a*12}" y="{b*12}" width="7" height="7" rx="2"/>' for a in range(3) for b in range(3))
    elif kind==1:shape='<path d="M0 4H30M0 16H30M0 28H30M5 0V32M25 0V32"/><circle cx="15" cy="16" r="6" fill="#fff"/>'
    elif kind==2:shape='<rect x="2" y="0" width="22" height="31" rx="3"/><path d="M8 8H18M8 14H18M8 20H14"/><circle cx="25" cy="25" r="7" fill="#fff"/><path d="M30 30L35 35"/>'
    elif kind==3:shape='<circle cx="16" cy="16" r="8"/><circle cx="0" cy="0" r="3"/><circle cx="32" cy="0" r="3"/><circle cx="0" cy="32" r="3"/><circle cx="32" cy="32" r="3"/><path d="M3 3L10 10M22 10L29 3M3 29L10 22M22 22L29 29"/>'
    else:shape='<path d="M16 32V12M16 20C0 20 0 3 16 12M16 16C32 16 32 0 16 8"/><path d="M3 32H29"/>'
    return start+shape+'</g>'

def shell(w,h,title,desc,body,animated):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L8 4L0 8" fill="{C['muted']}"/></marker>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#b5c8dd" opacity=".26"/></pattern></defs>
<style>text{{font-family:"Segoe UI",Arial,sans-serif}} .station{{animation:breathe 10s ease-in-out infinite}} @keyframes breathe{{0%,70%,100%{{stroke-opacity:.35}}35%{{stroke-opacity:1}}}} @media(prefers-reduced-motion:reduce){{.motion{{display:none}}.station{{animation:none}}}}</style>
{rect(0,0,w,h,C['bg'],r=24)}<rect width="{w}" height="{h}" fill="url(#grid)" rx="24"/>
{body}
</svg>'''


def write(name,title,desc,builder,w,h):
    for animated,suffix in [(True,''),(False,'-static')]:
        svg=shell(w,h,title,desc,builder(animated),animated)
        if not animated:svg=svg.replace('.station{animation:breathe 10s ease-in-out infinite}', '.station{animation:none}')
        (OUT/(name+suffix+'.svg')).write_text(svg)
    ART.append(dict(name=name,title=title,width=w,height=h,desc=desc))


def journey(animated):
    cols=[('1–4','Nền toán & phép đo','Task, baseline, gradient','Manifest + phép kiểm',C['teal']),
          ('5–14','Hiểu nội tại LLM','Autograd, Transformer','Code lõi + loss log',C['blue']),
          ('15–18','Retrieval & tài liệu','Nguồn, số, đơn vị','Evidence + báo cáo lỗi',C['cyan']),
          ('19–24','Agent & capstone','Tools, quota, recovery','Failure tests + capstone',C['purple']),
          ('25–36','Nghiên cứu & học','Lesson, eval, rollback','R01–R12 + protocol',C['gold'])]
    out=text(48,58,'CornAgents.AI',24,700,C['teal'])+text(48,112,'Từ một phép tính đến một vòng nghiên cứu',36,750)
    out+=text(48,149,'24 tuần nền tảng + 12 tuần nghiên cứu · Mỗi chặng để lại một sản phẩm để kiểm.',19,color=C['muted'])
    out+=path('M150 260H1050',C['line'],9)+flow('M150 260H1050',C['blue'],animated,16)
    for i,(weeks,title,learn,deliver,color) in enumerate(cols):
        x=48+i*224;cx=x+104
        out+=icon(i,cx-16,190,color)
        out+=f'<circle cx="{cx}" cy="260" r="16" fill="#fff" stroke="{color}" stroke-width="4" class="station" style="animation-delay:{i*1.7}s"/>'
        out+=f'<circle cx="{cx}" cy="260" r="5" fill="{color}"/>'
        out+=rect(x,302,208,163,'#fff',C['line'])+rect(x+16,318,90,29,color,r=8)
        out+=text(x+61,339,'Tuần '+weeks,16,650,'#fff','middle')+text(x+16,382,title,19,700)
        out+=text(x+16,414,learn,15,color=C['muted'])+text(x+16,442,deliver,15,650,color)
    out+=text(48,509,'Tự viết  →  Gây lỗi  →  Đo  →  Giải thích  →  Thử bài mới',22,650)
    out+=text(48,541,'Hình mô tả lịch học; chuyển động không biểu thị tiến độ hoặc kết quả đã đạt.',16,color=C['muted'])
    return out


def mobile_journey(animated):
    out=text(32,52,'CornAgents.AI',27,700,C['teal'])+text(32,92,'Hành trình 36 tuần',32,750)
    out+=text(32,128,'24 tuần nền + 12 tuần nghiên cứu',20,color=C['muted'])
    out+=path('M62 208V970',C['line'],7)+flow('M62 208V970',C['blue'],animated,16)
    cols=[('1–4','Nền toán và phép đo','Task, baseline, gradient','Manifest + phép kiểm',C['teal']),('5–14','Hiểu nội tại LLM','Autograd, Transformer','Code lõi + loss log',C['blue']),('15–18','Retrieval và tài liệu','Evidence, số, đơn vị','Nguồn + báo cáo lỗi',C['cyan']),('19–24','Agent và capstone','Tools, quota, recovery','Failure tests + capstone',C['purple']),('25–36','Nghiên cứu và học','Lesson, eval, rollback','R01–R12 + protocol',C['gold'])]
    for i,(week,title,learn,deliver,color) in enumerate(cols):
        y=178+i*180
        out+=f'<circle cx="62" cy="{y+48}" r="14" fill="#fff" stroke="{color}" stroke-width="4"/>'
        out+=rect(98,y,466,150,'#fff',C['line'])+text(120,y+31,'Tuần '+week,20,700,color)+text(120,y+65,title,26,700)+text(120,y+98,learn,21,color=C['muted'])+text(120,y+130,deliver,21,650,color)
    out+=text(32,1120,'Tự viết · Gây lỗi · Đo · Giải thích',23,650)+text(32,1157,'Motion minh họa, không phải tiến độ thực.',19,color=C['muted'])
    return out


def node(x,y,w,title,sub,color):
    return rect(x,y,w,92,'#fff',C['line'])+rect(x,y,5,92,color,r=2)+text(x+16,y+34,title,20,700)+text(x+16,y+64,sub,16,color=C['muted'])


def cornloop(animated):
    out=text(48,56,'CornLoop',26,700,C['purple'])+text(48,104,'Nghiên cứu, học và kiểm soát: ba vòng riêng',34,750)
    out+=rect(48,149,760,255,'#eaf3fb')+text(72,184,'Vòng nhiệm vụ',23,700,C['blue'])+text(292,184,'Tìm điều đúng trong phạm vi đã giao',17,color=C['muted'])
    specs=[('Câu hỏi','Scope + budget'),('Tìm nguồn','Evidence ledger'),('Thử & kiểm','Lưu cả lần sai'),('Kết luận','Nêu giới hạn')]
    for i,(title,sub) in enumerate(specs):
        x=72+i*181;out+=node(x,218,166,title,sub,C['blue'])
        if i<3:out+=flow(f'M{x+166} 264H{x+180}',C['blue'],animated,4,i)
    out+=flow('M698 318V353H155V317',C['blue'],animated,14)
    out+=text(344,381,'Còn câu hỏi? Lặp trong budget; hết thì dừng.',16,color=C['muted'])
    out+=rect(842,149,310,255,'#fff',C['purple'])+text(866,184,'Vòng kiểm soát',23,700,C['purple'])
    out+=text(866,222,'Quyền · quota · hủy · thu hồi',18,650)+text(866,254,'Kiểm bên ngoài model',18,color=C['muted'])
    out+=text(866,291,'Evaluator độc lập',19,700)+text(866,323,'Duyệt đúng digest và scope',18,color=C['muted'])
    out+=text(866,378,'Agent đề nghị; không tự duyệt.',17,650,C['purple'])
    out+=path('M842 279H811',C['purple'],3,True,'6 6')
    out+=flow('M430 404V465',C['cyan'],animated,5)+text(451,443,'Trải nghiệm có nguồn',17,color=C['muted'])
    out+=rect(48,466,1104,167,'#ecf7f1')+text(72,500,'Vòng học',23,700,C['green'])+text(214,500,'Thay đổi nhỏ, giữ riêng để kiểm',17,color=C['muted'])
    specs=[('Nhận diện lỗi','Không học đáp án test'),('Đề nghị lesson','Điều kiện + phản ví dụ'),('Đánh giá','Task mới + retention'),('G3: xét thay đổi','Đủ bằng chứng mới duyệt')]
    for i,(title,sub) in enumerate(specs):
        x=72+i*275;out+=node(x,522,252,title,sub,C['green'])
        if i<3:out+=flow(f'M{x+252} 568H{x+274}',C['green'],animated,5,i)
    out+=path('M997 404V464',C['purple'],3,True,'6 6')
    gates=[('G1 · Người học','Tự giải thích và sửa lỗi',C['blue']),('G2 · Hệ thống','Outcome có bằng chứng',C['cyan']),('G3 · Bản cải tiến','Đúng bản, đúng phạm vi',C['purple'])]
    for i,(title,sub,color) in enumerate(gates):
        x=48+i*374;out+=text(x,688,title,22,700,color)+text(x,720,sub,19,color=C['muted'])
    out+=text(48,760,'Ba cửa không bù điểm cho nhau. Đây là thiết kế, không phải bằng chứng agent đã tự học hiệu quả.',16,color=C['muted'])
    return out


def lifecycle(animated):
    out=text(48,58,'Từ đề nghị đến bản được phép dùng',35,750)+text(48,96,'Một thay đổi cần bằng chứng gắn đúng nội dung, phạm vi và phiên bản.',20,color=C['muted'])
    specs=[('Candidate','Snapshot + digest',C['gold']),('Quarantine','Chờ kiểm chứng',C['cyan']),('Eval độc lập','Task mới + retention',C['blue']),('Duyệt G3','Đúng digest + scope',C['purple']),('Dùng có giới hạn','Shadow / canary trước',C['green'])]
    for i,(title,sub,color) in enumerate(specs):
        x=48+i*224;out+=node(x,168,204,title,sub,color)
        if i<4:out+=flow(f'M{x+204} 214H{x+222}',color,animated,6,i)
    out+=flow('M600 270V326H365V271',C['gold'],animated,9)
    out+=text(482,311,'Chưa đủ bằng chứng',17,650,C['gold'],'middle')
    out+=path('M1046 270V371H770',C['purple'],3,True,'6 6')
    out+=text(766,363,'Sự cố: rollback / revoke',18,650,C['purple'],'end')
    out+=text(48,410,'Rollback đổi bản đang dùng. Revoke thu hồi quyền/nguồn; không tự hoàn tác tác động bên ngoài.',17,color=C['muted'])
    out+=text(48,448,'Mũi tên mô tả quy trình. Mỗi bước có thể dừng hoặc bị từ chối; không phải luồng tự động qua môn.',16,color=C['muted'])
    return out


def main():
    curriculum=json.loads((ROOT/'curriculum.json').read_text())
    assert [w['week'] for w in curriculum['weeks']]==list(range(1,37))
    assert [[w['week'] for w in curriculum['weeks'] if w['phase']==n] for n in range(5)]==[list(range(1,5)),list(range(5,15)),list(range(15,19)),list(range(19,25)),list(range(25,37))]
    write('08-learning-journey','CornAgents.AI: hành trình 36 tuần','Năm chặng: tuần 1–4 phép đo và toán; 5–14 nội tại LLM; 15–18 retrieval và tài liệu; 19–24 agent và capstone; 25–36 nghiên cứu và học. Motion chỉ minh họa hướng học.',journey,1200,572)
    write('08-learning-journey-mobile','CornAgents.AI: hành trình 36 tuần, bản dọc','Cùng năm chặng của lịch học, bố cục dọc để đọc trên màn hình nhỏ.',mobile_journey,600,1190)
    write('09-cornloop','CornLoop: ba vòng và ba cửa','Vòng nhiệm vụ và vòng học chịu quyền, quota, hủy, thu hồi, evaluator độc lập và duyệt bên ngoài model. G1 người học; G2 hệ thống; G3 bản cải tiến.',cornloop,1200,790)
    write('10-candidate-lifecycle','Vòng đời bản cải tiến','Candidate đến quarantine, eval độc lập, duyệt G3 rồi dùng trong phạm vi. Thiếu bằng chứng giữ riêng; sự cố cần rollback hoặc revoke.',lifecycle,1200,480)
    (OUT/'motion-manifest.json').write_text(json.dumps(dict(source='curriculum.json',scope='Conceptual diagrams, not runtime progress or performance measurements',art=ART),ensure_ascii=False,indent=2)+'\n')
    print('Wrote 4 animated SVGs and 4 static variants; original 01–07 assets untouched.')

if __name__=='__main__':main()
