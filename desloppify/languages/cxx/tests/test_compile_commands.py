from __future__ import annotations

import json
from pathlib import Path

from desloppify.languages.cxx._helpers import build_cxx_dep_graph


def _write(root: Path, rel_path: str, content: str) -> Path:
    target = root / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return target


def test_build_dep_graph_from_compile_commands(tmp_path):
    source = _write(
        tmp_path,
        "src/main.cpp",
        '#include "generated.hpp"\nint main() { return 0; }\n',
    )
    header = _write(tmp_path, "generated/generated.hpp", "#pragma once\n")
    (tmp_path / "compile_commands.json").write_text(
        json.dumps(
            [
                {
                    "directory": str(tmp_path),
                    "file": "src/main.cpp",
                    "command": "clang++ -Igenerated -c src/main.cpp",
                }
            ]
        )
    )

    graph = build_cxx_dep_graph(tmp_path)

    assert str(source.resolve()) in graph
    assert str(header.resolve()) in graph[str(source.resolve())]["imports"]
