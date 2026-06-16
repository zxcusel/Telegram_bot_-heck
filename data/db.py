"""
БД — SQLite.
Таблицы: users, admins, roles, geos

geo: 'bo' (Bolivia) | 'pe' (Peru)
Пользователь должен иметь минимум 1 роль И минимум 1 гео для доступа.
"""
import json, os, sqlite3
from contextlib import contextmanager

BASE_DIR  = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
INFO_PATH = os.path.join(BASE_DIR, "info.json")
DB_PATH   = os.path.join(BASE_DIR, "bot.db")

VALID_ROLES = ("fd", "rd", "cr")
VALID_GEOS  = ("bo", "pe", "uy", "py", "ma")


@contextmanager
def _conn():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA foreign_keys=ON")
    try:
        yield con; con.commit()
    except Exception:
        con.rollback(); raise
    finally:
        con.close()


MIGRATIONS: list[tuple[str, str]] = [
    ("001_add_pinned_date", "ALTER TABLE users ADD COLUMN pinned_date TEXT DEFAULT NULL"),
    ("002_add_pinned_name", "ALTER TABLE users ADD COLUMN pinned_name TEXT DEFAULT NULL"),
    ("003_add_name_pin_enabled", "ALTER TABLE users ADD COLUMN name_pin_enabled INTEGER DEFAULT 0"),
    ("004_add_pinned_bank", "ALTER TABLE users ADD COLUMN pinned_bank TEXT DEFAULT NULL"),
    ("005_add_time_suffix", "ALTER TABLE users ADD COLUMN time_suffix TEXT DEFAULT NULL"),
    ("006_add_rand_enabled", "ALTER TABLE users ADD COLUMN rand_enabled INTEGER DEFAULT 0"),
    ("007_add_rand_min", "ALTER TABLE users ADD COLUMN rand_min INTEGER DEFAULT 17500"),
    ("008_add_rand_max", "ALTER TABLE users ADD COLUMN rand_max INTEGER DEFAULT 21999"),
    ("009_add_rand_perc_min", "ALTER TABLE users ADD COLUMN rand_perc_min REAL DEFAULT 10.0"),
    ("010_add_rand_perc_max", "ALTER TABLE users ADD COLUMN rand_perc_max REAL DEFAULT 1500.0"),
    ("011_add_rand_percent_enabled", "ALTER TABLE users ADD COLUMN rand_percent_enabled INTEGER DEFAULT 0"),
    ("012_add_rand_percent_min", "ALTER TABLE users ADD COLUMN rand_percent_min REAL DEFAULT 1.0"),
    ("013_add_rand_percent_max", "ALTER TABLE users ADD COLUMN rand_percent_max REAL DEFAULT 100.0"),
    ("014_add_rand_bank_enabled", "ALTER TABLE users ADD COLUMN rand_bank_enabled INTEGER DEFAULT 0"),
    ("015_add_rand_acc_enabled", "ALTER TABLE users ADD COLUMN rand_acc_enabled INTEGER DEFAULT 0"),
    ("016_add_rand_name_enabled", "ALTER TABLE users ADD COLUMN rand_name_enabled INTEGER DEFAULT 0"),
    ("017_add_blur_enabled", "ALTER TABLE users ADD COLUMN blur_enabled INTEGER DEFAULT 1"),
    ("018_add_blur_qr_enabled", "ALTER TABLE users ADD COLUMN blur_qr_enabled INTEGER DEFAULT 1"),
    ("019_add_jose_sender_enabled", "ALTER TABLE users ADD COLUMN jose_sender_enabled INTEGER DEFAULT 0"),
    ("020_add_rand_rocket_min", "ALTER TABLE users ADD COLUMN rand_rocket_min INTEGER DEFAULT 10"),
    ("021_add_rand_rocket_max", "ALTER TABLE users ADD COLUMN rand_rocket_max INTEGER DEFAULT 1000"),
    ("022_geos_table_recreate", "dummy"),
    ("023_add_jose_recipient_enabled", "ALTER TABLE users ADD COLUMN jose_recipient_enabled INTEGER DEFAULT 0")
]

