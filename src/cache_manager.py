from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
from langchain_community.cache import SQLiteCache


def use_memory_cache():
    """
    Enable in-memory caching.

    Data is stored in RAM and is lost when
    the application stops.
    """
    set_llm_cache(InMemoryCache())


def use_sqlite_cache():
    """
    Enable SQLite caching.

    Cached responses are stored in a local
    SQLite database and can survive app restarts.
    """
    set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))