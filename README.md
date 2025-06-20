MetaIntelligence: The Intelligence of Intelligent Systems🌟 Breaking Through "The Illusion of Thinking" - A Self-Evolving AI PlatformMetaIntelligence is a revolutionary AI integration system designed as "the intelligence of intelligent systems." Moving beyond mere LLM extension, it functions as a truly intelligent entity with self-awareness, self-improvement, and self-evolution capabilities. This platform implements solutions to overcome fundamental limitations identified in Apple Research's groundbreaking paper "The Illusion of Thinking".🚀 Core Features & Reasoning ModesMetaIntelligence provides a suite of research-based reasoning modes that dynamically select the optimal approach for a given problem, optimizing for both quality and efficiency.Key ConceptsTrue Self-Awareness (Meta-Cognition): The system analyzes its own thought processes to improve efficiency and logical consistency.Dynamic Architecture: Optimizes its internal component structure at runtime based on task requirements.Value Evolution: Autonomously learns and evolves its guiding values from experience, including successes, failures, and ethical dilemmas.Emergent Problem Discovery: Proactively identifies potential underlying issues from data and dialogue patterns that may not be apparent to humans.SuperIntelligence: Integrates and orchestrates multiple AI systems to create a collective intelligence that surpasses the sum of its parts.Research-Based Reasoning ModesModeTarget ComplexityPrimary BenefitUse CaseefficientLowOverthinking PreventionQuick questions, basic tasksbalancedMediumOptimal Reasoning QualityAnalysis, explanations, summarizationdecomposedHighCollapse Prevention & SpeedComplex problem-solving, system designadaptiveAuto-detectedDynamic Strategy OptimizationQuestions of unknown or mixed complexityparallelAllBest-of-Breed QualityMission-critical tasks, maximum qualityquantum_inspiredAllHolistic, Synthesized InsightBrainstorming, philosophical questionsedgeLowLightweight & FastLow-resource devices, quick checksspeculative_thoughtAllExploratory Idea GenerationEarly-stage ideation, multiple perspectivesself_discoverAllAutonomous Strategy ConstructionNovel or ill-defined problemspaper_optimizedAllComplete Research IntegrationTasks requiring the highest quality, benchmarking🛠️ Installation & Quick StartRequirementsPython 3.10+pip package managerAn API key for at least one LLM provider or a local Ollama/Llama.cpp setupffmpeg (optional, for audio processing)Setup# 1. Clone the repository
git clone https://github.com/matsushibadenki/Luca.git
cd Luca

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install spaCy models for advanced NLP (optional but recommended)
python -m spacy download en_core_web_sm
python -m spacy download ja_core_news_sm

# 4. Configure environment variables
cp .env.example .env
# Edit the .env file to add your API keys (e.g., OPENAI_API_KEY).
# Ensure the base URL and model path are correct for Ollama or Llama.cpp.

# 5. Verify your setup
python quick_test_v2.py
Quick Start (CLI)The fetch_llm_v2.py script is the main command-line interface.# Simple question (efficient mode)
python fetch_llm_v2.py ollama "What is the capital of Japan?" --mode efficient

# Analytical question (adaptive mode)
python fetch_llm_v2.py gemini "Analyze the economic impact of AI on the job market." --mode adaptive

# Complex design task (decomposed mode)
python fetch_llm_v2.py openai "Design a sustainable urban transportation system." --mode decomposed

# RAG query using Wikipedia
python fetch_llm_v2.py openai "What were the key findings of the LIGO experiment?" --mode balanced --wikipedia

# Tackle a novel problem with self-discover mode
python fetch_llm_v2.py claude "Define 'creativity' for an AI and propose a method to acquire it." --mode self_discover
🐍 Advanced Usage with Python APIYou can directly leverage the full power of the system by using the Python API, allowing for deep integration into your applications.Using the Master Integration SystemThe MasterIntegrationOrchestrator is the top-level component that orchestrates all subsystems to solve ultimate problems.# /examples/master_system_api_usage.py

import asyncio
from llm_api.providers import get_provider
from llm_api.master_system.orchestrator import MasterIntegrationOrchestrator, IntegrationConfig

async def use_master_system():
    # 1. Initialize a provider (use enhanced=True for V2 capabilities)
    provider = get_provider("ollama", enhanced=True)
    
    # 2. Configure the integration system (enabling all subsystems)
    config = IntegrationConfig(enable_all_systems=True)
    orchestrator = MasterIntegrationOrchestrator(provider, config)
    
    # 3. Initialize the integrated system
    print("🌟 Initializing MetaIntelligence Master System...")
    init_result = await orchestrator.initialize_integrated_system()
    print("✅ Initialization complete!")
    
    # 4. Solve an ultimate problem
    problem = "How should humanity maintain its value and purpose when artificial intelligence surpasses human intellect?"
    print(f"\n🎯 Solving ultimate problem: {problem[:50]}...")
    
    solution = await orchestrator.solve_ultimate_integrated_problem(problem)
    
    print("\n✨ Ultimate Problem Solved!")
    print(f"Excerpt from Integrated Solution:\n{solution.get('integrated_solution', 'N/A')[:200]}...")
    print(f"\n- Transcendence Achieved: {solution.get('transcendence_achieved', False)}")
    print(f"- Self-Evolution Triggered: {solution.get('self_evolution_triggered', False)}")

if __name__ == "__main__":
    asyncio.run(use_master_system())
🔬 Architecture & TestingSystem ArchitectureMetaIntelligence employs a hierarchical architecture composed of multiple advanced subsystems working in concert.MetaIntelligence Master System
├── Core Engine
│   ├── Pipelines (adaptive, parallel, quantum_inspired, etc.)
│   └── Reasoning Strategies (low, medium, high complexity)
├── Providers (OpenAI, Claude, Ollama, etc.)
├── Meta-Cognition Engine
├── Dynamic Architecture System
├── Value Evolution Engine
├── Problem Discovery Engine
├── SuperIntelligence Orchestrator
└── RAG (Retrieval-Augmented Generation)
For a detailed breakdown, see doc/directory_structure.md.Testing and ValidationThe project includes a comprehensive test suite to ensure reliability and stability.# 1. Run a quick diagnostic check of your environment
python quick_test_v2.py

# 2. Execute unit and integration tests for core components
pytest tests/

# 3. Run a comprehensive test across all available providers and V2 modes
python test_all_v2_providers.py
With the addition of tests/test_rag.py, tests/test_reasoning.py, tests/test_dynamic_architecture.py, and more, the quality of our primary features is well-assured.🤝 Support & DocumentationDetailed Documentation: The doc/ directory contains in-depth documents on architecture, the project roadmap, and the API reference.CLI Guide: Refer to doc/cli_guide.md or run python fetch_llm_v2.py --help.Troubleshooting: Run python quick_test_v2.py --troubleshooting for solutions to common problems.📜 LicenseThis project is licensed under the MIT License. See the LICENSE file for details."True intelligence is to know what you know, to know what you don't know, and most importantly, to know how to keep learning."