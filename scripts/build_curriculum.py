#!/usr/bin/env python3
"""Render authored curriculum metadata into weekly materials and portal data.

Source: curriculum.json. Quiz and theory JS still use their respective generators.
Existing fast-track folders and progress keys are not overwritten here.
"""
import html
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAB_SLUGS = ['research-contract', 'bounded-research', 'governed-memory', 'conditional-lessons',
             'candidate-search', 'experiment-design', 'risk-coverage', 'evaluator-boundary',
             'offline-learning', 'durable-research', 'promotion', 'cornbench-learning']
# Scope-limited excerpts, not a claim to have independently reproduced the sources.
SUBSECTIONS = {
    1:['3.1','10.1'],2:['7.1','7.2'],3:['16.1'],4:['7.6'],5:['16.1'],6:['6.5'],
    7:['6.2'],8:['7.6'],9:['16.1'],10:['10.6'],11:['7.6','5.5'],12:['16.3'],
    13:['11.3'],14:['6.3','11.4'],15:['6.1','6.5'],16:['5.1'],17:['13'],18:['17.4'],
    19:['4.3','10.4'],20:['4.2','4.4'],21:['4.5'],22:['7.7'],23:['12.4','12.5'],24:['3.4','18.1'],
    25:['3.1','5.1'],26:['3.1'],27:['5.2','5.3'],28:['5.4','11.6'],29:['6.4','11.2'],
    30:['6.4','16.3'],31:['7.2','7.3','7.5'],32:['7.6','7.7'],33:['11.3','11.6'],
    34:['4.4','4.5'],35:['14.1','14.2','14.5'],36:['12.3','12.4','12.5','18.1']}


def rel(directory, target):
    return os.path.relpath(ROOT / target, ROOT / directory).replace(os.sep, '/')


def excerpt(source, key):
    pattern = (rf'^## {re.escape(key)}\. .*?\n(.*?)(?=^<a id=|^## |\Z)' if '.' not in key else
               rf'^### {re.escape(key)}\. .*?\n(.*?)(?=^### |^<a id=|^## |\Z)')
    match = re.search(pattern, source, re.M | re.S)
    if not match:
        raise ValueError(f'Missing source section {key}')
    text = match[1].strip().removesuffix('---').strip()
    text = re.sub(r'\bv3\b', 'tài liệu chương trình', text, flags=re.I)
    text = re.sub(r'\bv2\b', 'chương trình nền tảng', text, flags=re.I)
    return text


def preserve_write(path, text):
    # Generated scaffolds must never erase a learner's work.
    if not path.exists():
        path.write_text(text)


