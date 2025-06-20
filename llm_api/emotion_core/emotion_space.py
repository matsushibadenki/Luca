# llm_api/emotion_core/emotion_space.py
# タイトル: Emotion Space Builder (Mypy Final Fix)
# 役割: 感情空間を構築・管理する。型エラーを完全に修正。

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import torch
from torch.nn.functional import cosine_similarity

from .sae_manager import SAEManager
from .types import EmotionCategory

# 循環参照を避けるための型チェック用インポート
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # このファイルでは型ヒントとしてのみ使用するため、実際のインポートはしない
    from ..llm_inference_engine import LLMInferenceEngine

logger = logging.getLogger(__name__)

class EmotionSpace:
    """
    感情とSAE特徴のマッピングを管理する「感情空間」を構築するクラス。
    """
    def __init__(self, llm_inference_engine: Optional["LLMInferenceEngine"], sae_manager: SAEManager):
        self.llm_engine = llm_inference_engine
        self.sae_manager = sae_manager
        self.device = sae_manager.device
        self.emotion_to_features: Dict[str, List[int]] = {}

    def get_emotion_feature_ids(self, emotion: EmotionCategory) -> List[int]:
        """
        指定された感情に対応するSAE特徴のIDリストを返します。
        """
        return self.emotion_to_features.get(emotion.value, [])

    def load_mapping(self, mapping_path: str) -> bool:
        """
        事前計算された感情-特徴マッピングをJSONファイルからロードします。
        """
        path = Path(mapping_path)
        if not path.exists():
            logger.warning(f"感情マッピングファイルが見つかりません: {mapping_path}")
            return False
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.emotion_to_features = json.load(f)
            logger.info(f"感情マッピングを正常にロードしました: {mapping_path}")
            return True
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"感情マッピングのロード中にエラーが発生しました: {e}")
            return False

    def save_mapping(self, output_path: str):
        """
        構築した感情-特徴マッピングをJSONファイルに保存します。
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.emotion_to_features, f, indent=4, ensure_ascii=False)
            logger.info(f"感情マッピングをファイルに保存しました: {output_path}")
        except IOError as e:
            logger.error(f"感情マッピングの保存中にエラーが発生しました: {e}")

    def build_space(self, concept_sets_path: str, top_k_words: int = 10):
        """
        コンセプトセットに基づき、感情空間を構築します。
        """
        logger.info(f"'{concept_sets_path}' から感情空間の構築を開始します...")
        
        try:
            with open(concept_sets_path, 'r', encoding='utf-8') as f:
                concept_sets = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"コンセプトセットファイルの読み込みに失敗しました: {e}")
            return

        for emotion_str, words in concept_sets.items():
            if not words: continue
            emotion_label = words[0]
            associated_words = words[1:]
            logger.info(f"'{emotion_label}' ({emotion_str}) の処理中...")

            try:
                label_features = self._get_features_for_word(emotion_label)
                if label_features is None: continue

                assoc_word_features = []
                for word in associated_words:
                    features = self._get_features_for_word(word)
                    if features is not None:
                        assoc_word_features.append({'word': word, 'features': features})
            except Exception as e:
                logger.error(f"'{emotion_label}' の単語特徴抽出中にエラー: {e}")
                continue

            similarities = []
            for item in assoc_word_features:
                if label_features is not None and item['features'] is not None:
                    # unsqueeze(0)でバッチ次元を追加して計算
                    sim = cosine_similarity(label_features.unsqueeze(0), item['features'].unsqueeze(0), dim=-1)
                    similarities.append((item['word'], sim.item(), item['features']))
            
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            final_word_features = [label_features] if label_features is not None else []
            for _, _, features in similarities[:top_k_words]:
                if features is not None:
                    final_word_features.append(features)

            if not final_word_features: continue

            all_feature_tensors = torch.stack(final_word_features)
            active_indices = torch.where(all_feature_tensors > 0)
            unique_feature_ids = torch.unique(active_indices[1]).tolist()
            
            self.emotion_to_features[emotion_str] = unique_feature_ids
            logger.info(f"  - '{emotion_label}' に {len(unique_feature_ids)} 個のユニークなSAE特徴をマッピングしました。")

        logger.info("全ての感情について感情空間の構築が完了しました。")

    def _get_features_for_word(self, word: str) -> Optional[torch.Tensor]:
        """
        単一の単語からSAE特徴ベクトルを取得するヘルパー関数。
        """
        if self.llm_engine is None:
            logger.warning(f"LLMエンジンがダミーのため、'{word}' の特徴取得はダミーデータです。")
            # mypyエラーを修正するため、ダミーの隠れ状態から特徴を生成する
            dummy_hidden_state = torch.randn(1, 1, 2048, device=self.device)
            dummy_features = self.sae_manager.extract_features(dummy_hidden_state)
            # squeeze(0)を2回呼び出して、(1, 1, dim) -> (dim) の形にする
            squeezed_features: torch.Tensor = dummy_features.squeeze(0).squeeze(0)
            return squeezed_features

        # 以下は、llm_engineが完全に実装された場合の本来のロジック
        hidden_states = self.llm_engine.get_hidden_states_for_text(word)
        if hidden_states is None:
            logger.warning(f"単語 '{word}' の隠れ状態を取得できませんでした。")
            return None
        
        last_token_hidden_state = hidden_states[:, -1, :]
        sae_features = self.sae_manager.extract_features(last_token_hidden_state)
        
        # squeeze(0)でバッチ次元を削除
        final_features: torch.Tensor = sae_features.squeeze(0)
        return final_features