"""
kg_pipeline.py — SKELETON Tuần 14: Knowledge Graph pipeline bằng Claude API.

Pipeline 4 bước (theo docs/Graph-Engineering-Athropic-Playbook.pdf):
    1. EXTRACTION  (Haiku)  — structured outputs thay trained NER + relation classifier
    2. RESOLUTION  (Sonnet) — cluster surface forms về canonical entity
    3. ASSEMBLY    (NetworkX MultiDiGraph) — node/edge mang provenance
    4. QUERYING    (Sonnet) — serialize k-hop subgraph, trả lời có cite edges

Chỗ TODO là phần bạn điền. Tự code trước, đối chiếu Anthropic
Knowledge Graph Construction Cookbook sau.

Cài đặt: pip install anthropic pydantic networkx
"""

from typing import Literal

import networkx as nx
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic()

EXTRACTION_MODEL = "claude-haiku-4-5-20251001"  # volume lớn, rẻ
REASONING_MODEL = "claude-sonnet-5"  # resolution / summarization / query


# ---------------------------------------------------------------
# 1) Schema — "training data" duy nhất của toàn pipeline.
#    Đổi domain = đổi EntityType, không cần label lại dữ liệu.
# ---------------------------------------------------------------
EntityType = Literal["PERSON", "ORGANIZATION", "LOCATION", "EVENT", "ARTIFACT"]
# TODO: thêm type cho domain Finance Banking của bạn,
#       vd. "REGULATION", "DOCUMENT", "PROCESS", "DISCREPANCY"


class Entity(BaseModel):
    name: str
    type: str
    description: str  # 1 câu, grounded trong tài liệu — chìa khoá cho resolution


class Relation(BaseModel):
    source: str
    predicate: str  # cụm động từ ngắn: "governs", "issued by", "part of"
    target: str


class ExtractedGraph(BaseModel):
    entities: list[Entity]
    relations: list[Relation]


# ---------------------------------------------------------------
# 2) EXTRACTION — precision-first: chỉ entity TRUNG TÂM của tài liệu
# ---------------------------------------------------------------
EXTRACTION_PROMPT = """Extract a knowledge graph from the document below.

<document>
{text}
</document>

Guidelines:
- Extract only entities that are central to what this document is about
  - skip incidental mentions.
- For each entity, write a one-sentence description grounded in this
  document. These descriptions are used later to disambiguate entities
  with similar names.
- Predicates should be short verb phrases ("governs", "issued by").
- Every relation must connect two entities you extracted."""


def extract(text: str) -> ExtractedGraph:
    """Một call duy nhất thay cả NER + relation classifier."""
    # TODO: gọi client.messages.parse(
    #           model=EXTRACTION_MODEL,
    #           messages=[{"role": "user",
    #                      "content": EXTRACTION_PROMPT.format(text=text)}],
    #           output_format=ExtractedGraph,
    #       ) và return response.parsed_output
    raise NotImplementedError


# ---------------------------------------------------------------
# 3) RESOLUTION — cluster surface forms, dùng descriptions làm ngữ cảnh
# ---------------------------------------------------------------
class Cluster(BaseModel):
    canonical: str  # form đầy đủ, ít mơ hồ nhất
    aliases: list[str]  # mọi surface form thuộc cluster


class ResolvedClusters(BaseModel):
    clusters: list[Cluster]


RESOLVE_PROMPT = """Below are {entity_type} entities extracted from several
documents. Some are different surface forms of the same real-world entity.

<entities>
{entity_list}
</entities>

Cluster them. Each input name must appear in exactly one cluster's aliases.
Entities that are genuinely distinct get their own single-element cluster.
Use the descriptions to distinguish entities that merely share a name.
The canonical name should be the most complete, unambiguous form."""


def resolve(entities: list[Entity]) -> dict[str, str]:
    """Trả về alias map: surface form -> canonical name.

    Gợi ý:
    - Group entities theo type, mỗi type một call Sonnet (task nhỏ, tập trung).
    - FALLBACK: tên nào không xuất hiện trong cluster nào -> tự thành
      cluster 1 phần tử (chống "silent entity loss").
    - Ở scale lớn: block bằng tín hiệu rẻ (token trùng, embedding) trước,
      chỉ để Sonnet phân xử trong block 50-100 tên.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------
# 4) ASSEMBLY — mọi edge mang provenance (source_doc)
# ---------------------------------------------------------------
def assemble(
    docs: dict[str, ExtractedGraph], alias_map: dict[str, str]
) -> nx.MultiDiGraph:
    """Rewrite mọi endpoint về canonical form rồi nạp vào MultiDiGraph."""
    G = nx.MultiDiGraph()
    # TODO: với mỗi (doc_id, graph):
    #   - add_node(canonical, type=..., description=..., source_docs={...})
    #   - add_edge(canonical_src, canonical_tgt,
    #              predicate=..., source_doc=doc_id)
    return G


def diagnostics(G: nx.MultiDiGraph) -> None:
    """Kiểm tra sức khoẻ graph trước khi query."""
    # TODO in ra:
    #   - số weakly connected components (1 = resolution tốt, nhiều = còn đảo)
    #   - degree distribution (power-law-ish = có hub nodes tự nhiên)
    #   - edges/nodes ratio (<1.0 = thưa; ~1.0-2.0 = khoẻ)
    raise NotImplementedError


# ---------------------------------------------------------------
# 5) QUERYING — grounded answer: chỉ dùng graph, cite edges
# ---------------------------------------------------------------
def serialize_subgraph(G: nx.MultiDiGraph, center: str, hops: int = 2) -> str:
    """BFS k-hop từ seed entity, format mỗi edge thành 1 dòng triple:
    (source) --[predicate]--> (target)

    k=2 là sweet spot: neighbors-of-neighbors bắt được chain multi-hop
    mà chưa nổ context window.
    """
    # TODO
    raise NotImplementedError


GROUNDED_PROMPT = """Answer using only the knowledge graph below.
Cite the specific edges that support your answer.

<graph>
{graph_context}
</graph>

Question: {question}"""


def ask(question: str, graph_context: str | None = None) -> str:
    """graph_context=None -> ungrounded (baseline so sánh);
    có graph_context -> grounded, model phải cite edges."""
    # TODO: gọi client.messages.create(model=REASONING_MODEL, ...)
    raise NotImplementedError


# ---------------------------------------------------------------
# 6) EVALUATION — feedback loop: đổi prompt -> chạy scorer -> xem F1
# ---------------------------------------------------------------
def score_extraction(
    extracted: ExtractedGraph, gold_entities: set[str], alias_map: dict[str, str]
) -> dict:
    """Precision/recall của extraction so với gold set (~10 entities tự label).

    Lưu ý từ playbook: precision quan trọng hơn recall — một entity SAI
    sinh quan hệ sai lan truyền qua multi-hop; entity THIẾU chỉ làm graph
    không đầy đủ. Chấm cả raw form lẫn resolved form.
    """
    # TODO: return {"precision": ..., "recall": ..., "f1": ...}
    raise NotImplementedError


if __name__ == "__main__":
    # Luồng chạy gợi ý:
    # 1) docs = {doc_id: đọc text từ corpus Finance Banking của bạn}
    # 2) extracted = {doc_id: extract(text)}
    # 3) alias_map = resolve(gộp mọi entities)
    # 4) G = assemble(extracted, alias_map); diagnostics(G)
    # 5) In grounded vs ungrounded answer cho 3-5 câu hỏi multi-hop
    # 6) score_extraction(...) trên gold set -> tune EXTRACTION_PROMPT -> đo lại
    pass
