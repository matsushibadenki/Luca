# /llm_api/core_engine/learner.py
import json
import logging
from typing import Dict, Optional, cast
from pathlib import Path
from .enums import ComplexityRegime

logger = logging.getLogger(__name__)

class ComplexityLearner:
    """プロンプトの複雑性レジームに関する過去の結果を学習するクラス"""
    def __init__(self, storage_path: str = 'complexity_learning.json'):
        self.storage_path = Path(storage_path)
        self.suggestions = self._load_suggestions()

    def _load_suggestions(self) -> Dict[str, str]:
        """学習済みの提案をファイルから読み込む"""
        if not self.storage_path.exists():
            return {}
        try:
            with self.storage_path.open('r') as f:
                # 修正: json.loadがAnyを返すため、期待する型にキャストします
                return cast(Dict[str, str], json.load(f))
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"学習データの読み込みに失敗: {e}")
            return {}

    def _save_suggestions(self) -> None:
        """現在の提案をファイルに保存する"""
        try:
            with self.storage_path.open('w') as f:
                json.dump(self.suggestions, f, indent=4)
        except IOError as e:
            logger.error(f"学習データの保存に失敗: {e}")

    def get_suggestion(self, prompt: str) -> Optional[ComplexityRegime]:
        """プロンプトに基づいて推奨レジームを返す"""
        prompt_key = prompt[:100] # プロンプトの最初の100文字をキーとして使用
        regime_str = self.suggestions.get(prompt_key)
        if regime_str:
            try:
                return ComplexityRegime(regime_str)
            except ValueError:
                return None
        return None

    def record_outcome(self, prompt: str, successful_regime: ComplexityRegime) -> None:
        """成功した結果を記録する"""
        prompt_key = prompt[:100]
        self.suggestions[prompt_key] = successful_regime.value
        self._save_suggestions()