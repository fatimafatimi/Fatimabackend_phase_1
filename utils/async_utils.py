import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=10)

def run_async(coro):
    """
    Safely run an async coroutine from sync code inside FastAPI.
    
    Strategy:
    - If there's a running loop (FastAPI context) → use executor in a new thread
    - If no running loop → use asyncio.run() directly
    """
    try:
        loop = asyncio.get_running_loop()
        # We ARE inside FastAPI's event loop
        # Submit to thread pool where we can safely call asyncio.run()
        future = loop.run_in_executor(
            _executor,
            _run_in_new_loop,  # runs coro in a brand new event loop
            coro
        )
        # Block until done (we're in sync code so this is fine)
        import concurrent.futures
        return future.result()  # ← this blocks the thread, not the event loop
    except RuntimeError:
        # No running loop at all → safe to use asyncio.run directly
        return asyncio.run(coro)
    except Exception as e:
        logger.error(f"[run_async ERROR]: {e}", exc_info=True)
        raise


def _run_in_new_loop(coro):
    """
    Run a coroutine in a completely fresh event loop.
    Called inside a thread so it doesn't conflict with FastAPI's loop.
    """
    new_loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(new_loop)
        return new_loop.run_until_complete(coro)
    finally:
        new_loop.close()
        asyncio.set_event_loop(None)