import os
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

import torch


class HuggingFaceCacheTest(TestCase):
    def test_webui_sets_hf_cache_before_gradio_import(self):
        webui_source = Path("webui.py").read_text(encoding="utf-8")

        self.assertLess(
            webui_source.index("os.environ.setdefault(\"HF_HUB_CACHE\""),
            webui_source.index("import gradio as gr"),
        )

    def test_infer_v2_uses_model_dir_cache_by_default(self):
        from indextts.infer_v2 import get_hf_cache_dir

        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                get_hf_cache_dir("custom_checkpoints"),
                os.path.abspath(os.path.join("custom_checkpoints", "hf_cache")),
            )

    def test_semantic_model_passes_explicit_cache_dir(self):
        from indextts.utils.maskgct_utils import build_semantic_model

        semantic_model = MagicMock()
        semantic_model.eval = MagicMock()

        with (
            patch(
                "indextts.utils.maskgct_utils.Wav2Vec2BertModel.from_pretrained",
                return_value=semantic_model,
            ) as from_pretrained,
            patch(
                "indextts.utils.maskgct_utils.torch.load",
                return_value={"mean": torch.tensor([0.0]), "var": torch.tensor([1.0])},
            ),
        ):
            build_semantic_model("wav2vec2bert_stats.pt", cache_dir="custom_cache")

        from_pretrained.assert_called_once_with(
            "facebook/w2v-bert-2.0",
            cache_dir="custom_cache",
        )


if __name__ == "__main__":
    main()
