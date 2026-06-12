"""
Центральный конфиг каталога.

text_config поля:
  font          : алиас из FONTS
  size          : размер в пунктах Photoshop (72dpi → 1pt = 1px)
  color         : (R, G, B)
  area          : (x1, y1, x2, y2) — текстовая область с автопереносом
  pos           : (x, y)           — фиксированная точка
  align         : "left" | "right" | "center"
  template      : строка с {key}-подстановкой
  format_number : True → форматировать как число (30000 → 30 000)
  suffix        : строка-суффикс (напр. "BOB")
  suffix_size   : pt размер суффикса
  segments      : список {text,font,size,color} — смешанные шрифты/цвета в одном блоке
  line_spacing  : множитель межстрочного интервала (default 1.2)
"""

# ── Алиасы шрифтов ───────────────────────────────────────────────────────────
FONTS: dict[str, str] = {
    "montserrat":        "assets/fonts/Montserrat-Regular.ttf",
    "montserrat_medium": "assets/fonts/Montserrat-Medium.ttf",
    "montserrat_bold":   "assets/fonts/Montserrat-Bold.ttf",
    "montserrat_light":  "assets/fonts/Montserrat-Light.otf",
    "montserrat_alt_med":"assets/fonts/MontserratAlternates-Medium.otf",
    "sfui_bold":         "assets/fonts/sfuidisplay_bold.ttf",
    "sfui_medium":       "assets/fonts/sfuidisplay_medium.ttf",
    "arial":         "assets/fonts/Arial-Regular.ttf",
    "arial_bold":    "assets/fonts/Arial-Bold.ttf",
    "new_world":     "assets/fonts/NewWorldVibes-Regular.ttf",
    "opensans_bold": "assets/fonts/OpenSans-Bold.ttf",
    "opensans_semi": "assets/fonts/OpenSans-Semibold.ttf",
    "opensans":      "assets/fonts/OpenSans-Regular.ttf",
    "sf_pro":        "assets/fonts/SFProText-Regular.ttf",
    "sf_pro_medium": "assets/fonts/SF-Pro-Text-Medium.ttf",
    "sf_pro_semibold": "assets/fonts/SF-Pro-Text-Semibold.otf",
    "sf_pro_bold": "assets/fonts/sfuidisplay_bold.ttf",
    "sf_pro_light":  "assets/fonts/SF-Pro-Text-Light.ttf",
    "myriad":        "assets/fonts/MyriadPro-Regular.ttf",
    "myriad_arabic": "assets/fonts/MyriadArabic-Italic.ttf",
    "myriad_arabic_bold": "assets/fonts/MyriadArabic-Bold.ttf",
    "times_bold":    "assets/fonts/Times-Bold.ttf",
    "times_roman":   "assets/fonts/Times-Roman-Regular.ttf",
    "araboto":       "assets/fonts/araboto-normal.ttf",
    "araboto_medium":"assets/fonts/araboto-medium.ttf",
    "araboto_bold":  "assets/fonts/araboto-bold.ttf",
    "flexo":         "assets/fonts/Flexo-Light.ttf",
    "flexo_medium":  "assets/fonts/Flexo-Medium.ttf",
    "flexo_demibold":"assets/fonts/Flexo-DemiBold.ttf",
    "flexo_bold":    "assets/fonts/Flexo-Bold.ttf",
    "geometria_bold": "assets/fonts/geometria_bold.otf",
    "geometria_medium": "assets/fonts/geometria_medium.otf",
    "roboto_cond_med": "assets/fonts/RobotoCondensed-Medium.ttf",
    "roboto_cond_reg": "assets/fonts/RobotoCondensed-Regular.ttf",
    "roboto_cond_extrabold": "assets/fonts/RobotoCondensed-ExtraBold.ttf",
    "roboto_cond_semibold": "assets/fonts/RobotoCondensed-SemiBold.ttf",
    "nunito_sans_italic":  "assets/fonts/NunitoSans-Italic-VariableFont_YTLC,opsz,wdth,wght.ttf",
    "nunito_medium":       "assets/fonts/Nunito-Medium.otf",
    "nunito_bold":         "assets/fonts/Nunito-Medium.otf",
    "quicksand":           "assets/fonts/Quicksand-VariableFont_wght.ttf",
    "quicksand_regular":   "assets/fonts/Quicksand-Regular.ttf",
    "quicksand_semibold":  "assets/fonts/Quicksand-SemiBold.otf",
    "alte_regular":        "assets/fonts/AlteHaasGroteskRegular.ttf",
    "alte_bold":           "assets/fonts/AlteHaasGroteskBold.ttf",
    "arial_italic":        "assets/fonts/Arial-Italic.ttf",
    "inter":               "assets/fonts/Inter-Regular.ttf",
    "inter_semibold":      "assets/fonts/Inter-SemiBold.ttf",
    "montserrat_extrabold": "assets/fonts/Montserrat-ExtraBold.ttf",
    "montserrat_semibold": "assets/fonts/Montserrat-SemiBold.ttf",
    "montserrat_extralight": "assets/fonts/Montserrat-ExtraLight.ttf",
    "sf_pro_text_medium": "assets/fonts/SF-Pro-Text-Medium.ttf",
    "sf_pro_text_regular": "assets/fonts/SFProText-Regular.ttf",
    "sf_pro_text_bold":    "assets/fonts/SFProText-Bold.otf",
    "inter_light":         "assets/fonts/Inter-Light.ttf",
    "inter_extralight":    "assets/fonts/Inter-ExtraLight.ttf",
}


# ── Каталог шаблонов ─────────────────────────────────────────────────────────
# GEO_LABELS определяют доступные геолокации для разделения шаблонов.
GEO_LABELS: dict[str, str] = {
    "bo": "🇧🇴 Bolivia",
    "pe": "🇵🇪 Peru",
    "uy": "🇺🇾 Uruguay",
    "py": "🇵🇾 Paraguay",
    "ma": "🇲🇦 Morocco",
}

# Каталог: верхний уровень — геолокация, затем категории.
# Каждый регион имеет свой набор шаблонов и свои asset-пути.
from data.templates import GEO_CATALOG
