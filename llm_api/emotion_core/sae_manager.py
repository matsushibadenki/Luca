# llm_api/emotion_core/sae_manager.py
# タイトル: Sparse Autoencoder (SAE) Manager (Mypy Fixed)
# 役割: sae-lensライブラリを使用してSAEモデルをロードし、特徴抽出を行う。

import logging
from typing import Optional, Dict, cast # castをインポート

import torch

try:
    from sae_lens import SAE
except ImportError:
    SAE = None

logger = logging.getLogger(__name__)

class SAEManager:
    """
    sae-lensライブラリを介してSAEモデルを管理し、特徴抽出と再構成を行うクラス。
    """
    def __init__(self, release: str, sae_id: str):
        if SAE is None:
            raise ImportError("sae-lensライブラリがインストールされていません。`pip install sae-lens`を実行してください。")

        self.release = release
        self.sae_id = sae_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.sae: Optional[SAE] = None
        self._load_model()

    @property
    def decoder_weights(self) -> Optional[torch.Tensor]:
        if self.sae:
            # 修正: self.sae.W_decがTensorであることをmypyに伝える
            return cast(torch.Tensor, self.sae.W_dec)
        return None

    def _load_model(self):
        try:
            logger.info(f"HuggingFaceからSAEモデルをロードしています: release='{self.release}', sae_id='{self.sae_id}'...")
            sae_model, _, _ = SAE.from_pretrained(
                release=self.release,
                sae_id=self.sae_id,
                device=self.device
            )
            self.sae = sae_model
            self.sae.eval()
            logger.info("✅ SAEモデルのロードに成功しました。")
        except Exception as e:
            logger.error(f"SAEモデルのロード中にエラーが発生しました: {e}", exc_info=True)
            raise

    def extract_features(self, hidden_states: torch.Tensor) -> torch.Tensor:
        if not self.sae:
            raise RuntimeError("SAEモデルがロードされていません。")
        
        hidden_states = hidden_states.to(self.device)
        with torch.no_grad():
            # 修正: 返り値がTensorであることをmypyに伝える
            features = self.sae.encode(hidden_states)
        
        return cast(torch.Tensor, features)

    def reconstruct(self, features: torch.Tensor) -> torch.Tensor:
        if not self.sae:
            raise RuntimeError("SAEモデルがロードされていません。")
            
        features = features.to(self.device)
        with torch.no_grad():
            # 修正: 返り値がTensorであることをmypyに伝える
            reconstructed_states = self.sae.decode(features)
        
        return cast(torch.Tensor, reconstructed_states)