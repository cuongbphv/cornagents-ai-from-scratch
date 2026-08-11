"""
agents.py — STUB Tuần 13. 3 agent SDLC + chỗ nối orchestration.

Mỗi agent là một hàm nhận input có cấu trúc, trả output có cấu trúc.
Triển khai thật bằng Claude Agent SDK / LangGraph; ở đây định nghĩa
CONTRACT (input/output) + prompt, để bạn nối dây.

Cài: pip install anthropic   (hoặc claude-agent-sdk / langgraph)
"""

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------
# Contract dữ liệu giữa các stage
# ---------------------------------------------------------------
@dataclass
class Requirement:
    feature_request: str
    domain_context: str = ""          # đoạn RAG từ Tuần 10–11 (tài liệu nghiệp vụ)


@dataclass
class Stories:
    user_stories: list = field(default_factory=list)
    acceptance_criteria: list = field(default_factory=list)


@dataclass
class ReviewResult:
    issues: list = field(default_factory=list)        # {severity, file, note}
    approved: bool = False


@dataclass
class TestSuite:
    tests: list = field(default_factory=list)


# ---------------------------------------------------------------
# Agent 1 — Requirements Analyst (thế mạnh BA + RAG grounding)
# ---------------------------------------------------------------
REQ_PROMPT = """Bạn là Business Analyst trong lĩnh vực Finance Banking.
Dựa trên feature request và ngữ cảnh domain (tài liệu nghiệp vụ nội bộ),
hãy sinh: (1) user stories dạng "As a..., I want..., so that...",
(2) acceptance criteria dạng Given/When/Then. Bám sát ngữ cảnh, không bịa."""


def requirements_agent(req: Requirement) -> Stories:
    # TODO: gọi LLM với REQ_PROMPT + req.feature_request + req.domain_context
    #   parse output thành Stories(user_stories=[...], acceptance_criteria=[...])
    raise NotImplementedError("TODO: requirements_agent")


# ---------------------------------------------------------------
# Agent 2 — Code Review
# ---------------------------------------------------------------
REVIEW_PROMPT = """Bạn là reviewer cẩn thận. Đọc diff và liệt kê issue
theo severity (high/med/low): bug, lỗ hổng bảo mật, style. Kết luận approved hay không."""


def code_review_agent(diff: str) -> ReviewResult:
    # TODO: gọi LLM với REVIEW_PROMPT + diff -> parse thành ReviewResult
    raise NotImplementedError("TODO: code_review_agent")


# ---------------------------------------------------------------
# Agent 3 — Test Generation
# ---------------------------------------------------------------
TEST_PROMPT = """Sinh test case (pytest) phủ acceptance criteria và biên/lỗi.
Mỗi test có tên rõ nghĩa + assertion cụ thể."""


def test_gen_agent(stories: Stories, code: Optional[str] = None) -> TestSuite:
    # TODO: gọi LLM với TEST_PROMPT + stories (+ code nếu có) -> TestSuite
    raise NotImplementedError("TODO: test_gen_agent")


# ---------------------------------------------------------------
# Orchestration + Human-in-the-loop gate
# ---------------------------------------------------------------
def human_gate(stage_name: str, payload) -> bool:
    """Cổng phê duyệt: in payload, hỏi người dùng approve. Production: thay bằng UI/Slack."""
    print(f"\n=== HUMAN GATE: {stage_name} ===")
    print(payload)
    return input("Approve? [y/N] ").strip().lower() == "y"


def run_workflow(req: Requirement):
    stories = requirements_agent(req)
    if not human_gate("Requirements", stories):
        return "Dừng ở gate Requirements."

    tests = test_gen_agent(stories)
    if not human_gate("Tests", tests):
        return "Dừng ở gate Tests."

    # (review chạy khi có code/PR thực tế)
    return {"stories": stories, "tests": tests}


if __name__ == "__main__":
    demo = Requirement(
        feature_request="Thêm kiểm tra tự động phát hiện discrepancy trong bộ chứng từ LC",
        domain_context="(đoạn RAG tài liệu nghiệp vụ sẽ được chèn ở đây)",
    )
    print("Stub Tuần 13 — điền TODO trong từng agent rồi chạy run_workflow().")