def main():
    curriculum = json.loads((ROOT/'curriculum.json').read_text())
    section_files = json.loads((ROOT/curriculum['source']).read_text())
    chunks = []
    for key in sorted(section_files, key=int):
        document = (ROOT/section_files[key]).read_text()
        match = re.search(rf'^## {key}\. .*?(?=^<a id=|^\[S\d+\]:|\Z)', document, re.M | re.S)
        if not match:
            raise ValueError(f'Missing section {key} in {section_files[key]}')
        chunks.append(f'<a id="s{key}"></a>\n\n' + match[0].strip())
    source = '\n\n'.join(chunks)
    refs = '\n'.join(re.findall(r'^\[S\d+\]: .*$', (ROOT/curriculum['references']).read_text(), re.M))
    phases = []
    for i,(name,span) in enumerate([('Phép đo và nền toán','1–4'),('Hiểu nội tại','5–14'),
            ('Retrieval và tài liệu','15–18'),('Agent và capstone nền','19–24'),
            ('Nghiên cứu và học có kiểm soát','25–36')]):
        phases.append(dict(id=i,no=f'PHASE {i}',name=name,weeks=f'Tuần {span}',cls=f'p{i}',
                           desc='Bài học và starter đã có. Kết quả học/live-model cần thực hiện và báo cáo riêng.'))
    portal=[]
    for w in curriculum['weeks']:
        n=w['week']; directory=w['directory']; d=ROOT/directory; d.mkdir(parents=True,exist_ok=True)
        refs_local=[f'[{Path(f).parent.name}/{Path(f).name}]({rel(directory,f)})' for f in w['reuse']]
        lab_path=f'labs/r{n-24:02d}-{LAB_SLUGS[n-25]}' if n>=25 else None
        lab_link=f'[{w["lab"]}]({rel(directory,lab_path+"/README.md")})' if lab_path else None
        sections=', '.join(str(x) for x in w['sections'])
        source_link=' · '.join(f'[{(ROOT/f).read_text().splitlines()[0].removeprefix(chr(35)+chr(32))}]({rel(directory, f)})' for f in dict.fromkeys(section_files[str(k)] for k in w['sections']))
        checklist=['Đọc ghi chú và phân biệt claim từ nguồn với đề xuất bài tập.',
                   'Tự viết phần lõi hoặc hoàn thành starter trước khi mở bản tham chiếu.',
                   'Chạy phép kiểm với cả trường hợp đúng, sai và thiếu bằng chứng.',
                   'Lưu cấu hình, output thực và mọi lần thử thất bại.',
                   'Nộp báo cáo, nêu giới hạn và trả lời bài AI-off bằng lời mình.']
        readme=f'''# Tuần {n}: {w['title']}

> CornAgents.AI · Lịch học chính · Phase {w['phase']}. Nguồn: {source_link}, mục {sections}; đọc bản local ngày 30/09/2026.

**Trạng thái:** tài liệu, quiz và starter đã có; bài làm của người học và đánh giá live-model chưa được thực hiện ở đây. Starter có phần cần tự triển khai. Reference offline (nếu dùng) chỉ kiểm các fixture công khai, không phải chứng nhận runtime production.

## Mục tiêu

- {w['principle']}
- Giải thích một phản ví dụ mới mà không nhờ AI làm hộ.
- Ghi rõ bằng chứng phép kiểm cung cấp và phần còn chưa biết.

## Nguồn học

- {source_link}, mục {sections}. Nội dung bên dưới là biên tập từ tài liệu chương trình; bài tập được bổ sung cho repo, chưa phải kết quả nghiên cứu.
'''
        readme+=''.join(f'- {r}\n' for r in refs_local)
        if lab_link: readme+=f'- Lab thực hành: {lab_link}.\n'
        readme+=f'''
## Thứ tự học trong tuần (mở file theo số)

1. [01_theory_notes.md](01_theory_notes.md): cơ chế, phản ví dụ và phần nguồn liên quan.
2. [02_exercise.py](02_exercise.py): starter; viết protocol trong [02_experiment_protocol.md](02_experiment_protocol.md) trước khi chạy.
3. [03_report.md](03_report.md): điền từ output thật; không điền số liệu mẫu như kết quả.
4. [quiz.md](quiz.md), rồi [quiz_solution.md](quiz_solution.md).

## Nhiệm vụ (Task)

{w['practice']}

**Gây lỗi:** {w['trap']}

## Deliverable

Code hoặc artifact thực hành; protocol trước thí nghiệm; output và báo cáo có nguồn/cấu hình. Bài kiểm mới cần mô tả expected outcome và lý do. Chưa chạy thì giữ ô kết quả trống, không ghi pass.

## Tiêu chí qua môn

- **G1 — AI-off:** trả lời và bảo vệ: {w['challenge']}
- **G2 — AI-on:** outcome được xác minh bằng fixture/nguồn/reviewer theo protocol, có cả lỗi và giới hạn.
- **G3 — thay đổi:** nếu đề nghị dùng candidate, phải có snapshot và đánh giá đúng phạm vi; chưa đủ bằng chứng thì chưa promote. Với tuần nền không tạo candidate, ghi “không áp dụng” cho cửa này.

## Thời lượng

{w['duration']}. Đây là giả định thiết kế ở mục 8.1 của nguồn, không cam kết mỗi bài hoàn thành trong thời lượng đó.

## Phần cứng

Bài offline dùng CPU và dữ liệu giả lập. Bài model tái sử dụng có thể cần NumPy/PyTorch hoặc runtime riêng; kiểm môi trường trước khi chạy. Không bắt mua API/GPU lớn; đo tài nguyên khi chọn workload.

## Checklist tiến độ

'''+''.join(f'- [ ] {x}\n' for x in checklist)
        readme+=f'\n## Đi tiếp\n\n[Toàn bộ đường học]({rel(directory, "ENTRYPOINTS.md")}) · [Tri thức tích hợp]({rel(directory, "modules/README.md")})\n\n'
        readme+='''
## File trong folder

| File | Vai trò |
|---|---|
| README.md | Mục tiêu, nguồn, trình tự học và tiêu chí |
| 01_theory_notes.md | Ghi chú và nội dung nguồn được chọn |
| 02_exercise.py | Starter của người học, chưa có lời giải |
| 02_experiment_protocol.md | Mẫu đăng ký phép kiểm trước khi chạy |
| 03_report.md | Mẫu báo cáo, giữ kết quả chưa chạy trống |
| quiz.md / quiz_solution.md | Sinh từ scripts/quiz_bank.json |
'''
        (d/'README.md').write_text(readme)
        notes=f'''# Tuần {n}: {w['title']} — ghi chú lý thuyết

## 1. Câu hỏi của bài

{w['challenge']}

## 2. Cơ chế cần hiểu

{w['principle']}

## 3. Phản ví dụ và lỗi cần chủ động thử

{w['trap']}

## 4. Từ nguyên lý sang bài thực hành

{w['practice']}

Đây là bài tập biên tập cho repo dựa trên {source_link}, không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

'''
        for key in SUBSECTIONS[n]: notes+=f'### Theo mục {key} của tài liệu chương trình\n\n'+excerpt(source,key)+'\n\n'
        notes+='## 6. Tài liệu tái sử dụng\n\n'+('\n'.join('- '+r for r in refs_local) if refs_local else 'Thực hành theo lab của tuần và các mục nguồn ở trên.')
        if lab_link:notes+=f'\n\nMở lab {lab_link}; fixture là dữ liệu giả lập công khai, không phải hidden benchmark.'
        notes+='\n\n## 7. Phạm vi kết luận\n\nTest offline xác nhận trường hợp đã thử, không xác nhận chất lượng model thật, runtime isolation, tính đại diện của dataset hoặc đủ điều kiện production. Không dùng số liệu của paper hay ví dụ trong nguồn để điền score của CornAgents.AI.\n\n'+refs+'\n'
        (d/'01_theory_notes.md').write_text(notes)
        preserve_write(d/'02_exercise.py', f'''"""Tuần {n}: {w['title']}.

Starter của người học; chạy file sẽ báo rõ phần chưa triển khai.
Không gọi API, không chứa secrets, không sinh số liệu benchmark mẫu.
"""

def solve(observation):
    """{w['practice']}"""
    raise NotImplementedError("Tự triển khai theo README và protocol của tuần")


if __name__ == "__main__":
    print("STARTER_ONLY: đọc README, tự triển khai solve và kiểm expected outcome.")
''')
        protocol=f'''# Protocol tuần {n}: {w['title']}

> Điền trước khi chạy. Không thay metric/điều kiện dừng chỉ để có kết quả đẹp.

- Câu hỏi và phạm vi:
- Giả thuyết; kết quả nào bác bỏ giả thuyết:
- Baseline/candidate, phiên bản và digest:
- Nguồn, giấy phép, quyền đọc/quyền train:
- Đơn vị lấy mẫu, quan hệ phụ thuộc:
- Development/calibration/confirmation/retention chia thế nào:
- Biến thay đổi / biến giữ cố định:
- Metric chính, ràng buộc không được bù điểm:
- Budget tổng (kể cả fail/retry), seeds, điều kiện dừng:
- Expected outcome, người/quy tắc xác minh:
- Runtime/code/data/config version:
- Quyền sửa / phần không được sửa:
- Nhãn kết quả: offline fixture / CPU toy / live-model:
'''
        preserve_write(d/'02_experiment_protocol.md', protocol)
        preserve_write(d/'03_report.md', f'''# Báo cáo tuần {n}: {w['title']}

**Trạng thái:** CHƯA CHẠY. Chỉ đổi trạng thái khi có output tương ứng.

## Protocol và nguồn

Liên kết protocol đã chốt, nguồn/phiên bản và phạm vi truy cập thực.

## Kết quả thực tế

| Run ID | Cấu hình/digest | Outcome | Lỗi/từ chối | Thời gian/chi phí thực | Artifact/log |
|---|---|---|---|---|---|

Giữ bảng trống khi chưa đo. Không suy thời gian/chi phí từ máy hoặc paper khác.

## So sánh và phản chứng

Baseline/candidate; số task và mẫu số; cùng budget hay khác gì; kết quả âm; task mới và retention khi có learning. Không có dữ liệu thì ghi chưa đủ bằng chứng.

## G1 / G2 / G3

Nêu bằng chứng cho từng cửa hoặc lý do không áp dụng. Quyết định reject/insufficient/promote cần phạm vi, không gộp vào một điểm.

## Giới hạn và điều chưa biết

Phép kiểm đã xác nhận gì, chưa xác nhận gì; cách chạy lại; lỗi nhãn/nguồn và phần cần người kiểm tra.
''')
        file_url='../'+directory+'/README.md'
        portal.append(dict(n=n,phase=w['phase'],title=w['title'],dur='10–12 giờ (giả định)',hw='CPU/toy; runtime theo bài',directory=directory,
            obj=[html.escape(w['principle']),html.escape('Tự giải thích phản ví dụ và lưu output thực.')],
            src=[f'Tài liệu CornAgents.AI, mục {sections}; bản local đọc 30/09/2026.']+['Tái sử dụng: '+html.escape(x) for x in w['reuse']],
            deliver=html.escape(w['practice'])+f' <a href="{file_url}" data-repo-file="{directory}/README.md">Mở bài học và starter</a>',
            know='<p>'+html.escape(w['trap'])+'</p>',check=checklist))
    out=ROOT/'report/assets/js/curriculum-data.js'
    out.write_text('/* Sinh từ curriculum.json bằng scripts/build_curriculum.py. */\nwindow.CORN_CURRICULUM = '+json.dumps(dict(phases=phases,weeks=portal),ensure_ascii=False)+';\n')
    lines=['# CornAgents.AI — chọn đường học','','Lịch học chính của chương trình: 24 tuần nền tảng và 12 tuần nghiên cứu. Bài học, ghi chú, quiz và starter nằm ở đường dẫn trong bảng; không phải chỉ là bảng mục tiêu. Các thư mục Week-01–18 cấp repo giữ lịch rút gọn trước đó, không quy đổi tiến độ tự động.','','## Lịch học chính','','| Tuần | Bài học | Trạng thái |','|---|---|---|']
    for w in curriculum['weeks']:lines.append(f'| {w["week"]} | [{w["title"]}]({w["directory"]}/README.md) | Tài liệu/starter; kết quả học chưa chạy |')
    lines+=['','## Lịch rút gọn hiện có','','Người có nền ML/systems có thể tái sử dụng Week-01–18 cấp repo theo [bảng quy đổi](Week-00/plan_llm_from_scratch_vi.md). Mở portal với `?track=fast` để giữ checklist cũ. Hoàn thành checklist không tự xác nhận đã đạt lịch học chính.','','## Trạng thái thực thi','','Code tham chiếu của labs dùng fixture công khai và phép kiểm hữu hạn. Starter để người học tự làm. Lab nào có test đã chạy sẽ được ghi trong báo cáo kiểm tra; hệ thống research agent, model training và confirmation live vẫn cần thực hiện riêng.']
    (ROOT/'ENTRYPOINTS.md').write_text('\n'.join(lines)+'\n')
    print(f'Generated {len(portal)} weekly material sets, entrypoints and portal metadata.')

if __name__=='__main__':main()
