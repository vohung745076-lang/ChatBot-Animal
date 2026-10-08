"""Kiểm thử các quy tắc tĩnh đối với file static UI và mã nguồn."""
from pathlib import Path


def test_static_files_exist_and_under_100_lines():
    static_js = Path("static/js")
    js_files = list(static_js.glob("*.js"))
    assert len(js_files) >= 10

    for f in js_files:
        lines = len(f.read_text(encoding="utf-8").splitlines())
        assert lines < 100, f"File {f.name} vượt quá 100 dòng ({lines} dòng)"


def test_no_inner_html_in_static_files():
    static_dir = Path("static")
    for f in static_dir.rglob("*.js"):
        content = f.read_text(encoding="utf-8")
        assert "innerHTML" not in content, f"File {f.name} chứa innerHTML nguy hiểm"
        assert "dangerouslySetInnerHTML" not in content, f"File {f.name} chứa dangerouslySetInnerHTML"


def test_all_python_files_under_100_lines():
    src_dir = Path("src/chatbot")
    for f in src_dir.rglob("*.py"):
        lines = len(f.read_text(encoding="utf-8").splitlines())
        assert lines < 100, f"File {f.name} vượt quá 100 dòng ({lines} dòng)"
