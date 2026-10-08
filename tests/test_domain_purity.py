"""Kiểm tra độ thuần khiết của tầng Domain."""
from pathlib import Path


FORBIDDEN = {
    "flask", "langchain", "google", "genai", "dotenv",
    "os", "sys", "json", "requests", "urllib"
}


def test_domain_has_no_impure_dependencies():
    domain_dir = Path("src/chatbot/domain")
    py_files = list(domain_dir.rglob("*.py"))
    assert len(py_files) >= 6

    for file_path in py_files:
        content = file_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            line_clean = line.strip()
            if line_clean.startswith("import ") or line_clean.startswith("from "):
                for pkg in FORBIDDEN:
                    err = f"Domain vi pham quy tac thuan khiet tai {file_path.name}: {line_clean}"
                    assert f" {pkg}" not in line_clean and f".{pkg}" not in line_clean, err
