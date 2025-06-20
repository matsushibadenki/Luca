# /llm_api/providers/__init__.py
"""
LLMプロバイダーの動的ロードとファクトリー機能
"""
import importlib
import inspect
import logging
import os
import pkgutil
from typing import  Optional, Any, Dict, List, Type, cast

from .base import LLMProvider, EnhancedLLMProvider

logger = logging.getLogger(__name__)

# --- グローバル変数 ---
_initialized = False
_standard_providers: Dict[str, Type[LLMProvider]] = {}
_enhanced_providers: Dict[str, set] = {"v2": set(), "all": set()}
_providers_cache: Dict[str, LLMProvider] = {}

def _initialize_providers():
    """プロバイダーモジュールを動的にインポートして初期化する"""
    global _initialized
    if _initialized:
        return

    logger.info("プロバイダーモジュール初期化開始")
    
    package_path = os.path.dirname(__file__)
    
    # 1. 標準プロバイダーをロード
    for _, name, _ in pkgutil.iter_modules([package_path]):
        if name.startswith('enhanced_') or name == 'base':
            continue
        try:
            module = importlib.import_module(f".{name}", package=__name__)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, LLMProvider) and not issubclass(obj, EnhancedLLMProvider) and obj is not LLMProvider):
                    provider_name = name.lower()
                    _standard_providers[provider_name] = obj
                    logger.debug(f"標準プロバイダー '{provider_name}' を登録: {obj.__name__}")
        except Exception as e:
            logger.warning(f"プロバイダーモジュール '{name}' のロードに失敗: {e}")

    # 2. 拡張プロバイダーをロード
    for _, name, _ in pkgutil.iter_modules([package_path]):
        if name.startswith('enhanced_') and name.endswith('_v2'):
            provider_name = name.replace('enhanced_', '').replace('_v2', '')
            if provider_name in _standard_providers:
                _enhanced_providers["v2"].add(provider_name)
                _enhanced_providers["all"].add(provider_name)
                logger.debug(f"V2拡張プロバイダー '{provider_name}' を発見")

    _initialized = True
    logger.info("プロバイダーモジュール初期化完了")
    logger.info(f"利用可能な標準プロバイダー: {sorted(_standard_providers.keys())}")
    logger.info(f"利用可能なV2拡張プロバイダー: {sorted(_enhanced_providers['v2'])}")


def list_providers() -> List[str]:
    """利用可能な標準プロバイダーの一覧を返す"""
    _initialize_providers()
    return sorted(list(_standard_providers.keys()))

def list_enhanced_providers() -> Dict[str, List[str]]:
    """利用可能な拡張プロバイダーの一覧を返す"""
    _initialize_providers()
    return {
        "v2": sorted(list(_enhanced_providers["v2"])),
    }

def _get_standard_provider_class(name: str) -> Type[LLMProvider]:
    """標準プロバイダークラスを取得する。"""
    if name not in _standard_providers:
        raise ValueError(f"標準プロバイダー '{name}' が見つかりません。")
    return _standard_providers[name]

def _get_enhanced_provider_class(name: str) -> Type[EnhancedLLMProvider]:
    """V2拡張プロバイダークラスを動的に取得する。"""
    if name not in _enhanced_providers['v2']:
        raise ValueError(f"V2拡張プロバイダー '{name}' が見つかりません。")
    try:
        module_name = f".enhanced_{name}_v2"
        module = importlib.import_module(module_name, package='llm_api.providers')
        for class_name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, EnhancedLLMProvider) and obj is not EnhancedLLMProvider:
                return obj
        raise AttributeError(f"モジュール '{module_name}' 内に EnhancedLLMProvider を継承したクラスが見つかりません。")
    except ImportError as e:
        raise ImportError(f"V2拡張プロバイダーモジュール '{name}' のインポートに失敗しました: {e}") from e

def get_provider(provider_name: str, enhanced: bool = True, **kwargs: Any) -> LLMProvider:
    """
    指定されたプロバイダーのインスタンスを取得するファクトリー関数。
    インスタンスはキャッシュされ、同じ引数での再呼び出しでは同じインスタンスを返します。
    """
    _initialize_providers()
    
    # "enhanced_openai_v2" のような名前を "openai" に変換
    provider_key = provider_name.lower().replace('enhanced_', '').replace('_v2', '')

    cache_key = f"{provider_key}_{'enhanced' if enhanced else 'standard'}"
    if cache_key in _providers_cache:
        logger.debug(f"キャッシュからプロバイダー '{cache_key}' を返します。")
        return _providers_cache[cache_key]

    logger.info(f"プロバイダー '{cache_key}' の新しいインスタンスを生成します。")

    try:
        StandardProviderClass = _get_standard_provider_class(provider_key)
    except ValueError:
        # 修正: エラーメッセージを英語に統一
        raise ValueError(f"Provider '{provider_key}' not found. Available providers: {list_providers()}")

    if not enhanced or provider_key not in _enhanced_providers['v2']:
        if enhanced and provider_key not in _enhanced_providers['v2']:
             logger.warning(f"V2 enhanced provider for '{provider_key}' is not available. Returning standard provider.")
        instance = StandardProviderClass(**kwargs)
        _providers_cache[cache_key] = instance
        return instance

    try:
        standard_instance = StandardProviderClass()
        EnhancedProviderClass = _get_enhanced_provider_class(provider_key)
        enhanced_instance = EnhancedProviderClass(standard_provider=standard_instance)
        
        _providers_cache[cache_key] = enhanced_instance
        return enhanced_instance
    except (ValueError, ImportError) as e:
        logger.error(f"Failed to get enhanced provider '{provider_key}': {e}. Falling back to standard provider.")
        instance = StandardProviderClass(**kwargs)
        _providers_cache[cache_key] = instance
        return instance

def get_default_provider(enhanced: bool = True) -> LLMProvider:
    """デフォルトのプロバイダー(Ollama)を返す"""
    return get_provider('ollama', enhanced)

def check_provider_health(provider_name: str, enhanced: bool) -> Dict:
    """プロバイダーの健全性チェック"""
    _initialize_providers()
    try:
        provider_key = provider_name.lower()
        if enhanced:
            if provider_key not in _enhanced_providers['v2']:
                 return {'available': False, 'reason': 'V2拡張はこのプロバイダーでは利用できません。'}
            _get_enhanced_provider_class(provider_key)
        else:
            _get_standard_provider_class(provider_key)
        return {'available': True, 'reason': '正常にロード可能です。'}
    except (ValueError, ImportError) as e:
        return {'available': False, 'reason': str(e)}