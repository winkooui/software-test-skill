from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = {
    "solo": ROOT / "adapters/solo/adapter-config.yaml",
    "claude-code": ROOT / "adapters/claude-code/adapter-config.yaml",
    "trae-qoder": ROOT / "adapters/trae-qoder/adapter-config.yaml",
    "codex": ROOT / "adapters/codex/adapter-config.yaml",
}


class AdapterConfigTest(unittest.TestCase):
    def test_adapter_files_exist(self) -> None:
        for path in ADAPTERS.values():
            self.assertTrue(path.exists(), path)

    def test_adapter_core_sections_exist(self) -> None:
        required_sections = [
            "tool_mapping:",
            "path_mapping:",
            "capabilities:",
            "dependencies:",
            "metadata:",
            "fallback_overrides:",
            "output:",
            "detection_rules:",
        ]
        for name, path in ADAPTERS.items():
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"platform: {name}", text)
            for section in required_sections:
                self.assertIn(section, text, f"{name} missing {section}")

    def test_codex_declares_fallback_limits(self) -> None:
        text = ADAPTERS["codex"].read_text(encoding="utf-8")
        self.assertIn("excel_generation: false", text)
        self.assertIn("chart_embedding: false", text)
        self.assertIn("command_execution: \"none\"", text)
        self.assertIn("输出 Markdown 表格 + CSV 格式", text)


if __name__ == "__main__":
    unittest.main()