def _run_migrations(con):
    con.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TEXT DEFAULT (datetime('now'))
        )
    """)
    applied = {r["version"] for r in con.execute("SELECT version FROM schema_migrations").fetchall()}
    for version, sql in MIGRATIONS:
        if version not in applied:
            try:
                if version == "022_geos_table_recreate":
                    schema_geos = con.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='geos'").fetchone()
                    if schema_geos and "'ma'" not in schema_geos[0]:
                        con.execute("PRAGMA foreign_keys=OFF")
                        con.execute("""
                            CREATE TABLE geos_new (
                                user_id  INTEGER NOT NULL,
                                geo      TEXT    NOT NULL CHECK(geo IN ('bo','pe','uy','py','ma')),
                                added_at TEXT    DEFAULT (datetime('now')),
                                PRIMARY KEY (user_id, geo)
                            )
                        """)
                        con.execute("INSERT INTO geos_new SELECT * FROM geos")
                        con.execute("DROP TABLE geos")
                        con.execute("ALTER TABLE geos_new RENAME TO geos")
                        con.execute("PRAGMA foreign_keys=ON")
                else:
                    con.execute(sql)
            except sqlite3.OperationalError as e:
                err_msg = str(e).lower()
                if "duplicate" not in err_msg and "already exists" not in err_msg:
                    raise
            con.execute("INSERT INTO schema_migrations (version) VALUES (?)", (version,))

def init_db():
    if not os.path.exists(INFO_PATH):
        raise FileNotFoundError(f"info.json не найден: {INFO_PATH}")
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT    DEFAULT NULL,
                first_name  TEXT    DEFAULT NULL,
                last_seen   TEXT    DEFAULT (datetime('now')),
                pinned_date TEXT    DEFAULT NULL,
                pinned_name TEXT    DEFAULT NULL,
                name_pin_enabled INTEGER DEFAULT 0,
                pinned_bank TEXT    DEFAULT NULL,
                time_suffix TEXT    DEFAULT NULL,
                rand_enabled INTEGER DEFAULT 0,
                rand_min     INTEGER DEFAULT 17500,
                rand_max     INTEGER DEFAULT 21999,
                rand_perc_min REAL DEFAULT 10.0,
                rand_perc_max REAL DEFAULT 1500.0,
                rand_percent_enabled INTEGER DEFAULT 0,
                rand_percent_min     REAL DEFAULT 1.0,
                rand_percent_max     REAL DEFAULT 100.0,
                rand_bank_enabled    INTEGER DEFAULT 0,
                rand_acc_enabled     INTEGER DEFAULT 0,
                rand_name_enabled    INTEGER DEFAULT 0,
                blur_enabled         INTEGER DEFAULT 1,
                blur_qr_enabled      INTEGER DEFAULT 1,
                jose_sender_enabled  INTEGER DEFAULT 0,
                jose_recipient_enabled INTEGER DEFAULT 0,
                rand_rocket_min      INTEGER DEFAULT 10,
                rand_rocket_max      INTEGER DEFAULT 1000
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS name_blacklist (
                name TEXT PRIMARY KEY
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS banned_users (
                user_id INTEGER PRIMARY KEY
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                user_id  INTEGER PRIMARY KEY,
                added_at TEXT DEFAULT (datetime('now'))
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                user_id  INTEGER NOT NULL,
                role     TEXT    NOT NULL CHECK(role IN ('fd','rd','cr')),
                added_at TEXT    DEFAULT (datetime('now')),
                PRIMARY KEY (user_id, role)
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS geos (
                user_id  INTEGER NOT NULL,
                geo      TEXT    NOT NULL CHECK(geo IN ('bo','pe','uy','py','ma')),
                added_at TEXT    DEFAULT (datetime('now')),
                PRIMARY KEY (user_id, geo)
            )
        """)
        
        _run_migrations(con)
        
        # Миграция из info.json
        data = json.load(open(INFO_PATH, encoding="utf-8"))
        for uid_str in data.get("admins", []):
            try: con.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (int(uid_str),))
            except ValueError: pass
        for role in VALID_ROLES:
            for uid_str in data.get(role, []):
                try:
                    uid = int(uid_str)
                    con.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (uid,))
                    con.execute("INSERT OR IGNORE INTO roles (user_id, role) VALUES (?,?)", (uid, role))
                except ValueError: pass
        old_users = data.get("users", data.get("usernames", {}))
        for uid_str, info in old_users.items():
            try:
                uid = int(uid_str)
                uname = info.get("username") if isinstance(info, dict) else info
                fname = info.get("first_name") if isinstance(info, dict) else None
                con.execute("""
                    INSERT INTO users (user_id, username, first_name)
                    VALUES (?,?,?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        username   = COALESCE(excluded.username, username),
                        first_name = COALESCE(excluded.first_name, first_name)
                """, (uid, uname, fname))
            except (ValueError, AttributeError): pass


