"""JSONL data loaders for the CM-EGQA mini experiment."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}") from exc
    return records


def load_samples(path: str | Path) -> list[dict[str, Any]]:
    return load_jsonl(path)


def load_evidence(path: str | Path) -> list[dict[str, Any]]:
    return load_jsonl(path)
