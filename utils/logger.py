"""
Централизованный логгер с эмодзи.
Используй: from utils.logger import log
"""
import logging

logging.basicConfig(
    level=logging.WARNING,          # глушим всё стороннее (aiogram, aiohttp и т.д.)
    format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Наш логгер — всегда INFO
_logger = logging.getLogger("bot")
_logger.setLevel(logging.INFO)
if not _logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    _logger.addHandler(_h)
_logger.propagate = False


def _u(uid: int | None, username: str | None, crown: bool = False) -> str:
    """Форматирует пользователя. crown=True → 👑, False → 👤"""
    icon = "👑" if crown else "👤"
    if uid and username:
        return f"{icon} [{uid} @{username}]"
    if uid:
        return f"{icon} [{uid}]"
    return ""


def _is_admin(uid: int | None) -> bool:
    if uid is None:
        return False
    try:
        from data.db import is_admin as _ia
        return _ia(uid)
    except Exception:
        return False


class BotLogger:

    # ── Запуск ─────────────────────────────────────────────────────────────────
    def startup(self):
        _logger.info("🚀 Бот запущен и готов к работе")

    def db_ready(self):
        _logger.info("🗄️  База данных инициализирована")

    # ── Доступ ─────────────────────────────────────────────────────────────────
    def user_seen(self, uid: int, username: str | None = None):
        _logger.info(f"👋 Новый пользователь  {_u(uid, username, _is_admin(uid))}")

    def access_denied(self, uid: int, username: str | None = None):
        _logger.info(f"🚫 Нет доступа  {_u(uid, username, False)}")

    # ── Навигация ──────────────────────────────────────────────────────────────
    def start(self, uid: int, username: str | None = None):
        _logger.info(f"▶️  /start  {_u(uid, username, _is_admin(uid))}")

    def open_category(self, uid: int, category: str, username: str | None = None):
        _logger.info(f"📂 Категория [{category}]  {_u(uid, username, _is_admin(uid))}")

    def open_section(self, uid: int, section: str, username: str | None = None):
        _logger.info(f"📁 Раздел [{section}]  {_u(uid, username, _is_admin(uid))}")

    def open_template(self, uid: int, template: str, username: str | None = None):
        _logger.info(f"🖼  Шаблон [{template}]  {_u(uid, username, _is_admin(uid))}")

    def cancel(self, uid: int, template: str, username: str | None = None):
        _logger.info(f"❌ Отмена [{template}]  {_u(uid, username, _is_admin(uid))}")

    def clear_chat(self, uid: int, username: str | None = None):
        _logger.info(f"🗑️  Очистил чат  {_u(uid, username, _is_admin(uid))}")

    def open_settings(self, uid: int, username: str | None = None):
        _logger.info(f"⚙️  Настройки  {_u(uid, username, _is_admin(uid))}")

    def setting_changed(self, uid: int, key: str, value: str | int | None, username: str | None = None):
        _logger.info(f"🔧 Настройка [{key}={value}]  {_u(uid, username, _is_admin(uid))}")

    # ── Рендер ─────────────────────────────────────────────────────────────────
    def render_start(self, uid: int, template: str, username: str | None = None):
        _logger.info(f"⚙️  Рендер [{template}]...  {_u(uid, username, _is_admin(uid))}")

    def render_done(self, uid: int, template: str, username: str | None = None):
        _logger.info(f"✅ Готово [{template}]  {_u(uid, username, _is_admin(uid))}")

    def render_error(self, uid: int, template: str, error: str, username: str | None = None):
        _logger.error(f"💥 Ошибка рендера [{template}]: {error}  {_u(uid, username, _is_admin(uid))}")

    # ── Админ ──────────────────────────────────────────────────────────────────
    def admin_panel(self, uid: int, username: str | None = None):
        _logger.info(f"👨‍💼 Админ-панель  {_u(uid, username)}")

    def role_changed(self, admin_uid: int, target_uid: int, role: str, action: str,
                     admin_uname: str | None = None):
        verb = "выдана ✅" if action == "add" else "убрана 🚫"
        _logger.info(f"🎭 Роль [{role.upper()}] {verb}  👤 target=[{target_uid}]  by={_u(admin_uid, admin_uname, True)}")

    def roles_cleared(self, admin_uid: int, target_uid: int, admin_uname: str | None = None):
        _logger.info(f"🗑️  Роли очищены у 👤[{target_uid}]  by={_u(admin_uid, admin_uname, True)}")

    def admin_promoted(self, admin_uid: int, target_uid: int, admin_uname: str | None = None):
        _logger.info(f"👑 Назначен админ [{target_uid}]  by={_u(admin_uid, admin_uname, True)}")

    def admin_demoted(self, admin_uid: int, target_uid: int, admin_uname: str | None = None):
        _logger.info(f"⬇️  Снят админ [{target_uid}]  by={_u(admin_uid, admin_uname, True)}")

    def unhandled_text(self, uid: int, text: str, username: str | None = None):
        _logger.info(f"💬 Неизвестный текст: [{text}]  {_u(uid, username, _is_admin(uid))}")

    def broadcast(self, uid: int, text: str, target: str, username: str | None = None):
        _logger.info(f"📢 Рассылка ({target}): [{text[:20]}...]  {_u(uid, username, _is_admin(uid))}")


log = BotLogger()