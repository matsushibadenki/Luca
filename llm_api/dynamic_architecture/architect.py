# /llm_api/dynamic_architecture/architect.py
# タイトル: System Architect
# 役割: 動的アーキテクチャシステムの主要オーケストレーター。コンポーネントアーキテクチャの管理、実行、進化を担当します。

import asyncio
import logging
from typing import Any, Dict, List, Optional, Deque, cast
from collections import deque

from ..providers.base import LLMProvider
from .types import ArchitectureBlueprint, ComponentType, AdaptiveComponent
from .components import MetaAnalyzer, AdaptiveReasoner, SynthesisOptimizer, ReflectionValidator, CreativeEnhancer

logger = logging.getLogger(__name__)

class SystemArchitect:
    """システムアーキテクト - 動的アーキテクチャ管理"""
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        self.components: Dict[str, AdaptiveComponent] = {}
        self.current_architecture: Optional[ArchitectureBlueprint] = None
        self.performance_history: Deque[Dict[str, Any]] = deque(maxlen=100)
        self.evolution_log: List[Dict[str, Any]] = []

    async def initialize_adaptive_architecture(self, initial_config: Dict[str, Any]) -> Dict[str, Any]:
        """適応的アーキテクチャの初期化"""
        logger.info("適応的アーキテクチャを初期化中...")
        
        self.components = {
            "meta_analyzer": MetaAnalyzer("meta_analyzer_001"),
            "adaptive_reasoner": AdaptiveReasoner("adaptive_reasoner_001", self.provider),
            "synthesis_optimizer": SynthesisOptimizer("synthesis_optimizer_001", self.provider),
            "reflection_validator": ReflectionValidator("reflection_validator_001", self.provider)
        }
        
        self.current_architecture = ArchitectureBlueprint(
            component_types=[ComponentType.ANALYZER, ComponentType.REASONER, ComponentType.SYNTHESIZER, ComponentType.VALIDATOR],
            connection_matrix={"meta_analyzer": ["adaptive_reasoner"], "adaptive_reasoner": ["synthesis_optimizer"], "synthesis_optimizer": ["reflection_validator"], "reflection_validator": ["meta_analyzer"]},
            execution_flow=["meta_analyzer", "adaptive_reasoner", "synthesis_optimizer", "reflection_validator"],
            optimization_targets={"accuracy": 0.8, "efficiency": 0.7, "adaptability": 0.9},
            constraints={"max_execution_time": 60, "memory_limit": "1GB"}
        )
        
        return {"architecture_initialized": True, "component_count": len(self.components)}

    async def execute_adaptive_pipeline(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """適応的パイプラインの実行"""
        logger.info("適応的パイプライン実行開始")
        if not self.current_architecture:
            raise RuntimeError("Architecture not initialized.")

        execution_trace: List[Dict[str, Any]] = []
        current_data = input_data
        pipeline_context = context.copy()
        
        for component_id in self.current_architecture.execution_flow:
            component = self.components.get(component_id)
            if not component: continue

            start_time = asyncio.get_event_loop().time()
            # 変更点: contextのコピーを渡すことで、意図しない変更を防ぐ
            result = await component.execute(current_data, pipeline_context.copy())
            execution_time = asyncio.get_event_loop().time() - start_time
            
            execution_trace.append({"component_id": component_id, "execution_time": execution_time, "confidence": result.get("confidence", 0.5)})
            current_data = result
            pipeline_context.update(result)
        
        performance_metrics = await self._evaluate_pipeline_performance(execution_trace, current_data)
        self.performance_history.append(performance_metrics)
        
        return {"final_output": current_data, "performance_metrics": performance_metrics}

    async def _evaluate_pipeline_performance(self, trace: List[Dict[str, Any]], output: Any) -> Dict[str, Any]:
        """パイプラインパフォーマンスの評価"""
        total_time = sum(s["execution_time"] for s in trace)
        avg_confidence = sum(s["confidence"] for s in trace) / len(trace) if trace else 0
        return {"total_time": total_time, "avg_confidence": avg_confidence, "output_quality": 0.8}

    async def _calculate_current_performance(self) -> float:
        if not self.performance_history:
            return 0.0
        performance = self.performance_history[-1].get("overall_score", 0.0)
        return cast(float, performance)