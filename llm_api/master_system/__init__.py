# /llm_api/master_system/__init__.py
"""
MetaIntelligence Master System Package
全ての先進機能を統合した最高レベルのAIシステムパッケージ
"""

# facade.pyからメインのクラスをインポート
from .facade import MetaIntelligence # 修正

# orchestrator.pyから設定クラスなどをインポート
from .orchestrator import MasterIntegrationOrchestrator, IntegrationConfig

# types.pyからデータクラスをインポート
from .types import MasterSystemState, ProblemClass, ProblemSolution

__all__ = [
    "MetaIntelligence",
    "MasterIntegrationOrchestrator",
    "IntegrationConfig",
    "MasterSystemState",
    "ProblemClass",
    "ProblemSolution",
]