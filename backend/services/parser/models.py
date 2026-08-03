from dataclasses import dataclass, field


@dataclass
class ParsedSubject:

    subject_code: str

    internal: int

    external: int

    total: int

    result: str


@dataclass
class ParsedStudent:

    usn: str

    name: str

    overall_result: str

    subjects: dict = field(default_factory=dict)