def get_token() -> str:
    import os
    from dotenv import load_dotenv
    # Явно указываем путь к .env в корне проекта (на случай если cwd != папка проекта)
    _env_path = os.path.join(BASE_DIR, ".env")
    load_dotenv(dotenv_path=_env_path, override=False)
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "BOT_TOKEN не найден. Убедитесь, что переменная окружения BOT_TOKEN "
            f"задана на хостинге или что файл .env существует по пути: {_env_path}"
        )
    
    # Очищаем от возможных пробелов и кавычек
    token = token.strip().strip("'\"")
    
    if token == "YOUR_TOKEN_HERE" or not token:
        raise RuntimeError(
            f"Ошибка: В значении BOT_TOKEN обнаружен стандартный плейсхолдер или пустая строка: '{token}'. "
            f"Пожалуйста, отредактируйте файл .env на хостинге и впишите туда настоящий токен бота от @BotFather."
        )
    return token


# ── Users ─────────────────────────────────────────────────────────────────────

def upsert_user(user_id: int, username: str | None, first_name: str | None = None):
    with _conn() as con:
        con.execute("""
            INSERT INTO users (user_id, username, first_name, last_seen)
            VALUES (?, ?, ?, datetime('now'))
            ON CONFLICT(user_id) DO UPDATE SET
                username   = COALESCE(excluded.username, username),
                first_name = COALESCE(excluded.first_name, first_name),
                last_seen  = excluded.last_seen
        """, (user_id, username, first_name))


def get_username(user_id: int) -> str | None:
    with _conn() as con:
        row = con.execute("SELECT username FROM users WHERE user_id = ?", (user_id,)).fetchone()
    return row["username"] if row else None


def get_user_display(user_id: int) -> str:
    uname = get_username(user_id)
    return f"{user_id} - @{uname}" if uname else str(user_id)

fmt_user = get_user_display




# ── Admins ────────────────────────────────────────────────────────────────────

def is_admin(user_id: int) -> bool:
    with _conn() as con:
        return con.execute("SELECT 1 FROM admins WHERE user_id = ?", (user_id,)).fetchone() is not None

def add_admin(user_id: int):
    with _conn() as con:
        con.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        con.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (user_id,))

def remove_admin(user_id: int):
    with _conn() as con:
        con.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))

def get_all_admins() -> list[int]:
    with _conn() as con:
        return [r["user_id"] for r in con.execute("SELECT user_id FROM admins ORDER BY user_id").fetchall()]


# ── Roles ─────────────────────────────────────────────────────────────────────

def get_roles(user_id: int) -> list[str]:
    with _conn() as con:
        return [r["role"] for r in con.execute(
            "SELECT role FROM roles WHERE user_id = ? ORDER BY role", (user_id,)).fetchall()]

def is_banned(user_id: int) -> bool:
    with _conn() as con:
        return con.execute("SELECT 1 FROM banned_users WHERE user_id = ?", (user_id,)).fetchone() is not None

def ban_user(user_id: int):
    with _conn() as con:
        con.execute("INSERT OR IGNORE INTO banned_users (user_id) VALUES (?)", (user_id,))

def unban_user(user_id: int):
    with _conn() as con:
        con.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))

def get_banned_users() -> list[int]:
    with _conn() as con:
        return [r["user_id"] for r in con.execute("SELECT user_id FROM banned_users").fetchall()]

def has_any_access(user_id: int) -> bool:
    """Доступ = есть роль И есть гео (или администратор). Забаненным доступ закрыт."""
    if is_banned(user_id):
        return False
    if is_admin(user_id):
        return True
    return bool(get_roles(user_id)) and bool(get_geos(user_id))

def get_role_string(user_id: int) -> str | None:
    """Возвращает строку ролей через '+': 'fd', 'rd+cr', 'all' и т.д."""
    if is_admin(user_id):
        return "all"
    roles = set(get_roles(user_id))
    if not roles:
        return None
    parts = []
    if "fd" in roles: parts.append("fd")
    if "rd" in roles: parts.append("rd")
    if "cr" in roles: parts.append("cr")
    return "+".join(parts) if parts else None

def add_role(user_id: int, role: str):
    if role not in VALID_ROLES: return
    with _conn() as con:
        con.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        con.execute("INSERT OR IGNORE INTO roles (user_id, role) VALUES (?,?)", (user_id, role))

def remove_role(user_id: int, role: str):
    if role not in VALID_ROLES: return
    with _conn() as con:
        con.execute("DELETE FROM roles WHERE user_id = ? AND role = ?", (user_id, role))

def clear_roles(user_id: int):
    with _conn() as con:
        con.execute("DELETE FROM roles WHERE user_id = ?", (user_id,))


# ── Geos ─────────────────────────────────────────────────────────────────────

def get_geos(user_id: int) -> list[str]:
    with _conn() as con:
        return [r["geo"] for r in con.execute(
            "SELECT geo FROM geos WHERE user_id = ? ORDER BY geo", (user_id,)).fetchall()]

