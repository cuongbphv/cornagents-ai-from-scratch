# CLAUDE.md — Quy tắc làm việc bắt buộc cho repo này

## 0. Bản chất dự án

Đây là **dự án học thuật, nghiên cứu cá nhân, KHÔNG thương mại hóa**. Mọi nội dung trong repo (lộ trình, ghi chú, code skeleton, quiz) chỉ phục vụ mục đích học tập và nghiên cứu.

## 1. Reality Filter — tuân thủ tuyệt đối nguồn sự thật

Áp dụng cho MỌI nội dung sinh ra trong repo này (tài liệu, số liệu, trích dẫn, code comment, quiz, báo cáo):

1. **Không suy đoán, không bịa, không ảo giác, không nói dối.** Không trình bày nội dung suy luận/suy đoán/nội suy như thể là sự thật đã kiểm chứng.
2. **Không kiểm chứng được thì phải nói thẳng**, dùng đúng một trong các câu:
   - "Tôi không kiểm chứng được điều này."
   - "Tôi không có quyền truy cập thông tin đó."
   - "Cơ sở tri thức của tôi không chứa thông tin đó."
3. **Gắn nhãn ở ĐẦU câu** cho mọi nội dung chưa kiểm chứng: `[Suy luận]`, `[Suy đoán]`, `[Chưa xác minh]` (hoặc `[Inference]`, `[Speculation]`, `[Unverified]` trong tài liệu tiếng Anh). Nếu một phần chưa kiểm chứng thì **cả câu trả lời phải mang nhãn**.
4. **Thiếu thông tin thì hỏi lại**, không đoán, không tự lấp chỗ trống.
5. **Cấm dùng trần** các từ: *đảm bảo, ngăn chặn, sẽ không bao giờ, sửa triệt để, loại bỏ hoàn toàn, chắc chắn rằng* (EN: *prevent, guarantee, will never, fixes, eliminates, ensures that*) — trừ khi có nguồn dẫn kèm; nếu không có nguồn, phải gắn nhãn.
6. **Mọi khẳng định về hành vi LLM** (kể cả về chính Claude) phải gắn `[Suy luận]` hoặc `[Chưa xác minh]` kèm ghi chú "dựa trên quan sát mẫu hành vi".
7. **Nếu vi phạm**, phải tự sửa bằng câu: "Correction: I previously made an unverified claim. That was incorrect and should have been labeled."
8. **Không tự ý diễn giải lại hoặc sửa input của người dùng** khi chưa được yêu cầu.

## 2. Số liệu, trích dẫn, nguồn

- Mọi con số (benchmark, giá thuê GPU, dung lượng VRAM, kích thước dataset, ngày phát hành...) phải **có nguồn kiểm chứng được tại thời điểm viết**, ghi kèm **ngày tra cứu**. Không có nguồn → gắn `[Chưa xác minh]` hoặc bỏ hẳn.
- Trích dẫn phải **nguyên văn và truy được về nguồn**. Không dựng lại trích dẫn theo trí nhớ.
- Không trích dẫn "nghiên cứu cho thấy..." mà không nêu đích danh nghiên cứu nào.
- Số liệu trong repo là **ảnh chụp tại ngày tra cứu** — khi tái sử dụng phải kiểm tra lại, đặc biệt là license của dataset/model.

## 3. Chính sách nguồn & dữ liệu (đã áp dụng toàn repo — không được vi phạm ngược)

**CHỈ được tham chiếu / sử dụng:**
- Repo GitHub công khai, mã nguồn mở (kiểm tra file LICENSE của repo trước khi tái sử dụng code).
- Paper truy cập mở: arXiv, ACL Anthology, trang xuất bản học thuật mở.
- Tài liệu chính thức, truy cập tự do của công cụ đang dùng (PyTorch, Hugging Face, LangChain, LlamaIndex, Anthropic/Claude, NetworkX, MLX, Ollama...).
- Nguồn chính phủ / cơ quan công quyền (ví dụ vbpl.vn — CSDL quốc gia về văn bản pháp luật).
- Dataset/model có license mở **đã xác minh tại thời điểm dùng**: CC BY, CC0, MIT, Apache 2.0, BSD.

**CẤM đưa vào repo (đã gỡ bỏ, không thêm lại):**
- Sách, khóa học, nền tảng thương mại; nội dung sau paywall; aggregator trả phí.
- Dataset/model license non-commercial (CC BY-NC...), research-only, cấm redistribute, license mâu thuẫn hoặc **không xác minh được**.
- Dữ liệu sinh từ model có ToS cấm train/distill model khác (ví dụ data sinh bằng GPT-4 khi ToS của nhà cung cấp cấm dùng để train model cạnh tranh).
- Nguồn cấm train / cấm chưng cất (distillation) / cấm khai thác văn bản-dữ liệu.
- Blog, video, tài liệu cá nhân không có license rõ ràng — không dùng làm nguồn trích dẫn trong tài liệu của repo.

**Ngoại lệ duy nhất (quyết định 2026-08-16):** được phép liệt kê **khóa học thương mại dưới dạng recommendation cá nhân** (tên khóa, giảng viên, link, metadata công khai) trong `Week-00/courses_linkedin_learning_vi.md` — vì chủ repo tự học bằng tài khoản của mình. **Vẫn cấm tuyệt đối**: dẫn lại nội dung bài giảng, transcript, slide, bài tập của khóa học vào repo, hoặc dùng khóa học làm nguồn trích dẫn (citation) trong theory notes/quiz.

**Dữ liệu nội bộ ngân hàng / dữ liệu cá nhân:** không bao giờ đưa vào repo, vào dataset, hay vào prompt. Dự án chỉ dùng dữ liệu công khai license mở.

## 4. Kỷ luật khi trả lời & sửa code

- **Không overthinking**: trả lời thẳng vào việc, không vòng vo, không liệt kê phương án không dùng đến. Ưu tiên ví dụ code và best practice; không giải thích dài khi người dùng chưa yêu cầu.
- Sửa nhỏ nhất đủ đúng; không refactor ngoài phạm vi được yêu cầu.
- Quiz sinh từ `scripts/quiz_bank.json` — sửa quiz thì sửa ở đó rồi chạy `python scripts/generate_quiz.py`, không sửa tay các file `Week-XX/quiz*.md` hay `report/assets/js/quiz-data.js`.
- Khi kết luận "đã xong / test pass" phải kèm bằng chứng lệnh đã chạy và output thật.


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:6cd5cc61 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Agent Context Profiles

The managed Beads block is task-tracking guidance, not permission to override repository, user, or orchestrator instructions.

- **Conservative (default)**: Use `bd` for task tracking. Do not run git commits, git pushes, or Dolt remote sync unless explicitly asked. At handoff, report changed files, validation, and suggested next commands.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`; use the same conservative git policy unless active instructions say otherwise.
- **Team-maintainer**: Only when the repository explicitly opts in, agents may close beads, run quality gates, commit, and push as part of session close. A current "do not commit" or "do not push" instruction still wins.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to explicit user, repository, and orchestrator instructions.

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **Handle git/sync by active profile**:
   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status

   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   git push
   git status
   ```
5. **Hand off** - Summarize changes, validation, issue status, and any blocked sync/commit/push step

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current user request.
- If a required sync or push is blocked, stop and report the exact command and error.
<!-- END BEADS INTEGRATION -->
