# /llm_api/core_engine/logic/self_adjustment.py
# タイトル: Self-Adjustment Logic for Adaptive Pipeline
# 役割: 自己評価と複雑性レジームの再調整を含む、メインの推論ループを担当する。

import logging
from typing import Any, Dict, Optional, Tuple

from ..reasoner import EnhancedReasoningEngine
from ..enums import ComplexityRegime
from ...providers.base import LLMProvider

logger = logging.getLogger(__name__)

MAX_ADJUSTMENT_ATTEMPTS = 2

async def run_reasoning_loop(
    reasoning_engine: EnhancedReasoningEngine,
    provider: LLMProvider,
    base_model_kwargs: Dict[str, Any],
    current_prompt: str,
    system_prompt: str,
    complexity_score: float,
    initial_regime: ComplexityRegime,
    original_prompt: str,
    enable_adjustment: bool
) -> Tuple[Optional[Dict[str, Any]], ComplexityRegime]:
    """
    自己調整ループを実行し、最終的な推論結果とレジームを返す。
    """
    current_regime = initial_regime
    final_reasoning_result = None

    for attempt in range(MAX_ADJUSTMENT_ATTEMPTS):
        logger.info(f"推論試行 {attempt + 1}/{MAX_ADJUSTMENT_ATTEMPTS} (レジーム: {current_regime.value})")
        
        reasoning_result = await reasoning_engine.execute_reasoning(
            current_prompt, system_prompt, complexity_score, current_regime
        )
        final_reasoning_result = reasoning_result.copy()

        if reasoning_result.get('error'):
            logger.error(f"推論エンジンでエラー: {reasoning_result['error']}")
            return None, current_regime

        if not enable_adjustment or (attempt + 1) >= MAX_ADJUSTMENT_ATTEMPTS:
            break

        evaluation = await _self_evaluate_solution(
            provider, base_model_kwargs, final_reasoning_result.get('solution', ''), original_prompt, current_regime
        )
        final_reasoning_result['self_evaluation'] = evaluation

        if evaluation.get("is_sufficient"):
            logger.info("自己評価の結果、解は十分と判断しました。")
            break
        else:
            new_regime_str = evaluation.get("next_regime")
            if new_regime_str:
                new_regime = ComplexityRegime(new_regime_str)
                if new_regime != current_regime:
                    logger.info(f"自己評価に基づき複雑性を再調整: {current_regime.value} -> {new_regime.value}")
                    current_regime = new_regime
                    current_prompt = f"前回の回答は不十分でした。より深く、包括的な分析を行ってください。\n元の質問: {original_prompt}\n前回の回答: {final_reasoning_result.get('solution', '')}\n"
                else:
                    logger.info("同じ複雑性レジームが推奨されたため、調整を終了します。")
                    break
            else:
                break
    
    return final_reasoning_result, current_regime


async def _self_evaluate_solution(
    provider: LLMProvider,
    base_model_kwargs: Dict[str, Any],
    solution: str,
    original_prompt: str,
    current_regime: ComplexityRegime
) -> Dict[str, Any]:
    """
    生成された解を自己評価し、十分かどうか、次の戦略をどうするかを判断する。
    """
    # 簡易的なルールベース評価
    if len(solution) < 150 and current_regime == ComplexityRegime.LOW:
        return {
            "is_sufficient": False,
            "reason": "Solution may be too brief.",
            "next_regime": ComplexityRegime.MEDIUM.value
        }
    
    # LLMによる評価（将来的にはより高度な評価を実装）
    # ...

    return {"is_sufficient": True, "reason": "Solution seems adequate based on initial checks."}