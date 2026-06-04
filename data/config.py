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
GEO_CATALOG: dict = {

    # ════════════════════════════════════════════════════════
    # Bolivia 🇧🇴 — шаблоны, относящиеся к Bolivia
    # В этой секции используются пути типа assets/fd/... и assets/rd/...
    # ════════════════════════════════════════════════════════
    "bo": {
        "label": "🇧🇴 Bolivia",
        "catalog":     {

        # ════════════════════════════════════════════════════════
        # FD
        # ════════════════════════════════════════════════════════
        "fd": {
            "label": "📁 Bolivia FD",
            "sections": {
                "proofs_fd": {
                    "label": "Bolivia Proofs FD",
                    "items": {
                        "fd_proof1": {
                            "label": "Bolivia FD 1", "asset": "assets/Bolivia/FD/proofs/psd1.png",
                            "fields": [
                                {"key": "name",   "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan)",
                                 "text_config": {"font": "montserrat", "size": 36, "color": (0,0,0), "pos": (100, 200)}},
                                {"key": "amount", "prompt": "💰 Введите сумму",
                                 "text_config": {"font": "montserrat", "size": 36, "color": (0,0,0), "pos": (100, 260)}},
                            ],
                        },
                        "fd_proof2": {
                            "label": "Bolivia FD 2", "asset": "assets/Bolivia/FD/proofs/psd2.png",
                            "fields": [
                                {"key": "name",   "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan)",
                                 "text_config": {"font": "montserrat", "size": 36, "color": (0,0,0), "pos": (100, 200)}},
                                {"key": "amount", "prompt": "💰 Введите сумму",
                                 "text_config": {"font": "montserrat", "size": 36, "color": (0,0,0), "pos": (100, 260)}},
                            ],
                        },
                        "fd_proof3": {
                            "label": "Bolivia FD 3", "asset": "assets/Bolivia/FD/proofs/psd3.png",
                            "fields": [
                                {"key": "name",   "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan)",
                                 "text_config": {"font": "montserrat", "size": 36, "color": (0,0,0), "pos": (100, 200)}},
                                {"key": "amount", "prompt": "💰 Введите сумму",
                                 "text_config": {"font": "montserrat", "size": 36, "color": (0,0,0), "pos": (100, 260)}},
                            ],
                        },
                    },
                },
            },
        },
        "rd": {
            "label": "📁 Bolivia RD",
            "sections": {

                "rd_main": {
                    "label": "Bolivia RD",
                    "items": {

                        # ── RD1 ──────────────────────────────────────────────────
                        "rd1": {
                            "label": "Bolivia RD 1", "asset": "assets/Bolivia/RD/rd1.jpg", "preview": "assets/Bolivia/Preview/RD/RD1_prew.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": "✏️ Введите Фамилия Имя (пример: Ivanov Ivan)",
                                    "text_config": {
                                        "area": (1250, 700, 2780, 925),
                                        "line_spacing": 1.25,
                                        "segments": [
                                            {"text": "Su pago al cliente ",
                                             "font": "montserrat", "size": 45, "color": (255, 255, 255)},
                                            {"text": "{name}",
                                             "font": "montserrat", "size": 45, "color": (255, 255, 255)},
                                            {"text": " por un monto de ",
                                             "font": "montserrat", "size": 45, "color": (255, 255, 255)},
                                            {"text": "Bs. 35,511.00",
                                             "font": "montserrat", "size": 45, "color": (0, 255, 84)},
                                            {"text": " ha sido bloqueado temporalmente. Para retirar los fondos de la plataforma a la cuenta del beneficiario, su cliente está obligado a pagar una tarifa de ",
                                             "font": "montserrat", "size": 45, "color": (255, 255, 255)},
                                            {"text": "Bs. {commission}.00.",
                                             "font": "montserrat", "size": 45, "color": (255, 0, 0), "format_number_comma": True},
                                        ],
                                    },
                                },
                                {
                                    "key": "commission",
                                    "prompt": "💰 Введите сумму (рекомендуется 1590, 890)",
                                    "text_config": {"collect_only": True}
                                },
                            ],
                        },

                        # ── RD2 ──────────────────────────────────────────────────
                        "rd2": {
                            "label": "Bolivia RD 2", "asset": "assets/Bolivia/RD/rd2.jpg", "preview": "assets/Bolivia/Preview/RD/RD2_prew.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": "✏️ Введите Фамилия Имя (пример: Ivanov Ivan)",
                                    "text_config": {
                                        "font": "montserrat", "size": 30,
                                        "color": (57, 62, 67),
                                        "template": "Cuenta bancaria del cliente {name}.",
                                        "area": (2235, 1420, 3050, 1460),
                                        "line_spacing": 1.2,
                                    }
                                },
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите сумму",
                                    "text_config": {"collect_only": True}
                                },
                                {
                                    "key": "_body_line1",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (2240, 490, 2992, 540),
                                        "segments": [
                                            {"text": "Es necesario pagar una tarifa por la", "font": "montserrat_light", "size": 44, "color": (255, 255, 255)}
                                        ]
                                    }
                                },
                                {
                                    "key": "_body_line2",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (2240, 537, 2992, 587),
                                        "segments": [
                                            {"text": "conversión de ", "font": "montserrat_light", "size": 44, "color": (255, 255, 255)},
                                            {"text": "USDT", "font": "montserrat_medium", "size": 44, "color": (136, 255, 164)},
                                            {"text": " a ", "font": "montserrat_light", "size": 44, "color": (255, 255, 255)},
                                            {"text": "BOB.", "font": "montserrat_medium", "size": 44, "color": (254, 68, 92)}
                                        ]
                                    }
                                },
                                {
                                    "key": "_body_line3",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (2240, 615, 2992, 665),
                                        "segments": [
                                            {"text": "Importe de la tarifa: ", "font": "montserrat_light", "size": 44, "color": (255, 255, 255)},
                                            {"text": "Bs. {amount}", "font": "montserrat_medium", "size": 44, "color": (255, 13, 13), "format_number_comma": True},
                                            {"text": ".", "font": "montserrat_light", "size": 44, "color": (255, 255, 255)}
                                        ]
                                    }
                                }
                            ],
                        },

                        # ── RD3 ──────────────────────────────────────────────────
                        "rd3": {
                            "label": "Bolivia RD 3",
                            "asset": "assets/Bolivia/RD/rd3.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": "✏️ Введите ФИО (пример: Nilda Mamani Apaza)",
                                    "text_config": {
                                        "font": "times_bold",
                                        "size": 59,
                                        "color": (0, 0, 0),
                                        "pos": (68, 474),
                                        "template": "Notificación para {name}"
                                    }
                                },
                                {
                                    "key": "gender",
                                    "prompt": "👤 Выберите пол (введите 'o' для мужского, 'a' для женского):",
                                    "text_config": {"collect_only": True}
                                },
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите сумму (рекомендуется 2 343)",
                                    "text_config": {"collect_only": True}
                                },
                                {
                                    "key": "_greeting",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (69, 1230, 2412, 1350),
                                        "segments": [
                                            {"text": "Estimad{gender} ", "font": "times_roman", "size": 59, "color": (0, 0, 0)},
                                            {"text": "{name}:", "font": "times_bold", "size": 59, "color": (0, 0, 0)}
                                        ]
                                    }
                                },
                                {
                                    "key": "_body",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (70, 1663, 2414, 2200),
                                        "line_spacing": 0.76,
                                        "segments": [
                                            {"text": "Le informamos acerca de una condición importante relacionada con la retirada de fondos a\nla cuenta bancaria que usted indicó. El pago estará disponible únicamente después de\nrealizar el abono por servicios por un importe de ", 
                                             "font": "times_roman", "size": 60, "color": (0, 0, 0)},
                                            {"text": "Bs. {amount}", 
                                             "font": "times_bold", "size": 60, "color": (0, 0, 0), "format_number": True},
                                            {"text": ". Le rogamos efectuar dicho\npago a la mayor brevedad; tras su confirmación y el procesamiento por parte de nuestros\ndepartamentos, recibirá inmediatamente en su cuenta bancaria la suma total de ", 
                                             "font": "times_roman", "size": 60, "color": (0, 0, 0)},
                                            {"text": "Bs. 35 511", 
                                             "font": "times_bold", "size": 60, "color": (0, 0, 0)},
                                            {"text": ".", 
                                             "font": "times_roman", "size": 60, "color": (0, 0, 0)}
                                        ]
                                    }
                                }
                            ]
                        },

                        # ── RD4 ──────────────────────────────────────────────────
                        "rd4": {
                            "label": "Bolivia RD 4", "asset": "assets/Bolivia/RD/rd4.jpg", "preview": "assets/Bolivia/Preview/RD/RD4_prew.jpg",
                            "fields": [
                                {
                                    "key": "time",
                                    "prompt": "🕐 Введите время (пример: 10:00) (24-часовой формат)",
                                    "text_config": {
                                        "font": "sf_pro_bold", "size": 34,
                                        "color": (82, 82, 82),
                                        "area": (115, 39, 243, 60),
                                    },
                                },
                                {
                                    "key": "name",
                                    "prompt": "✏️ Введите Фамилия Имя",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите сумму (рекомендуется 2 258)",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_body",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (84, 758, 743, 1022),
                                        "line_spacing": 1.2,
                                        "blank_line_size": 14,
                                        "segments": [
                                            {"text": "Para una ejecución exitosa y segura del pago a su cliente ",
                                             "font": "sf_pro", "size": 30, "color": (255, 255, 255)},
                                            {"text": "{name}",
                                             "font": "sf_pro", "size": 30, "color": (255, 255, 255)},
                                            {"text": ", es necesario que abone el proceso de segregación por un monto de ",
                                             "font": "sf_pro", "size": 30, "color": (255, 255, 255)},
                                            {"text": "Bs. {amount}.",
                                             "font": "sf_pro", "size": 30, "color": (255, 0, 0), "format_number_dot": True},
                                            {"text": "\n\n",
                                             "font": "sf_pro", "size": 30, "color": (255, 255, 255)},
                                            {"text": "Una vez abonada la segregación, todo el dinero se acreditará automáticamente en la cuenta de su cliente.",
                                             "font": "sf_pro", "size": 30, "color": (255, 255, 255)},
                                        ],
                                    },
                                },
                            ],
                        },

                        # ── RD5 ──────────────────────────────────────────────────
                        "rd5": {
                            "label": "Bolivia RD 5", "asset": "assets/Bolivia/RD/rd5.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": "✏️ Введите ФИО (пример: Nilda Mamani Apaza)",
                                    "text_config": {
                                        "font": "times_bold",
                                        "size": 59,
                                        "color": (0, 0, 0),
                                        "pos": (68, 474),
                                        "template": "Notificación para {name}"
                                    }
                                },
                                {
                                    "key": "gender",
                                    "prompt": "👤 Выберите пол (введите 'o' для мужского, 'a' для женского):",
                                    "text_config": {"collect_only": True}
                                },
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите сумму (рекомендуется 2 100)",
                                    "text_config": {"collect_only": True}
                                },
                                {
                                    "key": "_greeting",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (69, 1230, 2412, 1350),
                                        "segments": [
                                            {"text": "Estimad{gender} ", "font": "times_roman", "size": 59, "color": (0, 0, 0)},
                                            {"text": "{name}:", "font": "times_bold", "size": 59, "color": (0, 0, 0)}
                                        ]
                                    }
                                },
                                {
                                    "key": "_body",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (70, 1747, 2414, 2200),
                                        "line_spacing": 1.45,
                                        "segments": [
                                            {"text": "En el sistema figura un pago pendiente por concepto de prima de seguro por ", 
                                             "font": "times_roman", "size": 60, "color": (0, 0, 0)},
                                            {"text": "Bs. {amount}", 
                                             "font": "times_bold", "size": 60, "color": (0, 0, 0), "format_number": True},
                                            {"text": ", necesario para activar las garantías y el acceso completo a las funciones de protección. Le rogamos efectuar dicho pago a través de los métodos de recarga disponibles. Tras la confirmación del pago, se restaurará el acceso a los retiros y podrá iniciar la transferencia del monto total de ", 
                                             "font": "times_roman", "size": 60, "color": (0, 0, 0)},
                                            {"text": "Bs. 35 511", 
                                             "font": "times_bold", "size": 60, "color": (0, 0, 0)},
                                            {"text": " a la cuenta bancaria indicada.", 
                                             "font": "times_roman", "size": 60, "color": (0, 0, 0)}
                                        ]
                                    }
                                }
                            ]
                        },

                        # ── RD6 ──────────────────────────────────────────────────
                        "rd6": {
                            "label": "Bolivia RD 6", "asset": "assets/Bolivia/RD/rd6.jpg", "preview": "assets/Bolivia/Preview/RD/RD6_prew.jpg",
                            "fields": [
                                {
                                    "key": "date",
                                    "prompt": "📅 Дата 1 (пример: Fr 01/01)",
                                    "text_config": {
                                        "font": "opensans", "size": 14,
                                        "color": (44, 44, 44),
                                        "area": (540, 210, 613, 222),
                                    },
                                },
                                {
                                    "key": "date2",
                                    "prompt": "📅 Дата 2 (пример: Fr 01/01/2026)",
                                    "text_config": {
                                        "font": "opensans", "size": 14,
                                        "color": (147, 147, 147),
                                        "area": (1730, 236, 1845, 247),
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": "🏦 Название банка (пример: Yane)",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "tx_time",
                                    "prompt": "🕐 Время транзакции (пример: 10:00)",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "name",
                                    "prompt": "✏️ Введите ФИО клиента (пример: Ivan Ivanov Ivanovich)",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "commission",
                                    "prompt": "💰 Введите сумму налога (рекомендуется 1.920)",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_body",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (655, 457, 1620, 795),
                                        "line_spacing": 1.15,
                                        "blank_line_size": 10,
                                        "segments": [
                                            {"text": "Estimado José García!",
                                             "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                            {"text": "\n\n",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "Ha realizado un intercambio de USDT por un monto de ",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "Bs. 35.511",
                                             "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                            {"text": " para el pago a su cliente.",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "\n\n",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "Detalles de la transacción:",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "\n",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "  ID de la transacción: ",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "9489-4921-3991-002",
                                             "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                            {"text": "\n",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "  Banco del destinatario: ",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "{bank}",
                                             "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                            {"text": "\n",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "  Monto a recibir: ",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "Bs. 35.511",
                                             "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                            {"text": "\n",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "  Monto en USDT: ",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "3.855",
                                             "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                            {"text": "\n",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "  Hora de la transacción: ",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "{tx_time}",
                                             "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                            {"text": "\n\n",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "Su cliente, ",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "{name}",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": ", está obligado a pagar el 7% de impuesto sobre el intercambio de criptomonedas, es decir, ",
                                             "font": "arial", "size": 20, "color": (44, 44, 44)},
                                            {"text": "Bs. {commission}.",
                                             "font": "arial_bold", "size": 20, "color": (44, 44, 44), "format_number_dot": True},
                                        ],
                                    },
                                },
                            ],
                        },

                        # ── RD7 ──────────────────────────────────────────────────
                        "rd7": {
                            "label": "Bolivia RD 7", "asset": "assets/Bolivia/RD/rd7.jpg", "preview": "assets/Bolivia/Preview/RD/RD7_prew.jpg",
                            "fields": [
                                {
                                    "key": "time",
                                    "prompt": "🕐 Введите время (пример: 10:00) (24-часовой формат)",
                                    "text_config": {
                                        "font": "sf_pro_bold", "size": 32,
                                        "color": (255, 255, 255),
                                        "area": (100, 33, 200, 67),
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": "🏦 Введите название банка (пример: YAPE)",
                                    "text_config": {
                                        "font": "sf_pro_medium", "size": 29,
                                        "color": (0, 0, 0),
                                        "area": (398, 850, 710, 880),
                                    },
                                },
                                {
                                    "key": "fullname",
                                    "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan Ivanovich)",
                                    "text_config": {
                                        "font": "sf_pro_medium", "size": 29,
                                        "color": (0, 0, 0),
                                        "area": (398, 913, 710, 944),
                                    },
                                },
                                {
                                    "key": "number",
                                    "prompt": "🔢 Введите номер счёта (пример: 1234567890)",
                                    "text_config": {
                                        "font": "sf_pro_medium", "size": 29,
                                        "color": (0, 0, 0),
                                        "area": (398, 994, 663, 1025),
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите сумму (рекомендуется 1 745)",
                                    "text_config": {
                                        "font": "sf_pro_medium", "size": 29,
                                        "color": (0, 0, 0),
                                        "area": (395, 1206, 710, 1242),
                                        "template": "Bs. {amount}.00",
                                        "format_number_comma": True,
                                    },
                                },
                            ],
                        },

                        # RD8 - Видеоролик
                        "rd8":  {
                            "label": "Bolivia RD 8 (Видео)", 
                            "asset": "assets/Bolivia/RD/rd8.mp4",
                            # "preview": "assets/Bolivia/Preview/RD/rd8_prew.mp4",
                            "render_mode": "video",
                            "fields": [
                                {
                                    "key": "overlay_image",
                                    "prompt": "🖼 Отправьте картинку для вставки на видео",
                                    "text_config": {
                                        "image_paste": True,
                                        # ── РАЗМЕР КАРТИНКИ (ширина, высота) ───────────────────────
                                        "size": (192, 195),
                                        # ── ВРЕМЯ ОТОБРАЖЕНИЯ НА ВИДЕО ─────────────────────────────
                                        "start_time": 17.033,
                                        "end_time":   19.600,
                                        # ── ПЛАВНАЯ АНИМАЦИЯ ПО КООРДИНАТАМ ────────────────────────
                                        "vid_smooth": True,
                                        "vid_easing": "linear",
                                        # ── ПОКАДРОВАЯ НАСТРОЙКА ДВИЖЕНИЯ ──────────────────────────
                                        "vid_keyframes": [
                                            # --- ПОДЪЕМ ---
                                            {"t": 17.033, "x": 8, "y": 1304, "easing": "linear"}, # 17:01
                                            {"t": 17.233, "x": 8, "y": 1088, "easing": "linear"}, # 17:07
                                            {"t": 17.266, "x": 8, "y": 1052, "easing": "linear"}, # 17:08
                                            {"t": 17.300, "x": 8, "y": 1020, "easing": "linear"}, # 17:09
                                            {"t": 17.333, "x": 8, "y": 988, "easing": "linear"},  # 17:10
                                            {"t": 17.366, "x": 8, "y": 958, "easing": "linear"},  # 17:11
                                            {"t": 17.400, "x": 8, "y": 930, "easing": "linear"},  # 17:12
                                            {"t": 17.433, "x": 8, "y": 906, "easing": "linear"},  # 17:13
                                            {"t": 17.466, "x": 8, "y": 884, "easing": "linear"},  # 17:14
                                            {"t": 17.500, "x": 8, "y": 866, "easing": "linear"},  # 17:15
                                            {"t": 17.566, "x": 8, "y": 844, "easing": "linear"},  # 17:17 (конец подъема)
                                            
                                            # --- ОЖИДАНИЕ ---
                                            {"t": 19.000, "x": 8, "y": 844, "easing": "linear"},  # 19:00 (начало опускания)
                                            
                                            # --- ОПУСКАНИЕ ---
                                            {"t": 19.033, "x": 8, "y": 848, "easing": "linear"},  # 19:01
                                            {"t": 19.100, "x": 8, "y": 873, "easing": "linear"},  # 19:03
                                            {"t": 19.166, "x": 8, "y": 913, "easing": "linear"},  # 19:05
                                            {"t": 19.266, "x": 8, "y": 997, "easing": "linear"},  # 19:08
                                            {"t": 19.333, "x": 8, "y": 1064, "easing": "linear"}, # 19:10
                                            {"t": 19.566, "x": 8, "y": 1323, "easing": "linear"}, # 19:17 (конец)
                                        ]
                                    },
                                },
                                {
                                    "key": "time", 
                                    "prompt": "🕐 Введите время (24-часовой формат)",
                                    "text_config": {
                                        "font": "sf_pro_medium",
                                        "size": 27,
                                        "color": (255, 255, 255),
                                        "pos": (29, 34),
                                        "start_time": 0,
                                        "end_time": 9999
                                    }
                                },
                                {
                                    "key": "amount", 
                                    "prompt": "💰 Введите сумму",
                                    "text_config": {
                                        # ── Шрифт и цвет числа ─────────────────────────────────────
                                        "font":  "sfui_medium",
                                        "size":  81,                      # pt размер числа
                                        "color": (105, 50, 118),          # цвет числа
                                        # ── Запасная позиция (когда vid_keyframes не задан) ────────
                                        "pos":     (0, 509),              # x игнорируется; y = нижний край
                                        "y_bottom": True,                 # y — нижний край текста
                                        "start_time": 24.10,              # сек.ms (начало)
                                        "end_time":   24.30,              # сек.ms (конец)
                                        # ── Настройки префикса "Bs" ────────────────────────────────
                                        "vid_prefix":        "Bs",           # текст перед числом
                                        "vid_prefix_color":  (205, 168, 212), # цвет префикса (R,G,B)
                                        "vid_prefix_size":   56,             # pt размер шрифта префикса
                                        "vid_prefix_gap":    4,             # px расстояние Bs ↔ число
                                        "vid_prefix_char_w": 0.52,           # коэф. ширины символа (центровка)
                                        "vid_prefix_y_offset": -40,          # px: Bs выше числа (отрицат. = выше)
                                        "vid_x_offset":  20,                 # px: сдвиг всей группы (+ = правее)
                                        # ── Формат числа ───────────────────────────────────────────
                                        "vid_format_dot":    True,           # 10000 → 10.000
                                        # ── Плавная анимация ───────────────────────────────────────
                                        "vid_smooth": True,
                                        "vid_easing": "ease_out",  # ease_out/ease_in/ease_in_out/linear
                                        # ── Плавное исчезновение в конце ───────────────────────────
                                        "vid_fade_out_start": 25.00,         # c этого времени alpha: 1 -> 0
                                        "vid_fade_out_end":   25.20,         # к этому времени alpha = 0
                                        # ── ПОКАДРОВАЯ НАСТРОЙКА ПОЛОЖЕНИЯ ────────────────────────
                                        # Если задан — start_time/end_time/pos выше игнорируются.
                                        # Каждый кадр задаёт позицию на интервале [t, следующий_t).
                                        #   t        — время начала (сек.ms)
                                        #   y        — нижний край ЧИСЛА (px)
                                        #   x_offset — сдвиг от центра (px; 0 = строго по центру)
                                        #   y_bs     — нижний край BS (px); если не задан →
                                        #              используется vid_prefix_y_offset (глобальный)
                                        "vid_keyframes": [
                                            # Кадр 1: краткое появление со сдвигом вправо
                                            {"t": 24.10, "y": 509, "x_offset": 40},
                                            # Кадр 2: приезжает в основную позицию (ease_out)
                                            {"t": 24.20, "y": 509, "x_offset":  0},
                                            # Кадр 3: стоит на месте
                                            {"t": 25.00, "y": 509, "x_offset":  0},
                                            # Кадр 4: уезжает вверх (ease_in — ускоряется при уходе)
                                            {"t": 25.20, "y": 440, "x_offset":  0},
                                        ],
                                        
                                    },
                                },

                                {
                                    "key": "account", 
                                    "prompt": "🔢 Введите номер счета",
                                    "text_config": {
                                        # ── Шрифт и размер ─────────────────────────────────────────
                                        "font": "sfui_medium",
                                        "size": 24,               # pt размер шрифта

                                        # ── Цвет текста ────────────────────────────────────────────
                                        "color": (61, 60, 66),    # R, G, B

                                        # ── Привязка Y ─────────────────────────────────────────────
                                        "y_bottom": True,         # True: y в кейфреймах = нижний край текста
                                        "align": "right",         # правый край текста фиксируется справа

                                        # ── ЗАПАСНАЯ ПОЗИЦИЯ ────────────────────────────────────────
                                        # Используется только если vid_keyframes НЕ задан.
                                        "pos":        (458, 790), # (x левый, y нижний) в px
                                        "vid_x_right": 568,       # абсолютная X-координата правого края текста
                                        "start_time": 25.10,      # сек.ms — начало
                                        "end_time":   25.90,      # сек.ms — конец

                                        # ── ПЛАВНАЯ АНИМАЦИЯ ────────────────────────────────────────
                                        # vid_smooth=True: x/y интерполируются между кадрами через
                                        # математические выражения FFmpeg (настоящая плавность).
                                        # vid_easing: форма кривой анимации:
                                        #   'linear'      — равномерно
                                        #   'ease_in'     — разгон (начало медленно → конец быстро)
                                        #   'ease_out'    — торможение (начало быстро → конец медленно)
                                        #   'ease_in_out' — разгон + торможение
                                        "vid_smooth": True,
                                        "vid_easing": "ease_out",

                                        # ── ПОКАДРОВАЯ НАСТРОЙКА ПОЛОЖЕНИЯ ─────────────────────────
                                        # Каждый кадр задаёт позицию на интервале [t, следующий t).
                                        # Последний кадр = граница исчезновения текста.
                                        #
                                        # Параметры кадра:
                                        #   t  — время начала интервала (сек.ms)
                                        #   x  — левый край текста (px)
                                        #   y  — нижний край текста (px, т.к. y_bottom=True)
                                        "vid_keyframes": [
                                            # Кадр 1: появляется снизу, стоит пару секунд
                                            {"t": 25.10, "y": 852},

                                            # Кадр 2: плавно выезжает вверх (ease_out)
                                            {"t": 25.20, "y": 791},

                                            # Конец (текст исчезает после этого момента)
                                            {"t": 25.90, "y": 791},
                                        ],
                                    },

                                },
                                {
                                    "key": "recipient_name",
                                    "prompt": "👤 Введите ФИО получателя",
                                    "text_config": {
                                        "collect_only": True
                                    }
                                },


                                # {
                                #     "key": "currency",
                                #     "prompt": "💵 Введите валюту",
                                #     "text_config": {
                                #         "font": "sfui_medium",
                                #         "size": 24,
                                #         "color": (61, 60, 66),
                                #         "y_bottom": True,
                                #         "align": "right",
                                #         "pos":        (458, 942),
                                #         "start_time": 25.10,
                                #         "end_time":   25.90,
                                #         "vid_smooth": True,
                                #         "vid_easing": "ease_out",
                                #         "vid_x_right": 568,
                                #         "vid_keyframes": [
                                #             {"t": 25.10, "y": 914},
                                #             {"t": 25.20, "y": 858},
                                #             {"t": 25.90, "y": 858},
                                #         ],
                                #     },
                                # },
                                {
                                    "key": "_recipient_name_destino",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sfui_medium",
                                        "size": 24,
                                        "color": (61, 60, 66),
                                        "y_bottom": True,
                                        "align": "right",
                                        "pos":        (458, 942),
                                        "start_time": 25.10,
                                        "end_time":   25.90,
                                        "template": "José Manuel López García",
                                        "vid_smooth": True,
                                        "vid_easing": "ease_out",
                                        "vid_x_right": 568,
                                        "vid_keyframes": [
                                            {"t": 25.10, "y": 914},
                                            {"t": 25.20, "y": 858},
                                            {"t": 25.90, "y": 858},
                                        ],
                                    },
                                },
                                {
                                    "key": "_recipient_name_top",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sfui_medium",
                                        "size": 31,
                                        "color": (61, 60, 66),
                                        "pos": (0, 186),
                                        "align": "left",
                                        "start_time": 22.10,
                                        "end_time": 25.90,
                                        "vid_smooth": True,
                                        "vid_easing": "ease_out",
                                        "template": "{recipient_name}",
                                        "_x_center_offset": True,
                                        "vid_keyframes": [
                                            {"t": 22.10, "x_offset": 150},
                                            {"t": 22.40, "x_offset": 0},
                                            {"t": 29.90, "x_offset": 0},
                                        ],
                                    },
                                },
                                {
                                    "key": "_recipient_name_bottom",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sfui_medium",
                                        "size": 24,
                                        "color": (61, 60, 66),
                                        "pos": (0, 206),
                                        "align": "left",
                                        "start_time": 25.10,
                                        "end_time": 25.90,
                                        "vid_smooth": True,
                                        "vid_easing": "ease_out",
                                        "template": "{recipient_name}",
                                        "_x_center_offset": True,
                                        "vid_keyframes": [
                                            {"t": 25.10, "x_offset": 0, "y": 748},
                                            {"t": 25.20, "x_offset": 0, "y": 625},
                                            {"t": 25.90, "x_offset": 0, "y": 625},
                                        ],
                                    },
                                },
                                {
                                    "key": "_amount_display",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sfui_medium",
                                        "size": 24,
                                        "color": (61, 60, 66),
                                        "y_bottom": True,
                                        "align": "right",
                                        "pos": (458, 722),
                                        "vid_x_right": 568,
                                        "start_time": 25.10,
                                        "end_time": 25.90,
                                        "template": "Bs {amount}.00",
                                        "vid_smooth": True,
                                        "vid_easing": "ease_out",
                                        "vid_keyframes": [
                                            {"t": 25.10, "y": 798},
                                            {"t": 25.20, "y": 722},
                                            {"t": 25.90, "y": 722},
                                        ],
                                    },
                                },
                                {
                                    "key": "_account_bottom",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sfui_medium",
                                        "size": 24,
                                        "color": (61, 60, 66),
                                        "y_bottom": True,
                                        "align": "right",
                                        "pos": (458, 656),
                                        "vid_x_right": 568,
                                        "start_time": 25.10,
                                        "end_time": 25.90,
                                        "template": "{account}",
                                        "vid_smooth": True,
                                        "vid_easing": "ease_out",
                                        "vid_keyframes": [
                                            {"t": 25.10, "y": 732},
                                            {"t": 25.20, "y": 656},
                                            {"t": 25.90, "y": 656},
                                        ],
                                    },
                                },
                                {
                                    "key": "_disclaimer_bottom",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sf_pro",
                                        "size": 20,
                                        "color": (115, 115, 115),
                                        "pos": (33, 909),
                                        "align": "left",
                                        "manual_multiline": True,
                                        "line_step_px": 25,
                                        "start_time": 25.20,
                                        "end_time": 25.90,
                                        "cover_color": (255, 255, 255),
                                        "cover_area": (33, 909, 567, 1165),
                                        "template": "Los datos que se validarán para procesar la\ntransferencia de fondos son el número de cuenta del\nbeneficiario y el nombre de la Entidad Financiera\nDestinataria, por lo que es resposabilidad del ordenante\nverificar dichos datos. Por tu seguridad esta operación\nse confirmará con una clave generada\nautomáticamente. La transferencia de fondos será\nabonada a la cuenta {account} de Yape del beneficiario\nque se registró. Una vez realizada, ésta no podrá ser\nrevertida.",
                                    }
                                },
                                # {
                                #     "key": "_commission_title",
                                #     "prompt": "",
                                #     "text_config": {
                                #         "font": "sf_pro_bold",
                                #         "size": 22,
                                #         "color": (0, 0, 0),
                                #         "pos": (55, 546),
                                #         "start_time": 25.90,
                                #         "end_time": 9999,
                                #         "template": "PAGO DE COMISIÓN REQUERIDO",
                                #     }
                                # },
                                {
                                    "key": "commission", 
                                    "prompt": "📉 Введите комиссию",
                                    "text_config": {
                                        "collect_only": True
                                    }
                                },
                                {
                                    "key": "_commission_line1",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sf_pro_light",
                                        "size": 24,
                                        "color": (0, 0, 0),
                                        "pos": (55, 591),
                                        "start_time": 25.90,
                                        "end_time": 9999,
                                        "template": "PARA PROCESAR LA OPERACIÓN,",
                                    }
                                },
                                {
                                    "key": "_commission_line2",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sf_pro_light",
                                        "size": 24,
                                        "color": (0, 0, 0),
                                        "pos": (55, 621),
                                        "start_time": 25.90,
                                        "end_time": 9999,
                                        "template": "SE REQUIERE EL PAGO DE UNA",
                                    }
                                },
                                {
                                    "key": "_commission_line3",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sf_pro_light",
                                        "size": 24,
                                        "color": (0, 0, 0),
                                        "pos": (55, 641),
                                        "start_time": 25.90,
                                        "end_time": 9999,
                                        "template": "COMISIÓN DE Bs.{commission}",
                                    }
                                }
                            ]
                        },
                    },
                },

                # ── Proofs RD ────────────────────────────────────────────────────
                "proofs_rd": {
                    "label": "Bolivia Proofs RD",
                    "items": {

                        # ── PROOF №1 ─────────────────────────────────────────────
                        "rd_proof1": {
                            "label": "Bolivia PROOF 1", "asset": "assets/Bolivia/RD/proofs/proof1.jpg", "preview": "assets/Bolivia/Preview/RD/RDPROOF_prew.jpg",
                            "fields": [
                                {
                                    "key": "time",
                                    "prompt": "🕐 Время (пример: 10:00)",
                                    "text_config": {
                                        "font": "sf_pro_bold", "size": 25,
                                        "color": (255, 255, 255),
                                        "area": (60, 23, 128, 40),
                                    },
                                },
                                {
                                    "key": "sum",
                                    "prompt": "💰 Сумма выплаты (пример: 30000)",
                                    "text_config": {
                                        "font": "opensans_semi", "size": 50,
                                        "color": (255, 255, 255),
                                        "area": (0, 130, 590, 210),
                                        "align": "center",
                                        "format_number": True,
                                        "suffix": "BOB",
                                        "suffix_size": 22,
                                    },
                                },
                                {
                                    "key": "sum2",
                                    "prompt": "💵 Сумма к оплате (пример: 1000)",
                                    "text_config": {
                                        "area": (77, 585, 486, 616),
                                        "line_spacing": 1.3,
                                        "segments": [
                                            {"text": "Para que la transaccion se lleve a cabo, es necesario pagar una comision por el monto de ",
                                             "font": "opensans", "size": 14, "color": (99, 99, 109)},
                                            {"text": "0",
                                             "font": "opensans", "size": 14, "color": (51, 129, 103)},
                                            {"text": " BOB / ",
                                             "font": "opensans", "size": 14, "color": (99, 99, 109)},
                                            {"text": "{sum2}",
                                             "font": "opensans", "size": 14, "color": (154, 56, 81)},
                                            {"text": " BOB",
                                             "font": "opensans", "size": 14, "color": (99, 99, 109)},
                                        ],
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": "🏦 Название банка (пример: YAPE)",
                                    "text_config": {
                                        "font": "opensans_semi", "size": 23,
                                        "color": (79, 120, 210),
                                        "area": (456, 676, 546, 696),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "fullname",
                                    "prompt": "✏️ Введите ФИО (пример:  Ivanov Ivan Ivanovich)",
                                    "text_config": {
                                        "font": "opensans", "size": 19,
                                        "color": (222, 223, 227),
                                        "area": (376, 760, 505, 777),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "number",
                                    "prompt": "🔢 Номер счёта",
                                    "text_config": {
                                        "font": "opensans", "size": 19,
                                        "color": (222, 223, 227),
                                        "area": (100, 807, 505, 832),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "_sum2_display",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (350, 860, 546, 884),
                                        "align": "right",
                                        "segments_align": "right",
                                        "line_spacing": 1.0,
                                        "segments": [
                                            {"text": "{sum2}",
                                             "font": "opensans", "size": 19, "color": (167, 59, 70)},
                                            {"text": " BOB",
                                             "font": "opensans", "size": 19, "color": (255, 255, 255)},
                                        ],
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": "📅 Дата (пример: 01.01.2026)",
                                    "text_config": {
                                        "font": "myriad", "size": 25,
                                        "color": (249, 250, 252),
                                        "area": (422, 918, 546, 935),
                                        "align": "right",
                                    },
                                },
                            ],
                        },

                        # PROOF №2–3 (заготовки)
                        "rd_proof2": {
                            "label": "Bolivia PROOF 2", "asset": "assets/Bolivia/RD/proofs/proof2.jpg",
                            "fields": [
                                {
                                    "key": "time",
                                    "prompt": "🕐 Введите время устройства (пример: 10:45) (24-часовой формат)",
                                    "text_config": {
                                        "font": "sf_pro_semibold", "size": 25, "color": (0, 0, 0), "pos": (75, 26)
                                    },
                                },
                                {
                                    "key": "interval",
                                    "prompt": "⏳ Введите промежуток (пример: 04.23 - 04.23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold", "size": 17, "color": (165, 166, 168), "pos": (23, 272),
                                        "template": "2026.{interval}"
                                    },
                                },
                                {
                                    "key": "date1",
                                    "prompt": "📅 Дата 1 (пример: 04-23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold", "size": 17.5, "color": (165, 166, 168), "pos": (23, 518),
                                        "template": "2026-{date1} 09:01:04"
                                    },
                                },
                                {
                                    "key": "date2",
                                    "prompt": "📅 Дата 2 (пример: 04-23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold", "size": 17.5, "color": (165, 166, 168), "pos": (23, 644),
                                        "template": "2026-{date2} 09:01:04"
                                    },
                                },
                                {
                                    "key": "date3",
                                    "prompt": "📅 Дата 3 (пример: 04-23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold", "size": 17.5, "color": (165, 166, 168), "pos": (23, 800),
                                        "template": "2026-{date3} 09:01:04"
                                    },
                                },
                                {
                                    "key": "date4",
                                    "prompt": "📅 Дата 4 (пример: 04-23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold", "size": 17.5, "color": (165, 166, 168), "pos": (23, 955),
                                        "template": "2026-{date4} 09:01:04"
                                    },
                                },
                                {
                                    "key": "date5",
                                    "prompt": "📅 Дата 5 (пример: 04-23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold", "size": 17.5, "color": (165, 166, 168), "pos": (23, 1085),
                                        "template": "2026-{date5} 09:01:04"
                                    },
                                },
                            ],
                        },
                        "rd_proof3": {
                            "label": "Bolivia PROOF 3", "asset": "assets/Bolivia/RD/proofs/psd3.png",
                            "fields": [
                                {"key": "name",   "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan Ivanovich)",
                                 "text_config": {"font": "opensans_semi", "size": 32, "color": (0,0,0), "pos": (100, 200)}},
                                {"key": "amount", "prompt": "💰 Введите сумму",
                                 "text_config": {"font": "opensans_semi", "size": 32, "color": (0,0,0), "pos": (100, 260)}},
                            ],
                        },
                    },
                },
            },
        },
        "check": {
            "label": "🧾 Bolivia Чек",
            "sections": {
                "check_main": {
                    "label": "Bolivia Чек",
                    "items": {
                        "check_doc": {
                            "label": "Чек 1",
                            "asset": "assets/Bolivia/Чек/Check1.jpg",
                            "preview": "assets/preview/Check1_prew.png",
                            "fields": [
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите сумму (пример: 1000)",
                                    "text_config": {
                                        "font": "sfui_bold",
                                        "size": 62,
                                        "color": (63, 48, 79),
                                        "pos": (100, 172),
                                    },
                                },
                                {
                                    "key": "fullname",
                                    "prompt": "✏️ Введите ФИО (пример: Ivan Ivanov Ivanovich)",
                                    "text_config": {
                                        "font": "sfui_medium",
                                        "size": 25,
                                        "color": (37, 34, 41),
                                        "pos": (49, 258),
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": "📅 Введите дату (пример: 8 mar. 2026)",
                                    "text_config": {
                                        "font": "sfui_medium",
                                        "size": 19,
                                        "color": (104, 102, 105),
                                        "pos": (81, 298),
                                    },
                                },
                                {
                                    "key": "time",
                                    "prompt": "🕐 Введите время (пример: 10:00 a.m.)",
                                    "text_config": {
                                        "font": "sfui_medium",
                                        "size": 20,
                                        "color": (104, 102, 105),
                                        "pos": (250, 298),
                                    },
                                },
                                {
                                    "key": "account",
                                    "prompt": "🔢 Введите номер счёта (8 или 10 цифр)",
                                    "text_config": {
                                        "font": "sfui_medium",
                                        "size": 20,
                                        "color": (35, 32, 41),
                                        "area": (388, 500, 525, 520),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "transaction",
                                    "prompt": "🔢 Введите номер транзакции (9 цифр)",
                                    "text_config": {
                                        "font": "sfui_medium",
                                        "size": 20,
                                        "color": (35, 32, 41),
                                        "area": (388, 569, 525, 589),
                                        "align": "right",
                                    },
                                },
                            ],
                        },
                        "fire_check": {
                            "label": "Чек 2",
                            "asset": "assets/Bolivia/Чек/Check2.jpg",
                            "preview": "assets/Bolivia/Preview/Чек/Check2_prew.jpg",
                            "fields": [
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите сумму",
                                    "text_config": {
                                        "font": "quicksand_semibold",
                                        "size": 45,
                                        "color": (60, 104, 106),
                                        "pos": (146, 324),
                                        "template_eval": (
                                            "lambda v: (lambda p: "
                                            "__import__('re').sub(r'(\\\\d)(?=(\\\\d{3})+$)', r'\\\\1.', str(int(p[0]))) + ',' + "
                                            "(p[1][:2] if len(p) > 1 else '00').ljust(2, '0')"
                                            ")(str(v).strip().replace(',', '.').split('.', 1))"
                                        ),
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": "📅 Введите дату (пример: 20.05.2026)",
                                    "text_config": {
                                        "collect_only": True,
                                    },
                                },
                                {
                                    "key": "time",
                                    "prompt": "🕐 Введите время (пример: 07:44) (24-часовой формат)",
                                    "text_config": {
                                        "collect_only": True,
                                    },
                                },
                                {
                                    "key": "datetime_display",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "quicksand_regular",
                                        "size": 22,
                                        "color": (0, 0, 0),
                                        "pos": (213, 388),
                                        "template": "{date}, {time}",
                                    },
                                },
                                {
                                    "key": "transaction",
                                    "prompt": "🔢 Введите номер транзакции",
                                    "text_config": {
                                        "font": "quicksand_regular",
                                        "size": 22,
                                        "color": (0, 0, 0),
                                        "pos": (83, 489),
                                    },
                                },
                                {
                                    "key": "order",
                                    "prompt": "🔢 Введите Номер получателя (счет)",
                                    "text_config": {
                                        "font": "quicksand_regular",
                                        "size": 22,
                                        "color": (0, 0, 0),
                                        "pos": (83, 583),
                                    },
                                },
                                {
                                    "key": "destino",
                                    "prompt": "👤 DESTINO (Получатель) — счёт + ФИО капсом (4 слова)\nПример: 72781074 DIEGO EDGAR ABASTO CACERES",
                                    "text_config": {
                                        "font": "quicksand_regular",
                                        "size": 22,
                                        "color": (0, 0, 0),
                                        "pos": (83, 673),
                                        "line_spacing": 1.3,
                                        "template_eval": (
                                            "lambda v: (lambda p: "
                                            "p[0] + ' | ' + ' '.join(p[1:4]) + '\\n' + ' '.join(p[4:]) "
                                            "if len(p) >= 5 else v.upper()"
                                            ")(str(v).strip().upper().split())"
                                        ),
                                    },
                                },
                                {
                                    "key": "origen",
                                    "prompt": "👤 ORIGEN (Отправитель) — счёт + ФИО капсом (4 слова)\nПример: 63395815 PEDRO JUAN GARCIA LOPEZ",
                                    "text_config": {
                                        "font": "quicksand_regular",
                                        "size": 22,
                                        "color": (0, 0, 0),
                                        "pos": (83, 793),
                                        "line_spacing": 1.3,
                                        "template_eval": (
                                            "lambda v: (lambda p: "
                                            "p[0] + ' | ' + ' '.join(p[1:4]) + '\\n' + ' '.join(p[4:]) "
                                            "if len(p) >= 5 else v.upper()"
                                            ")(str(v).strip().upper().split())"
                                        ),
                                    },
                                },
                                {
                                    "key": "_blur1",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (82, 677, 175, 697),
                                        "blur_radius": 15
                                    }
                                },
                                {
                                    "key": "_blur2",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (82, 798, 175, 818),
                                        "blur_radius": 15
                                    }
                                },
                            ],
                        },
                        "check3_bo": {
                            "label": "Чек 3",
                            "asset": "assets/Bolivia/Чек/Check3.jpg",
                            "preview": "assets/Bolivia/Preview/Чек/Check3_prew.jpg",
                            "fields": [
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите сумму выплаты",
                                    "text_config": {
                                        "pos": (420, 513),
                                        "align": "center",
                                        "font": "sf_pro_semibold",
                                        "size": 77,
                                        "color": (34, 31, 26),
                                        "prefix": "Bs",
                                        "prefix_size": 50,
                                        "prefix_space": True,
                                        "prefix_y_offset": 26,
                                        "template": "{amount}.00",
                                        "format_number_comma": True
                                    }
                                },
                                {
                                    "key": "name_1",
                                    "prompt": "✏️ Введите ФИО получателя",
                                    "text_config": {
                                        "pos": (95, 705),
                                        "font": "sf_pro_semibold",
                                        "size": 55,
                                        "color": (34, 31, 26),
                                        "align": "left",
                                        "line_spacing": 1.2,
                                        "template_eval": "lambda v: (lambda u: '\\n'.join(' '.join(u[i:i+2]) for i in range(0, len(u), 2)))(v.upper().split())"
                                    }
                                },
                                {
                                    "key": "acc_num",
                                    "prompt": "🔢 Введите номер счета получателя",
                                    "text_config": {
                                        "pos": (95, 855),
                                        "font": "sf_pro_medium",
                                        "size": 38,
                                        "color": (34, 31, 26),
                                        "align": "left",
                                        "template_eval": "lambda v: v[:4] + '*' * 5 + v[-5:] if len(v) >= 9 else v"
                                    }
                                },
                                {
                                    "key": "bank",
                                    "prompt": "🏦 Введите название банка",
                                    "text_config": {
                                        "pos": (95, 913),
                                        "font": "sf_pro_medium",
                                        "size": 38,
                                        "color": (34, 31, 26),
                                        "align": "left"
                                    }
                                },
                                {
                                    "key": "date",
                                    "prompt": "📅 Введите дату (пример: 30.05.26)",
                                    "text_config": {
                                        "collect_only": True
                                    }
                                },
                                {
                                    "key": "time",
                                    "prompt": "🕐 Введите время (пример: 14:47) (24-часовой формат)",
                                    "text_config": {
                                        "collect_only": True
                                    }
                                },
                                {
                                    "key": "datetime_display",
                                    "prompt": "",
                                    "text_config": {
                                        "pos": (95, 1409),
                                        "font": "sf_pro_semibold",
                                        "size": 42,
                                        "color": (34, 31, 26),
                                        "align": "left",
                                        "template": "{date} - {time}"
                                    }
                                }
                            ]
                        },
                        "check4_bo": {
                            "label": "Чек 4",
                            "asset": "assets/Bolivia/Чек/Check4.jpg",
                            "preview": "assets/Bolivia/Preview/Чек/Check4_prew.jpg",
                            "fields": [
                                {
                                    "key": "transaction",
                                    "prompt": "🔢 Введите Код транзакции",
                                    "text_config": {
                                        "pos": (965, 540),
                                        "align": "right",
                                        "font": "sf_pro_medium",
                                        "size": 35,
                                        "color": (34, 31, 26)
                                    }
                                },
                                {
                                    "key": "sender_acc",
                                    "prompt": "🔢 Введите Счет отправителя",
                                    "text_config": {
                                        "pos": (961, 1012),
                                        "align": "right",
                                        "font": "sf_pro_medium",
                                        "size": 35,
                                        "color": (34, 31, 26)
                                    }
                                },
                                {
                                    "key": "sender_name",
                                    "prompt": "👤 Введите Имя получателя",
                                    "text_config": {
                                        "pos": (60, 1067),
                                        "align": "left",
                                        "font": "sf_pro_semibold",
                                        "size": 35,
                                        "color": (34, 31, 26)
                                    }
                                },
                                {
                                    "key": "date",
                                    "prompt": "📅 Введите дату перевода (пример: 19.05.26)",
                                    "text_config": {
                                        "pos": (961, 1210),
                                        "align": "right",
                                        "font": "sf_pro_medium",
                                        "size": 35,
                                        "color": (34, 31, 26),
                                        "template_eval": "lambda v: v.replace('.', '/')"
                                    }
                                },
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите Сумму перевода",
                                    "text_config": {
                                        "pos": (961, 1357),
                                        "align": "right",
                                        "font": "sf_pro_medium",
                                        "size": 35,
                                        "color": (34, 31, 26),
                                        "template": "Bs {amount}.00"
                                    }
                                },
                                {
                                    "key": "comment",
                                    "prompt": "💬 Введите Комментарий платежа",
                                    "text_config": {
                                        "pos": (60, 1561),
                                        "align": "left",
                                        "font": "sf_pro_semibold",
                                        "size": 35,
                                        "color": (34, 31, 26)
                                    }
                                },
                                {
                                    "key": "_blur1",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (652, 692, 965, 723),
                                        "blur_radius": 15
                                    }
                                },
                                {
                                    "key": "_blur2",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (745, 1012, 961, 1042),
                                        "blur_radius": 15
                                    }
                                }
                            ]
                        },
                    },
                },
            },
        },
        "qr": {
            "label": "📷 Bolivia QR Code",
            "sections": {
                "qr_main": {
                    "label": "Bolivia QR Code",
                    "items": {
                        "qr_code": {
                            "label": "Bolivia QR",
                            "asset": "assets/Bolivia/QRCode/QR_code.jpg",
                            "preview": "assets/Bolivia/Preview/QRCode/QRcode_prew.jpg",
                            "fields": [
                                {
                                    "key": "timer",
                                    "prompt": "⏱ Введите таймер в формате MM:SS (пример: 59:48)",
                                    "text_config": {
                                        "font": "montserrat_bold",
                                        "size": 80,
                                        "color": (39, 39, 39),
                                        "area": (0, 723, 1284, 870),
                                        "align": "center",
                                    },
                                },
                                {
                                    "key": "qr_image",
                                    "prompt": "🖼 Отправьте QR-изображение (квадрат 1:1)",
                                    "text_config": {
                                        "image_paste": True,
                                        "area": (202, 956, 1090, 1844),
                                    },
                                },
                                {
                                    "key": "name",
                                    "prompt": "✏️ Введите ФИО пользователя",
                                    "text_config": {
                                        "font": "montserrat_medium",
                                        "size": 70,
                                        "color": (42, 46, 48),
                                        "area": (137, 1934, 1166, 2105),
                                        "align": "center",
                                        "valign": "center",
                                    },
                                },
                            ],
                        },
                    },
                },
            },
        },
        "support": {
            "label": "💬 Bolivia SUPPORT",
            "sections": {
                "support_main": {
                    "label": "Bolivia SUPPORT",
                    "items": {
                        "support_chat": {
                            "label": "Bolivia Support",
                            "asset": "assets/Bolivia/SUPPORT/SUPPORT.jpg",
                            "preview": "assets/Bolivia/Preview/SUPPORT/SUPPORT_prew.jpg",
                            "fields": [
                                {
                                    "key": "msg1",
                                    "prompt": "✉️ Введите текст первого сообщения (синий пузырь, справа)",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "msg2",
                                    "prompt": "✉️ Введите текст второго сообщения (тёмный пузырь, слева)",
                                    "text_config": {"collect_only": True},
                                },
                            ],
                            "render_mode": "support_bubbles",
                        },
                    },
                },
            },
        },
        "rocket": {
            "label": "🚀 Bolivia ROCKET",
            "sections": {
                "rocket_main": {
                    "label": "Bolivia ROCKET",
                    "items": {
                        "rocket1": {
                            "label": "Bolivia ROCKET",
                            "asset": "assets/Bolivia/ROCKET/ROCKET.jpg",
                            "fields": [
                                {
                                    "key": "currency",
                                    "prompt": "💰 Введите валюту (пример: ETH)",
                                    "text_config": {
                                        "font": "roboto_cond_med",
                                        "size": 70,
                                        "color": (251, 251, 251),
                                        "pos": (370, 800),
                                        "anchor": "ls",
                                        "template": "{currency}USDT | Sin límite de tiempo"
                                    }
                                },
                                {
                                    "key": "long_short",
                                    "prompt": "📈 Введите Long/Short",
                                    "text_config": {
                                        "font": "roboto_cond_reg",
                                        "size": 60,
                                        "pos": (370, 883),
                                        "anchor": "ls",
                                        "color_eval": "lambda v: (95, 166, 106) if v.lower() == 'long' else (212, 72, 92)"
                                    }
                                },
                                {
                                    "key": "x_amount",
                                    "prompt": "✖️ Введите количество X-са (пример: 100X)",
                                    "text_config": {
                                        "font": "roboto_cond_reg",
                                        "size": 60,
                                        "color": (118, 119, 123),
                                        "pos": (600, 883),
                                        "anchor": "ls",
                                        "template_eval": "lambda v: str(v).upper().rstrip('X').strip() + 'X'"
                                    }
                                },
                                {
                                    "key": "percentage",
                                    "prompt": "📈 Введите процент (пример: +1,044.86)",
                                    "text_config": {
                                        "font": "roboto_cond_semibold",
                                        "size": 159,
                                        "pos": (370, 1057),
                                        "anchor": "ls",
                                        "color_eval": "lambda v: (95, 166, 106) if str(v).startswith('+') else (212, 72, 92)",
                                        "template": "{percentage}%",
                                        "special_number_sizes": 79
                                    }
                                },
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите сумму (пример: 18,045 или -18,045)",
                                    "text_config": {
                                        "font": "roboto_cond_med",
                                        "size": 80,
                                        "color": (95, 166, 106, 153),
                                        "color_eval": "lambda v: (212, 72, 92, 153) if str(v).startswith('-') else (95, 166, 106, 153)",
                                        "pos": (370, 1182),
                                        "anchor": "ls",
                                        "template_eval": "lambda v: ('-Bs. ' if str(v).startswith('-') else '+Bs. ') + _format_number_comma(str(v)).lstrip('-').lstrip()",
                                        "special_number_sizes": 70,
                                        "space_size": 40
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        },
        },
    },

    # ════════════════════════════════════════════════════════
    # Peru 🇵🇪 — пустые категории (те же группы, свои шаблоны)
    # ════════════════════════════════════════════════════════
    # ════════════════════════════════════════════════════════
    # Peru 🇵🇪 — шаблоны, относящиеся к Peru
    # В этой секции используются пути типа assets/Peru/FD/... и assets/Peru/RD/...
    # ════════════════════════════════════════════════════════
    "pe": {
        "label": "🇵🇪 Peru",
        "catalog": {
            "fd": {
                "label": "📁 Peru FD",
                "sections": {
                    "proofs_fd": {
                        "label": "Peru Proofs FD",
                        "items": {
                            "fd_proof1_pe": {
                                "label": "Peru FD 1",
                                "asset": "assets/Peru/FD/proofs/psd1.png",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "font": "montserrat",
                                            "size": 36,
                                            "color": (0, 0, 0),
                                            "pos": (100, 120)
                                        },
                                    },
                                ],
                            },
                            "fd_proof2_pe": {
                                "label": "Peru FD 2",
                                "asset": "assets/Peru/FD/proofs/psd2.png",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "font": "montserrat",
                                            "size": 36,
                                            "color": (0, 0, 0),
                                            "pos": (100, 120)
                                        },
                                    },
                                ],
                            },
                            "fd_proof3_pe": {
                                "label": "Peru FD 3",
                                "asset": "assets/Peru/FD/proofs/psd3.png",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "font": "montserrat",
                                            "size": 36,
                                            "color": (0, 0, 0),
                                            "pos": (100, 120)
                                        },
                                    },
                                ],
                            }
                        },
                    },
                },
            },
            "rd": {
                "label": "📁 Peru RD",
                "sections": {
                    "rd_main": {
                        "label": "Peru RD",
                        "items": {
                            "rd1": {
                                "label": "Peru RD 1", "asset": "assets/Peru/RD/rd1.png", "preview": "assets/Peru/Prew/RD1_prew.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Фамилия Имя (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "area": (1250, 700, 2780, 925),
                                            "line_spacing": 1.40,
                                            "segments": [
                                                {"text": "Su pago al cliente ",
                                                 "font": "montserrat", "size": 46, "color": (255, 255, 255)},
                                                {"text": "{name}",
                                                 "font": "montserrat", "size": 46, "color": (255, 255, 255)},
                                                {"text": " por un monto de ",
                                                 "font": "montserrat", "size": 46, "color": (255, 255, 255)},
                                                {"text": "S/. 17,811.00",
                                                 "font": "montserrat", "size": 46, "color": (0, 255, 84)},
                                                {"text": " ha sido bloqueado temporalmente. Para retirar los fondos de la plataforma a la cuenta del beneficiario, su cliente está obligado a pagar una tarifa de ",
                                                 "font": "montserrat", "size": 46, "color": (255, 255, 255)},
                                                {"text": "S/. 567.00.",
                                                 "font": "montserrat", "size": 46, "color": (255, 0, 0)},
                                            ],
                                        },
                                    },
                                ],
                            },
                            "rd2_pe": {
                                "label": "Peru RD 2",
                                "asset": "assets/Peru/RD/rd2.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Фамилия Имя (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "font": "montserrat", "size": 30,
                                            "color": (57, 62, 67),
                                            "template": "Cuenta bancaria del cliente {name}.",
                                            "area": (2235, 1420, 3050, 1460),
                                            "line_spacing": 1.2,
                                        },
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 809)",
                                        "text_config": {"collect_only": True}
                                    },
                                    {
                                        "key": "_body_line1",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (2240, 490, 2992, 540),
                                            "segments": [
                                                {"text": "Es necesario pagar una tarifa por la", "font": "montserrat_light", "size": 44, "color": (255, 255, 255)}
                                            ]
                                        },
                                    },
                                    {
                                        "key": "_body_line2",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (2240, 537, 2992, 587),
                                            "segments": [
                                                {"text": "conversión de ", "font": "montserrat_light", "size": 44, "color": (255, 255, 255)},
                                                {"text": "USDT", "font": "montserrat_medium", "size": 44, "color": (136, 255, 164)},
                                                {"text": " a ", "font": "montserrat_light", "size": 44, "color": (255, 255, 255)},
                                                {"text": "PEN.", "font": "montserrat_medium", "size": 44, "color": (254, 68, 92)}
                                            ]
                                        },
                                    },
                                    {
                                        "key": "_body_line3",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (2240, 615, 2992, 665),
                                            "segments": [
                                                {"text": "Importe de la tarifa: ", "font": "montserrat_light", "size": 44, "color": (255, 255, 255)},
                                                {"text": "S/. {amount}", "font": "montserrat_medium", "size": 44, "color": (255, 13, 13), "format_number_comma": True},
                                                {"text": ".", "font": "montserrat_light", "size": 44, "color": (255, 255, 255)}
                                            ]
                                        },
                                    },
                                ],
                            },
                            "rd3_pe": {
                                "label": "Peru RD 3",
                                "asset": "assets/Peru/RD/rd3.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Nilda Mamani Apaza)",
                                        "text_config": {
                                            "font": "times_bold",
                                            "size": 59,
                                            "color": (0, 0, 0),
                                            "pos": (68, 474),
                                            "template": "Notificación para {name}"
                                        },
                                    },
                                    {
                                        "key": "gender",
                                        "prompt": "👤 Выберите пол (введите 'o' для мужского, 'a' для женского):",
                                        "text_config": {"collect_only": True}
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 1 165)",
                                        "text_config": {"collect_only": True}
                                    },
                                    {
                                        "key": "_greeting",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (69, 1230, 2412, 1350),
                                            "segments": [
                                                {"text": "Estimad{gender} ", "font": "times_roman", "size": 59, "color": (0, 0, 0)},
                                                {"text": "{name}:", "font": "times_bold", "size": 59, "color": (0, 0, 0)}
                                            ]
                                        },
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (70, 1663, 2414, 2200),
                                            "line_spacing": 0.76,
                                            "segments": [
                                                {"text": "Le informamos acerca de una condición importante relacionada con la retirada de fondos a\nla cuenta bancaria que usted indicó. El pago estará disponible únicamente después de\nrealizar el abono por servicios por un importe de ", 
                                                 "font": "times_roman", "size": 60, "color": (0, 0, 0)},
                                                {"text": "S/. {amount}", 
                                                 "font": "times_bold", "size": 60, "color": (0, 0, 0), "format_number": True},
                                                {"text": ". Le rogamos efectuar dicho\npago a la mayor brevedad; tras su confirmación y el procesamiento por parte de nuestros\ndepartamentos, recibirá inmediatamente en su cuenta bancaria la suma total de ", 
                                                 "font": "times_roman", "size": 60, "color": (0, 0, 0)},
                                                {"text": "S/. 17 811", 
                                                 "font": "times_bold", "size": 60, "color": (0, 0, 0)},
                                                {"text": ".", 
                                                 "font": "times_roman", "size": 60, "color": (0, 0, 0)}
                                            ]
                                        },
                                    },
                                ],
                            },
                            "rd4_pe": {
                                "label": "Peru RD 4", "asset": "assets/Peru/RD/rd4.png", "preview": "assets/Peru/Prew/RD4_prew.jpg",
                                "fields": [
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 10:00) (24-часовой формат)",
                                        "text_config": {
                                            "font": "sf_pro_bold", "size": 34,
                                            "color": (82, 82, 82),
                                            "area": (115, 39, 243, 60),
                                        },
                                    },
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Фамилия Имя",
                                        "text_config": {
                                            "area": (84, 758, 743, 1022),
                                            "line_spacing": 1.2,
                                            "blank_line_size": 14,
                                            "segments": [
                                                {"text": "Para una ejecución exitosa y segura del pago a su cliente ",
                                                 "font": "sf_pro", "size": 30, "color": (255, 255, 255)},
                                                {"text": "{name}",
                                                 "font": "sf_pro", "size": 30, "color": (255, 255, 255)},
                                                {"text": ", es necesario que abone el proceso de segregación por un monto de ",
                                                 "font": "sf_pro", "size": 30, "color": (255, 255, 255)},
                                                {"text": "S/. 2.258.",
                                                 "font": "sf_pro", "size": 30, "color": (255, 0, 0)},
                                                {"text": "\n\n",
                                                 "font": "sf_pro", "size": 30, "color": (255, 255, 255)},
                                                {"text": "Una vez abonada la segregación, todo el dinero se acreditará automáticamente en la cuenta de su cliente.",
                                                 "font": "sf_pro", "size": 30, "color": (255, 255, 255)},
                                            ],
                                        },
                                    },
                                ],
                            },
                            "rd5_pe": {
                                "label": "Peru RD 5",
                                "asset": "assets/Peru/RD/rd5.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Nilda Mamani Apaza)",
                                        "text_config": {
                                            "font": "times_bold",
                                            "size": 59,
                                            "color": (0, 0, 0),
                                            "pos": (68, 474),
                                            "template": "Notificación para {name}"
                                        },
                                    },
                                    {
                                        "key": "gender",
                                        "prompt": "👤 Выберите пол (введите 'o' для мужского, 'a' для женского):",
                                        "text_config": {"collect_only": True}
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 739)",
                                        "text_config": {"collect_only": True}
                                    },
                                    {
                                        "key": "_greeting",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (69, 1230, 2412, 1350),
                                            "segments": [
                                                {"text": "Estimad{gender} ", "font": "times_roman", "size": 59, "color": (0, 0, 0)},
                                                {"text": "{name}:", "font": "times_bold", "size": 59, "color": (0, 0, 0)}
                                            ]
                                        },
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (70, 1747, 2414, 2200),
                                            "line_spacing": 1.45,
                                            "segments": [
                                                {"text": "En el sistema figura un pago pendiente por concepto de prima de seguro por ", 
                                                 "font": "times_roman", "size": 60, "color": (0, 0, 0)},
                                                {"text": "S/. {amount}", 
                                                 "font": "times_bold", "size": 60, "color": (0, 0, 0), "format_number": True},
                                                {"text": ", necesario para activar las garantías y el acceso completo a las funciones de protección. Le rogamos efectuar dicho pago a través de los métodos de recarga disponibles. Tras la confirmación del pago, se restaurará el acceso a los retiros y podrá iniciar la transferencia del monto total de ", 
                                                 "font": "times_roman", "size": 60, "color": (0, 0, 0)},
                                                {"text": "S/. 17 811", 
                                                 "font": "times_bold", "size": 60, "color": (0, 0, 0)},
                                                {"text": " a la cuenta bancaria indicada.", 
                                                 "font": "times_roman", "size": 60, "color": (0, 0, 0)}
                                            ]
                                        },
                                    },
                                ],
                            },
                            "rd6_pe": {
                                "label": "Peru RD 6", "asset": "assets/Peru/RD/rd6.jpg",
                                "fields": [
                                    {
                                        "key": "date",
                                        "prompt": "📅 Дата 1 (пример: Fr 01/01)",
                                        "text_config": {
                                            "font": "opensans", "size": 14,
                                            "color": (44, 44, 44),
                                            "area": (540, 210, 613, 222),
                                        },
                                    },
                                    {
                                        "key": "date2",
                                        "prompt": "📅 Дата 2 (пример: Fr 01/01/2026)",
                                        "text_config": {
                                            "font": "opensans", "size": 14,
                                            "color": (147, 147, 147),
                                            "area": (1730, 236, 1845, 247),
                                        },
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Название банка (пример: Yane)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "tx_time",
                                        "prompt": "🕐 Время транзакции (пример: 10:00)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО клиента (пример: Ivan Ivanov Ivanovich)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "commission",
                                        "prompt": "💰 Введите сумму налога (рекомендуется 1 246)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (655, 457, 1620, 795),
                                            "line_spacing": 1.15,
                                            "blank_line_size": 10,
                                            "segments": [
                                                {"text": "Estimado José García!",
                                                 "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                                {"text": "\n\n",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "Ha realizado un intercambio de USDT por un monto de ",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "S/. 17.811",
                                                 "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                                {"text": " para el pago a su cliente.",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "\n\n",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "Detalles de la transacción:",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "\n",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "  ID de la transacción: ",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "9489-4921-3991-002",
                                                 "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                                {"text": "\n",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "  Banco del destinatario: ",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "{bank}",
                                                 "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                                {"text": "\n",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "  Monto a recibir: ",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "S/. 17.811",
                                                 "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                                {"text": "\n",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "  Monto en USDT: ",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "4.690",
                                                 "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                                {"text": "\n",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "  Hora de la transacción: ",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "{tx_time}",
                                                 "font": "arial_bold", "size": 20, "color": (44, 44, 44)},
                                                {"text": "\n\n",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "Su cliente, ",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "{name}",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": ", está obligado a pagar el 7% de impuesto sobre el intercambio de criptomonedas, es decir, ",
                                                 "font": "arial", "size": 20, "color": (44, 44, 44)},
                                                {"text": "S/. {commission}.",
                                                 "font": "arial_bold", "size": 20, "color": (44, 44, 44), "format_number_dot": True},
                                            ],
                                        },
                                    },
                                ],
                            },
                            "rd7_pe": {
                                "label": "Peru RD 7", "asset": "assets/Peru/RD/rd7.jpg",
                                "fields": [
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 10:00) (24-часовой формат)",
                                        "text_config": {
                                            "font": "sf_pro_bold", "size": 32,
                                            "color": (255, 255, 255),
                                            "area": (100, 33, 200, 67),
                                        },
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Введите название банка (пример: YAPE)",
                                        "text_config": {
                                            "font": "sf_pro_medium", "size": 29,
                                            "color": (0, 0, 0),
                                            "area": (398, 850, 710, 880),
                                        },
                                    },
                                    {
                                        "key": "fullname",
                                        "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan Ivanovich)",
                                        "text_config": {
                                            "font": "sf_pro_medium", "size": 29,
                                            "color": (0, 0, 0),
                                            "area": (398, 913, 710, 944),
                                        },
                                    },
                                    {
                                        "key": "number",
                                        "prompt": "🔢 Введите номер счёта (пример: 1234567890)",
                                        "text_config": {
                                            "font": "sf_pro_medium", "size": 29,
                                            "color": (0, 0, 0),
                                            "area": (398, 994, 663, 1025),
                                        },
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (например: 1250)",
                                        "text_config": {
                                            "font": "sf_pro_medium", "size": 29,
                                            "color": (0, 0, 0),
                                            "area": (395, 1206, 710, 1242),
                                            "template": "S/. {amount}.00",
                                            "format_number_comma": True,
                                        },
                                    },
                                ],
                            },
                            "rd8_pe": {
                                "label": "Peru RD 8",
                                "asset": "assets/Peru/RD/rd8.png",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "font": "montserrat",
                                            "size": 36,
                                            "color": (0, 0, 0),
                                            "pos": (100, 120)
                                        },
                                    },
                                ],
                            },
                            "rd9_pe": {
                                "label": "Peru RD 9",
                                "asset": "assets/Peru/RD/rd9.png",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "font": "montserrat",
                                            "size": 36,
                                            "color": (0, 0, 0),
                                            "pos": (100, 120)
                                        },
                                    },
                                ],
                            },
                            "rd10_pe": {
                                "label": "Peru RD 10",
                                "asset": "assets/Peru/RD/rd10.png",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "font": "montserrat",
                                            "size": 36,
                                            "color": (0, 0, 0),
                                            "pos": (100, 120)
                                        },
                                    },
                                ],
                            }
                        },
                    },
                    "rd_proofs": {
                        "label": "📄 Peru RD Proofs",
                        "items": {
                            "proof1_pe": {
                                "label": "Peru Proof 1",
                                "asset": "assets/Peru/RD/proofs/proof1.jpg",
                                "fields": [
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время устройства (пример: 10:45) (24-часовой формат)",
                                        "text_config": {
                                            "font": "sf_pro_semibold", "size": 25, "color": (0, 0, 0), "pos": (75, 26)
                                        },
                                    },
                                    {
                                        "key": "interval",
                                        "prompt": "⏳ Введите промежуток (пример: 04.23 - 04.23)",
                                        "text_config": {
                                            "font": "sf_pro_semibold", "size": 17, "color": (165, 166, 168), "pos": (23, 272),
                                            "template": "2026.{interval}"
                                        },
                                    },
                                    {
                                        "key": "date1",
                                        "prompt": "📅 Дата 1 (пример: 04-23)",
                                        "text_config": {
                                            "font": "sf_pro_semibold", "size": 17.5, "color": (165, 166, 168), "pos": (23, 518),
                                            "template": "2026-{date1} 09:01:04"
                                        },
                                    },
                                    {
                                        "key": "date2",
                                        "prompt": "📅 Дата 2 (пример: 04-23)",
                                        "text_config": {
                                            "font": "sf_pro_semibold", "size": 17.5, "color": (165, 166, 168), "pos": (23, 644),
                                            "template": "2026-{date2} 09:01:04"
                                        },
                                    },
                                    {
                                        "key": "date3",
                                        "prompt": "📅 Дата 3 (пример: 04-23)",
                                        "text_config": {
                                            "font": "sf_pro_semibold", "size": 17.5, "color": (165, 166, 168), "pos": (23, 800),
                                            "template": "2026-{date3} 09:01:04"
                                        },
                                    },
                                    {
                                        "key": "date4",
                                        "prompt": "📅 Дата 4 (пример: 04-23)",
                                        "text_config": {
                                            "font": "sf_pro_semibold", "size": 17.5, "color": (165, 166, 168), "pos": (23, 955),
                                            "template": "2026-{date4} 09:01:04"
                                        },
                                    },
                                    {
                                        "key": "date5",
                                        "prompt": "📅 Дата 5 (пример: 04-23)",
                                        "text_config": {
                                            "font": "sf_pro_semibold", "size": 17.5, "color": (165, 166, 168), "pos": (23, 1085),
                                            "template": "2026-{date5} 09:01:04"
                                        },
                                    },
                                ],
                            },
                        },
                    },
                },
            },
            "check": {
                "label": "🧾 Peru Чек",
                "sections": {
                    "check_main": {
                        "label": "Peru Чек",
                        "items": {
                            "check_pe": {
                                "label": "Peru Чек 1",
                                "asset": "assets/Peru/Чек/Check1.jpg",
                                "fields": [
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 120)",
                                        "text_config": {
                                            "font": "araboto_bold", "size": 93,
                                            "color": (63, 48, 79), "pos": (124, 324),
                                            "format_number_none": True,
                                        },
                                    },
                                    {
                                        "key": "fullname",
                                        "prompt": "✏️ Введите ФИО (пример: Dennis Fabricio Estrada Garcia)",
                                        "text_config": {
                                            "font": "araboto_medium", "size": 36,
                                            "color": (37, 34, 41), "pos": (59, 432),
                                        },
                                    },
                                    {
                                        "key": "date",
                                        "prompt": "📅 Введите дату (пример: 22 abr. 2026)",
                                        "text_config": {
                                            "font": "araboto", "size": 26,
                                            "color": (104, 102, 105), "pos": (96, 487),
                                        },
                                    },
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 04:07 p.m.)",
                                        "text_config": {
                                            "font": "araboto", "size": 26,
                                            "color": (104, 102, 105), "pos": (315, 487),
                                        },
                                    },
                                    {
                                        "key": "account",
                                        "prompt": "🔢 Введите три цифры карты (пример: 266)",
                                        "text_config": {
                                            "font": "araboto", "size": 25,
                                            "color": (37, 34, 41), "pos": (553, 638),
                                        },
                                    },
                                    {
                                        "key": "transaction",
                                        "prompt": "🔢 Введите номер транзакции (пример: 01750451)",
                                        "text_config": {
                                            "font": "araboto", "size": 25,
                                            "color": (37, 34, 41), "pos": (481, 727),
                                        },
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Введите название банка (пример: BCP)",
                                        "text_config": {
                                            "font": "araboto", "size": 26,
                                            "color": (37, 34, 41), "pos": (596, 680),
                                            "align": "right",
                                            "cover_area": (530, 678, 610, 710),
                                            "cover_color": (255, 255, 255),
                                        },
                                    },
                                ],
                            },
                            "check2_pe": {
                                "label": "Peru Чек 2",
                                "asset": "assets/Peru/Чек/Check2.jpg",
                                "fields": [
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 22)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "date",
                                        "prompt": "📅 Введите дату (пример: 22.04.2026)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 09:47) (24-часовой формат)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "fullname",
                                        "prompt": "✏️ ФИО получателя (пример: Dennis Fabricio Estrada G.)",
                                        "text_config": {
                                            "font": "flexo_bold", "size": 33,
                                            "color": (32, 36, 48), "area": (100, 478, 629, 515),
                                            "align": "right",
                                        },
                                    },
                                    {
                                        "key": "card_recipient",
                                        "prompt": "💳 Последние 4 цифры карты получателя (пример: 3899)",
                                        "text_config": {
                                            "font": "flexo_demibold", "size": 32,
                                            "color": (103, 107, 110), "area": (300, 519, 629, 555),
                                            "align": "right",
                                        },
                                    },
                                    {
                                        "key": "card_sender",
                                        "prompt": "💳 Последние 4 цифры карты отправителя (пример: 4013)",
                                        "text_config": {
                                            "font": "flexo_demibold", "size": 32,
                                            "color": (103, 107, 110), "area": (300, 936, 629, 972),
                                            "align": "right",
                                        },
                                    },
                                    {
                                        "key": "operation",
                                        "prompt": "🔢 Номер операции (пример: 01097102)",
                                        "text_config": {
                                            "font": "flexo_bold", "size": 32,
                                            "color": (42, 44, 59), "area": (300, 1046, 629, 1082),
                                            "align": "right",
                                        },
                                    },
                                    {
                                        "key": "_amount_large",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (0, 256, 670, 359),
                                            "line_spacing": 1.0,
                                            "segments_align": "center",
                                            "segments": [
                                                {"text": "S/ {amount}.00", "font": "flexo_medium",
                                                 "size": 87, "color": (7, 41, 138), "format_number": True},
                                            ],
                                        },
                                    },
                                    {
                                        "key": "_datetime",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (0, 366, 670, 453),
                                            "align": "center",
                                            "font": "flexo_medium",
                                            "size": 28,
                                            "color": (106, 110, 113),
                                            "template": "{date} - {time}",
                                        },
                                    },
                                    {
                                        "key": "_amount_total",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (300, 776, 629, 815),
                                            "line_spacing": 1.0,
                                            "segments_align": "right",
                                            "segments": [
                                                {"text": "S/ {amount}.00", "font": "flexo_bold",
                                                 "size": 32, "color": (0, 0, 0), "format_number": True},
                                            ],
                                        },
                                    },
                                ],
                            },
                            "check3_pe": {
                                "label": "Peru Чек 3",
                                "asset": "assets/Peru/Чек/Check3.jpg",
                                "fields": [
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 169)",
                                        "text_config": {
                                            "area": (0, 353, 729, 470),
                                            "line_spacing": 1.0,
                                            "segments_align": "center",
                                            "segments": [
                                                {"text": "S/ ", "font": "geometria_bold", "size": 45, "color": (18, 170, 80)},
                                                {"text": "{amount}", "font": "geometria_bold", "size": 70, "color": (18, 170, 80), "format_number": True},
                                                {"text": ".00", "font": "geometria_bold", "size": 70, "color": (18, 170, 80)},
                                            ],
                                        },
                                    },
                                    {
                                        "key": "fullname",
                                        "prompt": "✏️ Введите ФИО отправителя",
                                        "text_config": {
                                            "font": "geometria_medium", "size": 35,
                                            "color": (19, 24, 27), "pos": (90, 558),
                                        },
                                    },
                                    {
                                        "key": "date",
                                        "prompt": "📅 Введите дату (пример: 19 Abr 2026)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 12:32 PM)",
                                        "text_config": {
                                            "font": "geometria_medium", "size": 35,
                                            "color": (19, 24, 27), "pos": (91, 856),
                                            "template": "{date}   {time}",
                                        },
                                    },
                                    {
                                        "key": "operation",
                                        "prompt": "🔢 Номер операции (пример: 02688276)",
                                        "text_config": {
                                            "font": "geometria_medium", "size": 35,
                                            "color": (19, 24, 27), "pos": (90, 973),
                                        },
                                    },
                                ],
                            },
                            "check4_pe": {
                                "label": "Peru Чек 4",
                                "asset": "assets/Peru/Чек/Check4.jpg",
                                "fields": [
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 22)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "date",
                                        "prompt": "📅 Введите дату (пример: 22.04.2026)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 09:47) (24-часовой формат)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "fullname",
                                        "prompt": "✏️ ФИО получателя (пример: Shumi Claudia Aro C.)",
                                        "text_config": {
                                            "font": "flexo_medium", "size": 22,
                                            "color": (32, 36, 48), "area": (100, 543, 543, 580),
                                            "align": "right",
                                        },
                                    },
                                    {
                                        "key": "card_recipient",
                                        "prompt": "💳 Последние 4 цифры карты получателя (пример: 3899)",
                                        "text_config": {
                                            "font": "flexo_medium", "size": 22,
                                            "color": (103, 107, 110), "area": (250, 571, 543, 607),
                                            "align": "right",
                                        },
                                    },
                                    {
                                        "key": "card_sender",
                                        "prompt": "💳 Последние 4 цифры карты отправителя (пример: 4013)",
                                        "text_config": {
                                            "font": "flexo_medium", "size": 22,
                                            "color": (103, 107, 110), "area": (250, 873, 543, 972),
                                            "align": "right",
                                        },
                                    },
                                    {
                                        "key": "operation",
                                        "prompt": "🔢 Номер операции (пример: 02043395)",
                                        "text_config": {
                                            "font": "flexo_medium", "size": 22,
                                            "color": (42, 44, 59), "area": (250, 956, 543, 1082),
                                            "align": "right",
                                        },
                                    },
                                    {
                                        "key": "_amount_large",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (0, 252, 576, 359),
                                            "line_spacing": 1.0,
                                            "segments_align": "center",
                                            "segments": [
                                                {"text": "S/ {amount}.00", "font": "flexo_medium",
                                                 "size": 65, "color": (7, 41, 138), "format_number": True},
                                            ],
                                        },
                                    },
                                    {
                                        "key": "_datetime",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (0, 343, 576, 453),
                                            "align": "center",
                                            "font": "flexo_medium",
                                            "size": 22,
                                            "color": (106, 110, 113),
                                            "template": "{date} - {time}",
                                        },
                                    },
                                    {
                                        "key": "_amount_total",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (250, 761, 543, 815),
                                            "line_spacing": 1.0,
                                            "segments_align": "right",
                                            "segments": [
                                                {"text": "S/ {amount}.00", "font": "flexo_medium",
                                                 "size": 22, "color": (64, 66, 70), "format_number": True},
                                            ],
                                        },
                                    },
                                ],
                            },
                        },
                    },
                },
            },
            "qr": {
                "label": "📷 Peru QR Code",
                "sections": {
                    "qr_main": {
                        "label": "Peru QR",
                        "items": {
                            "qr_pe": {
                                "label": "Peru QR",
                                "asset": "assets/Peru/QRCode/QR_code1.jpg",
                                "fields": [
                                    {
                                        "key": "expiry_time",
                                        "prompt": "⏱ Введите таймер в формате MM:SS (пример: 59:48)",
                                        "text_config": {
                                            "font": "montserrat_bold",
                                            "size": 80,
                                            "color": (39, 39, 39),
                                            "area": (0, 645, 1284, 792),
                                            "align": "center",
                                        },
                                    },
                                    {
                                        "key": "qr_image",
                                        "prompt": "🖼 Отправьте QR-изображение (квадрат 1:1)",
                                        "text_config": {
                                            "image_paste": True,
                                            "area": (318, 815, 972, 1469),
                                        },
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Введите название банка",
                                        "text_config": {
                                            "font": "montserrat_medium",
                                            "size": 70,
                                            "color": (42, 46, 48),
                                            "pos": (313, 1586),
                                        },
                                    },
                                    {
                                        "key": "fullname",
                                        "prompt": "👤 Введите ФИО пользователя",
                                        "text_config": {
                                            "font": "montserrat_medium",
                                            "size": 70,
                                            "color": (42, 46, 48),
                                            "pos": (313, 1751),
                                        },
                                    },
                                    {
                                        "key": "account",
                                        "prompt": "🔢 Введите номер счета",
                                        "text_config": {
                                            "font": "montserrat_medium",
                                            "size": 70,
                                            "color": (42, 46, 48),
                                            "pos": (313, 1925),
                                        },
                                    },
                                    {
                                        "key": "phone",
                                        "prompt": "📞 Введите номер телефона",
                                        "text_config": {
                                            "font": "montserrat_medium",
                                            "size": 70,
                                            "color": (42, 46, 48),
                                            "pos": (313, 2106),
                                        },
                                    },
                                ],
                            },
                        },
                    },
                },
            },
            "support": {
                "label": "💬 Peru SUPPORT",
                "sections": {
                    "support_main": {
                        "label": "Peru SUPPORT",
                        "items": {
                            "support_pe": {
                                "label": "Peru Support",
                                "asset": "assets/Peru/SUPPORT/SUPPORT.jpg",
                                "fields": [
                                    {
                                        "key": "msg1",
                                        "prompt": "✉️ Введите текст первого сообщения (синий пузырь, справа)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "msg2",
                                        "prompt": "✉️ Введите текст второго сообщения (тёмный пузырь, слева)",
                                        "text_config": {"collect_only": True},
                                    },
                                ],
                                "render_mode": "support_bubbles",
                            },
                        },
                    },
                },
            },
            "rocket": {
                "label": "🚀 Peru ROCKET",
                "sections": {
                    "rocket_main": {
                        "label": "Peru ROCKET",
                        "items": {
                            "rocket1_pe": {
                                "label": "Peru ROCKET",
                                "asset": "assets/Peru/ROCKET/ROCKET.jpg",
                                "fields": [
                                    {
                                        "key": "currency",
                                        "prompt": "💰 Введите валюту (пример: ETH)",
                                        "text_config": {
                                            "font": "roboto_cond_med",
                                            "size": 70,
                                            "color": (251, 251, 251),
                                            "pos": (370, 800),
                                            "anchor": "ls",
                                            "template": "{currency}USDT | Sin límite de tiempo"
                                        }
                                    },
                                    {
                                        "key": "long_short",
                                        "prompt": "📈 Введите Long/Short",
                                        "text_config": {
                                            "font": "roboto_cond_reg",
                                            "size": 60,
                                            "pos": (370, 883),
                                            "anchor": "ls",
                                            "color_eval": "lambda v: (95, 166, 106) if v.lower() == 'long' else (212, 72, 92)"
                                        }
                                    },
                                    {
                                        "key": "x_amount",
                                        "prompt": "✖️ Введите количество X-са (пример: 100X)",
                                        "text_config": {
                                            "font": "roboto_cond_reg",
                                            "size": 60,
                                            "color": (118, 119, 123),
                                            "pos": (600, 883),
                                            "anchor": "ls",
                                            "template_eval": "lambda v: str(v).upper().rstrip('X').strip() + 'X'"
                                        }
                                    },
                                    {
                                        "key": "percentage",
                                    "prompt": "📈 Введите процент (пример: +1,044.86)",
                                    "text_config": {
                                        "font": "roboto_cond_semibold",
                                        "size": 159,
                                            "pos": (370, 1057),
                                            "anchor": "ls",
                                            "color_eval": "lambda v: (95, 166, 106) if str(v).startswith('+') else (212, 72, 92)",
                                            "template": "{percentage}%",
                                            "special_number_sizes": 79
                                        }
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 18,045 или -18,045)",
                                        "text_config": {
                                            "font": "roboto_cond_med",
                                            "size": 80,
                                            "color": (95, 166, 106, 153),
                                            "color_eval": "lambda v: (212, 72, 92, 153) if str(v).startswith('-') else (95, 166, 106, 153)",
                                            "pos": (370, 1182),
                                            "anchor": "ls",
                                            "template_eval": "lambda v: ('-S/. ' if str(v).startswith('-') else '+S/. ') + _format_number_comma(str(v)).lstrip('-').lstrip()",
                                            "special_number_sizes": 70,
                                            "space_size": 40
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            },
        },
    },

    # ════════════════════════════════════════════════════════
    # Uruguay 🇺🇾
    # ════════════════════════════════════════════════════════
    "uy": {
        "label": "🇺🇾 Uruguay",
        "catalog": {
            "fd": { "label": "📁 Uruguay FD", "sections": {} },
            "rd": {
                "label": "📁 Uruguay RD",
                "sections": {
                    "rd_main": {
                        "items": {
                            "rd1_uy": {
                                "asset": "assets/Uruguay/RD/rd1.png",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Фамилия Имя (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "area": (1250, 700, 2780, 925),
                                            "line_spacing": 1.25,
                                            "segments": [
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat",
                                                    "size": 45,
                                                    "text": "Su pago al cliente ",
                                                },
                                                {"color": (255, 255, 255), "font": "montserrat", "size": 45, "text": "{name}"},
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat",
                                                    "size": 45,
                                                    "text": " por un monto de ",
                                                },
                                                {
                                                    "color": (0, 255, 84),
                                                    "font": "montserrat",
                                                    "size": 45,
                                                    "text": "$U 168,286",
                                                },
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat",
                                                    "size": 45,
                                                    "text": " ha sido bloqueado temporalmente. Para retirar los fondos de la "
                                                    "plataforma a la cuenta del beneficiario, su cliente está obligado a "
                                                    "pagar una tarifa de ",
                                                },
                                                {
                                                    "color": (255, 0, 0),
                                                    "font": "montserrat",
                                                    "format_number_comma": True,
                                                    "size": 45,
                                                    "text": "$U {commission}.",
                                                },
                                            ],
                                        },
                                    },
                                    {
                                        "key": "commission",
                                        "prompt": "💰 Введите сумму (рекомендуется 6720)",
                                        "text_config": {"collect_only": True},
                                    },
                                ],
                                "label": "Uruguay RD 1",
                                "preview": "assets/Uruguay/Preview/RD/RD1_prew.jpg",
                            },
                            "rd2_uy": {
                                "asset": "assets/Uruguay/RD/rd2.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Фамилия Имя (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "area": (2235, 1420, 3050, 1460),
                                            "color": (57, 62, 67),
                                            "font": "montserrat",
                                            "line_spacing": 1.2,
                                            "size": 30,
                                            "template": "Cuenta bancaria del cliente {name}.",
                                        },
                                    },
                                    {"key": "amount", "prompt": "💰 Введите сумму (рекомендуется 10920)", "text_config": {"collect_only": True}},
                                    {
                                        "key": "_body_line1",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (2240, 490, 2992, 540),
                                            "segments": [
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat_light",
                                                    "size": 44,
                                                    "text": "Es necesario pagar una tarifa por la",
                                                }
                                            ],
                                        },
                                    },
                                    {
                                        "key": "_body_line2",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (2240, 537, 2992, 587),
                                            "segments": [
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat_light",
                                                    "size": 44,
                                                    "text": "conversión de ",
                                                },
                                                {
                                                    "color": (136, 255, 164),
                                                    "font": "montserrat_medium",
                                                    "size": 44,
                                                    "text": "USDT",
                                                },
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat_light",
                                                    "size": 44,
                                                    "text": " a ",
                                                },
                                                {
                                                    "color": (254, 68, 92),
                                                    "font": "montserrat_medium",
                                                    "size": 44,
                                                    "text": "UYU.",
                                                },
                                            ],
                                        },
                                    },
                                    {
                                        "key": "_body_line3",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (2240, 615, 2992, 665),
                                            "segments": [
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat_light",
                                                    "size": 44,
                                                    "text": "Importe de la tarifa: ",
                                                },
                                                {
                                                    "color": (255, 13, 13),
                                                    "font": "montserrat_medium",
                                                    "format_number_comma": True,
                                                    "size": 44,
                                                    "text": "$U {amount}",
                                                },
                                                {"color": (255, 255, 255), "font": "montserrat_light", "size": 44, "text": "."},
                                            ],
                                        },
                                    },
                                ],
                                "label": "Uruguay RD 2",
                                "preview": "assets/Uruguay/Preview/RD/RD2_prew.jpg",
                            },
                            "rd3_uy": {
                                "asset": "assets/Uruguay/RD/rd3.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Nilda Mamani Apaza)",
                                        "text_config": {
                                            "color": (0, 0, 0),
                                            "font": "times_bold",
                                            "pos": (68, 474),
                                            "size": 59,
                                            "template": "Notificación para {name}",
                                        },
                                    },
                                    {
                                        "key": "gender",
                                        "prompt": "👤 Выберите пол (введите 'o' для мужского, 'a' для женского):",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 13860)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "_greeting",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (69, 1230, 2412, 1350),
                                            "segments": [
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 59,
                                                    "text": "Estimad{gender} ",
                                                },
                                                {"color": (0, 0, 0), "font": "times_bold", "size": 59, "text": "{name}:"},
                                            ],
                                        },
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (70, 1663, 2414, 2200),
                                            "line_spacing": 0.76,
                                            "segments": [
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 60,
                                                    "text": "Le informamos acerca de una condición importante relacionada con la "
                                                    "retirada de fondos a\n"
                                                    "la cuenta bancaria que usted indicó. El pago estará disponible "
                                                    "únicamente después de\n"
                                                    "realizar el abono por servicios por un importe de ",
                                                },
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_bold",
                                                    "format_number": True,
                                                    "size": 60,
                                                    "text": "$U {amount}",
                                                },
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 60,
                                                    "text": ". Le rogamos efectuar dicho\n"
                                                    "pago a la mayor brevedad; tras su confirmación y el procesamiento por "
                                                    "parte de nuestros\n"
                                                    "departamentos, recibirá inmediatamente en su cuenta bancaria la suma "
                                                    "total de ",
                                                },
                                                {"color": (0, 0, 0), "font": "times_bold", "size": 60, "text": "$U 168 286"},
                                                {"color": (0, 0, 0), "font": "times_roman", "size": 60, "text": "."},
                                            ],
                                        },
                                    },
                                ],
                                "label": "Uruguay RD 3",
                            },
                            "rd4_uy": {
                                "asset": "assets/Uruguay/RD/rd4.jpg",
                                "fields": [
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 10:00) (24-часовой формат)",
                                        "text_config": {
                                            "area": (115, 39, 243, 60),
                                            "color": (82, 82, 82),
                                            "font": "sf_pro_bold",
                                            "size": 34,
                                        },
                                    },
                                    {"key": "name", "prompt": "✏️ Введите Фамилия Имя", "text_config": {"collect_only": True}},
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 7980)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (84, 758, 743, 1022),
                                            "blank_line_size": 14,
                                            "line_spacing": 1.2,
                                            "segments": [
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "sf_pro",
                                                    "size": 30,
                                                    "text": "Para una ejecución exitosa y segura del pago a su cliente ",
                                                },
                                                {"color": (255, 255, 255), "font": "sf_pro", "size": 30, "text": "{name}"},
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "sf_pro",
                                                    "size": 30,
                                                    "text": ", es necesario que abone el proceso de segregación por un monto de ",
                                                },
                                                {
                                                    "color": (255, 0, 0),
                                                    "font": "sf_pro",
                                                    "format_number_dot": True,
                                                    "size": 30,
                                                    "text": "$U {amount}.",
                                                },
                                                {"color": (255, 255, 255), "font": "sf_pro", "size": 30, "text": "\n\n"},
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "sf_pro",
                                                    "size": 30,
                                                    "text": "Una vez abonada la segregación, todo el dinero se acreditará "
                                                    "automáticamente en la cuenta de su cliente.",
                                                },
                                            ],
                                        },
                                    },
                                ],
                                "label": "Uruguay RD 4",
                                "preview": "assets/Uruguay/Preview/RD/RD4_prew.jpg",
                            },
                            "rd5_uy": {
                                "asset": "assets/Uruguay/RD/rd5.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Nilda Mamani Apaza)",
                                        "text_config": {
                                            "color": (0, 0, 0),
                                            "font": "times_bold",
                                            "pos": (68, 474),
                                            "size": 59,
                                            "template": "Notificación para {name}",
                                        },
                                    },
                                    {
                                        "key": "gender",
                                        "prompt": "👤 Выберите пол (введите 'o' для мужского, 'a' для женского):",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 23520)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "_greeting",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (69, 1230, 2412, 1350),
                                            "segments": [
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 59,
                                                    "text": "Estimad{gender} ",
                                                },
                                                {"color": (0, 0, 0), "font": "times_bold", "size": 59, "text": "{name}:"},
                                            ],
                                        },
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (70, 1747, 2414, 2200),
                                            "line_spacing": 1.45,
                                            "segments": [
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 60,
                                                    "text": "En el sistema figura un pago pendiente por concepto de prima de seguro "
                                                    "por ",
                                                },
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_bold",
                                                    "format_number": True,
                                                    "size": 60,
                                                    "text": "$U {amount}",
                                                },
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 60,
                                                    "text": ", necesario para activar las garantías y el acceso completo a las "
                                                    "funciones de protección. Le rogamos efectuar dicho pago a través de "
                                                    "los métodos de recarga disponibles. Tras la confirmación del pago, se "
                                                    "restaurará el acceso a los retiros y podrá iniciar la transferencia "
                                                    "del monto total de ",
                                                },
                                                {"color": (0, 0, 0), "font": "times_bold", "size": 60, "text": "$U 169 286"},
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 60,
                                                    "text": " a la cuenta bancaria indicada.",
                                                },
                                            ],
                                        },
                                    },
                                ],
                                "label": "Uruguay RD 5",
                            },
                            "rd6_uy": {
                                "asset": "assets/Uruguay/RD/rd6.jpg",
                                "fields": [
                                    {
                                        "key": "date",
                                        "prompt": "📅 Дата 1 (пример: Fr 01/01)",
                                        "text_config": {
                                            "area": (540, 210, 613, 222),
                                            "color": (44, 44, 44),
                                            "font": "opensans",
                                            "size": 14,
                                        },
                                    },
                                    {
                                        "key": "date2",
                                        "prompt": "📅 Дата 2 (пример: Fr 01/01/2026)",
                                        "text_config": {
                                            "area": (1730, 236, 1845, 247),
                                            "color": (147, 147, 147),
                                            "font": "opensans",
                                            "size": 14,
                                        },
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Название банка (пример: Yane)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "tx_time",
                                        "prompt": "🕐 Время транзакции (пример: 10:00)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО клиента (пример: Ivan Ivanov Ivanovich)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "commission",
                                        "prompt": "💰 Введите сумму (рекомендуется 33600)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (655, 485, 1620, 860),
                                            "blank_line_size": 10,
                                            "line_spacing": 1.25,
                                            "segments": [
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial_bold",
                                                    "size": 20,
                                                    "text": "Estimado José García!",
                                                },
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "Ha realizado un intercambio de USDT por un monto de ",
                                                },
                                                {"color": (44, 44, 44), "font": "arial_bold", "size": 20, "text": "U$ 168,286"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": " para el pago a su cliente.",
                                                },
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "Detalles de la transacción:",
                                                },
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "  ID de la transacción: ",
                                                },
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial_bold",
                                                    "size": 20,
                                                    "text": "9489-4921-3991-002",
                                                },
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "  Banco del destinatario: ",
                                                },
                                                {"color": (44, 44, 44), "font": "arial_bold", "size": 20, "text": "{bank}"},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "  Monto a recibir: ",
                                                },
                                                {"color": (44, 44, 44), "font": "arial_bold", "size": 20, "text": "U$ 168,286"},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "  Monto en USDT: ",
                                                },
                                                {"color": (44, 44, 44), "font": "arial_bold", "size": 20, "text": "4,089"},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "  Hora de la transacción: ",
                                                },
                                                {"color": (44, 44, 44), "font": "arial_bold", "size": 20, "text": "{tx_time}"},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n\n"},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "Su cliente, "},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "{name}"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": ", está obligado a pagar el 7% de impuesto sobre el intercambio de "
                                                    "criptomonedas, es decir, ",
                                                },
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial_bold",
                                                    "format_number_dot": True,
                                                    "size": 20,
                                                    "text": "$U {commission}.",
                                                },
                                            ],
                                        },
                                    },
                                ],
                                "label": "Uruguay RD 6",
                                "preview": "assets/Uruguay/Preview/RD/RD6_prew.jpg",
                            },
                            "rd7_uy": {
                                "asset": "assets/Uruguay/RD/rd7.jpg",
                                "fields": [
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 10:00) (24-часовой формат)",
                                        "text_config": {
                                            "area": (100, 33, 200, 67),
                                            "color": (255, 255, 255),
                                            "font": "sf_pro_bold",
                                            "size": 32,
                                        },
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Введите название банка (пример: YAPE)",
                                        "text_config": {
                                            "area": (398, 850, 710, 880),
                                            "color": (0, 0, 0),
                                            "font": "sf_pro_medium",
                                            "size": 29,
                                        },
                                    },
                                    {
                                        "key": "fullname",
                                        "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan Ivanovich)",
                                        "text_config": {
                                            "area": (398, 913, 710, 944),
                                            "color": (0, 0, 0),
                                            "font": "sf_pro_medium",
                                            "size": 29,
                                        },
                                    },
                                    {
                                        "key": "number",
                                        "prompt": "🔢 Введите номер счёта (пример: 1234567890)",
                                        "text_config": {
                                            "area": (398, 994, 663, 1025),
                                            "color": (0, 0, 0),
                                            "font": "sf_pro_medium",
                                            "size": 29,
                                        },
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 29400)",
                                        "text_config": {
                                            "area": (395, 1206, 710, 1242),
                                            "color": (0, 0, 0),
                                            "font": "sf_pro_medium",
                                            "format_number_comma": True,
                                            "size": 29,
                                            "template": "$U {amount}",
                                        },
                                    },
                                ],
                                "label": "Uruguay RD 7",
                                "preview": "assets/Uruguay/Preview/RD/RD7_prew.jpg",
                            },
                        },
                        "label": "Uruguay RD",
                    }
                },
            },
            "check": {
                "label": "🧾 Uruguay Чек",
                "sections": {
                    "check_main": {
                        "label": "Uruguay Чеки",
                        "items": {
                            "check1_uy": {
                                "label": "🧾 Чек 1",
                                "asset": "assets/Uruguay/Чек/Check1.jpg",
                                "preview": "assets/Uruguay/Preview/Чек/Check1_prew.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Имя",
                                        "text_config": {
                                            "font": "alte_regular", "size": 19, "color": (46, 49, 54),
                                            "pos": (92, 67), "align": "left",
                                            "template_eval": "lambda v: f'Transferiste a {str(v).upper()}'"
                                        }
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 1950)",
                                        "text_config": {
                                            "font": "alte_bold", "size": 40, "color": (54, 57, 74),
                                            "pos": (122, 97), "align": "left",
                                            "template": "{amount},00",
                                            "format_number_dot": True
                                        }
                                    },
                                    {
                                        "key": "date",
                                        "prompt": "📅 Введите дату (пример: 20.04.2026)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 12:20) (24-часовой формат)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "datetime_display",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "alte_regular", "size": 19, "color": (171, 171, 179),
                                            "pos": (92, 145), "align": "left",
                                            "template": "{date} {time}"
                                        }
                                    },
                                    {
                                        "key": "comment",
                                        "prompt": "💬 Введите комментарий (пример: PAGO)",
                                        "text_config": {
                                            "font": "arial_italic", "size": 19, "color": (57, 56, 68),
                                            "pos": (107, 225), "align": "left"
                                        }
                                    },
                                    {
                                        "key": "acc_1",
                                        "prompt": "🔢 Введите Номер счета 1",
                                        "text_config": {
                                            "font": "alte_regular", "size": 21, "color": (34, 37, 44),
                                            "pos": (504, 342), "align": "right"
                                        }
                                    },
                                    {
                                        "key": "payer_1",
                                        "prompt": "👤 Введите имя плательщика 1",
                                        "text_config": {
                                            "font": "alte_regular", "size": 21, "color": (34, 37, 44),
                                            "pos": (503, 373), "align": "right",
                                            "template_eval": "lambda v: str(v).upper()"
                                        }
                                    },
                                    {
                                        "key": "service",
                                        "prompt": "🔧 Введите Сервис (пример: MIDINERO)",
                                        "text_config": {
                                            "font": "alte_bold", "size": 21.5, "color": (32, 36, 56),
                                            "pos": (503, 434), "align": "right"
                                        }
                                    },
                                    {
                                        "key": "acc_2",
                                        "prompt": "🔢 Введите Номер счета 2",
                                        "text_config": {
                                            "font": "alte_regular", "size": 21, "color": (34, 37, 44),
                                            "pos": (504, 483), "align": "right"
                                        }
                                    },
                                    {
                                        "key": "payer_2",
                                        "prompt": "👤 Введите имя плательщика 2",
                                        "text_config": {
                                            "font": "alte_regular", "size": 21, "color": (34, 37, 44),
                                            "pos": (503, 514), "align": "right",
                                            "template_eval": "lambda v: str(v).upper()"
                                        }
                                    },
                                    {
                                        "key": "ref_num",
                                        "prompt": "📄 Введите Справочный номер",
                                        "text_config": {
                                            "font": "alte_regular", "size": 21, "color": (34, 37, 44),
                                            "pos": (499, 634), "align": "right"
                                        }
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "alte_regular", "size": 21, "color": (34, 37, 44),
                                            "pos": (503, 769), "align": "right",
                                            "template": "$ {amount},00",
                                            "format_number_dot": True
                                        }
                                    }
                                ]
                            },
                            "check2_uy": {
                                "label": "🧾 Чек 2",
                                "asset": "assets/Uruguay/Чек/Check2.jpg",
                                "preview": "assets/Uruguay/Preview/Чек/Check2_prew.jpg",
                                "fields": [
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 123456)",
                                        "text_config": {
                                            "font": "sf_pro_text_bold", "size": 54, "color": (47, 47, 47),
                                            "pos": (385, 189), "align": "center",
                                            "template": "{amount},00",
                                            "format_number_dot": True,
                                            "prefix": "UYU",
                                            "prefix_size": 37,
                                            "prefix_y_offset": 10
                                        }
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "sf_pro_text_bold", "size": 24, "color": (8, 8, 8),
                                            "pos": (725, 870), "align": "right",
                                            "template": "UYU {amount}.0"
                                        }
                                    },
                                    {
                                        "key": "sender_acc",
                                        "prompt": "🔢 Введите Номер отправителя (10 цифр)",
                                        "text_config": {
                                            "font": "sf_pro_text_bold", "size": 28, "color": (8, 8, 8),
                                            "pos": (385, 351), "align": "center",
                                            "template": "CA UYU {sender_acc}"
                                        }
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Введите Банк (пример: Itaú)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "receiver_acc",
                                        "prompt": "🔢 Введите Номер получателя (7 цифр)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "_bank_acc",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "sf_pro_text_bold", "size": 28, "color": (8, 8, 8),
                                            "pos": (385, 451), "align": "center",
                                            "template": "{bank} {receiver_acc}"
                                        }
                                    },
                                    {
                                        "key": "name",
                                        "prompt": "👤 Введите получателя (пример: CARD BUE WILF)",
                                        "text_config": {
                                            "font": "sf_pro_text_bold", "size": 28, "color": (48, 52, 52),
                                            "pos": (304, 539), "align": "left",
                                            "template_eval": "lambda v: ' '.join(w[:len(w)//2] + '*' * (len(w) - len(w)//2) if len(w) > 1 else w for w in str(v).upper().split())"
                                        }
                                    },
                                    {
                                        "key": "date",
                                        "prompt": "📅 Введите дату (пример: 04.01.2026)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 15:23) (24-часовой формат)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "_datetime",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "sf_pro_text_bold", "size": 24, "color": (8, 8, 8),
                                            "pos": (725, 647), "align": "right",
                                            "template": "{date} {time}"
                                        }
                                    },
                                    {
                                        "key": "account",
                                        "prompt": "🔢 Введите Ссылку",
                                        "text_config": {
                                            "font": "sf_pro_text_bold", "size": 24, "color": (8, 8, 8),
                                            "pos": (725, 795), "align": "right"
                                        }
                                    }
                                ]
                            },
                            "check3_uy": {
                                "label": "🧾 Чек 3",
                                "asset": "assets/Uruguay/Чек/Check3.jpg",
                                "preview": "assets/Uruguay/Preview/Чек/Check3_prew.jpg",
                                "fields": [
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 15:23) (24-часовой формат)",
                                        "text_config": {
                                            "font": "sf_pro_text_bold", "size": 40, "color": (8, 8, 8),
                                            "pos": (93, 38), "align": "left"
                                        }
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 1700)",
                                        "text_config": {
                                            "font": "nunito_bold", "size": 62, "color": (40, 42, 59),
                                            "pos": (461, 718), "align": "center",
                                            "template": "Enviaste UYU {amount},00",
                                            "format_number_dot": True,
                                            "stroke_width": 1,
                                            "stroke_fill": (40, 42, 59)
                                        }
                                    },
                                    {
                                        "key": "receiver_name",
                                        "prompt": "👤 Введите получателя (пример: VIGN FERR AYR)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Выберите банк:",
                                        "text_config": {
                                            "collect_only": True
                                        },
                                        "options": [
                                            {"text": "Itaú", "value": "Itaú"},
                                            {"text": "Santander", "value": "Santander"},
                                            {"text": "BBVA", "value": "BBVA"},
                                            {"text": "Scotiabank", "value": "Scotiabank"},
                                            {"text": "Oca blue", "value": "Oca blue"}
                                        ]
                                    },
                                    {
                                        "key": "_info_text",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "nunito_medium", "size": 35, "color": (43, 43, 52),
                                            "pos": (461, 839), "align": "center",
                                            "line_spacing": 1.2,
                                            "template_eval": "lambda v, fv: f\"{ ' '.join(w + '*' * (3 if i==0 else 4 if i==1 else 3) for i, w in enumerate(str(fv.get('receiver_name','')).upper().split())) } recibe el dinero en\\nsu cuenta {fv.get('bank','')}.\\nSi querés podés compartirle el comprobante.\"",
                                            "template": "{_info_text}"
                                        }
                                    },
                                    {
                                        "key": "network",
                                        "prompt": "📶 Сеть",
                                        "text_config": {
                                            "image_paste": True,
                                            "area": (673, 44, 721, 77)
                                        }
                                    },
                                    {
                                        "key": "wifi",
                                        "prompt": "🌐 Интернет",
                                        "text_config": {
                                            "image_paste": True,
                                            "area": (738, 46, 778, 77)
                                        }
                                    },
                                    {
                                        "key": "battery",
                                        "prompt": "🔋 Зарядка",
                                        "text_config": {
                                            "image_paste": True,
                                            "area": (794, 45, 861, 78)
                                        }
                                    }
                                ]
                            },
                            "check4_uy": {
                                "label": "🧾 Чек 4",
                                "asset": "assets/Uruguay/Чек/Check4.jpg",
                                "preview": "assets/Uruguay/Preview/Чек/Check4_prew.jpg",
                                "fields": [
                                    {
                                        "key": "sender_name",
                                        "prompt": "👤 Имя отправителя",
                                        "text_config": {
                                            "font": "montserrat_medium", "size": 27, "color": (35, 53, 65),
                                            "pos": (836, 535), "align": "right"
                                        }
                                    },
                                    {
                                        "key": "account",
                                        "prompt": "💳 Счет списания",
                                        "text_config": {
                                            "font": "sf_pro_medium", "size": 28, "color": (106, 115, 126),
                                            "pos": (835, 590), "align": "right",
                                            "template": "{account} ($)"
                                        }
                                    },
                                    {
                                        "key": "receiver_name",
                                        "prompt": "👤 Имя получателя",
                                        "text_config": {
                                            "font": "montserrat_medium", "size": 27, "color": (35, 53, 65),
                                            "pos": (835, 684), "align": "right"
                                        }
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Банк",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "_bank_text",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "sf_pro_medium", "size": 28, "color": (106, 115, 126),
                                            "pos": (835, 738), "align": "right",
                                            "template_eval": "lambda v, fv: fv.get('account', '') if fv.get('bank') == 'Oca Blue' else f\"{fv.get('bank', '')} {fv.get('account', '')}\""
                                        }
                                    },
                                    {
                                        "key": "_bank_img",
                                        "prompt": "",
                                        "text_config": {
                                            "image_paste": True,
                                            "area": (596, 735, 707, 774),
                                            "image_eval": "lambda v, fv: 'assets/Uruguay/Чек/bank/Oca.jpg' if fv.get('bank') == 'Oca Blue' else None"
                                        }
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Сумма перевода (пример: 6424)",
                                        "text_config": {
                                            "font": "sf_pro", "size": 37, "color": (35, 53, 65),
                                            "pos": (835, 851), "align": "right",
                                            "template": "$ {amount},00",
                                            "format_number_dot": True
                                        }
                                    },
                                    {
                                        "key": "date",
                                        "prompt": "📅 Дата (пример: 18.11.2025)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Время (пример: 03:19)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "_date_time",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "sf_pro_medium", "size": 28, "color": (97, 106, 116),
                                            "pos": (62, 1304), "align": "left",
                                            "template_eval": "lambda v, fv: 'Realizada el ' + fv.get('date', '').split('.')[0] + ' ' + {'01':'enero','02':'febrero','03':'marzo','04':'abril','05':'mayo','06':'junio','07':'julio','08':'agosto','09':'septiembre','10':'octubre','11':'noviembre','12':'diciembre'}.get(fv.get('date', '').split('.')[1] if '.' in fv.get('date', '') else '', '') + '. ' + fv.get('date', '').split('.')[-1] + ' a las ' + fv.get('time', '').lower()"
                                        }
                                    },
                                    {
                                        "key": "_amount_2",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "sf_pro", "size": 37, "color": (35, 53, 65),
                                            "pos": (835, 999), "align": "right",
                                            "template": "$ {amount},00",
                                            "format_number_dot": True
                                        }
                                    },
                                    {
                                        "key": "acc_2",
                                        "prompt": "🔢 Номер счета",
                                        "text_config": {
                                            "font": "sf_pro", "size": 37, "color": (35, 53, 65),
                                            "pos": (835, 1442), "align": "right"
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            "qr": { "label": "📱 Uruguay QR", "sections": {} },
            "support": { "label": "🎧 Uruguay Поддержка", "sections": {} },
            "rocket": {
                "label": "🚀 Uruguay ROCKET",
                "sections": {
                    "rocket_main": {
                        "label": "Uruguay ROCKET",
                        "items": {
                            "rocket1_uy": {
                                "label": "Uruguay ROCKET",
                                "asset": "assets/Uruguay/ROCKET/ROCKET.jpg",
                                "fields": [
                                    {
                                        "key": "currency",
                                        "prompt": "💰 Введите валюту (пример: ETH)",
                                        "text_config": {
                                            "font": "roboto_cond_med",
                                            "size": 70,
                                            "color": (251, 251, 251),
                                            "pos": (370, 800),
                                            "anchor": "ls",
                                            "template": "{currency}USDT | Sin límite de tiempo"
                                        }
                                    },
                                    {
                                        "key": "long_short",
                                        "prompt": "📈 Введите Long/Short",
                                        "text_config": {
                                            "font": "roboto_cond_reg",
                                            "size": 60,
                                            "pos": (370, 883),
                                            "anchor": "ls",
                                            "color_eval": "lambda v: (95, 166, 106) if v.lower() == 'long' else (212, 72, 92)"
                                        }
                                    },
                                    {
                                        "key": "x_amount",
                                        "prompt": "✖️ Введите количество X-са (пример: 100X)",
                                        "text_config": {
                                            "font": "roboto_cond_reg",
                                            "size": 60,
                                            "color": (118, 119, 123),
                                            "pos": (600, 883),
                                            "anchor": "ls",
                                            "template_eval": "lambda v: str(v).upper().rstrip('X').strip() + 'X'"
                                        }
                                    },
                                    {
                                        "key": "percentage",
                                        "prompt": "📈 Введите процент (пример: +1,044.86)",
                                        "text_config": {
                                            "font": "roboto_cond_semibold",
                                            "size": 159,
                                            "pos": (370, 1057),
                                            "anchor": "ls",
                                            "color_eval": "lambda v: (95, 166, 106) if str(v).startswith('+') else (212, 72, 92)",
                                            "template": "{percentage}%",
                                            "special_number_sizes": 79
                                        }
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 18,045 или -18,045)",
                                        "text_config": {
                                            "font": "roboto_cond_med",
                                            "size": 80,
                                            "color": (95, 166, 106, 153),
                                            "color_eval": "lambda v: (212, 72, 92, 153) if str(v).startswith('-') else (95, 166, 106, 153)",
                                            "pos": (370, 1182),
                                            "anchor": "ls",
                                            "template_eval": "lambda v: ('-$U ' if str(v).startswith('-') else '+$U ') + _format_number_comma(str(v)).lstrip('-').lstrip()",
                                            "special_number_sizes": 70,
                                            "space_size": 40
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            "fire": { "label": "🔥 Uruguay FIRE", "sections": {} },
        },
    },

    # ════════════════════════════════════════════════════════
    # Paraguay 🇵🇾
    # ════════════════════════════════════════════════════════
    "py": {
        "label": "🇵🇾 Paraguay",
        "catalog": {
            "fd": { "label": "📁 Paraguay FD", "sections": {} },
            "rd": {
                "label": "📁 Paraguay RD",
                "sections": {
                    "rd_main": {
                        "items": {
                            "rd1_py": {
                                "asset": "assets/Paraguay/RD/rd1.png",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Фамилия Имя (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "area": (1250, 700, 2780, 925),
                                            "line_spacing": 1.25,
                                            "segments": [
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat",
                                                    "size": 45,
                                                    "text": "Su pago al cliente ",
                                                },
                                                {"color": (255, 255, 255), "font": "montserrat", "size": 45, "text": "{name}"},
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat",
                                                    "size": 45,
                                                    "text": " por un monto de ",
                                                },
                                                {
                                                    "color": (0, 255, 84),
                                                    "font": "montserrat",
                                                    "size": 45,
                                                    "text": "Gs. 24,951,100",
                                                },
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat",
                                                    "size": 45,
                                                    "text": " ha sido bloqueado temporalmente. Para retirar los fondos de la "
                                                    "plataforma a la cuenta del beneficiario, su cliente está obligado a "
                                                    "pagar una tarifa de ",
                                                },
                                                {
                                                    "color": (255, 0, 0),
                                                    "font": "montserrat",
                                                    "format_number_comma": True,
                                                    "size": 45,
                                                    "text": "Gs. {commission}.",
                                                },
                                            ],
                                        },
                                    },
                                    {
                                        "key": "commission",
                                        "prompt": "💰 Введите сумму (рекомендуется 980000)",
                                        "text_config": {"collect_only": True},
                                    },
                                ],
                                "label": "Paraguay RD 1",
                                "preview": "assets/Paraguay/Preview/RD/RD1_prew.jpg",
                            },
                            "rd2_py": {
                                "asset": "assets/Paraguay/RD/rd2.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Фамилия Имя (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "area": (2235, 1420, 3050, 1460),
                                            "color": (57, 62, 67),
                                            "font": "montserrat",
                                            "line_spacing": 1.2,
                                            "size": 30,
                                            "template": "Cuenta bancaria del cliente {name}.",
                                        },
                                    },
                                    {"key": "amount", "prompt": "💰 Введите сумму (рекомендуется 1560000)", "text_config": {"collect_only": True}},
                                    {
                                        "key": "_body_line1",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (2240, 490, 2992, 540),
                                            "segments": [
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat_light",
                                                    "size": 44,
                                                    "text": "Es necesario pagar una tarifa por la",
                                                }
                                            ],
                                        },
                                    },
                                    {
                                        "key": "_body_line2",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (2240, 537, 2992, 587),
                                            "segments": [
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat_light",
                                                    "size": 44,
                                                    "text": "conversión de ",
                                                },
                                                {
                                                    "color": (136, 255, 164),
                                                    "font": "montserrat_medium",
                                                    "size": 44,
                                                    "text": "USDT",
                                                },
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat_light",
                                                    "size": 44,
                                                    "text": " a ",
                                                },
                                                {
                                                    "color": (254, 68, 92),
                                                    "font": "montserrat_medium",
                                                    "size": 44,
                                                    "text": "PYG.",
                                                },
                                            ],
                                        },
                                    },
                                    {
                                        "key": "_body_line3",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (2240, 615, 2992, 665),
                                            "segments": [
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "montserrat_light",
                                                    "size": 44,
                                                    "text": "Importe de la tarifa: ",
                                                },
                                                {
                                                    "color": (255, 13, 13),
                                                    "font": "montserrat_medium",
                                                    "format_number_comma": True,
                                                    "size": 44,
                                                    "text": "Gs. {amount}",
                                                },
                                                {"color": (255, 255, 255), "font": "montserrat_light", "size": 44, "text": "."},
                                            ],
                                        },
                                    },
                                ],
                                "label": "Paraguay RD 2",
                                "preview": "assets/Paraguay/Preview/RD/RD2_prew.jpg",
                            },
                            "rd3_py": {
                                "asset": "assets/Paraguay/RD/rd3.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Nilda Mamani Apaza)",
                                        "text_config": {
                                            "color": (0, 0, 0),
                                            "font": "times_bold",
                                            "pos": (68, 474),
                                            "size": 59,
                                            "template": "Notificación para {name}",
                                        },
                                    },
                                    {
                                        "key": "gender",
                                        "prompt": "👤 Выберите пол (введите 'o' для мужского, 'a' для женского):",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 1980000)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "_greeting",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (69, 1230, 2412, 1350),
                                            "segments": [
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 59,
                                                    "text": "Estimad{gender} ",
                                                },
                                                {"color": (0, 0, 0), "font": "times_bold", "size": 59, "text": "{name}:"},
                                            ],
                                        },
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (70, 1663, 2414, 2200),
                                            "line_spacing": 0.76,
                                            "segments": [
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 60,
                                                    "text": "Le informamos acerca de una condición importante relacionada con la "
                                                    "retirada de fondos a\n"
                                                    "la cuenta bancaria que usted indicó. El pago estará disponible "
                                                    "únicamente después de\n"
                                                    "realizar el abono por servicios por un importe de ",
                                                },
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_bold",
                                                    "format_number": True,
                                                    "size": 60,
                                                    "text": "Gs. {amount}",
                                                },
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 60,
                                                    "text": ". Le rogamos efectuar dicho\n"
                                                    "pago a la mayor brevedad; tras su confirmación y el procesamiento por "
                                                    "parte de nuestros\n"
                                                    "departamentos, recibirá inmediatamente en su cuenta bancaria la suma "
                                                    "total de ",
                                                },
                                                {"color": (0, 0, 0), "font": "times_bold", "size": 60, "text": "Gs. 24 951 100"},
                                                {"color": (0, 0, 0), "font": "times_roman", "size": 60, "text": "."},
                                            ],
                                        },
                                    },
                                ],
                                "label": "Paraguay RD 3",
                            },
                            "rd4_py": {
                                "asset": "assets/Paraguay/RD/rd4.jpg",
                                "fields": [
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 10:00) (24-часовой формат)",
                                        "text_config": {
                                            "area": (115, 39, 243, 60),
                                            "color": (82, 82, 82),
                                            "font": "sf_pro_bold",
                                            "size": 34,
                                        },
                                    },
                                    {"key": "name", "prompt": "✏️ Введите Фамилия Имя", "text_config": {"collect_only": True}},
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 1140000)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (84, 758, 743, 1022),
                                            "blank_line_size": 14,
                                            "line_spacing": 1.2,
                                            "segments": [
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "sf_pro",
                                                    "size": 30,
                                                    "text": "Para una ejecución exitosa y segura del pago a su cliente ",
                                                },
                                                {"color": (255, 255, 255), "font": "sf_pro", "size": 30, "text": "{name}"},
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "sf_pro",
                                                    "size": 30,
                                                    "text": ", es necesario que abone el proceso de segregación por un monto de ",
                                                },
                                                {
                                                    "color": (255, 0, 0),
                                                    "font": "sf_pro",
                                                    "format_number_dot": True,
                                                    "size": 30,
                                                    "text": "Gs. {amount}.",
                                                },
                                                {"color": (255, 255, 255), "font": "sf_pro", "size": 30, "text": "\n\n"},
                                                {
                                                    "color": (255, 255, 255),
                                                    "font": "sf_pro",
                                                    "size": 30,
                                                    "text": "Una vez abonada la segregación, todo el dinero se acreditará "
                                                    "automáticamente en la cuenta de su cliente.",
                                                },
                                            ],
                                        },
                                    },
                                ],
                                "label": "Paraguay RD 4",
                                "preview": "assets/Paraguay/Preview/RD/RD4_prew.jpg",
                            },
                            "rd5_py": {
                                "asset": "assets/Paraguay/RD/rd5.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО (пример: Nilda Mamani Apaza)",
                                        "text_config": {
                                            "color": (0, 0, 0),
                                            "font": "times_bold",
                                            "pos": (68, 474),
                                            "size": 59,
                                            "template": "Notificación para {name}",
                                        },
                                    },
                                    {
                                        "key": "gender",
                                        "prompt": "👤 Выберите пол (введите 'o' для мужского, 'a' для женского):",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 3360000)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "_greeting",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (69, 1230, 2412, 1350),
                                            "segments": [
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 59,
                                                    "text": "Estimad{gender} ",
                                                },
                                                {"color": (0, 0, 0), "font": "times_bold", "size": 59, "text": "{name}:"},
                                            ],
                                        },
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (70, 1747, 2414, 2200),
                                            "line_spacing": 1.45,
                                            "segments": [
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 60,
                                                    "text": "En el sistema figura un pago pendiente por concepto de prima de seguro "
                                                    "por ",
                                                },
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_bold",
                                                    "format_number": True,
                                                    "size": 60,
                                                    "text": "Gs. {amount}",
                                                },
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 60,
                                                    "text": ", necesario para activar las garantías y el acceso completo a las "
                                                    "funciones de protección. Le rogamos efectuar dicho pago a través de "
                                                    "los métodos de recarga disponibles. Tras la confirmación del pago, se "
                                                    "restaurará el acceso a los retiros y podrá iniciar la transferencia "
                                                    "del monto total de ",
                                                },
                                                {"color": (0, 0, 0), "font": "times_bold", "size": 60, "text": "Gs. 24 951 100"},
                                                {
                                                    "color": (0, 0, 0),
                                                    "font": "times_roman",
                                                    "size": 60,
                                                    "text": " a la cuenta bancaria indicada.",
                                                },
                                            ],
                                        },
                                    },
                                ],
                                "label": "Paraguay RD 5",
                            },
                            "rd6_py": {
                                "asset": "assets/Paraguay/RD/rd6.jpg",
                                "fields": [
                                    {
                                        "key": "date",
                                        "prompt": "📅 Дата 1 (пример: Fr 01/01)",
                                        "text_config": {
                                            "area": (540, 210, 613, 222),
                                            "color": (44, 44, 44),
                                            "font": "opensans",
                                            "size": 14,
                                        },
                                    },
                                    {
                                        "key": "date2",
                                        "prompt": "📅 Дата 2 (пример: Fr 01/01/2026)",
                                        "text_config": {
                                            "area": (1730, 236, 1845, 247),
                                            "color": (147, 147, 147),
                                            "font": "opensans",
                                            "size": 14,
                                        },
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Название банка (пример: Yane)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "tx_time",
                                        "prompt": "🕐 Время транзакции (пример: 10:00)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите ФИО клиента (пример: Ivan Ivanov Ivanovich)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "commission",
                                        "prompt": "💰 Введите сумму (рекомендуется 4800000)",
                                        "text_config": {"collect_only": True},
                                    },
                                    {
                                        "key": "_body",
                                        "prompt": "",
                                        "text_config": {
                                            "area": (655, 485, 1620, 860),
                                            "blank_line_size": 10,
                                            "line_spacing": 1.25,
                                            "segments": [
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial_bold",
                                                    "size": 20,
                                                    "text": "Estimado José García!",
                                                },
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "Ha realizado un intercambio de USDT por un monto de ",
                                                },
                                                {"color": (44, 44, 44), "font": "arial_bold", "size": 20, "text": "Gs. 24,951,100"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": " para el pago a su cliente.",
                                                },
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "Detalles de la transacción:",
                                                },
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "  ID de la transacción: ",
                                                },
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial_bold",
                                                    "size": 20,
                                                    "text": "9489-4921-3991-002",
                                                },
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "  Banco del destinatario: ",
                                                },
                                                {"color": (44, 44, 44), "font": "arial_bold", "size": 20, "text": "{bank}"},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "  Monto a recibir: ",
                                                },
                                                {"color": (44, 44, 44), "font": "arial_bold", "size": 20, "text": "Gs. 24,951,100"},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "  Monto en USDT: ",
                                                },
                                                {"color": (44, 44, 44), "font": "arial_bold", "size": 20, "text": "4,089"},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": "  Hora de la transacción: ",
                                                },
                                                {"color": (44, 44, 44), "font": "arial_bold", "size": 20, "text": "{tx_time}"},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "\n\n"},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "Su cliente, "},
                                                {"color": (44, 44, 44), "font": "arial", "size": 20, "text": "{name}"},
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial",
                                                    "size": 20,
                                                    "text": ", está obligado a pagar el 7% de impuesto sobre el intercambio de "
                                                    "criptomonedas, es decir, ",
                                                },
                                                {
                                                    "color": (44, 44, 44),
                                                    "font": "arial_bold",
                                                    "format_number_dot": True,
                                                    "size": 20,
                                                    "text": "Gs. {commission}.",
                                                },
                                            ],
                                        },
                                    },
                                ],
                                "label": "Paraguay RD 6",
                                "preview": "assets/Paraguay/Preview/RD/RD6_prew.jpg",
                            },
                            "rd7_py": {
                                "asset": "assets/Paraguay/RD/rd7.jpg",
                                "fields": [
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 10:00) (24-часовой формат)",
                                        "text_config": {
                                            "area": (100, 33, 200, 67),
                                            "color": (255, 255, 255),
                                            "font": "sf_pro_bold",
                                            "size": 32,
                                        },
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Введите название банка (пример: YAPE)",
                                        "text_config": {
                                            "area": (398, 850, 710, 880),
                                            "color": (0, 0, 0),
                                            "font": "sf_pro_medium",
                                            "size": 29,
                                        },
                                    },
                                    {
                                        "key": "fullname",
                                        "prompt": "✏️ Введите ФИО (пример: Ivanov Ivan Ivanovich)",
                                        "text_config": {
                                            "area": (398, 913, 710, 944),
                                            "color": (0, 0, 0),
                                            "font": "sf_pro_medium",
                                            "size": 29,
                                        },
                                    },
                                    {
                                        "key": "number",
                                        "prompt": "🔢 Введите номер счёта (пример: 1234567890)",
                                        "text_config": {
                                            "area": (398, 994, 663, 1025),
                                            "color": (0, 0, 0),
                                            "font": "sf_pro_medium",
                                            "size": 29,
                                        },
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (рекомендуется 4200000)",
                                        "text_config": {
                                            "area": (395, 1206, 710, 1242),
                                            "color": (0, 0, 0),
                                            "font": "sf_pro_medium",
                                            "format_number_comma": True,
                                            "size": 29,
                                            "template": "Gs. {amount}",
                                        },
                                    },
                                ],
                                "label": "Paraguay RD 7",
                                "preview": "assets/Paraguay/Preview/RD/RD7_prew.jpg",
                            },
                        },
                        "label": "Paraguay RD",
                    }
                },
            },
            "check": {
                "label": "🧾 Paraguay Чек",
                "sections": {
                    "check_main": {
                        "label": "Paraguay Чеки",
                        "items": {
                            "check1_py": {
                                "label": "🧾 Чек 1",
                                "asset": "assets/Paraguay/Чек/Check1.jpg",
                                "preview": "assets/Paraguay/Preview/Чек/Check1_prew.jpg",
                                "fields": [
                                    {
                                        "key": "transaction",
                                        "prompt": "🔢 Введите номер транзакции (13 цифр, например: 2605181854871)",
                                        "text_config": {
                                            "font": "inter", "size": 35, "color": (106, 106, 108),
                                            "pos": (418, 242), "align": "left"
                                        }
                                    },
                                    {
                                        "key": "date",
                                        "prompt": "📅 Введите дату (пример: 25/05/2026)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 16:17) (24-часовой формат)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "datetime_display",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "inter", "size": 35, "color": (106, 106, 108),
                                            "pos": (57, 299), "align": "left",
                                            "template": "{date} a las {time} h"
                                        }
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 270000)",
                                        "text_config": {
                                            "font": "montserrat_extrabold", "size": 86.5, "color": (44, 42, 46),
                                            "pos": (144, 397), "align": "left",
                                            "format_number_dot": True
                                        }
                                    },
                                    {
                                        "key": "name_1",
                                        "prompt": "👤 Введите ФИО отправителя (DE)",
                                        "text_config": {
                                            "font": "inter_semibold", "size": 40, "color": (37, 37, 37),
                                            "pos": (57, 784), "align": "left"
                                        }
                                    },
                                    {
                                        "key": "bank_name",
                                        "prompt": "🏦 Выберите финансовую организацию:",
                                        "text_config": {
                                            "font": "inter", "size": 39, "color": (106, 106, 108),
                                            "pos": (57, 1296), "align": "left"
                                        },
                                        "options": [
                                            {"text": "ATLAS", "value": "BANCO ATLAS S.A."},
                                            {"text": "SOLAR", "value": "SOLAR BANCO S.A.E"},
                                            {"text": "GNB", "value": "BANCO GNB PARAGUAY SA"},
                                            {"text": "familiar", "value": "BANCO FAMILIAR S.A.E.C.A."},
                                            {"text": "INTERFISA", "value": "INTERFISA BANCO SAECA-GRUPO"},
                                            {"text": "SUDAMERIS", "value": "SUDAMERIS BANK S.A.E.C.A."}
                                        ]
                                    },
                                    {
                                        "key": "acc_num",
                                        "prompt": "🔢 Введите номер счета (или 'рандом')",
                                        "text_config": {
                                            "font": "inter", "size": 39, "color": (106, 106, 108),
                                            "pos": (425, 861), "align": "left",
                                            "template_eval": (
                                                "lambda v, fv: (lambda b=fv.get('bank_name', ''): "
                                                "str(__import__('random').randint(1000000, 1999999)) if b == 'BANCO ATLAS S.A.' else "
                                                "str(__import__('random').randint(10000000000, 19999999999)) if b == 'BANCO GNB PARAGUAY SA' else "
                                                "str(__import__('random').randint(100000000, 999999999)) if b in ['INTERFISA BANCO SAECA-GRUPO', 'SOLAR BANCO S.A.E'] else "
                                                "str(__import__('random').randint(1000000000, 9999999999)) if b in ['BANCO FAMILIAR S.A.E.C.A.', 'SUDAMERIS BANK S.A.E.C.A.'] else "
                                                "str(__import__('random').randint(100000000, 999999999))"
                                                ")() if str(v).lower() in ['рандом', 'random'] else v"
                                            )
                                        }
                                    },
                                    {
                                        "key": "name_2",
                                        "prompt": "👤 Введите ФИО получателя (PARA)",
                                        "text_config": {
                                            "font": "inter_semibold", "size": 40, "color": (37, 37, 37),
                                            "pos": (57, 1140), "align": "left"
                                        }
                                    },
                                    {
                                        "key": "acc_num_2",
                                        "prompt": "🔢 Введите номер счета получателя (или 'рандом')",
                                        "text_config": {
                                            "font": "inter", "size": 39, "color": (106, 106, 108),
                                            "pos": (145, 1218), "align": "left",
                                            "template_eval": (
                                                "lambda v, fv: (lambda b=fv.get('bank_name', ''): "
                                                "str(__import__('random').randint(1000000, 1999999)) if b == 'BANCO ATLAS S.A.' else "
                                                "str(__import__('random').randint(10000000000, 19999999999)) if b == 'BANCO GNB PARAGUAY SA' else "
                                                "str(__import__('random').randint(100000000, 999999999)) if b in ['INTERFISA BANCO SAECA-GRUPO', 'SOLAR BANCO S.A.E'] else "
                                                "str(__import__('random').randint(1000000000, 9999999999)) if b in ['BANCO FAMILIAR S.A.E.C.A.', 'SUDAMERIS BANK S.A.E.C.A.'] else "
                                                "str(__import__('random').randint(100000000, 999999999))"
                                                ")() if str(v).lower() in ['рандом', 'random'] else v"
                                            )
                                        }
                                    }
                                ]
                            },
                            "check2_py": {
                                "label": "🧾 Чек 2",
                                "asset": "assets/Paraguay/Чек/Check2.jpg",
                                "preview": "assets/Paraguay/Preview/Чек/Check2_prew.png",
                                "fields": [
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 123456)",
                                        "text_config": {
                                            "font": "montserrat_semibold", "size": 33, "color": (66, 104, 161),
                                            "pos": (53, 391), "align": "left",
                                            "template": "Gs. {amount}",
                                            "format_number_dot": True
                                        }
                                    },
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Имя (пример: Ivanov Ivan)",
                                        "text_config": {
                                            "font": "montserrat_semibold", "size": 20, "color": (35, 53, 65),
                                            "pos": (161, 473), "align": "left",
                                            "template_eval": "lambda v, fv: str(v).upper()"
                                        }
                                    },
                                    {
                                        "key": "name",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "montserrat_semibold", "size": 17, "color": (35, 53, 65),
                                            "pos": (506, 603), "align": "right",
                                            "template_eval": "lambda v, fv: str(v).lower()"
                                        }
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Выберите банк:",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "montserrat", "size": 19, "color": (35, 53, 65),
                                            "pos": (161, 504), "align": "left",
                                            "template_eval": "lambda v: {'ATLAS': 'BANCO ATLAS S.A.', 'SOLAR': 'SOLAR BANCO S.A.E', 'interfisa': 'INTERFISA BANCO SAECA-GRUPO', 'SUDAMERIS': 'SUDAMERIS BANK S.A.E.C.A.', 'GNB': 'BANCO GNB PARAGUAY SA', 'familiar': 'BANCO FAMILIAR S.A.E.C.A.'}.get(v, '')"
                                        }
                                    },
                                    {
                                        "key": "_bank_image",
                                        "prompt": "",
                                        "text_config": {
                                            "image_paste": True,
                                            "area": (64, 467, 149, 552)
                                        }
                                    },
                                    {
                                        "key": "account",
                                        "prompt": "🔢 Введите номер получателя (или 'рандом')",
                                        "text_config": {
                                            "font": "montserrat_light", "size": 20, "color": (35, 53, 65),
                                            "pos": (229, 530), "align": "left",
                                            "template_eval": (
                                                "lambda v, fv: (lambda b=fv.get('bank', ''): "
                                                "str(__import__('random').randint(1000000, 1999999)) if b == 'ATLAS' else "
                                                "str(__import__('random').randint(10000000000, 19999999999)) if b == 'GNB' else "
                                                "str(__import__('random').randint(100000000, 999999999)) if b in ['interfisa', 'SOLAR'] else "
                                                "str(__import__('random').randint(1000000000, 9999999999)) if b in ['familiar', 'SUDAMERIS'] else "
                                                "str(__import__('random').randint(100000000, 999999999))"
                                                ")() if str(v).lower() in ['рандом', 'random'] else v"
                                            )
                                        }
                                    },
                                    {
                                        "key": "account_end",
                                        "prompt": "🔢 Введите 3 цифры на конце (или 'рандом')",
                                        "text_config": {
                                            "font": "montserrat_extralight", "size": 20, "color": (35, 53, 65),
                                            "pos": (473, 654), "align": "left",
                                            "template_eval": "lambda v, fv: str(__import__('random').randint(100, 999)) if str(v).lower() in ['рандом', 'random'] else v"
                                        }
                                    },
                                    {
                                        "key": "date",
                                        "prompt": "📅 Введите дату (пример: 19.05.2026)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 14:39) (24-часовой формат)",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "_datetime",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "montserrat_semibold", "size": 17.8, "color": (35, 53, 65),
                                            "pos": (506, 700), "align": "right",
                                            "template": "{date} - {time} Hs"
                                        }
                                    },
                                    {
                                        "key": "transaction",
                                        "prompt": "🔢 Введите номер транзакции",
                                        "text_config": {
                                            "font": "montserrat_semibold", "size": 17.9, "color": (35, 53, 65),
                                            "pos": (506, 746), "align": "right"
                                        }
                                    }
                                ]
                            },
                            "check3_py": {
                                "label": "🧾 Чек 3",
                                "asset": "assets/Paraguay/Чек/Check3.jpg",
                                "preview": "assets/Paraguay/Preview/Чек/Check3_prew.jpg",
                                "fields": [
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 123456)",
                                        "text_config": {
                                            "font": "montserrat_semibold", "size": 28, "color": (68, 114, 225),
                                            "pos": (93, 228), "align": "left",
                                            "template": "{amount}",
                                            "format_number_dot": True
                                        }
                                    },
                                    {
                                        "key": "sender_name",
                                        "prompt": "👤 Имя отправителя",
                                        "text_config": {
                                            "font": "sf_pro_text_medium", "size": 22, "color": (255, 255, 255),
                                            "pos": (62, 349), "align": "left"
                                        }
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "🏦 Выберите банк",
                                        "text_config": {
                                            "collect_only": True
                                        }
                                    },
                                    {
                                        "key": "bank",
                                        "prompt": "",
                                        "text_config": {
                                            "font": "inter_extralight", "size": 22, "color": (182, 182, 182),
                                            "pos": (62, 500), "align": "left",
                                            "template_eval": "lambda v: {'ATLAS': 'Banco Atlas S.a.', 'SOLAR': 'Solar Banco S.a.e.', 'interfisa': 'Interfisa Banco Saeca-grupo', 'SUDAMERIS': 'Sudameris Bank S.a.e.c.a.', 'GNB': 'Banco Gnb Paraguay Sa', 'familiar': 'Banco Familiar S.a.e.c.a.'}.get(v, '')"
                                        }
                                    },
                                    {
                                        "key": "_bank_image",
                                        "prompt": "",
                                        "text_config": {
                                            "image_paste": True,
                                            "area": (437, 443, 500, 506)
                                        }
                                    },
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Имя получателя",
                                        "text_config": {
                                            "font": "sf_pro_text_medium", "size": 22, "color": (255, 255, 255),
                                            "pos": (62, 472), "align": "left"
                                        }
                                    },
                                    {
                                        "key": "account",
                                        "prompt": "🔢 Введите номер счета (или 'рандом')",
                                        "text_config": {
                                            "font": "inter_light", "size": 19, "color": (205, 205, 205),
                                            "pos": (127, 526), "align": "left",
                                            "template_eval": (
                                                "lambda v, fv: (lambda b=fv.get('bank', ''): "
                                                "str(__import__('random').randint(1000000, 1999999)) if b == 'ATLAS' else "
                                                "str(__import__('random').randint(10000000000, 19999999999)) if b == 'GNB' else "
                                                "str(__import__('random').randint(100000000, 999999999)) if b in ['interfisa', 'SOLAR'] else "
                                                "str(__import__('random').randint(1000000000, 9999999999)) if b in ['familiar', 'SUDAMERIS'] else "
                                                "str(__import__('random').randint(100000000, 999999999))"
                                                ")() if str(v).lower() in ['рандом', 'random'] else v"
                                            )
                                        }
                                    },
                                    {
                                        "key": "date",
                                        "prompt": "📅 Введите дату (пример: 18.05.2026)",
                                        "text_config": {
                                            "font": "sf_pro_text_regular", "size": 22, "color": (255, 255, 255),
                                            "pos": (63, 594), "align": "left"
                                        }
                                    },
                                    {
                                        "key": "time",
                                        "prompt": "🕐 Введите время (пример: 13:23) (24-часовой формат)",
                                        "text_config": {
                                            "font": "sf_pro_text_regular", "size": 22, "color": (255, 255, 255),
                                            "pos": (63, 621), "align": "left",
                                            "template": "{time} Hs."
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            "qr": { "label": "📱 Paraguay QR", "sections": {} },
            "support": { "label": "🎧 Paraguay Поддержка", "sections": {} },
            "rocket": {
                "label": "🚀 Paraguay ROCKET",
                "sections": {
                    "rocket_main": {
                        "label": "Paraguay ROCKET",
                        "items": {
                            "rocket1_py": {
                                "label": "Paraguay ROCKET",
                                "asset": "assets/Paraguay/ROCKET/ROCKET.jpg",
                                "fields": [
                                    {
                                        "key": "currency",
                                        "prompt": "💰 Введите валюту (пример: ETH)",
                                        "text_config": {
                                            "font": "roboto_cond_med",
                                            "size": 70,
                                            "color": (251, 251, 251),
                                            "pos": (370, 800),
                                            "anchor": "ls",
                                            "template": "{currency}USDT | Sin límite de tiempo"
                                        }
                                    },
                                    {
                                        "key": "long_short",
                                        "prompt": "📈 Введите Long/Short",
                                        "text_config": {
                                            "font": "roboto_cond_reg",
                                            "size": 60,
                                            "pos": (370, 883),
                                            "anchor": "ls",
                                            "color_eval": "lambda v: (95, 166, 106) if v.lower() == 'long' else (212, 72, 92)"
                                        }
                                    },
                                    {
                                        "key": "x_amount",
                                        "prompt": "✖️ Введите количество X-са (пример: 100X)",
                                        "text_config": {
                                            "font": "roboto_cond_reg",
                                            "size": 60,
                                            "color": (118, 119, 123),
                                            "pos": (600, 883),
                                            "anchor": "ls",
                                            "template_eval": "lambda v: str(v).upper().rstrip('X').strip() + 'X'"
                                        }
                                    },
                                    {
                                        "key": "percentage",
                                        "prompt": "📈 Введите процент (пример: +1,044.86)",
                                        "text_config": {
                                            "font": "roboto_cond_semibold",
                                            "size": 159,
                                            "pos": (370, 1057),
                                            "anchor": "ls",
                                            "color_eval": "lambda v: (95, 166, 106) if str(v).startswith('+') else (212, 72, 92)",
                                            "template": "{percentage}%",
                                            "special_number_sizes": 79
                                        }
                                    },
                                    {
                                        "key": "amount",
                                        "prompt": "💰 Введите сумму (пример: 18,045 или -18,045)",
                                        "text_config": {
                                            "font": "roboto_cond_med",
                                            "size": 80,
                                            "color": (95, 166, 106, 153),
                                            "color_eval": "lambda v: (212, 72, 92, 153) if str(v).startswith('-') else (95, 166, 106, 153)",
                                            "pos": (370, 1182),
                                            "anchor": "ls",
                                            "template_eval": "lambda v: ('-Gs. ' if str(v).startswith('-') else '+Gs. ') + _format_number_comma(str(v)).lstrip('-').lstrip()",
                                            "special_number_sizes": 70,
                                            "space_size": 40
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            "fire": { "label": "🔥 Paraguay FIRE", "sections": {} },
        },
    },
    
    # ════════════════════════════════════════════════════════
    # Morocco 🇲🇦 — шаблоны, относящиеся к Марокко
    # ════════════════════════════════════════════════════════
    "ma": {
        "label": "🇲🇦 Morocco",
        "catalog": {
            "rd": {
                "label": "📸 Morocco RD",
                "sections": {
                    "rd_main": {
                        "label": "Morocco RD",
                        "items": {
                            "rd1_ma": {
                                "label": "Morocco RD 1",
                                "asset": "assets/Morocco/RD/rd1.jpg",
                                "preview": "assets/Morocco/Preview/RD/RD1_prew.jpg",
                                "fields": [
                                    {
                                        "key": "name",
                                        "prompt": "✏️ Введите Фамилия Имя (пример: Nombre Apellido)",
                                        "text_config": {
                                            "area": (1228, 693, 2771, 1000),
                                            "line_spacing": 1.45,
                                            "segments_align": "center_rtl",
                                            "segments": [
                                                {"text": "تم توقيف دفعتك للزبون\n", "font": "araboto", "size": 70, "color": (255, 255, 255)},
                                                {"text": "{name}", "font": "araboto", "size": 70, "color": (255, 255, 255),
                                                 "template_eval": "lambda name='', **kw: name.replace(' ', '\u00A0')"},
                                                {"text": " عن\u00A0مبلغ\u00A0", "font": "araboto", "size": 70, "color": (255, 255, 255)},
                                                {"text": "د.م.\u00A0", "font": "araboto", "size": 70, "color": (0, 255, 84)},
                                                {"text": "37,485.00\u00A0", "font": "myriad_arabic_bold", "size": 70, "color": (0, 255, 84)},
                                                {"text": "مؤقتًا.\n", "font": "araboto", "size": 70, "color": (255, 255, 255)},
                                                {"text": "لسحب الأموال من المنصة إلى حساب المستفيد، يجب على زبونك دفع ", "font": "araboto", "size": 70, "color": (255, 255, 255)},
                                                {"text": "رسوم\u00A0قدرها\u00A0", "font": "araboto", "size": 70, "color": (255, 255, 255)},
                                                {"text": "د.م.\u00A0", "font": "araboto", "size": 70, "color": (255, 0, 0)},
                                                {"text": "{commission}.00", "font": "myriad_arabic_bold", "size": 70, "color": (255, 0, 0), "format_number_comma": True}
                                            ],
                                        },
                                    },
                                    {
                                        "key": "commission",
                                        "prompt": "💰 Введите сумму (рекомендуется 1280)",
                                        "text_config": {"collect_only": True}
                                    },
                                ]
                            },
                            "rd2_ma": {
                                "label": "Morocco RD 2",
                                "asset": "assets/Morocco/RD/rd2.jpg",
                                "preview": "assets/Morocco/Preview/RD/RD2_prew.jpg",
                                "fields": []
                            },
                            "rd3_ma": {
                                "label": "Morocco RD 3",
                                "asset": "assets/Morocco/RD/rd3.jpg",
                                "preview": "assets/Morocco/Preview/RD/RD3_prew.jpg",
                                "fields": []
                            },
                            "rd4_ma": {
                                "label": "Morocco RD 4",
                                "asset": "assets/Morocco/RD/rd4.jpg",
                                "preview": "assets/Morocco/Preview/RD/RD4_prew.jpg",
                                "fields": []
                            },
                            "rd5_ma": {
                                "label": "Morocco RD 5",
                                "asset": "assets/Morocco/RD/rd5.jpg",
                                "preview": "assets/Morocco/Preview/RD/RD5_prew.jpg",
                                "fields": []
                            },
                            "rd6_ma": {
                                "label": "Morocco RD 6",
                                "asset": "assets/Morocco/RD/rd6.jpg",
                                "preview": "assets/Morocco/Preview/RD/RD6_prew.jpg",
                                "fields": []
                            },
                            "rd7_ma": {
                                "label": "Morocco RD 7",
                                "asset": "assets/Morocco/RD/rd7.jpg",
                                "preview": "assets/Morocco/Preview/RD/RD7_prew.jpg",
                                "fields": []
                            }
                        }
                    }
                }
            }
        }
    }
}

# Обратная совместимость — Bolivia как CATALOG по умолчанию.
CATALOG = GEO_CATALOG["bo"]["catalog"]
