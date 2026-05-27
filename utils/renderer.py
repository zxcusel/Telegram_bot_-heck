"""
Pillow renderer v3.
Режимы отрисовки поля:
  segments  — список {text, font, size, color} с поддержкой {key}-подстановки
              и \n для явных переносов. Единственный режим для смешанных шрифтов/цветов.
  area      — простой текст с автопереносом в прямоугольник (x1,y1,x2,y2)
  pos       — одна точка без переноса
Дополнительные флаги (только для area/pos):
  align         : "left" | "right" | "center"
  template      : строка с {key}-подстановкой
  format_number : True → форматировать как число (30000 → "30 000")
  suffix        : суффикс-строка (напр. "BOB")
  suffix_size   : pt размер суффикса
  suffix_align  : "center" → весь комплекс (число + суффикс) центрируется в area
  line_spacing  : множитель межстрочного интервала (default 1.2)
"""
import io
import os
from PIL import Image, ImageDraw, ImageFont

from data.config import CATALOG, FONTS, GEO_CATALOG

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
PT_TO_PX = 1.0   # Photoshop 72 dpi → 1 pt = 1 px


# ─────────────────────────────── helpers ─────────────────────────────────────

def _find_item(item_key: str, geo: str = "bo") -> dict | None:
    catalog = GEO_CATALOG.get(geo, {}).get("catalog", {})
    for line in catalog.values():
        for section in line["sections"].values():
            if item_key in section["items"]:
                return section["items"][item_key]
    return None


def _resolve_geo_asset_path(asset_path: str, geo: str = "bo") -> str:
    """Return a geo-specific asset path when the default asset is present in a geo folder."""
    if not asset_path.startswith("assets/"):
        return asset_path

    if geo == "bo":
        candidates = []
        if asset_path.startswith("assets/fd/proofs/"):
            candidates.append(asset_path.replace("assets/fd/proofs/", "assets/Bolivia/FD/proofs/", 1))
        elif asset_path.startswith("assets/fd/"):
            candidates.append(asset_path.replace("assets/fd/", "assets/Bolivia/FD/", 1))
        if asset_path.startswith("assets/rd/proofs/"):
            candidates.append(asset_path.replace("assets/rd/proofs/", "assets/Bolivia/RD/proofs/", 1))
        elif asset_path.startswith("assets/rd/"):
            candidates.append(asset_path.replace("assets/rd/", "assets/Bolivia/RD/", 1))
        if asset_path == "assets/other/Check.png":
            candidates.append("assets/Bolivia/Чек/Check.png")
        if asset_path == "assets/other/QR_code.png":
            candidates.append("assets/Bolivia/QRCode/QR_code.png")
        if asset_path == "assets/other/SUPPORT.jpg":
            candidates.append("assets/Bolivia/SUPPORT/SUPPORT.jpg")

        for candidate in candidates:
            full_candidate = os.path.normpath(os.path.join(BASE_DIR, candidate))
            if os.path.exists(full_candidate):
                return candidate

    # fallback to original path if no geo-specific override exists
    return asset_path


def _load_font(alias: str, size_pt: int | float) -> ImageFont.FreeTypeFont:
    size_px = max(1, round(float(size_pt) * PT_TO_PX))
    path = os.path.join(BASE_DIR, FONTS.get(alias, FONTS["montserrat"]))
    
    # Решаем проблему с регистром на Linux (Pterodactyl)
    dir_name, base_name = os.path.split(path)
    if os.path.exists(dir_name):
        lower_base = base_name.lower()
        for f in os.listdir(dir_name):
            if f.lower() == lower_base:
                path = os.path.join(dir_name, f)
                break

    try:
        return ImageFont.truetype(path, size=size_px)
    except (IOError, OSError):
        return ImageFont.load_default()


def _line_h(font: ImageFont.FreeTypeFont, spacing: float = 1.2) -> int:
    bb = font.getbbox("Hg")
    return round((bb[3] - bb[1]) * spacing)


