"""Opt-in, localhost-only Ollama method proposals for the v0.5 decision engine.

The LLM cannot execute methods, fabricate verified evidence, or silently confirm
user preferences. Only DecisionHubV05 computes results on confirmed state.
"""

import json
import os
from threading import Lock
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from .decision_v05 import DecisionHubV05

MODEL_DEFAULT = "qwen3.5:4b-q4_K_M"
ALLOWED_MODELS = frozenset({MODEL_DEFAULT, "psychohistory:v0"})
OLLAMA_API = "http://127.0.0.1:11434/api/chat"
MAX_RESPONSE_BYTES = 16_384
MAX_QUESTION_BYTES = 6_000


class ModelUnavailable(Exception):
    """The local Ollama runtime is unreachable, timed out, or returned invalid data."""


class _RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class OllamaClient:
    """No proxies, redirects, arbitrary URLs, cloud providers, or API credentials."""

    def __init__(self, model=MODEL_DEFAULT, timeout_seconds=45):
        if model not in ALLOWED_MODELS:
            raise ValueError("本地 AI 模型未列入允许清单。")
        self.model = model
        self.timeout_seconds = timeout_seconds
        self._opener = build_opener(ProxyHandler({}), _RejectRedirects())

    def chat(self, system, question):
        payload = json.dumps({
            "model": self.model,
            "stream": False,
            "think": False,
            "format": "json",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": question},
            ],
            "options": {"temperature": 0, "num_ctx": 4096, "num_predict": 384},
        }, ensure_ascii=False).encode("utf-8")
        request = Request(OLLAMA_API, data=payload, method="POST", headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        try:
            with self._opener.open(request, timeout=self.timeout_seconds) as response:
                data = response.read(MAX_RESPONSE_BYTES + 1)
            if len(data) > MAX_RESPONSE_BYTES:
                raise ModelUnavailable("本地模型响应过大。")
            result = json.loads(data)
            output = result["message"]["content"]
            if not isinstance(output, str):
                raise ValueError("response content must be string")
            return output
        except (HTTPError, URLError, TimeoutError, OSError, ValueError, KeyError, TypeError) as exc:
            raise ModelUnavailable("本地 Ollama 无法返回有效结果。") from exc


def _object_without_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key")
        obj[key] = value
    return obj


def validate_proposal(raw, allowed_keys):
    """Reject fabricated method names and inconsistent or unbounded JSON."""
    if not isinstance(raw, str) or len(raw.encode("utf-8")) > 10_000:
        raise ValueError("响应长度无效")
    proposal = json.loads(raw, object_pairs_hook=_object_without_duplicate_keys)
    if not isinstance(proposal, dict) or set(proposal) != {
        "model_key", "initial_analysis", "reason", "ask", "candidate_options"
    }:
        raise ValueError("响应字段不符合契约")
    key = proposal["model_key"]
    if not isinstance(key, str) or key not in set(allowed_keys) | {"NONE"}:
        raise ValueError("不允许不存在或未经注册的模型")
    for field, limit in (("initial_analysis", 400), ("reason", 300), ("ask", 180)):
        value = proposal[field]
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError("文本字段无效")
    options = proposal["candidate_options"]
    if not isinstance(options, list) or len(options) > 5 or any(
        not isinstance(item, str) or not item.strip() or len(item) > 100 for item in options
    ):
        raise ValueError("待确认的候选方案无效")
    return proposal


def _system_prompt(methods):
    catalog = [
        {"key": method.key, "title": method.title, "applicability": method.applicability,
         "failure_conditions": method.failure_conditions}
        for method in methods
    ]
    return (
        "你是心理史学本地决策助手的初步理解层。以下是唯一允许选择的已登记数学方法目录：\n"
        + json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
        + "\n请选择一个最适合继续核对的方法，输出其精确 key。若不适合则选 NONE。"
        "方法选择仅表示候选，不代表已执行计算。缺少参数时指出缺口，不能编造数值、概率、"
        "科学来源或用户权重。先给最多三句中文初步分析，只问一个最影响判断的问题。"
        "candidate_options 只能填用户原文中逐字出现的完整短语，不得自行添加方案。"
        "仅输出以下 JSON 对象，不要 Markdown、思考过程或额外字段："
        '{"model_key":"登记key或NONE","initial_analysis":"简短分析",'
        '"reason":"选择依据与缺少的数据","ask":"一个关键追问或空字符串",'
        '"candidate_options":["原文里的原样短语"]}'
    )


class LocalDecisionAI:
    def __init__(self, *, client=None, hub=None, enabled=None):
        self.hub = hub if hub is not None else DecisionHubV05()
        self.enabled = (
            os.environ.get("PSYCHOHISTORY_LOCAL_AI", "0") == "1"
            if enabled is None else bool(enabled)
        )
        self.model = os.environ.get("PSYCHOHISTORY_LOCAL_AI_MODEL", MODEL_DEFAULT)
        self.client = client if client is not None else (
            OllamaClient(model=self.model) if self.model in ALLOWED_MODELS else None
        )
        self._lock = Lock()

    def status(self):
        return {
            "enabled": self.enabled and self.client is not None,
            "model": self.model if self.model in ALLOWED_MODELS else None,
            "transport": "localhost_only",
            "evidence": "ENGINEERING_CANDIDATE_NOT_REAL_WORLD_VALIDATED",
            "stores_messages": False,
        }

    def propose(self, question):
        if not isinstance(question, str) or not question.strip() or len(question.encode("utf-8")) > MAX_QUESTION_BYTES:
            return {"status": "INVALID_QUERY", "proposal": None}
        if not self.enabled or self.client is None:
            return {"status": "LOCAL_AI_DISABLED", "proposal": None}
        if not self._lock.acquire(blocking=False):
            return {"status": "MODEL_BUSY", "proposal": None}
        try:
            methods = self.hub.registry.methods()
            raw = self.client.chat(_system_prompt(methods), question)
            proposal = validate_proposal(raw, {method.key for method in methods})
            if any(option not in question for option in proposal["candidate_options"]):
                raise ValueError("候选方案未在用户原文中出现")
            start = self.hub.start(question)
            return {
                "status": "NEEDS_CONFIRMATION", "provider": "ollama_local_candidate_v1",
                "model": self.model, "proposal": proposal,
                "candidate_method": next((m.describe() for m in methods if m.key == proposal["model_key"]), None),
                "draft_state": start["state"],
                "questions": start["questions"],
                "evidence": "UNVERIFIED_USER_WORDING",
                "calculated": False,
            }
        except ModelUnavailable:
            return {"status": "LOCAL_MODEL_UNAVAILABLE", "proposal": None}
        except (ValueError, TypeError, KeyError, AttributeError):
            return {"status": "MODEL_OUTPUT_REJECTED", "proposal": None}
        finally:
            self._lock.release()

    def analyze_confirmed(self, state, model_key, confirmed_by_user=False):
        """The deterministic engine exclusively owns numerical results."""
        if not confirmed_by_user:
            return {"status": "USER_CONFIRMATION_REQUIRED", "calculated": False}
        validated = self.hub.state_model.model_validate(state)
        if not validated.confirmed or not validated.constraints_confirmed:
            return {"status": "USER_CONFIRMATION_REQUIRED", "calculated": False}
        available = {method.key for method in self.hub.registry.methods()}
        if model_key not in available:
            return {"status": "INVALID_METHOD", "calculated": False}
        analysis = self.hub.analyze(validated)
        result = next((m for m in analysis["methods"]
                       if f'{m["model_id"]}@{m["version"]}' == model_key), None)
        executed = bool(result and result["status"] == "EXECUTED")
        return {
            "status": analysis["status"], "model_key": model_key,
            "calculated": executed, "selected_method": result, "analysis": analysis,
            "source": "DecisionHubV05_deterministic",
            "evidence": "CONDITIONAL_ON_CONFIRMED_INPUT",
        }
