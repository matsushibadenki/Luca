# /llm_api/master_system/orchestrator.py
# タイトル: Master Integration Orchestrator (Refactored)
# 役割: 全システムの統合と協調を管理する最高レベルのオーケストレーター。

import logging
from typing import Any, Dict, List, Optional
from .types import MasterSystemConfig, IntegrationConfig
from ..providers.base import LLMProvider
from .initializer import SystemInitializer
from .solver import IntegratedProblemSolver

logger = logging.getLogger(__name__)


class MasterIntegrationOrchestrator:
    def __init__(self, primary_provider: LLMProvider, config: Optional[IntegrationConfig] = None, initializer: Optional[SystemInitializer] = None):
        self.primary_provider = primary_provider
        self.config = config or IntegrationConfig()
        # 修正：初期化を遅延させることで、テスト時のパッチ適用を可能にする
        self._initializer_instance = initializer
        self.subsystems: Dict[str, Any] = {}
        self.solver: Optional[IntegratedProblemSolver] = None
        self.integration_status = "uninitialized"
        self._initializer: Optional[SystemInitializer] = None # 内部用のイニシャライザインスタンス
        logger.info("🌟 マスター統合オーケストレーター(DI対応版)インスタンス作成")

    def _get_initializer(self) -> SystemInitializer:
        """
        テストでパッチが適用されるように、イニシャライザの取得を遅延させる。
        """
        if self._initializer:
            return self._initializer
        
        if self._initializer_instance:
            self._initializer = self._initializer_instance
            return self._initializer
        
        # このメソッドが呼ばれるタイミングでは、テストのpatchが有効になっている
        self._initializer = SystemInitializer(self.primary_provider, self.config)
        return self._initializer


    async def initialize_integrated_system(self) -> Dict[str, Any]:
        """このメソッドで全ての初期化を実行する"""
        self.integration_status = "initializing"
        logger.info("🚀 統合システム完全初期化プロセスを呼び出します...")
        try:
            initializer = self._get_initializer()
            self.subsystems = initializer.initialize_subsystems()
            self.solver = IntegratedProblemSolver(self.subsystems.get("superintelligence"))

            status_report = initializer.get_subsystem_status(self.subsystems)

            self.integration_status = "operational"

            logger.info("✨ 統合システム完全初期化完了! ✨")
            return {
                "integration_status": "🌟 FULLY INTEGRATED AND OPERATIONAL",
                "subsystem_status": status_report
            }
        except Exception as e:
            logger.error(f"❌ 統合システム初期化エラー: {e}", exc_info=True)
            self.integration_status = "failed"
            return {"integration_status": "❌ INTEGRATION FAILED", "error": str(e)}

    async def solve_ultimate_integrated_problem(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """究極的問題解決をSolverに委譲する。"""
        if self.integration_status != "operational":
            # 初期化されていない場合は初期化を試みる
            if self.integration_status == "uninitialized":
                logger.warning("システムが初期化されていなかったため、自動的に初期化します。")
                await self.initialize_integrated_system()
                # 初期化に失敗した場合はエラーを返す
                if self.integration_status != "operational":
                     return {"error": f"システムの自動初期化に失敗しました。現在の状態: '{self.integration_status}'"}
            else: # "initializing" または "failed" の場合
                 return {"error": f"システムが '{self.integration_status}' 状態のため、解決処理を実行できません。"}

        if not self.solver:
             return {"error": "問題解決システムが初期化されていません。"}
        return await self.solver.solve_ultimate_problem(problem, context)

    # --- 将来的な拡張（他の専門クラスへの委譲） ---
    async def evolve_integrated_consciousness(self) -> Dict[str, Any]:
        """統合意識の進化をEvolverに委譲する（将来的な実装）。"""
        logger.info("🧠 統合意識進化プロセス開始...")
        return {"status": "not_implemented"}

    async def generate_unified_wisdom(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """統一知恵の生成をSynthesizerに委譲する（将来的な実装）。"""
        logger.info(f"💎 統一知恵生成開始: {domain or '全領域'}")
        return {"status": "not_implemented"}

    async def monitor_integration_health(self) -> Dict[str, Any]:
        """統合システム健全性監視をMonitorに委譲する（将来的な実装）。"""
        logger.info("🔍 統合システム健全性監視開始...")
        return {"status": "not_implemented"}