def _wrap(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    """Word-wrap single paragraph to pixel width."""
    lines, cur = [], ""
    for word in text.split():
        test = (cur + " " + word).strip()
        if font.getlength(test) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


import re

def _format_number(value: str) -> str:
    clean = re.sub(r'[^\d]', '', value)
    try:
        return f"{int(clean):,}".replace(",", " ")
    except ValueError:
        return value.strip()


def _format_number_dot(value: str) -> str:
    """Форматирование с точкой-разделителем тысяч: 10000 → 10.000"""
    clean = re.sub(r'[^\d]', '', value)
    try:
        return f"{int(clean):,}".replace(",", ".")
    except ValueError:
        return value.strip()


def _format_number_comma(value: str) -> str:
    """Форматирование с запятой-разделителем тысяч: 10000 → 10,000"""
    clean = re.sub(r'[^\d]', '', value)
    try:
        return f"{int(clean):,}"
    except ValueError:
        return value.strip()


def _format_number_none(value: str) -> str:
    """Убирает все разделители: 1 000 -> 1000"""
    clean = re.sub(r'[^\d]', '', value)
    return clean


# ─────────────────────── simple area/pos drawing ─────────────────────────────

def _draw_area(draw, text, font, color, area, align="left", spacing=1.2, valign="top"):
    x1, y1, x2, y2 = area
    max_w = x2 - x1
    lh = _line_h(font, spacing)
    # split on explicit \n first, then word-wrap each paragraph
    lines = []
    for para in text.split("\n"):
        if para == "":
            lines.append("")
        else:
            lines.extend(_wrap(para, font, max_w))
    # Vertical alignment
    if valign == "center":
        total_h = len(lines) * lh
        y = y1 + max(0, ((y2 - y1) - total_h) // 2)
    else:
        y = y1
    for line in lines:
        if y > y2:
            break
        lw = font.getlength(line) if line else 0
        if align == "right":
            x = x2 - lw
        elif align == "center":
            x = x1 + (max_w - lw) / 2
        else:
            x = x1
        if line:
            draw.text((x, y), line, font=font, fill=color)
        y += lh


def _draw_multiline_from_pos(draw, text, font, color, pos, spacing=1.0, align="left"):
    """
    Многострочный текст от одной позиции (x, y).
    Текст разделяется только по явным \n, без горизонтального переноса.
    y в pos — верхний край первой строки.
    """
    x, y = pos
    lh = _line_h(font, spacing)
    lines = text.split("\n")
    
    for line in lines:
        if align == "center":
            lw = font.getlength(line) if line else 0
            draw_x = x - lw / 2
        elif align == "right":
            lw = font.getlength(line) if line else 0
            draw_x = x - lw
        else:
            draw_x = x
        
        if line:
            draw.text((draw_x, y), line, font=font, fill=color)
        y += lh


# ─────────────────────── segments block drawing ──────────────────────────────

def _draw_segments(draw, segments: list[dict], area: tuple,
                   spacing: float = 1.3, field_values: dict | None = None,
                   blank_line_size: int = 0, align: str = "left"):
    """
    Draw a rich text block where every segment can have its own font/size/color.
    Segments with text="\n" or text containing "\n" produce line breaks.
    field_values are substituted via str.format(**field_values).
    """
    if field_values is None:
        field_values = {}

    x1, y1, x2, y2 = area
    max_w = x2 - x1

    # ── 1. Resolve: substitute field values, load fonts ──────────────────────
    resolved: list[dict] = []
    for seg in segments:
        raw = seg["text"]
        try:
            if seg.get("template_eval"):
                eval_func = eval(seg["template_eval"])
                raw = eval_func(**field_values)
            if seg.get("format_number"):
                local_fields = {k: _format_number(v) for k, v in field_values.items()}
                raw = raw.format(**local_fields)
            elif seg.get("format_number_comma"):
                local_fields = {k: _format_number_comma(v) for k, v in field_values.items()}
                raw = raw.format(**local_fields)
            elif seg.get("format_number_dot"):
                local_fields = {k: _format_number_dot(v) for k, v in field_values.items()}
                raw = raw.format(**local_fields)
            elif seg.get("format_number_none"):
                local_fields = {k: _format_number_none(v) for k, v in field_values.items()}
                raw = raw.format(**local_fields)
            else:
                raw = raw.format(**field_values)
        except (KeyError, ValueError):
            pass
        resolved.append({
            "text":  raw,
            "font":  _load_font(seg.get("font", "montserrat"), seg.get("size", 20)),
            "color": seg.get("color", (0, 0, 0)),
        })

    # ── 2. Tokenise: (text_chunk, font, color); "\n" → newline sentinel ───────
    tokens: list[tuple] = []   # (str, font|None, color|None)
    for seg in resolved:
        parts = seg["text"].split("\n")
        for i, part in enumerate(parts):
            if i > 0:
                tokens.append(("\n", None, None))
            # split into words+spaces so we can wrap
            words = part.split(" ")
            for j, w in enumerate(words):
                if w:
                    tokens.append((w, seg["font"], seg["color"]))
                if j < len(words) - 1:
                    # preserve inter-word space, carry font of left word
                    tokens.append((" ", seg["font"], seg["color"]))

    # ── 3. Layout: greedy line packing ───────────────────────────────────────
    lines: list[list[tuple]] = []
    cur_line: list[tuple] = []
    cur_w: float = 0.0

    def flush():
        nonlocal cur_line, cur_w
        # strip trailing spaces
        while cur_line and cur_line[-1][0] == " ":
            cur_line.pop()
        lines.append(cur_line)
        cur_line, cur_w = [], 0.0

    for tok, font, color in tokens:
        if tok == "\n":
            flush()
            lines.append([])   # blank line
            continue
        # skip leading spaces on a new line
        if tok == " " and not cur_line:
            continue
        w = font.getlength(tok)
        if cur_w + w > max_w + 0.5 and cur_line:
            flush()
            if tok.strip():
                cur_line.append((tok, font, color))
                cur_w = w
        else:
            cur_line.append((tok, font, color))
            cur_w += w
    flush()

    # ── 4. Draw ───────────────────────────────────────────────────────────────
    y = float(y1)
    # blank_line_size > 0 → фиксированная высота пустой строки в px
    # иначе — высота строки рассчитывается из шрифта
    default_lh = round(20 * spacing)
    
    global_lh = max((_line_h(f, spacing) for line in lines for _, f, _ in line if f), default=default_lh)
    global_max_ascent = max((f.getmetrics()[0] for line in lines for _, f, _ in line if f), default=0)

    for line in lines:
        if not line:
            if blank_line_size > 0:
                y += blank_line_size
            else:
                y += global_lh
            continue
            
        lh = global_lh
        if y + lh > y2 + lh:   # allow slight overflow on last line
            break
            
        if align == "right":
            # measure total line width, then draw from right edge
            line_w = sum(f.getlength(t) for t, f, _ in line if f)
            x = float(x2) - line_w
        elif align == "center":
            line_w = sum(f.getlength(t) for t, f, _ in line if f)
            x = float(x1) + (max_w - line_w) / 2
        else:
            x = float(x1)
            
        for tok, font, color in line:
            # Используем anchor="ls" (left, baseline) для выравнивания шрифтов
            draw.text((x, y + global_max_ascent), tok, font=font, fill=color, anchor="ls")
            x += font.getlength(tok)
        y += lh



# ─────────────────────────── chat bubble drawing ─────────────────────────────

def _wrap_text_bubble(text: str, font: ImageFont.FreeTypeFont, inner_w: int) -> list[str]:
    """Word-wrap текст под заданную ширину. Принудительно разбивает слишком длинные слова."""

    def _split_long_word(word: str) -> list[str]:
        """Разбивает одно слово на части которые влезают в inner_w."""
        parts, cur = [], ""
        for ch in word:
            test = cur + ch
            if font.getlength(test) <= inner_w:
                cur = test
            else:
                if cur:
                    parts.append(cur)
                cur = ch
        if cur:
            parts.append(cur)
        return parts or [word]

    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split()
        cur = ""
        for word in words:
            # Если само слово шире inner_w — принудительно разбиваем
            if font.getlength(word) > inner_w:
                if cur:
                    lines.append(cur)
                    cur = ""
                for part in _split_long_word(word):
                    test = (cur + " " + part).strip() if cur else part
                    if font.getlength(test) <= inner_w:
                        cur = test
                    else:
                        if cur:
                            lines.append(cur)
                        cur = part
                continue
            test = (cur + " " + word).strip() if cur else word
            if font.getlength(test) <= inner_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines if lines else [""]


def _draw_bubble(
    img: Image.Image,
    text: str,
    font: ImageFont.FreeTypeFont,
    x: int,
    y: int,
    max_bubble_w: int,
    bg_color: tuple,
    text_color: tuple,
    radius: int = 15,
    pad_top: int = 12,
    pad_side: int = 15,
    pad_bottom: int = 12,
) -> int:
    """
    Рисует пузырь с текстом. Возвращает y нижней границы.
    """
    inner_w = max_bubble_w - pad_side * 2
    lines = _wrap_text_bubble(text, font, inner_w)

    bb = font.getbbox("Hg")
    line_h = bb[3] - bb[1]
    line_spacing = round(line_h * 0.25)

    # Реальная ширина пузыря по самой длинной строке
    max_line_w = max((font.getlength(ln) for ln in lines if ln), default=40)
    bubble_w = min(max_bubble_w, int(max_line_w + pad_side * 2) + 2)
    bubble_w = max(bubble_w, 60)

    total_text_h = len(lines) * line_h + max(0, len(lines) - 1) * line_spacing
    bubble_h = pad_top + total_text_h + pad_bottom

    # Рисуем скруглённый прямоугольник на отдельном слое
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle(
        [x, y, x + bubble_w, y + bubble_h],
        radius=radius,
        fill=bg_color
    )
    img.alpha_composite(layer)

    # Рисуем текст
    draw = ImageDraw.Draw(img)
    ty = y + pad_top
    for line in lines:
        if line:
            draw.text((x + pad_side, ty), line, font=font, fill=text_color)
        ty += line_h + line_spacing

    return y + bubble_h


def render_support(field_values: dict[str, str], asset_path: str,
                   font_path: str, font_size_pt: int = 20) -> io.BytesIO:
    """
    Рисует два диалоговых пузыря на SUPPORT.jpg.
    msg1 — синий (правый, от пользователя)
    msg2 — тёмный (левый, от поддержки)
    """
    img = Image.open(asset_path).convert("RGBA")
    img_w, img_h = img.size

    size_px = max(1, round(font_size_pt * PT_TO_PX))
    try:
        font = ImageFont.truetype(font_path, size=size_px)
    except (IOError, OSError):
        font = ImageFont.load_default()

    margin_x     = 18
    gap           = 12
    start_y       = 330
    max_bubble_w  = int(img_w * 0.77)

    msg1 = field_values.get("msg1", "")
    msg2 = field_values.get("msg2", "")

    # ── Пузырь 1: вычисляем реальную ширину и прижимаем к правому краю ───────
    pad_side  = 15
    inner_w   = max_bubble_w - pad_side * 2
    lines1    = _wrap_text_bubble(msg1, font, inner_w)
    max_lw1   = max((font.getlength(l) for l in lines1 if l), default=40)
    actual_w1 = min(max_bubble_w, int(max_lw1 + pad_side * 2) + 2)
    actual_w1 = max(actual_w1, 60)
    x1 = img_w - margin_x - actual_w1

    bottom1 = _draw_bubble(
        img, msg1, font,
        x=x1, y=start_y,
        max_bubble_w=actual_w1,
        bg_color=(30, 100, 220, 255),
        text_color=(255, 255, 255, 255),
        radius=15, pad_top=12, pad_side=15, pad_bottom=12
    )

    # ── Пузырь 2: левый ───────────────────────────────────────────────────────
    _draw_bubble(
        img, msg2, font,
        x=margin_x, y=bottom1 + gap,
        max_bubble_w=max_bubble_w,
        bg_color=(40, 47, 70, 255),
        text_color=(255, 255, 255, 255),
        radius=15, pad_top=12, pad_side=15, pad_bottom=12
    )

    out = io.BytesIO()
    img.convert("RGB").save(out, format="PNG")
    out.seek(0)
    return out

# ─────────────────────────── main render ─────────────────────────────────────

def render_image(item_key: str, field_values: dict[str, str], geo: str = "bo") -> io.BytesIO:
    item = _find_item(item_key, geo)
    if item is None:
        raise ValueError(f"Unknown item_key: {item_key}")

    asset_path = _resolve_geo_asset_path(item["asset"], geo)
    asset_path = os.path.normpath(os.path.join(BASE_DIR, asset_path))
    img = Image.open(asset_path).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    for field in item["fields"]:
        key = field["key"]
        tc  = field.get("text_config", {})

        # ── collect_only: поле только собирает значение, не рисует ничего ────────
        if tc.get("collect_only"):
            continue

        # ── cover_area: закрашиваем область цветом перед рисованием ─────────────
        if tc.get("cover_color") and tc.get("cover_area"):
            color = tc["cover_color"]
            if len(color) == 3:
                color = color + (255,)
            draw.rectangle(tc["cover_area"], fill=color)

        # ── image_paste: вставляем пользовательское изображение в area ───────────
        if tc.get("image_paste"):
            if "image_eval" in tc:
                img_data = eval(tc["image_eval"])(field_values.get(key, ""), field_values)
            else:
                img_data = field_values.get(key)
            if img_data:
                area = tc["area"]  # (x1, y1, x2, y2)
                x1, y1, x2, y2 = area
                w, h = x2 - x1, y2 - y1
                if isinstance(img_data, (bytes, bytearray)):
                    import io as _io
                    user_img = Image.open(_io.BytesIO(img_data)).convert("RGBA")
                else:
                    user_img = Image.open(os.path.join(BASE_DIR, img_data)).convert("RGBA")
                # Растягиваем точно по области (stretch, без сохранения пропорций)
                user_img = user_img.resize((w, h), Image.LANCZOS)
                img.paste(user_img, (x1, y1), user_img)
                draw = ImageDraw.Draw(img)
            continue

        # ── segments mode ─────────────────────────────────────────────────────
        if "segments" in tc:
            _draw_segments(
                draw, tc["segments"], tc["area"],
                spacing=tc.get("line_spacing", 1.3),
                field_values=field_values,
                blank_line_size=tc.get("blank_line_size", 0),
                align=tc.get("segments_align", "left"),
            )
            continue

        # ── normal mode ───────────────────────────────────────────────────────
        font  = _load_font(tc.get("font", "montserrat"), tc.get("size", 32))
        color = tc.get("color", (0, 0, 0))
        align = tc.get("align", "left")

        # resolve value
        val = field_values.get(key, "")
        
        template = tc.get("template")
        if "template_eval" in tc:
            try:
                fn = eval(tc["template_eval"])
                try:
                    template = fn(val, field_values)
                except TypeError:
                    template = fn(val)
            except Exception:
                pass
        
        # Apply formatting to the specific value if it's a direct field
        if tc.get("format_number"):
            val = _format_number(val)
        elif tc.get("format_number_comma"):
            val = _format_number_comma(val)
        elif tc.get("format_number_dot"):
            val = _format_number_dot(val)
        elif tc.get("format_number_none"):
            val = _format_number_none(val)
            
        if template:
            try:
                # To support formatting inside template, we can pass formatted val
                # Or just format a copy of field_values. We'll do it for all fields:
                local_fields = field_values.copy()
                local_fields[key] = val
                display = template.format(**local_fields)
            except (KeyError, ValueError):
                display = template
        else:
            display = val

        if not display:
            continue

        if "color_eval" in tc:
            try:
                fn = eval(tc["color_eval"])
                color = fn(val)
            except Exception:
                pass

        if "special_number_sizes" in tc:
            pos = tc.get("pos", (0, 0))
            f_main = font
            f_small = _load_font(tc.get("font", "montserrat"), tc["special_number_sizes"])
            f_space = _load_font(tc.get("font", "montserrat"), tc.get("space_size", tc["special_number_sizes"]))
            x, y = pos
            for ch in display:
                if ch == " ":
                    f_curr = f_space
                elif ch in ",.":
                    f_curr = f_small
                else:
                    f_curr = f_main
                draw.text((x, y), ch, font=f_curr, fill=color, anchor=tc.get("anchor", "ls"))
                x += f_curr.getlength(ch)
            continue

        area = tc.get("area")

        # ── suffix mode (e.g. "30 000 BOB" with two sizes) ───────────────────
        suffix      = tc.get("suffix")
        suffix_size = tc.get("suffix_size")
        if suffix and suffix_size and area:
            x1, y1, x2, y2 = area
            f_main   = font
            f_suffix = _load_font(tc.get("font", "montserrat"), suffix_size)
            main_w   = f_main.getlength(display)
            sp_w     = f_main.getlength(" ")
            suf_w    = f_suffix.getlength(suffix)
            total_w  = main_w + sp_w + suf_w
            area_w   = x2 - x1

            if align == "center":
                x_main = x1 + (area_w - total_w) / 2
            elif align == "right":
                x_main = x2 - total_w
            else:
                x_main = x1

            x_suffix = x_main + main_w + sp_w

            # Vertical center: use main font height to center block in area
            asc_m, desc_m = f_main.getmetrics()
            asc_s, _      = f_suffix.getmetrics()
            text_h = asc_m + abs(desc_m)
            area_h = y2 - y1
            # center vertically: push down by half the remaining space
            y_main   = float(y1) + max(0, (area_h - text_h) / 2)
            # align suffix baseline with main baseline
            y_suffix = y_main + (asc_m - asc_s)

            draw.text((x_main,   y_main),   display, font=f_main,   fill=color)
            draw.text((x_suffix, y_suffix), suffix,  font=f_suffix, fill=color)
            continue

        # ── prefix mode (e.g. "UYU 30 000" with two sizes) ───────────────────
        prefix      = tc.get("prefix")
        prefix_size = tc.get("prefix_size")
        if prefix and prefix_size and not area:
            f_main   = font
            f_prefix = _load_font(tc.get("font", "montserrat"), prefix_size)
            main_w   = f_main.getlength(display)
            sp_w     = f_main.getlength(" ") if tc.get("prefix_space", True) else 0
            pref_w   = f_prefix.getlength(prefix)
            total_w  = pref_w + sp_w + main_w
            
            pos = tc.get("pos", (50, 50))
            x, y = pos
            if align == "center":
                x_start = x - total_w / 2
            elif align == "right":
                x_start = x - total_w
            else:
                x_start = x
            
            x_pref = x_start
            x_main = x_start + pref_w + sp_w
            
            asc_m, _ = f_main.getmetrics()
            asc_p, _ = f_prefix.getmetrics()
            
            y_pref = y + tc.get("prefix_y_offset", 0)
            y_main = y + tc.get("main_y_offset", 0)
            
            draw.text((x_pref, y_pref), prefix, font=f_prefix, fill=color)
            draw.text((x_main, y_main), display, font=f_main, fill=color)
            continue

        # ── area or pos ───────────────────────────────────────────────────────
        if area:
            _draw_area(draw, display, font, color, area,
                       align=align, spacing=tc.get("line_spacing", 1.2),
                       valign=tc.get("valign", "top"))
        else:
            pos = tc.get("pos", (50, 50))
            # Многострочный текст от одной позиции (если есть \n)
            if "\n" in display:
                _draw_multiline_from_pos(draw, display, font, color, pos,
                                        spacing=tc.get("line_spacing", 1.0),
                                        align=align)
            else:
                # Однострочный текст
                anchor = tc.get("anchor")
                sw = tc.get("stroke_width", 0)
                sf = tc.get("stroke_fill", color)
                if align == "right":
                    lw = font.getlength(display)
                    if anchor:
                        draw.text((pos[0] - lw, pos[1]), display, font=font, fill=color, anchor=anchor, stroke_width=sw, stroke_fill=sf)
                    else:
                        draw.text((pos[0] - lw, pos[1]), display, font=font, fill=color, stroke_width=sw, stroke_fill=sf)
                elif align == "center":
                    lw = font.getlength(display)
                    if anchor:
                        draw.text((pos[0] - lw / 2, pos[1]), display, font=font, fill=color, anchor=anchor, stroke_width=sw, stroke_fill=sf)
                    else:
                        draw.text((pos[0] - lw / 2, pos[1]), display, font=font, fill=color, stroke_width=sw, stroke_fill=sf)
                else:
                    if anchor:
                        draw.text(pos, display, font=font, fill=color, anchor=anchor, stroke_width=sw, stroke_fill=sf)
                    else:
                        draw.text(pos, display, font=font, fill=color, stroke_width=sw, stroke_fill=sf)

    img = Image.alpha_composite(img, txt_layer)
    out = io.BytesIO()
    img.convert("RGB").save(out, format="PNG")
    out.seek(0)
    return out

# ─────────────────────────── video render ──────────────────────────────────────

def _rgb_to_hex(color_tuple):
    if len(color_tuple) >= 3:
        return "{:02x}{:02x}{:02x}".format(color_tuple[0], color_tuple[1], color_tuple[2])
    return "ffffff"


def _interp_expr(v0: int, v1: int, t0: float, t1: float, easing: str = "linear") -> str:
    """
    Генерирует FFmpeg-выражение для интерполяции v0 → v1 за время [t0, t1].
    Использует только базовую арифметику (без pow), чтобы FFmpeg drawtext надёжно парсил.
    easing: 'linear' | 'ease_in' | 'ease_out' | 'ease_in_out'
    """
    if v0 == v1:
        return str(v0)
    dur = round(t1 - t0, 6)
    if dur <= 0:
        return str(v1)
    p = f"((t-{t0})/{dur})"
    if easing == "ease_out":
        # 1-(1-p)^2  = p*(2-p)
        e = f"({p}*(2-{p}))"
    elif easing == "ease_out_3":
        # 1-(1-p)^3
        inv = f"(1-{p})"
        e = f"(1-{inv}*{inv}*{inv})"
    elif easing == "ease_out_4":
        inv = f"(1-{p})"
        e = f"(1-{inv}*{inv}*{inv}*{inv})"
    elif easing == "ease_in":
        # p^2
        e = f"({p}*{p})"
    elif easing == "ease_in_3":
        e = f"({p}*{p}*{p})"
    elif easing == "ease_in_4":
        e = f"({p}*{p}*{p}*{p})"
    elif easing == "ease_in_5":
        e = f"({p}*{p}*{p}*{p}*{p})"
    elif easing == "ease_in_out":
        # p<0.5: 2*p^2; p>=0.5: 1-(-2p+2)^2/2
        e = f"if(lt({p},0.5),2*{p}*{p},1-(-2*{p}+2)*(-2*{p}+2)/2)"
    elif easing == "ease_in_out_sine":
        # Идеальная "волна" F9: 50% / 50%
        e = f"(1-cos(PI*{p}))/2"
    elif easing == "ease_in_out_3":
        # p<0.5: 4*p^3; p>=0.5: 1-(-2p+2)^3/2
        inv = f"(-2*{p}+2)"
        e = f"if(lt({p},0.5),4*{p}*{p}*{p},1-({inv}*{inv}*{inv})/2)"
    else:  # linear
        e = p
    return f"({v0}+({v1-v0})*{e})"


def _esc(text: str) -> str:
    """Escape text content for FFmpeg drawtext filter."""
    return (
        text
        .replace("\\", "\\\\")
        .replace("'", "\u2019")
        .replace(":", "\\:")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _make_alpha_opt(tc: dict) -> str:
    """
    Возвращает суффикс :alpha='...' для drawtext, если задан fade-out.
    Поддерживаемые ключи text_config:
      vid_fade_out_start, vid_fade_out_end
    """
    fade_s = tc.get("vid_fade_out_start")
    fade_e = tc.get("vid_fade_out_end")
    if fade_s is None or fade_e is None:
        return ""
    try:
        fs = float(fade_s)
        fe = float(fade_e)
    except (TypeError, ValueError):
        return ""
    if fe <= fs:
        return ""

    # alpha = 1 до fs, затем линейно -> 0 к fe, после fe = 0
    alpha_expr = f"if(lt(t,{fs}),1,if(lt(t,{fe}),({fe}-t)/({fe}-{fs}),0))"
    return f":alpha='{alpha_expr}'"


def _build_chained_expr(kfs: list[dict], smooth: bool, easing: str, axis: str, default_val: float) -> str:
    """
    Собирает вложенное if-выражение для FFmpeg overlay по X или Y
    из списка кейфреймов, поддерживая плавную анимацию.
    """
    if not kfs:
        return str(default_val)
    if len(kfs) == 1:
        return str(kfs[0].get(axis, default_val))
    
    expr = str(kfs[-1].get(axis, default_val))
    for i in range(len(kfs)-2, -1, -1):
        kf = kfs[i]
        kf_next = kfs[i+1]
        v0 = kf.get(axis, default_val)
        v1 = kf_next.get(axis, v0)
        t0 = kf["t"]
        t1 = kf_next["t"]
        current_easing = kf.get("easing", easing)
        
        if smooth and v0 != v1:
            interp = _interp_expr(v0, v1, t0, t1, current_easing)
        else:
            interp = str(v0)
            
        expr = f"if(lt(t,{t1}),{interp},{expr})"
    
    t0 = kfs[0]["t"]
    v0 = kfs[0].get(axis, default_val)
    expr = f"if(lt(t,{t0}),{v0},{expr})"
    return expr


def render_video(item_key: str, field_values: dict[str, str], geo: str = "bo") -> io.BytesIO:
    import subprocess
    import tempfile
    import uuid

    item = _find_item(item_key, geo)
    if item is None:
        raise ValueError(f"Unknown item_key: {item_key}")

    asset_path = _resolve_geo_asset_path(item["asset"], geo)
    asset_path = os.path.normpath(os.path.join(BASE_DIR, asset_path))
    out_path = os.path.join(tempfile.gettempdir(), f"render_{uuid.uuid4().hex}.mp4")
    import shutil
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        # Fallback to local files if not in PATH
        local_exe = os.path.join(BASE_DIR, "ffmpeg.exe")
        local_bin = os.path.join(BASE_DIR, "ffmpeg")
        ffmpeg_path = local_exe if os.path.exists(local_exe) else local_bin

    drawtexts = []
    overlay_images = []

    for field in item["fields"]:
        key = field["key"]
        tc = field.get("text_config", {})
        if tc.get("collect_only"):
            continue

        if tc.get("image_paste"):
            img_data = field_values.get(key)
            if img_data:
                if "size" in tc:
                    w, h = tc["size"]
                elif "area" in tc:
                    w, h = tc["area"][2] - tc["area"][0], tc["area"][3] - tc["area"][1]
                else:
                    w, h = 100, 100
                    
                pos = tc.get("pos")
                if pos:
                    x1, y1 = pos
                elif "area" in tc:
                    x1, y1 = tc["area"][0], tc["area"][1]
                else:
                    x1, y1 = 0, 0

                img_path = os.path.join(tempfile.gettempdir(), f"img_{uuid.uuid4().hex}.png")
                
                from PIL import Image
                import io as _io
                if isinstance(img_data, (bytes, bytearray)):
                    user_img = Image.open(_io.BytesIO(img_data)).convert("RGBA")
                else:
                    user_img = Image.open(img_data).convert("RGBA")
                
                user_img = user_img.resize((w, h), Image.LANCZOS)
                user_img.save(img_path, format="PNG")
                
                overlay_images.append({
                    "path": img_path,
                    "x": x1,
                    "y": y1,
                    "tc": tc,
                    "start_time": tc.get("start_time", 0),
                    "end_time": tc.get("end_time", 9999)
                })
            continue

        raw_value = field_values.get(key, "")
        template = tc.get("template")
        
        # Пропускаем поле только если оно пусто И нет template И нет cover
        # Если есть template — используем его, даже если raw_value пусто
        if not raw_value and not template and not (tc.get("cover_color") and tc.get("cover_area")):
            continue

        display_value = raw_value
        if template:
            try:
                # Используем format_map с collections.defaultdict для безопасности
                from collections import defaultdict
                safe_fields = defaultdict(str, field_values)
                display_value = template.format_map(safe_fields)
            except (KeyError, ValueError, Exception):
                display_value = template
        # Поддерживаем оба формата: реальные переводы строк и литералы "\n" из конфига.
        if isinstance(display_value, str):
            display_value = display_value.replace("\\n", "\n")
        
        # Пропускаем, если после обработки текст всё еще пуст и нет cover
        if not display_value and not (tc.get("cover_color") and tc.get("cover_area")):
            continue

        # Отрисовка подложки/закраски (cover_area) для видео через drawbox filter
        if tc.get("cover_color") and tc.get("cover_area"):
            cc = tc["cover_color"]
            cc_hex = _rgb_to_hex(cc) if isinstance(cc, tuple) else str(cc).replace("#", "")
            cx1, cy1, cx2, cy2 = tc["cover_area"]
            cw = cx2 - cx1
            ch = cy2 - cy1
            c_start = tc.get("start_time", 0)
            c_end   = tc.get("end_time", 30)
            c_en    = f"between(t,{c_start},{c_end})"
            drawtexts.append(f"drawbox=x={cx1}:y={cy1}:w={cw}:h={ch}:color=0x{cc_hex}:t=fill:enable='{c_en}'")

        if not display_value:
            continue

        start_time = tc.get("start_time", 0)
        end_time   = tc.get("end_time", 30)
        color      = tc.get("color", (255, 255, 255))
        color_hex  = _rgb_to_hex(color) if isinstance(color, tuple) else str(color).replace("#", "")
        shadow     = tc.get("shadow", False)
        alpha_opt  = _make_alpha_opt(tc)

        # ── Режим двух сегментов (prefix_font + value) по центру ─────────────
        if "prefix_font" in tc:
            prefix_text = _esc(tc.get("prefix", ""))
            value_text  = _esc(raw_value)
            size        = tc.get("size", 40)

            prefix_font = FONTS.get(tc["prefix_font"], FONTS["sf_pro"])
            value_font  = FONTS.get(tc.get("value_font", "sf_pro_medium"), FONTS["sf_pro_medium"])
            prefix_fp   = prefix_font.replace("\\", "/").replace(":", "\\:")
            value_fp    = value_font.replace("\\", "/").replace(":", "\\:")

            y_pos       = tc.get("y", 600)
            x_offset    = tc.get("x_offset", 0)
            enable_expr = f"between(t,{start_time},{end_time})"

            prefix_str  = tc.get("prefix", "")
            tw_prefix   = round(size * 0.48 * len(prefix_str))
            tw_value    = round(size * 0.48 * len(raw_value))
            tw_combined = tw_prefix + tw_value

            if x_offset != 0:
                # Используем {:+d} чтобы получить +20 или -20 (а не +-20)
                x_start = f"(w-{tw_combined})/2{x_offset:+d}"
                x_val   = f"(w-{tw_combined})/2+{tw_prefix}{x_offset:+d}"
            else:
                x_start = f"(w-{tw_combined})/2"
                x_val   = f"(w-{tw_combined})/2+{tw_prefix}"

            shadow_sfx = ":shadowcolor=0x000000@0.6:shadowx=2:shadowy=2" if shadow else ""
            dt1 = (f"drawtext=fontfile='{prefix_fp}':text='{prefix_text}':"
                   f"fontcolor=0x{color_hex}:fontsize={size}:x={x_start}:y={y_pos}:"
                   f"enable='{enable_expr}'{shadow_sfx}")
            dt2 = (f"drawtext=fontfile='{value_fp}':text='{value_text}':"
                   f"fontcolor=0x{color_hex}:fontsize={size}:"
                   f"x={x_val}:y={y_pos}:enable='{enable_expr}'{shadow_sfx}")
            drawtexts.append(dt1)
            drawtexts.append(dt2)
            continue

        # ── Режим: числовой префикс + число (vid_prefix) ─────────────────────
        # Рисует "Bs 10.000" двумя слоями drawtext с разными цветами.
        # Поддерживает покадровую анимацию через vid_keyframes (см. config.py).
        #
        # Параметры в text_config:
        #   vid_prefix        — строка-префикс ("Bs")
        #   vid_prefix_color  — RGB цвет префикса
        #   vid_prefix_size   — pt размер шрифта префикса
        #   vid_prefix_gap    — px расстояние между префиксом и числом
        #   vid_prefix_char_w — коэф. ширины символа для центровки (0.48–0.56)
        #   vid_format_dot    — True: 10000 → 10.000
        #   y_bottom          — True: pos[1] = нижний край текста
        #   vid_keyframes     — список {"t": сек, "y": px, "x_offset": px}
        #                       каждый кадр задаёт позицию на интервале [t, t_next)
        if "vid_prefix" in tc:
            display      = _format_number_dot(raw_value) if tc.get("vid_format_dot") else raw_value
            size         = tc.get("size", 40)
            prefix_text  = tc["vid_prefix"]
            prefix_color = tc.get("vid_prefix_color", (255, 255, 255))
            prefix_size  = tc.get("vid_prefix_size", size)
            gap          = tc.get("vid_prefix_gap", 12)
            char_w       = tc.get("vid_prefix_char_w", 0.52)
            y_bottom     = tc.get("y_bottom", True)
            prefix_y_off = tc.get("vid_prefix_y_offset", 0)  # px вверх относительно числа (отрицат. = выше)
            global_x_off = tc.get("vid_x_offset", 0)         # px глобальный сдвиг (положит. = правее)

            prefix_hex = (_rgb_to_hex(prefix_color) if isinstance(prefix_color, tuple)
                          else str(prefix_color).replace("#", ""))

            tw_p = round(prefix_size * char_w * len(prefix_text))
            tw_n = round(size        * char_w * len(display))
            tw_t = tw_p + gap + tw_n

            font_alias  = tc.get("font", "montserrat")
            font_path_e = FONTS.get(font_alias, FONTS["montserrat"]).replace("\\", "/").replace(":", "\\:")

            def _make_pair(t_s, t_e, y_val, x_off=0, y_bs=None,
                           _tw_t=tw_t, _tw_p=tw_p, _gap=gap, _y_b=y_bottom,
                           _fpe=font_path_e, _pt=prefix_text, _phex=prefix_hex,
                           _psz=prefix_size, _disp=display, _chex=color_hex, _sz=size,
                           _py_off=prefix_y_off, _gx=global_x_off):
                """Два drawtext: префикс + число для одного временного интервала."""
                # x_total = глобальный сдвиг + покадровый сдвиг
                xt = _gx + x_off
                x_p = f"(w-{_tw_t})/2{xt:+d}" if xt else f"(w-{_tw_t})/2"
                x_n = f"(w-{_tw_t})/2+{_tw_p}+{_gap}{xt:+d}" if xt else f"(w-{_tw_t})/2+{_tw_p}+{_gap}"
                y_e = f"{y_val}-text_h" if _y_b else str(y_val)
                # y_p: позиция Bs по вертикали
                # 1й приоритет: y_bs в кейфрейме (абсолютное y нижнего края)
                # 2й приоритет: vid_prefix_y_offset (сдвиг от y числа)
                if y_bs is not None:
                    y_p = f"{y_bs}-text_h" if _y_b else str(y_bs)
                elif _py_off:
                    y_p = (f"{y_val}-text_h{_py_off:+d}" if _y_b else f"{y_val}{_py_off:+d}")
                else:
                    y_p = y_e
                en  = f"between(t,{t_s},{t_e})"
                return [
                    (f"drawtext=fontfile='{_fpe}':text='{_esc(_pt)}':"
                     f"fontcolor=0x{_phex}:fontsize={_psz}:x={x_p}:y={y_p}:enable='{en}'{alpha_opt}"),
                    (f"drawtext=fontfile='{_fpe}':text='{_esc(_disp)}':"
                     f"fontcolor=0x{_chex}:fontsize={_sz}:x={x_n}:y={y_e}:enable='{en}'{alpha_opt}"),
                ]

            keyframes = tc.get("vid_keyframes")
            smooth    = tc.get("vid_smooth", False)
            easing    = tc.get("vid_easing", "ease_out")

            if keyframes and len(keyframes) >= 2:
                for i in range(len(keyframes) - 1):
                    kf = keyframes[i]; kf_e = keyframes[i + 1]
                    t0, t1 = kf["t"], kf_e["t"]
                    ky0 = kf.get("y", tc.get("pos", (0, 509))[1])
                    ky1 = kf_e.get("y", ky0)
                    xo0 = kf.get("x_offset", 0);  xo1 = kf_e.get("x_offset", xo0)
                    xt0 = global_x_off + xo0;      xt1 = global_x_off + xo1
                    en  = f"between(t,{t0},{t1})"

                    if smooth and (ky0 != ky1 or xt0 != xt1):
                        # ── Плавная интерполяция y и x через FFmpeg-выражения ──────
                        yi = _interp_expr(ky0, ky1, t0, t1, easing)  # y числа
                        xi = _interp_expr(xt0, xt1, t0, t1, easing)  # горизонт. сдвиг

                        y_e = f"({yi})-text_h" if y_bottom else yi

                        # y_p: Bs по вертикали (y_bs > vid_prefix_y_offset > y числа)
                        y_bs_kf = kf.get("y_bs")
                        if y_bs_kf is not None:
                            y_bs_e1  = kf_e.get("y_bs", y_bs_kf)
                            ybi = _interp_expr(y_bs_kf, y_bs_e1, t0, t1, easing)
                            y_p = f"({ybi})-text_h" if y_bottom else ybi
                        elif prefix_y_off:
                            y_p = f"({yi}{prefix_y_off:+d})-text_h" if y_bottom else f"({yi}{prefix_y_off:+d})"
                        else:
                            y_p = y_e

                        # x_p и x_n с интерполированным сдвигом
                        x_p = f"(w-{tw_t})/2+({xi})"
                        x_n = f"(w-{tw_t})/2+{tw_p}+{gap}+({xi})"

                        font_path_e = FONTS.get(tc.get("font", "montserrat"), FONTS["montserrat"]).replace("\\", "/").replace(":", "\\:")
                        drawtexts.append(
                            f"drawtext=fontfile='{font_path_e}':text='{_esc(prefix_text)}':"
                            f"fontcolor=0x{prefix_hex}:fontsize={prefix_size}:x={x_p}:y={y_p}:enable='{en}'{alpha_opt}"
                        )
                        drawtexts.append(
                            f"drawtext=fontfile='{font_path_e}':text='{_esc(display)}':"
                            f"fontcolor=0x{color_hex}:fontsize={size}:x={x_n}:y={y_e}:enable='{en}'{alpha_opt}"
                        )
                    else:
                        # ── Статичная позиция (через _make_pair) ─────────────────────
                        for dt in _make_pair(t0, t1, ky0, xo0, kf.get("y_bs")):
                            drawtexts.append(dt)
            else:
                # Одна позиция на весь отрезок (start_time / end_time / pos)
                pos = tc.get("pos", (0, 509))
                for dt in _make_pair(start_time, end_time, pos[1]):
                    drawtexts.append(dt)
            continue


        # ── Обычный режим ───────────────────────────────────────────────────────
        text = _esc(display_value)

        font_alias = tc.get("font", "montserrat")
        font_path = FONTS.get(font_alias, FONTS["montserrat"])
        font_path_esc = font_path.replace('\\', '/').replace(':', '\\:')

        size = tc.get("size", 40)
        color = tc.get("color", (255, 255, 255))
        if isinstance(color, tuple):
            color_hex = _rgb_to_hex(color)
        else:
            color_hex = str(color).replace("#", "")

        pos = tc.get("pos", (50, 50))
        x, y = pos
        start_time = tc.get("start_time", 0)
        end_time   = tc.get("end_time", 30)

        align = tc.get("align", "left")
        vid_x_right = tc.get("vid_x_right")
        if align == "center":
            x_expr = "(w-text_w)/2"
        elif align == "right":
            # Backward compatibility:
            # - if vid_x_right is set, treat it as absolute right edge x
            # - otherwise keep old behavior where pos.x is right margin from screen edge
            if vid_x_right is not None:
                x_expr = f"{vid_x_right}-text_w"
            else:
                x_expr = f"w-text_w-{x}"
        else:
            x_expr = str(x)

        # y_bottom=True → y задаёт нижний край текста
        if tc.get("y_bottom", False):
            y_expr = f"{y}-text_h"
        else:
            y_expr = str(y)

        # area-режим для видео: переносы + ограничение внутри прямоугольника
        area = tc.get("area")
        manual_multiline = bool(tc.get("manual_multiline", False))
        if manual_multiline and "\n" in str(display_value):
            lines = str(display_value).split("\n")
            line_step_px = int(tc.get("line_step_px", 0) or 0)
            if line_step_px <= 0:
                f_tmp = _load_font(font_alias, size)
                line_step_px = _line_h(f_tmp, tc.get("line_spacing", 1.2))

            for idx, ln in enumerate(lines):
                y_line = int(y + idx * line_step_px)

                if align == "right":
                    if vid_x_right is not None:
                        x_line = f"{vid_x_right}-text_w"
                    else:
                        x_line = f"w-text_w-{x}"
                elif align == "center":
                    x_line = "(w-text_w)/2"
                else:
                    x_line = str(int(x))

                if tc.get("y_bottom", False):
                    y_line_expr = f"{y_line}-text_h"
                else:
                    y_line_expr = str(y_line)

                if ln:
                    drawtexts.append(
                        f"drawtext=fontfile='{font_path_esc}':text='{_esc(ln)}':"
                        f"fontcolor=0x{color_hex}:fontsize={size}:x={x_line}:y={y_line_expr}:"
                        f"enable='between(t,{start_time},{end_time})'"
                    )
            continue

        if area:
            x1, y1, x2, y2 = area
            max_w = max(1, x2 - x1)
            spacing = tc.get("line_spacing", 1.2)
            f_wrap = _load_font(font_alias, size)
            first_char_delta = int(tc.get("first_char_size_delta", 0) or 0)
            f_first = _load_font(font_alias, size + first_char_delta) if first_char_delta > 0 else None
            line_gap_px = tc.get("line_gap_px")
            if line_gap_px is not None:
                bb = f_wrap.getbbox("Hg")
                font_h = bb[3] - bb[1]
                line_h = int(font_h + int(line_gap_px))
            else:
                line_h = _line_h(f_wrap, spacing)

            wrapped_lines: list[str] = []
            no_wrap = bool(tc.get("no_wrap", False))
            for para in str(display_value).split("\n"):
                if para == "":
                    wrapped_lines.append("")
                elif no_wrap:
                    # Используем только явные переносы из шаблона без автопереноса.
                    wrapped_lines.append(para)
                else:
                    wrapped_lines.extend(_wrap(para, f_wrap, max_w))

            y_cur = float(y1)
            for idx, ln in enumerate(wrapped_lines):
                if y_cur + line_h > y2 + 0.5:
                    break

                if align == "right":
                    lw = f_wrap.getlength(ln) if ln else 0
                    x_line = float(x2) - float(lw)
                elif align == "center":
                    lw = f_wrap.getlength(ln) if ln else 0
                    x_line = float(x1) + (float(max_w) - float(lw)) / 2.0
                else:
                    x_line = float(x1)

                if ln:
                    # Опционально увеличиваем первую букву самой первой строки.
                    if idx == 0 and first_char_delta > 0 and f_first and len(ln) > 0:
                        first_ch = ln[0]
                        rest = ln[1:]
                        drawtexts.append(
                            f"drawtext=fontfile='{font_path_esc}':text='{_esc(first_ch)}':"
                            f"fontcolor=0x{color_hex}:fontsize={size + first_char_delta}:x={x_line}:y={y_cur}:"
                            f"enable='between(t,{start_time},{end_time})'"
                        )
                        if rest:
                            first_w = f_first.getlength(first_ch)
                            drawtexts.append(
                                f"drawtext=fontfile='{font_path_esc}':text='{_esc(rest)}':"
                                f"fontcolor=0x{color_hex}:fontsize={size}:x={x_line + first_w}:y={y_cur}:"
                                f"enable='between(t,{start_time},{end_time})'"
                            )
                    else:
                        drawtexts.append(
                            f"drawtext=fontfile='{font_path_esc}':text='{_esc(ln)}':"
                            f"fontcolor=0x{color_hex}:fontsize={size}:x={x_line}:y={y_cur}:"
                            f"enable='between(t,{start_time},{end_time})'"
                        )
                y_cur += line_h
            continue

        # ── Покадровая анимация в обычном режиме (vid_keyframes) ──────────────
        # Параметры кадра: t, x, y
        # vid_smooth=True  → плавная интерполяция между кадрами через FFmpeg-выражения
        # vid_easing       → 'linear' | 'ease_in' | 'ease_out' | 'ease_in_out'
        kfs = tc.get("vid_keyframes")
        text_lines = str(display_value).split("\n")
        has_multiline_pos = ("\n" in str(display_value)) and not area and not kfs
        if has_multiline_pos:
            line_spacing_px = int(tc.get("line_spacing_px", 0) or 0)
            first_char_delta = int(tc.get("first_char_size_delta", 0) or 0)
            
            # Если line_spacing_px не задан, но задан line_spacing — вычисляем его
            if not line_spacing_px and "line_spacing" in tc:
                f_tmp = _load_font(font_alias, size)
                bb = f_tmp.getbbox("Hg")
                font_h = bb[3] - bb[1]
                line_h = int(font_h * tc["line_spacing"])
                line_spacing_px = max(0, line_h - font_h)
            
            ls_opt = f":line_spacing={line_spacing_px}" if line_spacing_px else ""

            # Один drawtext для всего многострочного блока:
            # FFmpeg сам задает одинаковый интервал между всеми строками.
            full_text = str(display_value)
            drawtexts.append(
                f"drawtext=fontfile='{font_path_esc}':text='{_esc(full_text)}':"
                f"fontcolor=0x{color_hex}:fontsize={size}:x={int(x)}:y={int(y)}:"
                f"enable='between(t,{start_time},{end_time})'{ls_opt}"
            )

            # Опционально увеличиваем первую букву поверх базового текста,
            # не влияя на межстрочный интервал блока.
            if first_char_delta > 0 and text_lines and text_lines[0]:
                first_ch = text_lines[0][0]
                drawtexts.append(
                    f"drawtext=fontfile='{font_path_esc}':text='{_esc(first_ch)}':"
                    f"fontcolor=0x{color_hex}:fontsize={size + first_char_delta}:x={int(x)}:y={int(y)}:"
                    f"enable='between(t,{start_time},{end_time})'"
                )
            continue

        if kfs and len(kfs) >= 2:
            y_bot   = tc.get("y_bottom", False)
            smooth  = tc.get("vid_smooth", False)
            easing  = tc.get("vid_easing", "ease_out")
            use_center_offset = tc.get("_x_center_offset", False)
            for i in range(len(kfs) - 1):
                kf = kfs[i]; kf_e = kfs[i + 1]
                kx0, ky0 = kf.get("x", x),   kf.get("y", y)
                kx1, ky1 = kf_e.get("x", x), kf_e.get("y", y)
                xo0 = kf.get("x_offset", 0)
                xo1 = kf_e.get("x_offset", 0)
                t0, t1   = kf["t"], kf_e["t"]
                en = f"between(t,{t0},{t1})"
                current_easing = kf.get("easing", easing)

                if align == "right":
                    xr0 = kf.get("x_right", tc.get("vid_x_right", kx0))
                    xr1 = kf_e.get("x_right", tc.get("vid_x_right", kx1))

                    if smooth and (xr0 != xr1 or ky0 != ky1):
                        xi = _interp_expr(int(xr0), int(xr1), t0, t1, current_easing)
                        yi = _interp_expr(int(ky0), int(ky1), t0, t1, current_easing)
                        kx_expr = f"({xi})-text_w"
                        ky_expr = f"{yi}-text_h" if y_bot else yi
                    else:
                        kx_expr = f"{xr0}-text_w"
                        ky_expr = f"{ky0}-text_h" if y_bot else str(ky0)
                elif use_center_offset:
                    # Центровка через (w-text_w)/2 + x_offset для плавной анимации
                    if smooth and (xo0 != xo1 or ky0 != ky1):
                        oi = _interp_expr(int(xo0), int(xo1), t0, t1, current_easing)
                        yi = _interp_expr(int(ky0), int(ky1), t0, t1, current_easing)
                        kx_expr = f"(w-text_w)/2+({oi})"
                        ky_expr = f"{yi}-text_h" if y_bot else yi
                    else:
                        kx_expr = f"(w-text_w)/2+{int(xo0)}"
                        ky_expr = f"{ky0}-text_h" if y_bot else str(ky0)
                elif smooth and (kx0 != kx1 or ky0 != ky1):
                    # Плавная интерполяция через FFmpeg математику
                    xi = _interp_expr(kx0, kx1, t0, t1, current_easing)
                    yi = _interp_expr(ky0, ky1, t0, t1, current_easing)
                    kx_expr = xi
                    ky_expr = f"{yi}-text_h" if y_bot else yi
                else:
                    # Статичная позиция
                    kx_expr = str(kx0)
                    ky_expr = f"{ky0}-text_h" if y_bot else str(ky0)

                drawtexts.append(
                    f"drawtext=fontfile='{font_path_esc}':text='{text}':"
                    f"fontcolor=0x{color_hex}:fontsize={size}:x={kx_expr}:y={ky_expr}:"
                    f"enable='{en}'"
                )
        else:
            dt = (f"drawtext=fontfile='{font_path_esc}':text='{text}':"
                  f"fontcolor=0x{color_hex}:fontsize={size}:x={x_expr}:y={y_expr}:"
                  f"enable='between(t,{start_time},{end_time})'")
            drawtexts.append(dt)

    if not drawtexts and not overlay_images:
        subprocess.run([ffmpeg_path, "-y", "-i", asset_path, "-c", "copy", out_path],
                       check=True, cwd=BASE_DIR)
    else:
        cmd = [ffmpeg_path, "-y", "-i", asset_path]
        for ov in overlay_images:
            cmd.extend(["-i", ov["path"]])
            
        if overlay_images:
            filters = []
            last_out = "0:v"
            for i, ov in enumerate(overlay_images):
                enable_expr = f"between(t,{ov['start_time']},{ov['end_time']})"
                current_out = f"ov{i}"
                tc = ov.get("tc", {})
                kfs = tc.get("vid_keyframes")
                
                if kfs and len(kfs) >= 2:
                    smooth = tc.get("vid_smooth", False)
                    easing = tc.get("vid_easing", "ease_out")
                    x_expr = _build_chained_expr(kfs, smooth, easing, "x", ov["x"])
                    y_expr = _build_chained_expr(kfs, smooth, easing, "y", ov["y"])
                    # overlay filter expressions shouldn't have escaped commas if we wrap them in quotes properly, but FFmpeg syntax can be tricky.
                    # Since we use variables, it's safest to use single quotes if possible, or unescaped commas inside evaluated parts.
                    # We escaped commas as \, in _build_chained_expr so it should be fine inside unquoted overlay string.
                else:
                    x_expr = str(ov["x"])
                    y_expr = str(ov["y"])

                filters.append(f"[{last_out}][{i+1}:v]overlay=x='{x_expr}':y='{y_expr}':enable='{enable_expr}':eval=frame[{current_out}]")
                last_out = current_out
            
            if drawtexts:
                dt_str = ",".join(drawtexts) + ",gblur=sigma=1.2"
                filters.append(f"[{last_out}]{dt_str}[vout]")
                last_out = "vout"
                
            cmd.extend(["-filter_complex", ";".join(filters), "-map", f"[{last_out}]", "-map", "0:a?"])
        else:
            vf = ",".join(drawtexts) + ",gblur=sigma=1.2"
            cmd.extend(["-vf", vf])

        cmd.extend([
            "-c:v", "mpeg4",          # Универсальный кодек (работает везде)
            "-q:v", "5",              # Качество (1-31, меньше = лучше)
            "-c:a", "copy",
            out_path
        ])
        
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE, cwd=BASE_DIR)
        if result.returncode != 0:
            ffmpeg_err = result.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"FFmpeg вернул код {result.returncode}.\n{ffmpeg_err}")

    with open(out_path, "rb") as f:
        out_bytes = io.BytesIO(f.read())

    try:
        os.remove(out_path)
    except Exception:
        pass
        
    for ov in overlay_images:
        try:
            os.remove(ov["path"])
        except Exception:
            pass

    out_bytes.seek(0)
    return out_bytes
