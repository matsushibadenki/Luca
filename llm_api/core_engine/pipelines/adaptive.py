# /llm_api/core_engine/pipelines/adaptive.py
# タイトル: Adaptive Pipeline Handler (Refactored)
# 役割: 適応型推論のプロセス全体を調整するオーケストレーター。

import logging
from typing import Any, Dict, Optional, Tuple

from ...providers.base import LLMProvider
from ...rag import RAGManager
from ..analyzer import AdaptiveComplexityAnalyzer
from ..reasoner import EnhancedReasoningEngine  # <<<--- 修正: インポート元を変更
from ..enums import ComplexityRegime
from ..learner import ComplexityLearner
from ..logic import self_adjustment, finalization

logger = logging.getLogger(__name__)

class AdaptivePipeline:
    """適応型パイプライン処理を担当するクラス（リファクタリング版）"""

    def __init__(self, provider: LLMProvider, base_model_kwargs: Dict[str, Any]):
        self.provider = provider
        self.base_model_kwargs = base_model_kwargs
        self.learner = ComplexityLearner()
        self.complexity_analyzer = AdaptiveComplexityAnalyzer(learner=self.learner)
        # EnhancedReasoningEngineの初期化時にanalyzerは不要
        self.reasoning_engine = EnhancedReasoningEngine(provider, base_model_kwargs) 
        logger.info("AdaptivePipeline (Refactored) を初期化しました")

    async def execute(
        self,
        prompt: str,
        system_prompt: str = "",
        force_regime: Optional[ComplexityRegime] = None,
        use_rag: bool = False,
        knowledge_base_path: Optional[str] = None,
        use_wikipedia: bool = False,
        real_time_adjustment: bool = True,
        mode: str = 'adaptive'
    ) -> Dict[str, Any]:
        """適応型パイプラインの実行（オーケストレーション）"""
        logger.info(f"適応型パイプライン開始 (モード: {mode}): {prompt[:80]}...")

        try:
            # 0. Edgeモードの特別処理
            if mode == 'edge':
                logger.info("エッジ最適化モードで実行。高度な機能を無効化します。")
                use_rag, use_wikipedia, real_time_adjustment = False, False, False
                force_regime = ComplexityRegime.LOW

            # 1. RAGのセットアップ
            current_prompt, rag_source = await self._setup_rag(prompt, use_rag, knowledge_base_path, use_wikipedia)

            # 2. 複雑性分析
            complexity_score, initial_regime = self.complexity_analyzer.analyze_complexity(current_prompt, mode=mode)
            current_regime = force_regime or initial_regime

            # 3. 推論ループの実行（自己調整ロジックを呼び出し）
            final_reasoning_result, final_regime = await self_adjustment.run_reasoning_loop(
                reasoning_engine=self.reasoning_engine,
                provider=self.provider,
                base_model_kwargs=self.base_model_kwargs,
                current_prompt=current_prompt,
                system_prompt=system_prompt,
                complexity_score=complexity_score,
                initial_regime=current_regime,
                original_prompt=prompt,
                enable_adjustment=(real_time_adjustment and not force_regime)
            )

            if not final_reasoning_result:
                return self._format_error_response("推論結果が得られませんでした。")

            # 4. 学習と最終化（最終化ロジックを呼び出し）
            return await finalization.finalize_and_learn(
                learner=self.learner,
                provider=self.provider,
                base_model_kwargs=self.base_model_kwargs,
                reasoning_result=final_reasoning_result,
                original_prompt=prompt,
                system_prompt=system_prompt,
                final_regime=final_regime,
                initial_regime=initial_regime,
                complexity_score=complexity_score,
                rag_source=rag_source,
                mode=mode
            )

        except Exception as e:
            logger.error(f"適応型パイプライン実行中に予期せぬエラー: {e}", exc_info=True)
            return self._format_error_response(str(e))

    async def _setup_rag(
        self, prompt: str, use_rag: bool, knowledge_base_path: Optional[str], use_wikipedia: bool
    ) -> Tuple[str, Optional[str]]:
        """RAGのセットアップを行い、拡張されたプロンプトと情報源を返す。"""
        if not (use_rag or use_wikipedia):
            return prompt, None

        rag_manager = RAGManager(provider=self.provider, use_wikipedia=use_wikipedia, knowledge_base_path=knowledge_base_path)
        augmented_prompt = await rag_manager.retrieve_and_augment(prompt)
        rag_source = 'wikipedia' if use_wikipedia else 'knowledge_base'
        return augmented_prompt, rag_source

    def _format_error_response(self, error_message: str) -> Dict[str, Any]:
        """エラーレスポンスの形式"""
        return {
            'success': False,
            'final_solution': None,
            'image_url': None,
            'thought_process': {'error': error_message},
            'v2_improvements': {'adaptive_execution': True, 'error_occurred': True},
            'version': 'v2',
            'error': error_message
        }