def add_geo(user_id: int, geo: str):
    if geo not in VALID_GEOS: return
    with _conn() as con:
        con.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        try:
            con.execute("INSERT INTO geos (user_id, geo) VALUES (?,?)", (user_id, geo))
        except sqlite3.IntegrityError:
            pass

def remove_geo(user_id: int, geo: str):
    if geo not in VALID_GEOS: return
    with _conn() as con:
        con.execute("DELETE FROM geos WHERE user_id = ? AND geo = ?", (user_id, geo))

def clear_geos(user_id: int):
    with _conn() as con:
        con.execute("DELETE FROM geos WHERE user_id = ?", (user_id,))


# ── User lists ────────────────────────────────────────────────────────────────

def get_all_users_all() -> list[int]:
    with _conn() as con:
        return [r["user_id"] for r in con.execute("""
            SELECT DISTINCT user_id FROM (
                SELECT user_id FROM roles UNION SELECT user_id FROM admins
            ) ORDER BY user_id
        """).fetchall()]

def get_all_users_with_roles() -> list[int]:
    with _conn() as con:
        return [r["user_id"] for r in con.execute(
            "SELECT DISTINCT user_id FROM roles ORDER BY user_id").fetchall()]


# ── Settings ──────────────────────────────────────────────────────────────────

def get_settings(user_id: int) -> dict:
    with _conn() as con:
        row = con.execute("""
            SELECT pinned_date, pinned_name, name_pin_enabled, pinned_bank,
                   time_suffix, rand_enabled, rand_min, rand_max,
                   rand_perc_min, rand_perc_max,
                   rand_percent_enabled, rand_percent_min, rand_percent_max,
                   rand_bank_enabled, rand_acc_enabled, rand_name_enabled, blur_enabled, blur_qr_enabled, jose_sender_enabled, jose_recipient_enabled,
                   rand_rocket_min, rand_rocket_max
            FROM users WHERE user_id = ?
        """, (user_id,)).fetchone()
    if not row:
        return {"pinned_date": None, "pinned_name": None, "name_pin_enabled": 0,
                "pinned_bank": None, "time_suffix": None,
                "rand_enabled": 0, "rand_min": 17500, "rand_max": 21999,
                "rand_perc_min": 10.0, "rand_perc_max": 1500.0,
                "rand_percent_enabled": 0, "rand_percent_min": 1.0, "rand_percent_max": 100.0,
                "rand_bank_enabled": 0, "rand_acc_enabled": 0, "rand_name_enabled": 0,
                "blur_enabled": 1, "blur_qr_enabled": 1, "jose_sender_enabled": 0, "jose_recipient_enabled": 0,
                "rand_rocket_min": 10, "rand_rocket_max": 1000}
    return dict(row)

def update_setting(user_id: int, key: str, value):
    valid_keys = ("pinned_date","pinned_name","name_pin_enabled","pinned_bank",
                  "time_suffix","rand_enabled","rand_min","rand_max",
                  "rand_perc_min", "rand_perc_max",
                  "rand_percent_enabled", "rand_percent_min", "rand_percent_max",
                  "rand_bank_enabled", "rand_acc_enabled", "rand_name_enabled", "blur_enabled", "blur_qr_enabled", "jose_sender_enabled", "jose_recipient_enabled",
                  "rand_rocket_min", "rand_rocket_max")
    if key not in valid_keys: return
    with _conn() as con:
        con.execute(f"UPDATE users SET {key} = ? WHERE user_id = ?", (value, user_id))


# ── Name Randomizer & Blacklist ───────────────────────────────────────────────

def get_all_names() -> list[str]:
    names_path = os.path.join(BASE_DIR, "name.json")
    if not os.path.exists(names_path):
        return []
    try:
        with open(names_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading name.json: {e}")
        return []

def get_available_names() -> list[str]:
    all_names = get_all_names()
    with _conn() as con:
        rows = con.execute("SELECT name FROM name_blacklist").fetchall()
    blacklisted = {r["name"] for r in rows}
    return [name for name in all_names if name not in blacklisted]

def blacklist_name(name: str):
    with _conn() as con:
        con.execute("INSERT OR IGNORE INTO name_blacklist (name) VALUES (?)", (name,))

def clear_name_blacklist():
    with _conn() as con:
        con.execute("DELETE FROM name_blacklist")

def get_and_blacklist_random_name() -> str:
    import random
    available = get_available_names()
    if not available:
        raise ValueError("No names left")
    name = random.choice(available)
    blacklist_name(name)
    return name

