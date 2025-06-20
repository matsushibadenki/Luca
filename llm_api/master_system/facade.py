# /llm_api/master_system/facade.py
# タイトル: MetaIntelligence System Facade
# 役割: マスターシステムの主要なサブシステムを統合し、シンプルなインターフェースを提供する。

import logging
from typing import Dict, Any, Optional

from ..providers.base import LLMProvider
from .types import MasterSystemConfig, IntegrationConfig
from .orchestrator import MasterIntegrationOrchestrator

logger = logging.getLogger(__name__)

class MetaIntelligence:
    """
    MetaIntelligence Master System
    This class acts as a facade, orchestrating the various sub-systems.
    """
    def __init__(self, primary_provider: LLMProvider, config: Optional[MasterSystemConfig] = None):
        self.primary_provider = primary_provider
        self.config = config or MasterSystemConfig()
        # IntegrationConfigにMasterSystemConfigを渡す
        integration_config = IntegrationConfig(master_system_config=self.config)
        self.orchestrator = MasterIntegrationOrchestrator(primary_provider, integration_config)
        logger.info("🌟 MetaIntelligence Master System Facade インスタンス作成")

    async def initialize_master_system(self) -> Dict[str, Any]:
        """Initializes the entire master system via the orchestrator."""
        return await self.orchestrator.initialize_integrated_system()

    async def solve_ultimate_problem(self, problem: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Solves an ultimate problem by delegating to the orchestrator."""
        return await self.orchestrator.solve_ultimate_integrated_problem(problem, context)
    
    async def evolve_consciousness(self) -> Dict[str, Any]:
        """Evolves the system's consciousness by delegating to the orchestrator."""
        return await self.orchestrator.evolve_integrated_consciousness()

    async def generate_ultimate_wisdom(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """Generates ultimate wisdom by delegating to the orchestrator."""
        return await self.orchestrator.generate_unified_wisdom(domain)