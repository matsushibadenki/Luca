# /cli/request_processor.py
# タイトル: CLI Request Processor
# 役割: ユーザーからのリクエストを処理し、V2拡張と標準プロバイダーへのフォールバックロジックを実行する。

import logging
import time
from typing import Any, Dict, List, Optional

from llm_api.providers import get_provider
from llm_api.providers.base import EnhancedLLMProvider
from llm_api.core_engine.engine import MetaIntelligenceEngine

from .utils import enhance_kwargs_for_v2, convert_kwargs_for_standard, generate_error_suggestions
from llm_api.emotion_core.types import EmotionCategory
from llm_api.emotion_core.steering_manager import EmotionSteeringManager
from llm_api.autonomous_action.trigger import EmotionActionTrigger
from llm_api.autonomous_action.orchestrator import ActionOrchestrator

logger = logging.getLogger(__name__)

class RequestProcessor:
    """リクエスト処理のコアロジックを担当するクラス"""

    def __init__(
        self,
        emotion_steering_manager: Optional[EmotionSteeringManager],
        action_trigger: Optional[EmotionActionTrigger],
        action_orchestrator: Optional[ActionOrchestrator],
    ):
        self.v2_modes = {
            'efficient', 'balanced', 'decomposed', 'adaptive', 'paper_optimized', 'parallel',
            'quantum_inspired', 'edge', 'speculative_thought', 'self_discover'
        }
        self.emotion_steering_manager = emotion_steering_manager
        self.action_trigger = action_trigger
        self.action_orchestrator = action_orchestrator
        self.emotion_system_enabled = all([emotion_steering_manager, action_trigger, action_orchestrator])

    async def process_request(self, provider_name: str, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """
        リクエストを処理し、必要に応じてフォールバックを実行する。
        """
        start_time = time.time()
        mode = kwargs.get('mode', 'simple')
        use_v2 = mode in self.v2_modes or kwargs.get('force_v2', False)
        no_fallback = kwargs.get('no_fallback', False)
        errors_encountered: List[str] = []

        final_kwargs = await self._apply_emotion_steering(kwargs)

        if use_v2:
            try:
                logger.info(f"V2拡張モード (mode: {mode}) でプロバイダー '{provider_name}' の呼び出しを試みます。")

                # 1. 拡張プロバイダーインスタンスを取得
                enhanced_provider = get_provider(provider_name, enhanced=True)
                
                if not isinstance(enhanced_provider, EnhancedLLMProvider):
                    raise TypeError(f"'{provider_name}' はV2拡張プロバイダーではありません。")

                # 2. MetaIntelligenceEngineをここでインスタンス化する
                #    エンジンには「標準プロバイダー」と「最適化されたパラメータ」を渡す
                standard_provider = enhanced_provider.standard_provider
                base_model_kwargs = enhanced_provider._get_optimized_params(mode, final_kwargs)
                engine = MetaIntelligenceEngine(standard_provider, base_model_kwargs)

                # 3. エンジンのsolve_problemメソッドを呼び出す
                system_kwargs = {
                    'use_rag': final_kwargs.get('use_rag', False),
                    'knowledge_base_path': final_kwargs.get('knowledge_base_path'),
                    'use_wikipedia': final_kwargs.get('use_wikipedia', False),
                    'real_time_adjustment': final_kwargs.get('real_time_adjustment', True),
                    'mode': mode
                }
                response = await engine.solve_problem(
                    prompt,
                    system_prompt=final_kwargs.get("system_prompt", ""),
                    **system_kwargs
                )


                if not response.get('error'):
                    response = await self._trigger_autonomous_action(response, prompt)
                    return response
                else:
                    error_msg = f"V2拡張モードでエラー: {response.get('error')}"
                    logger.warning(error_msg)
                    errors_encountered.append(error_msg)

            except Exception as e:
                error_msg = f"V2拡張プロバイダーの呼び出し中に例外が発生しました: {e}"
                logger.error(error_msg, exc_info=True)
                errors_encountered.append(error_msg)

        if no_fallback:
            logger.warning("フォールバックが無効化されているため、処理を終了します。")
            return {'text': "", 'error': "V2拡張モードでの処理に失敗し、フォールバックは無効です。", 'all_errors': errors_encountered}

        # V2が失敗した場合、またはV2が指定されなかった場合に標準プロバイダーにフォールバック
        logger.info(f"標準プロバイダー (mode: {mode}) にフォールバックします。")
        try:
            provider = get_provider(provider_name, enhanced=False)
            standard_kwargs = convert_kwargs_for_standard(final_kwargs)
            response = await provider.call(prompt, **standard_kwargs)
            if not response.get('error'):
                 return response
            else:
                error_msg = f"標準フォールバックモードでエラー: {response.get('error')}"
                logger.error(error_msg)
                errors_encountered.append(error_msg)
        except Exception as e:
            error_msg = f"標準プロバイダーの呼び出し中に例外が発生しました: {e}"
            logger.error(error_msg, exc_info=True)
            errors_encountered.append(error_msg)

        final_error_message = "全てのリクエスト戦略が失敗しました。"
        suggestions = generate_error_suggestions(provider_name, errors_encountered)
        logger.critical(f"{final_error_message} 提案: {suggestions}")

        return {'text': "", 'error': final_error_message, 'all_errors': errors_encountered, 'suggestions': suggestions}

    async def _apply_emotion_steering(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """感情ステアリングが有効な場合にkwargsを更新する"""
        final_kwargs = kwargs.copy()
        if self.emotion_system_enabled and self.emotion_steering_manager and kwargs.get('steer_emotion'):
            emotion_str = kwargs['steer_emotion']
            try:
                emotion_cat = EmotionCategory(emotion_str.lower())
                intensity = kwargs.get('steering_intensity', 5.0)
                steering_vector = self.emotion_steering_manager.get_steering_vector(emotion_cat, intensity)
                if steering_vector is not None:
                    final_kwargs['steering_vector'] = steering_vector
                    logger.info(f"感情ステアリング '{emotion_str}' を適用します。")
            except (ValueError, AttributeError) as e:
                logger.warning(f"無効な感情名またはステアリングエラーです: {e}")
        return final_kwargs

    async def _trigger_autonomous_action(self, response: Dict[str, Any], prompt: str) -> Dict[str, Any]:
        """自律行動がトリガーされた場合にアクションを実行する"""
        if self.emotion_system_enabled and self.action_trigger and self.action_orchestrator:
            from llm_api.emotion_core.types import EmotionAnalysisResult
            # これはダミーの分析結果です。実際の分析には `emotion_monitor` を使用します。
            analysis_result = EmotionAnalysisResult(interest_score=0.9)
            action_context = {"prompt_history": [prompt]}
            action_request = self.action_trigger.check_and_trigger(analysis_result, action_context)

            if action_request:
                logger.info(f"自律行動 '{action_request.requested_action}' がトリガーされました。")
                action_result = await self.action_orchestrator.execute_action(action_request)
                if action_result:
                    response['autonomous_action_result'] = action_result
                    logger.info(f"自律行動の結果: {action_result}")
        return response