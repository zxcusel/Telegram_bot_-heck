GEO_ENTRY = {
    "label": "🇵🇾 Paraguay",
    "catalog": {
        "fd": {"label": "📁 Paraguay FD", "sections": {}},
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
                                    "prompt": '✏️ Введите Фамилия Имя (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "area": (1250, 700, 2780, 925),
                                        "line_spacing": 1.25,
                                        "segments": [
                                            {
                                                "color": (255, 255, 255),
                                                "font": "montserrat",
                                                "size": 45,
                                                "text": 'Su pago al cliente ',
                                            },
                                            {
                                                "color": (255, 255, 255),
                                                "font": "montserrat",
                                                "size": 45,
                                                "text": "{name}",
                                            },
                                            {
                                                "color": (255, 255, 255),
                                                "font": "montserrat",
                                                "size": 45,
                                                "text": ' por un monto de ',
                                            },
                                            {
                                                "color": (0, 255, 84),
                                                "font": "montserrat",
                                                "size": 45,
                                                "text": 'Gs. 24,951,100',
                                            },
                                            {
                                                "color": (255, 255, 255),
                                                "font": "montserrat",
                                                "size": 45,
                                                "text": ' ha sido bloqueado temporalmente. Para retirar los fondos de la plataforma a la cuenta del beneficiario, su cliente está obligado a pagar una tarifa de ',
                                            },
                                            {
                                                "color": (255, 0, 0),
                                                "font": "montserrat",
                                                "format_number_comma": True,
                                                "size": 45,
                                                "text": 'Gs. {commission}.',
                                            },
                                        ],
                                    },
                                },
                                {
                                    "key": "commission",
                                    "prompt": '💰 Введите сумму (рекомендуется 980000)',
                                    "text_config": {"collect_only": True},
                                },
                            ],
                            "label": "Paraguay RD 1",
                            "preview": "assets/Paraguay/Preview/RD/RD1_prew.jpg",
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "raw",
                            "name_format": "py_fio",
                        },
                        "rd2_py": {
                            "asset": "assets/Paraguay/RD/rd2.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите Фамилия Имя (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "area": (2235, 1420, 3050, 1460),
                                        "color": (57, 62, 67),
                                        "font": "montserrat",
                                        "line_spacing": 1.2,
                                        "size": 30,
                                        "template": 'Cuenta bancaria del cliente {name}.',
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (рекомендуется 1560000)',
                                    "text_config": {"collect_only": True},
                                },
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
                                                "text": 'Es necesario pagar una tarifa por la',
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
                                                "text": 'conversión de ',
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
                                                "text": ' a ',
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
                                                "text": 'Importe de la tarifa: ',
                                            },
                                            {
                                                "color": (255, 13, 13),
                                                "font": "montserrat_medium",
                                                "format_number_comma": True,
                                                "size": 44,
                                                "text": 'Gs. {amount}',
                                            },
                                            {
                                                "color": (255, 255, 255),
                                                "font": "montserrat_light",
                                                "size": 44,
                                                "text": ".",
                                            },
                                        ],
                                    },
                                },
                            ],
                            "label": "Paraguay RD 2",
                            "preview": "assets/Paraguay/Preview/RD/RD2_prew.jpg",
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "raw",
                            "name_format": "py_fio",
                        },
                        "rd3_py": {
                            "asset": "assets/Paraguay/RD/rd3.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Nilda Mamani Apaza)',
                                    "text_config": {
                                        "color": (0, 0, 0),
                                        "font": "times_bold",
                                        "pos": (68, 474),
                                        "size": 59,
                                        "template": 'Notificación para {name}',
                                    },
                                },
                                {
                                    "key": "gender",
                                    "prompt": "👤 Выберите пол (введите 'o' для мужского, 'a' для женского):",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (рекомендуется 1980000)',
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
                                            {
                                                "color": (0, 0, 0),
                                                "font": "times_bold",
                                                "size": 59,
                                                "text": "{name}:",
                                            },
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
                                                "text": """Le informamos acerca de una condición importante relacionada con la retirada de fondos a
la cuenta bancaria que usted indicó. El pago estará disponible únicamente después de
realizar el abono por servicios por un importe de """,
                                            },
                                            {
                                                "color": (0, 0, 0),
                                                "font": "times_bold",
                                                "format_number": True,
                                                "size": 60,
                                                "text": 'Gs. {amount}',
                                            },
                                            {
                                                "color": (0, 0, 0),
                                                "font": "times_roman",
                                                "size": 60,
                                                "text": """. Le rogamos efectuar dicho
pago a la mayor brevedad; tras su confirmación y el procesamiento por parte de nuestros
departamentos, recibirá inmediatamente en su cuenta bancaria la suma total de """,
                                            },
                                            {
                                                "color": (0, 0, 0),
                                                "font": "times_bold",
                                                "size": 60,
                                                "text": 'Gs. 24 951 100',
                                            },
                                            {
                                                "color": (0, 0, 0),
                                                "font": "times_roman",
                                                "size": 60,
                                                "text": ".",
                                            },
                                        ],
                                    },
                                },
                            ],
                            "label": "Paraguay RD 3",
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "raw",
                            "name_format": "py_fio",
                        },
                        "rd4_py": {
                            "asset": "assets/Paraguay/RD/rd4.jpg",
                            "fields": [
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 10:00) (24-часовой формат)',
                                    "text_config": {
                                        "area": (115, 39, 243, 60),
                                        "color": (82, 82, 82),
                                        "font": "sf_pro_bold",
                                        "size": 34,
                                    },
                                },
                                {
                                    "key": "name",
                                    "prompt": "✏️ Введите Фамилия Имя",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (рекомендуется 1140000)',
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
                                                "text": 'Para una ejecución exitosa y segura del pago a su cliente ',
                                            },
                                            {
                                                "color": (255, 255, 255),
                                                "font": "sf_pro",
                                                "size": 30,
                                                "text": "{name}",
                                            },
                                            {
                                                "color": (255, 255, 255),
                                                "font": "sf_pro",
                                                "size": 30,
                                                "text": ', es necesario que abone el proceso de segregación por un monto de ',
                                            },
                                            {
                                                "color": (255, 0, 0),
                                                "font": "sf_pro",
                                                "format_number_dot": True,
                                                "size": 30,
                                                "text": 'Gs. {amount}.',
                                            },
                                            {
                                                "color": (255, 255, 255),
                                                "font": "sf_pro",
                                                "size": 30,
                                                "text": """

""",
                                            },
                                            {
                                                "color": (255, 255, 255),
                                                "font": "sf_pro",
                                                "size": 30,
                                                "text": 'Una vez abonada la segregación, todo el dinero se acreditará automáticamente en la cuenta de su cliente.',
                                            },
                                        ],
                                    },
                                },
                            ],
                            "label": "Paraguay RD 4",
                            "preview": "assets/Paraguay/Preview/RD/RD4_prew.jpg",
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "raw",
                            "name_format": "py_fio",
                        },
                        "rd5_py": {
                            "asset": "assets/Paraguay/RD/rd5.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Nilda Mamani Apaza)',
                                    "text_config": {
                                        "color": (0, 0, 0),
                                        "font": "times_bold",
                                        "pos": (68, 474),
                                        "size": 59,
                                        "template": 'Notificación para {name}',
                                    },
                                },
                                {
                                    "key": "gender",
                                    "prompt": "👤 Выберите пол (введите 'o' для мужского, 'a' для женского):",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (рекомендуется 3360000)',
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
                                            {
                                                "color": (0, 0, 0),
                                                "font": "times_bold",
                                                "size": 59,
                                                "text": "{name}:",
                                            },
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
                                                "text": 'En el sistema figura un pago pendiente por concepto de prima de seguro por ',
                                            },
                                            {
                                                "color": (0, 0, 0),
                                                "font": "times_bold",
                                                "format_number": True,
                                                "size": 60,
                                                "text": 'Gs. {amount}',
                                            },
                                            {
                                                "color": (0, 0, 0),
                                                "font": "times_roman",
                                                "size": 60,
                                                "text": ', necesario para activar las garantías y el acceso completo a las funciones de protección. Le rogamos efectuar dicho pago a través de los métodos de recarga disponibles. Tras la confirmación del pago, se restaurará el acceso a los retiros y podrá iniciar la transferencia del monto total de ',
                                            },
                                            {
                                                "color": (0, 0, 0),
                                                "font": "times_bold",
                                                "size": 60,
                                                "text": 'Gs. 24 951 100',
                                            },
                                            {
                                                "color": (0, 0, 0),
                                                "font": "times_roman",
                                                "size": 60,
                                                "text": ' a la cuenta bancaria indicada.',
                                            },
                                        ],
                                    },
                                },
                            ],
                            "label": "Paraguay RD 5",
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "raw",
                            "name_format": "py_fio",
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
                                    "prompt": '📅 Дата 2 (пример: Fr 01/01/2026)',
                                    "text_config": {
                                        "area": (1730, 236, 1845, 247),
                                        "color": (147, 147, 147),
                                        "font": "opensans",
                                        "size": 14,
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": '🏦 Название банка (пример: Yane)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "tx_time",
                                    "prompt": '🕐 Время транзакции (пример: 10:00)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО клиента (пример: Ivan Ivanov Ivanovich)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "commission",
                                    "prompt": '💰 Введите сумму (рекомендуется 4800000)',
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
                                                "text": 'Estimado José García!',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": """

""",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": 'Ha realizado un intercambio de USDT por un monto de ',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial_bold",
                                                "size": 20,
                                                "text": 'Gs. 24,951,100',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": ' para el pago a su cliente.',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": """

""",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": 'Detalles de la transacción:',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": "\n",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": '  ID de la transacción: ',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial_bold",
                                                "size": 20,
                                                "text": "9489-4921-3991-002",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": "\n",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": '  Banco del destinatario: ',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial_bold",
                                                "size": 20,
                                                "text": "{bank}",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": "\n",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": '  Monto a recibir: ',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial_bold",
                                                "size": 20,
                                                "text": 'Gs. 24,951,100',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": "\n",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": '  Monto en USDT: ',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial_bold",
                                                "size": 20,
                                                "text": "4,089",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": "\n",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": '  Hora de la transacción: ',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial_bold",
                                                "size": 20,
                                                "text": "{tx_time}",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": """

""",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": 'Su cliente, ',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": "{name}",
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial",
                                                "size": 20,
                                                "text": ', está obligado a pagar el 7% de impuesto sobre el intercambio de criptomonedas, es decir, ',
                                            },
                                            {
                                                "color": (44, 44, 44),
                                                "font": "arial_bold",
                                                "format_number_dot": True,
                                                "size": 20,
                                                "text": 'Gs. {commission}.',
                                            },
                                        ],
                                    },
                                },
                            ],
                            "label": "Paraguay RD 6",
                            "preview": "assets/Paraguay/Preview/RD/RD6_prew.jpg",
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "raw",
                            "name_format": "py_fio",
                        },
                        "rd7_py": {
                            "asset": "assets/Paraguay/RD/rd7.jpg",
                            "fields": [
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 10:00) (24-часовой формат)',
                                    "text_config": {
                                        "area": (100, 33, 200, 67),
                                        "color": (255, 255, 255),
                                        "font": "sf_pro_bold",
                                        "size": 32,
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": '🏦 Введите название банка (пример: YAPE)',
                                    "text_config": {
                                        "area": (398, 850, 710, 880),
                                        "color": (0, 0, 0),
                                        "font": "sf_pro_medium",
                                        "size": 29,
                                    },
                                },
                                {
                                    "key": "fullname",
                                    "prompt": '✏️ Введите ФИО (пример: Ivanov Ivan Ivanovich)',
                                    "text_config": {
                                        "area": (398, 913, 710, 944),
                                        "color": (0, 0, 0),
                                        "font": "sf_pro_medium",
                                        "size": 29,
                                    },
                                },
                                {
                                    "key": "number",
                                    "prompt": '🔢 Введите номер счёта (пример: 1234567890)',
                                    "text_config": {
                                        "area": (398, 994, 663, 1025),
                                        "color": (0, 0, 0),
                                        "font": "sf_pro_medium",
                                        "size": 29,
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (рекомендуется 4200000)',
                                    "text_config": {
                                        "area": (395, 1206, 710, 1242),
                                        "color": (0, 0, 0),
                                        "font": "sf_pro_medium",
                                        "format_number_comma": True,
                                        "size": 29,
                                        "template": 'Gs. {amount}',
                                    },
                                },
                            ],
                            "label": "Paraguay RD 7",
                            "preview": "assets/Paraguay/Preview/RD/RD7_prew.jpg",
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "raw",
                            "name_format": "py_fio",
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
                                    "prompt": '🔢 Введите номер транзакции (13 цифр, например: 2605181854871)',
                                    "text_config": {
                                        "font": "inter",
                                        "size": 35,
                                        "color": (106, 106, 108),
                                        "pos": (418, 242),
                                        "align": "left",
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": '📅 Введите дату (пример: 25/05/2026)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 16:17) (24-часовой формат)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "datetime_display",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "inter",
                                        "size": 35,
                                        "color": (106, 106, 108),
                                        "pos": (57, 299),
                                        "align": "left",
                                        "template": '{date} a las {time} h',
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (пример: 270000)',
                                    "text_config": {
                                        "font": "montserrat_extrabold",
                                        "size": 86.5,
                                        "color": (44, 42, 46),
                                        "pos": (144, 397),
                                        "align": "left",
                                        "format_number_dot": True,
                                    },
                                },
                                {
                                    "key": "name_1",
                                    "prompt": '👤 Введите ФИО отправителя',
                                    "text_config": {
                                        "font": "inter_semibold",
                                        "size": 40,
                                        "color": (37, 37, 37),
                                        "pos": (57, 784),
                                        "align": "left",
                                    },
                                },
                                {
                                    "key": "acc_num",
                                    "prompt": "🔢 Введите номер счета отправителя",
                                    "text_config": {
                                        "font": "inter",
                                        "size": 39,
                                        "color": (106, 106, 108),
                                        "pos": (425, 861),
                                        "align": "left",
                                        "template_eval": (
                                            "lambda v, fv: (lambda b=fv.get('bank_name_sender', ''): str(__import__('random').randint(1000000, 1999999)) if b == 'BANCO ATLAS S.A.' else str(__import__('random').randint(10000000000, 19999999999)) if b == 'BANCO GNB PARAGUAY SA' else str(__import__('random').randint(100000000, 999999999)) if b in ['INTERFISA BANCO SAECA-GRUPO', 'SOLAR BANCO S.A.E'] else str(__import__('random').randint(1000000000, 9999999999)) if b in ['BANCO FAMILIAR S.A.E.C.A.', 'SUDAMERIS BANK S.A.E.C.A.'] else str(__import__('random').randint(100000000, 999999999)))() if str(v).lower() in ['рандом', 'random'] else v"
                                        ),
                                    },
                                },
                                {
                                    "key": "bank_name_sender",
                                    "prompt": '🏦 Выберите банк отправителя',
                                    "text_config": {
                                        "font": "inter",
                                        "size": 39,
                                        "color": (106, 106, 108),
                                        "pos": (57, 940),
                                        "align": "left",
                                    },
                                    "options": [
                                        {
                                            "text": "ATLAS",
                                            "value": 'BANCO ATLAS S.A.',
                                        },
                                        {
                                            "text": "SOLAR",
                                            "value": 'SOLAR BANCO S.A.E',
                                        },
                                        {
                                            "text": "GNB",
                                            "value": 'BANCO GNB PARAGUAY SA',
                                        },
                                        {
                                            "text": "familiar",
                                            "value": 'BANCO FAMILIAR S.A.E.C.A.',
                                        },
                                        {
                                            "text": "INTERFISA",
                                            "value": 'INTERFISA BANCO SAECA-GRUPO',
                                        },
                                        {
                                            "text": "SUDAMERIS",
                                            "value": 'SUDAMERIS BANK S.A.E.C.A.',
                                        },
                                    ],
                                },
                                {
                                    "key": "name_2",
                                    "prompt": '👤 Введите ФИО получателя',
                                    "text_config": {
                                        "font": "inter_semibold",
                                        "size": 40,
                                        "color": (37, 37, 37),
                                        "pos": (57, 1140),
                                        "align": "left",
                                        "template_eval": 'lambda v, fv: str(v).upper()',
                                    },
                                },
                                {
                                    "key": "acc_num_2",
                                    "prompt": "🔢 Введите номер счета получателя",
                                    "text_config": {
                                        "font": "inter",
                                        "size": 39,
                                        "color": (106, 106, 108),
                                        "pos": (145, 1218),
                                        "align": "left",
                                        "template_eval": (
                                            "lambda v, fv: (lambda b=fv.get('bank_name', ''): str(__import__('random').randint(1000000, 1999999)) if b == 'BANCO ATLAS S.A.' else str(__import__('random').randint(10000000000, 19999999999)) if b == 'BANCO GNB PARAGUAY SA' else str(__import__('random').randint(100000000, 999999999)) if b in ['INTERFISA BANCO SAECA-GRUPO', 'SOLAR BANCO S.A.E'] else str(__import__('random').randint(1000000000, 9999999999)) if b in ['BANCO FAMILIAR S.A.E.C.A.', 'SUDAMERIS BANK S.A.E.C.A.'] else str(__import__('random').randint(100000000, 999999999)))() if str(v).lower() in ['рандом', 'random'] else v"
                                        ),
                                    },
                                },
                                {
                                    "key": "bank_name",
                                    "prompt": '🏦 Выберите банк получателя',
                                    "text_config": {
                                        "font": "inter",
                                        "size": 39,
                                        "color": (106, 106, 108),
                                        "pos": (57, 1296),
                                        "align": "left",
                                    },
                                    "options": [
                                        {
                                            "text": "ATLAS",
                                            "value": 'BANCO ATLAS S.A.',
                                        },
                                        {
                                            "text": "SOLAR",
                                            "value": 'SOLAR BANCO S.A.E',
                                        },
                                        {
                                            "text": "GNB",
                                            "value": 'BANCO GNB PARAGUAY SA',
                                        },
                                        {
                                            "text": "familiar",
                                            "value": 'BANCO FAMILIAR S.A.E.C.A.',
                                        },
                                        {
                                            "text": "INTERFISA",
                                            "value": 'INTERFISA BANCO SAECA-GRUPO',
                                        },
                                        {
                                            "text": "SUDAMERIS",
                                            "value": 'SUDAMERIS BANK S.A.E.C.A.',
                                        },
                                    ],
                                },
                                {
                                    "key": "_blur_mask1",
                                    "prompt": "",
                                    "text_config": {"blur_area": (420, 862, 564, 904)},
                                },
                                {
                                    "key": "_blur_mask2",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (144, 1222, 294, 1260)
                                    },
                                },
                            ],
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "raw",
                            "name_format": "py_fio",
                        },
                        "check2_py": {
                            "label": "🧾 Чек 2",
                            "asset": "assets/Paraguay/Чек/Check2.jpg",
                            "preview": "assets/Paraguay/Preview/Чек/Check2_prew.png",
                            "fields": [
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (пример: 123456)',
                                    "text_config": {
                                        "font": "montserrat_semibold",
                                        "size": 33,
                                        "color": (66, 104, 161),
                                        "pos": (53, 391),
                                        "align": "left",
                                        "template": 'Gs. {amount}',
                                        "format_number_dot": True,
                                    },
                                },
                                {
                                    "key": "name1",
                                    "prompt": '✏️ Введите ФИО получателя',
                                    "text_config": {
                                        "font": "montserrat_semibold",
                                        "size": 20,
                                        "color": (35, 53, 65),
                                        "pos": (161, 473),
                                        "align": "left",
                                        "template_eval": 'lambda v, fv: str(v).upper()',
                                    },
                                },
                                {
                                    "key": "name2",
                                    "prompt": '✏️ Введите ФИО отправителя',
                                    "text_config": {
                                        "font": "montserrat_semibold",
                                        "size": 17,
                                        "color": (35, 53, 65),
                                        "pos": (506, 603),
                                        "align": "right",
                                        "template_eval": 'lambda v, fv: str(v).lower()',
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": "🏦 Выберите банк",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "bank",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "montserrat",
                                        "size": 19,
                                        "color": (35, 53, 65),
                                        "pos": (161, 504),
                                        "align": "left",
                                        "template_eval": "lambda v: {'ATLAS': 'BANCO ATLAS S.A.', 'SOLAR': 'SOLAR BANCO S.A.E', 'interfisa': 'INTERFISA BANCO SAECA-GRUPO', 'SUDAMERIS': 'SUDAMERIS BANK S.A.E.C.A.', 'GNB': 'BANCO GNB PARAGUAY SA', 'familiar': 'BANCO FAMILIAR S.A.E.C.A.'}.get(v, '')",
                                    },
                                },
                                {
                                    "key": "_bank_image",
                                    "prompt": "",
                                    "text_config": {
                                        "image_paste": True,
                                        "area": (64, 467, 149, 552),
                                    },
                                },
                                {
                                    "key": "account",
                                    "prompt": '🔢 Введите номер счета получателя',
                                    "text_config": {
                                        "font": "montserrat_light",
                                        "size": 20,
                                        "color": (35, 53, 65),
                                        "pos": (229, 530),
                                        "align": "left",
                                        "template_eval": "lambda v, fv: (lambda b=fv.get('bank', ''): str(__import__('random').randint(1000000, 1999999)) if b == 'ATLAS' else str(__import__('random').randint(10000000000, 19999999999)) if b == 'GNB' else str(__import__('random').randint(100000000, 999999999)) if b in ['interfisa', 'SOLAR'] else str(__import__('random').randint(1000000000, 9999999999)) if b in ['familiar', 'SUDAMERIS'] else str(__import__('random').randint(100000000, 999999999)))() if str(v).lower() in ['рандом', 'random'] else v",
                                    },
                                },
                                {
                                    "key": "account_end",
                                    "prompt": '🔢 Введите последние 3 цифры счета отправителя',
                                    "text_config": {
                                        "font": "montserrat_extralight",
                                        "size": 20,
                                        "color": (35, 53, 65),
                                        "pos": (473, 654),
                                        "align": "left",
                                        "template_eval": "lambda v, fv: str(__import__('random').randint(100, 999)) if str(v).lower() in ['рандом', 'random'] else v",
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": '📅 Введите дату (пример: 19.05.2026)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 14:39) (24-часовой формат)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_datetime",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "montserrat_semibold",
                                        "size": 17.8,
                                        "color": (35, 53, 65),
                                        "pos": (506, 700),
                                        "align": "right",
                                        "template": '{date} - {time} Hs',
                                    },
                                },
                                {
                                    "key": "transaction",
                                    "prompt": '🔢 Введите номер транзакции',
                                    "text_config": {
                                        "font": "montserrat_semibold",
                                        "size": 17.9,
                                        "color": (35, 53, 65),
                                        "pos": (506, 746),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "_blur_mask",
                                    "prompt": "",
                                    "text_config": {"blur_area": (224, 531, 300, 555)},
                                },
                            ],
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "py",
                            "name_format": "py_fio",
                        },
                        "check3_py": {
                            "label": "🧾 Чек 3",
                            "asset": "assets/Paraguay/Чек/Check3.jpg",
                            "preview": "assets/Paraguay/Preview/Чек/Check3_prew.jpg",
                            "fields": [
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (пример: 123456)',
                                    "text_config": {
                                        "font": "montserrat_semibold",
                                        "size": 28,
                                        "color": (68, 114, 225),
                                        "pos": (93, 228),
                                        "align": "left",
                                        "template": "{amount}",
                                        "format_number_dot": True,
                                    },
                                },
                                {
                                    "key": "sender_name",
                                    "prompt": "👤 ФИО отправителя",
                                    "text_config": {
                                        "font": "sf_pro_text_medium",
                                        "size": 22,
                                        "color": (255, 255, 255),
                                        "pos": (62, 349),
                                        "align": "left",
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": "🏦 Выберите банк",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "bank",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "inter_extralight",
                                        "size": 22,
                                        "color": (182, 182, 182),
                                        "pos": (62, 500),
                                        "align": "left",
                                        "template_eval": "lambda v: {'ATLAS': 'Banco Atlas S.a.', 'SOLAR': 'Solar Banco S.a.e.', 'interfisa': 'Interfisa Banco Saeca-grupo', 'SUDAMERIS': 'Sudameris Bank S.a.e.c.a.', 'GNB': 'Banco Gnb Paraguay Sa', 'familiar': 'Banco Familiar S.a.e.c.a.'}.get(v, '')",
                                    },
                                },
                                {
                                    "key": "_bank_image",
                                    "prompt": "",
                                    "text_config": {
                                        "image_paste": True,
                                        "area": (437, 443, 500, 506),
                                    },
                                },
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите Имя получателя',
                                    "text_config": {
                                        "font": "sf_pro_text_medium",
                                        "size": 22,
                                        "color": (255, 255, 255),
                                        "pos": (62, 472),
                                        "align": "left",
                                    },
                                },
                                {
                                    "key": "account",
                                    "prompt": "🔢 Введите номер счета (или 'рандом')",
                                    "text_config": {
                                        "font": "inter_light",
                                        "size": 19,
                                        "color": (205, 205, 205),
                                        "pos": (127, 526),
                                        "align": "left",
                                        "template_eval": "lambda v, fv: (lambda b=fv.get('bank', ''): str(__import__('random').randint(1000000, 1999999)) if b == 'ATLAS' else str(__import__('random').randint(10000000000, 19999999999)) if b == 'GNB' else str(__import__('random').randint(100000000, 999999999)) if b in ['interfisa', 'SOLAR'] else str(__import__('random').randint(1000000000, 9999999999)) if b in ['familiar', 'SUDAMERIS'] else str(__import__('random').randint(100000000, 999999999)))() if str(v).lower() in ['рандом', 'random'] else v",
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": '📅 Введите дату (пример: 18.05.2026)',
                                    "text_config": {
                                        "font": "sf_pro_text_regular",
                                        "size": 22,
                                        "color": (255, 255, 255),
                                        "pos": (63, 594),
                                        "align": "left",
                                    },
                                },
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 13:23) (24-часовой формат)',
                                    "text_config": {
                                        "font": "sf_pro_text_regular",
                                        "size": 22,
                                        "color": (255, 255, 255),
                                        "pos": (63, 621),
                                        "align": "left",
                                        "template": '{time} Hs.',
                                    },
                                },
                                {
                                    "key": "_blur_mask",
                                    "prompt": "",
                                    "text_config": {"blur_area": (167, 528, 207, 548)},
                                },
                            ],
                            "banks": ["ATLAS", "SOLAR", "GNB"],
                            "date_format": "py3",
                            "name_format": "py_fio",
                        },
                    },
                }
            },
        },
        "qr": {"label": "📱 Paraguay QR", "sections": {}},
        "support": {"label": "🎧 Paraguay Поддержка", "sections": {}},
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
                                    "prompt": '💰 Введите валюту (пример: ETH)',
                                    "text_config": {
                                        "font": "roboto_cond_med",
                                        "size": 70,
                                        "color": (251, 251, 251),
                                        "pos": (370, 800),
                                        "anchor": "ls",
                                        "template": '{currency}USDT | Sin límite de tiempo',
                                    },
                                },
                                {
                                    "key": "long_short",
                                    "prompt": '📈 Введите Long/Short',
                                    "text_config": {
                                        "font": "roboto_cond_reg",
                                        "size": 60,
                                        "pos": (370, 883),
                                        "anchor": "ls",
                                        "color_eval": "lambda v: (95, 166, 106) if v.lower() == 'long' else (212, 72, 92)",
                                    },
                                },
                                {
                                    "key": "x_amount",
                                    "prompt": '✖️ Введите количество X-са (пример: 100X)',
                                    "text_config": {
                                        "font": "roboto_cond_reg",
                                        "size": 60,
                                        "color": (118, 119, 123),
                                        "pos": (600, 883),
                                        "anchor": "ls",
                                        "template_eval": "lambda v: str(v).upper().rstrip('X').strip() + 'X'",
                                    },
                                },
                                {
                                    "key": "percentage",
                                    "prompt": '📈 Введите процент (пример: +1,044.86)',
                                    "text_config": {
                                        "font": "roboto_cond_semibold",
                                        "size": 159,
                                        "pos": (370, 1057),
                                        "anchor": "ls",
                                        "color_eval": "lambda v: (95, 166, 106) if str(v).startswith('+') else (212, 72, 92)",
                                        "template": "{percentage}%",
                                        "special_number_sizes": 79,
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (пример: 18,045 или -18,045)',
                                    "text_config": {
                                        "font": "roboto_cond_med",
                                        "size": 80,
                                        "color": (95, 166, 106, 153),
                                        "color_eval": "lambda v: (212, 72, 92, 153) if str(v).startswith('-') else (95, 166, 106, 153)",
                                        "pos": (370, 1182),
                                        "anchor": "ls",
                                        "template_eval": "lambda v: ('-Gs. ' if str(v).startswith('-') else '+Gs. ') + _format_number_comma(str(v)).lstrip('-').lstrip()",
                                        "special_number_sizes": 70,
                                        "space_size": 40,
                                    },
                                },
                            ],
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "raw",
                            "name_format": "py_fio",
                        }
                    },
                }
            },
        },
        "payment": {
            "label": "💳 Оплата",
            "sections": {
                "payment_main": {
                    "label": "Оплата",
                    "items": {
                        "payment1_py": {
                            "label": "Оплата Парагвай",
                            "asset": "assets/Paraguay/Оплата/PAYMENT.jpg",
                            "preview": "assets/Paraguay/Preview/Оплата/PAYMENT_prew.jpg",
                            "fields": [
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 10:00)',
                                    "text_config": {
                                        "pos": (640, 646),
                                        "align": "center",
                                        "color": (41, 41, 41),
                                        "font": "montserrat_bold",
                                        "size": 76,
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": '🏦 Введите название банка (пример: ATLAS)',
                                    "text_config": {
                                        "pos": (307, 1187),
                                        "align": "left",
                                        "color": (19, 20, 21),
                                        "font": "montserrat_medium",
                                        "size": 66,
                                    },
                                },
                                {
                                    "key": "fullname",
                                    "prompt": '✏️ Введите ФИО (пример: Ivanov Ivan Ivanovich)',
                                    "text_config": {
                                        "pos": (306, 1420),
                                        "align": "left",
                                        "color": (19, 20, 21),
                                        "font": "montserrat_medium",
                                        "size": 66,
                                    },
                                },
                                {
                                    "key": "account",
                                    "prompt": '🔢 Введите Номер счета (11 символов)',
                                    "text_config": {
                                        "pos": (312, 1667),
                                        "align": "left",
                                        "color": (19, 20, 21),
                                        "font": "montserrat_medium",
                                        "size": 66,
                                        "blur_area": (308, 1678, 795, 1738),
                                        "blur_radius": 15,
                                    },
                                },
                            ],
                            "banks": [
                                "ATLAS",
                                "CONTINENTAL",
                                "SOLAR",
                                "INTERFISA",
                                "SUDAMERIS",
                                "GNB",
                                "familiar",
                                "interfisa",
                            ],
                            "date_format": "raw",
                            "name_format": "py_fio",
                        }
                    },
                }
            },
        },
        "fire": {"label": "🔥 Paraguay FIRE", "sections": {}},
    },
}
