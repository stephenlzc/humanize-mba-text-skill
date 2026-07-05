"""Shared data contracts used by every analyzer in this package.

Kept tiny on purpose: callers (AIPatternDetector / StatisticalDetector) read
only ``issues`` and ``metrics``; tests use both.

- ``analyzer_id`` matches the dimension number documented in
  ``docs/swarm-prose-analyzers.md``.
- ``severity`` is the *displayed* severity in the merged report. Treat
  ``high`` as "almost certainly AI", ``medium`` as "probably machine-like",
  ``low`` as "worth a second look".
- ``confidence`` is independent of severity: it describes how sure the analyzer
  is about its own observation. Tests use both fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AnalyzerIssue:
    analyzer_id: str
    severity: str
    confidence: float
    location: str
    evidence: str
    suggestion: str


@dataclass
class AnalyzerReport:
    issues: list[AnalyzerIssue] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def merge(self, other: "AnalyzerReport") -> None:
        self.issues.extend(other.issues)
        for key, value in other.metrics.items():
            # If both analyzers report the same metric, last writer wins; this
            # matches how StatisticalDetector's existing features are overwritten.
            self.metrics[key] = value
