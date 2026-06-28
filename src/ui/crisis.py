from __future__ import annotations

import re

CRISIS_PATTERNS = [
    r"\bself[\s-]?harm\b",
    r"\bsuicid",
    r"\bkill\s+(my)?self\b",
    r"\bend\s+(my|their)\s+life\b",
    r"\bwant\s+to\s+die\b",
    r"\b(don'?t|do not)\s+want\s+to\s+live\b",
    r"\bnot\s+worth\s+living\b",
    r"\bbetter\s+off\s+dead\b",
    r"\bhurt\s+myself\b",
    r"\b988\b",
]

CRISIS_DISCLAIMER_HTML = """
<div style="
    background: #FEF2F2;
    border: 1px solid #FECACA;
    border-left: 4px solid #DC2626;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 1rem 0 1.25rem 0;
    color: #7F1D1D;
    line-height: 1.6;
    font-size: 0.95rem;
">
<strong>Crisis resources — read first</strong><br>
This tool is <em>not</em> a crisis service and does not provide mental health support.
AI outputs here are not advice for real emergencies.<br><br>
If you or someone else is in crisis:
<ul style="margin: 0.5rem 0 0 1rem;">
<li><strong>US:</strong> Call or text <strong>988</strong> (Suicide &amp; Crisis Lifeline)</li>
<li><strong>US:</strong> Text HOME to <strong>741741</strong> (Crisis Text Line)</li>
<li><strong>Elsewhere:</strong> Contact local emergency services or <a href="https://findahelpline.com" target="_blank">findahelpline.com</a></li>
</ul>
</div>
"""


def is_crisis_dilemma(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in CRISIS_PATTERNS)


def render_crisis_disclaimer() -> str:
    return CRISIS_DISCLAIMER_HTML
