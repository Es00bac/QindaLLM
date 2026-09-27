"""qinda-llm-top's parsers: metrics, journal timings, presets, sparklines."""

import importlib.machinery
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
loader = importlib.machinery.SourceFileLoader("qinda_llm_top", str(ROOT / "monitor/qinda-llm-top"))
spec = importlib.util.spec_from_loader("qinda_llm_top", loader)
top = importlib.util.module_from_spec(spec)
sys.modules["qinda_llm_top"] = top
loader.exec_module(top)

JOURNAL = """\
2026-09-27T14:20:01-06:00 qinda llama-server[900]: srv load_models: spawning server instance with name=ornith on port 41233
2026-09-27T14:20:09-06:00 qinda llama-server[900]: [41233] load_tensors: offloaded 41/41 layers to GPU
2026-09-27T14:20:09-06:00 qinda llama-server[900]: [41233] load_tensors:      Vulkan0 model buffer size =  5530.12 MiB
2026-09-27T14:20:09-06:00 qinda llama-server[900]: [41233] load_tensors:   CPU_Mapped model buffer size = 20480.50 MiB
2026-09-27T14:21:40-06:00 qinda llama-server[900]: [41233] slot print_timing: id  0 | task 12 | prompt eval time =   46000.00 ms / 18204 tokens (    2.53 ms per token,   395.74 tokens per second)
2026-09-27T14:22:14-06:00 qinda llama-server[900]: [41233] slot print_timing: id  0 | task 12 |        eval time =   34190.00 ms /   612 tokens (   55.86 ms per token,    17.90 tokens per second)
2026-09-27T14:22:14-06:00 qinda llama-server[900]: [41233] slot print_timing: id  0 | task 12 |       total time =   80190.00 ms / 18816 tokens
"""


class MonitorTest(unittest.TestCase):
    def test_metrics(self):
        m = top.parse_metrics("# HELP x\nllamacpp:prompt_tokens_total 1200\n"
                              "llamacpp:tokens_predicted_seconds_total 3.5\nbogus\n")
        self.assertEqual(m["prompt_tokens_total"], 1200)
        self.assertEqual(m["tokens_predicted_seconds_total"], 3.5)

    def test_journal_requests_and_facts(self):
        requests, facts, tail = top.parse_journal(JOURNAL.splitlines())
        self.assertEqual(len(requests), 1)
        r = requests[0]
        self.assertEqual((r.when, r.model, r.prompt_tokens, r.gen_tokens), ("14:21:40", "ornith", 18204, 612))
        self.assertAlmostEqual(r.gen_tps, 17.90)
        self.assertEqual(facts["layers"], "41/41")
        self.assertEqual(facts["gpu_buf"], "5530.12")
        self.assertEqual(len(tail), 7)

    def test_presets_merge_defaults(self):
        presets = top.read_presets(ROOT / "config/models.ini")
        self.assertEqual(set(presets), {"ornith", "qwen3.6"})
        self.assertEqual(presets["qwen3.6"]["ctx-size"], "131072")
        self.assertTrue(presets["ornith"]["model"].endswith(".gguf"))

    def test_sparkline(self):
        self.assertEqual(top.sparkline([0, 5, 10], 3), " ▄█")
        self.assertEqual(len(top.sparkline([1] * 50, 20)), 20)


if __name__ == "__main__":
    unittest.main()
