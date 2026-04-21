"""database/connection.py — MySQL connection pool with dict-row wrapper."""
from mysql.connector import pooling
from config.settings import DB_CONFIG

_POOL = None

def _get_pool():
    global _POOL
    if _POOL is None:
        _POOL = pooling.MySQLConnectionPool(pool_name="portal_pool", pool_size=8, **DB_CONFIG)
    return _POOL

class _DictCursor:
    def __init__(self, cur): self._c = cur
    def execute(self, sql, p=None): self._c.execute(sql, p) if p else self._c.execute(sql)
    def fetchone(self):
        row = self._c.fetchone()
        if row is None: return None
        return dict(zip([d[0] for d in self._c.description], row))
    def fetchall(self):
        rows = self._c.fetchall()
        if not rows: return []
        cols = [d[0] for d in self._c.description]
        return [dict(zip(cols, r)) for r in rows]
    @property
    def lastrowid(self): return self._c.lastrowid

class _Conn:
    def __init__(self, conn): self._conn = conn
    def cursor(self): return _DictCursor(self._conn.cursor())
    def commit(self): self._conn.commit()
    def close(self): self._conn.close()

def get_connection(): return _Conn(_get_pool().get_connection())
