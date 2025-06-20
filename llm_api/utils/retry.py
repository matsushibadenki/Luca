# /llm_api/utils/retry.py
# Title: Async Retry Decorator
# Role: Provides a generic asynchronous retry decorator for handling transient errors in API calls.

import asyncio
import logging
from functools import wraps
from typing import Any, Callable, Coroutine, Type, Tuple

from ..config import settings
import httpx
from openai import APIConnectionError as OpenAIConnectionError
from anthropic import APIConnectionError as AnthropicConnectionError
from google.api_core import exceptions as GoogleAPIErrors

logger = logging.getLogger(__name__)

# リトライ対象とする例外のリスト
RETRYABLE_EXCEPTIONS: Tuple[Type[Exception], ...] = (
    httpx.RequestError,
    httpx.HTTPStatusError,  # 5xx系エラーを対象にするロジックを内部で追加
    OpenAIConnectionError,
    AnthropicConnectionError,
    GoogleAPIErrors.ServiceUnavailable,
    GoogleAPIErrors.DeadlineExceeded,
)

def async_retry(
    max_attempts: int = settings.RETRY_MAX_ATTEMPTS,
    initial_wait: float = settings.RETRY_INITIAL_WAIT,
    backoff_factor: float = settings.RETRY_BACKOFF_FACTOR,
    max_wait: float = settings.RETRY_MAX_WAIT,
    retryable_exceptions: Tuple[Type[Exception], ...] = RETRYABLE_EXCEPTIONS
) -> Callable[..., Coroutine[Any, Any, Any]]:
    """
    非同期関数が一時的なエラーで失敗した場合に、指数関数的バックオフでリトライするデコレータ。
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Optional[Exception] = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    is_retryable = False
                    if isinstance(e, httpx.HTTPStatusError) and 500 <= e.response.status_code < 600:
                        is_retryable = True
                    elif isinstance(e, retryable_exceptions):
                         is_retryable = True

                    if is_retryable and attempt < max_attempts - 1:
                        wait_time = min(initial_wait * (backoff_factor ** attempt), max_wait)
                        logger.warning(
                            f"Call to '{func.__name__}' failed due to {type(e).__name__}. "
                            f"Retrying in {wait_time:.2f}s... (Attempt {attempt + 1}/{max_attempts})"
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(
                            f"Call to '{func.__name__}' failed after {attempt + 1} attempts. "
                            f"Final exception: {type(e).__name__}: {e}",
                            exc_info=True
                        )
                        raise e from last_exception
            return None # Should not be reached
        return wrapper
    return decorator