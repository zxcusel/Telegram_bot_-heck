GEO_ENTRY = {
    "label": "🇺🇾 Uruguay",
    "catalog": {
        "fd": {"label": "📁 Uruguay FD", "sections": {}},
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
                                                "text": '$U 168,286',
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
                                                "text": '$U {commission}.',
                                            },
                                        ],
                                    },
                                },
                                {
                                    "key": "commission",
                                    "prompt": '💰 Введите сумму (рекомендуется 6720)',
                                    "text_config": {"collect_only": True},
                                },
                            ],
                            "label": "Uruguay RD 1",
                            "preview": "assets/Uruguay/Preview/RD/RD1_prew.jpg",
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd2_uy": {
                            "asset": "assets/Uruguay/RD/rd2.jpg",
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
                                    "prompt": '💰 Введите сумму (рекомендуется 10920)',
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
                                                "text": 'Importe de la tarifa: ',
                                            },
                                            {
                                                "color": (255, 13, 13),
                                                "font": "montserrat_medium",
                                                "format_number_comma": True,
                                                "size": 44,
                                                "text": '$U {amount}',
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
                            "label": "Uruguay RD 2",
                            "preview": "assets/Uruguay/Preview/RD/RD2_prew.jpg",
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd3_uy": {
                            "asset": "assets/Uruguay/RD/rd3.jpg",
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
                                    "prompt": '💰 Введите сумму (рекомендуется 13860)',
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
                                                "text": '$U {amount}',
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
                                                "text": '$U 168 286',
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
                            "label": "Uruguay RD 3",
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd4_uy": {
                            "asset": "assets/Uruguay/RD/rd4.jpg",
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
                                    "prompt": '💰 Введите сумму (рекомендуется 7980)',
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
                                                "text": '$U {amount}.',
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
                            "label": "Uruguay RD 4",
                            "preview": "assets/Uruguay/Preview/RD/RD4_prew.jpg",
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd5_uy": {
                            "asset": "assets/Uruguay/RD/rd5.jpg",
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
                                    "prompt": '💰 Введите сумму (рекомендуется 23520)',
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
                                                "text": '$U {amount}',
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
                                                "text": '$U 169 286',
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
                            "label": "Uruguay RD 5",
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
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
                                    "prompt": '💰 Введите сумму (рекомендуется 33600)',
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
                                                "text": 'U$ 168,286',
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
                                                "text": 'U$ 168,286',
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
                                                "text": '$U {commission}.',
                                            },
                                        ],
                                    },
                                },
                            ],
                            "label": "Uruguay RD 6",
                            "preview": "assets/Uruguay/Preview/RD/RD6_prew.jpg",
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd7_uy": {
                            "asset": "assets/Uruguay/RD/rd7.jpg",
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
                                    "prompt": '💰 Введите сумму (рекомендуется 29400)',
                                    "text_config": {
                                        "area": (395, 1206, 710, 1242),
                                        "color": (0, 0, 0),
                                        "font": "sf_pro_medium",
                                        "format_number_comma": True,
                                        "size": 29,
                                        "template": '$U {amount}',
                                    },
                                },
                            ],
                            "label": "Uruguay RD 7",
                            "preview": "assets/Uruguay/Preview/RD/RD7_prew.jpg",
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
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
                                    "prompt": "✏️ Введите Имя получателя",
                                    "text_config": {
                                        "font": "alte_regular",
                                        "size": 19,
                                        "color": (46, 49, 54),
                                        "pos": (92, 67),
                                        "align": "left",
                                        "template_eval": "lambda v: f'Transferiste a {str(v).upper()}'",
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите Сумму (пример: 1950)',
                                    "text_config": {
                                        "font": "alte_bold",
                                        "size": 40,
                                        "color": (54, 57, 74),
                                        "pos": (122, 97),
                                        "align": "left",
                                        "template": "{amount},00",
                                        "format_number_dot": True,
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": '📅 Введите дату (пример: 20.04.2026)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 12:20) (24-часовой формат)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "datetime_display",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "alte_regular",
                                        "size": 19,
                                        "color": (171, 171, 179),
                                        "pos": (92, 145),
                                        "align": "left",
                                        "template": '{date} {time}',
                                    },
                                },
                                {
                                    "key": "comment",
                                    "prompt": '💬 Введите Комментарий (пример: PAGO)',
                                    "text_config": {
                                        "font": "arial_italic",
                                        "size": 19,
                                        "color": (57, 56, 68),
                                        "pos": (107, 225),
                                        "align": "left",
                                    },
                                },
                                {
                                    "key": "sender_bank",
                                    "prompt": '🔧 Введите Банк отправителя (пример: MIDINERO)',
                                    "text_config": {
                                        "font": "alte_bold",
                                        "size": 21.5,
                                        "color": (32, 36, 56),
                                        "pos": (503, 293),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "acc_2",
                                    "prompt": '🔢 Введите Счет отправителя',
                                    "text_config": {
                                        "font": "alte_regular",
                                        "size": 21,
                                        "color": (34, 37, 44),
                                        "pos": (504, 483),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "payer_2",
                                    "prompt": '👤 Введите ФИО отправителя',
                                    "text_config": {
                                        "font": "alte_regular",
                                        "size": 21,
                                        "color": (34, 37, 44),
                                        "pos": (503, 514),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "service",
                                    "prompt": '🔧 Введите Банк получателя (пример: MIDINERO)',
                                    "text_config": {
                                        "font": "alte_bold",
                                        "size": 21.5,
                                        "color": (32, 36, 56),
                                        "pos": (503, 434),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "acc_1",
                                    "prompt": '🔢 Введите Счет получателя',
                                    "text_config": {
                                        "font": "alte_regular",
                                        "size": 21,
                                        "color": (34, 37, 44),
                                        "pos": (504, 342),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "payer_1",
                                    "prompt": '👤 Введите ФИО получателя',
                                    "text_config": {
                                        "font": "alte_regular",
                                        "size": 21,
                                        "color": (34, 37, 44),
                                        "pos": (503, 373),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "ref_num",
                                    "prompt": '📄 Введите Справочный номер',
                                    "text_config": {
                                        "font": "alte_regular",
                                        "size": 21,
                                        "color": (34, 37, 44),
                                        "pos": (499, 634),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "alte_regular",
                                        "size": 21,
                                        "color": (34, 37, 44),
                                        "pos": (503, 769),
                                        "align": "right",
                                        "template": '$ {amount},00',
                                        "format_number_dot": True,
                                    },
                                },
                                {
                                    "key": "_blur_1",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (391, 486, 469, 506),
                                        "blur_radius": 15,
                                    },
                                },
                                {
                                    "key": "_blur_2",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (391, 345, 469, 364),
                                        "blur_radius": 15,
                                    },
                                },
                            ],
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "uy",
                            "name_format": "raw",
                        },
                        "check2_uy": {
                            "label": "🧾 Чек 2",
                            "asset": "assets/Uruguay/Чек/Check2.jpg",
                            "preview": "assets/Uruguay/Preview/Чек/Check2_prew.jpg",
                            "fields": [
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (пример: 1500)',
                                    "text_config": {
                                        "font": "sf_pro_text_bold",
                                        "size": 54,
                                        "color": (47, 47, 47),
                                        "pos": (385, 189),
                                        "align": "center",
                                        "template": "{amount},00",
                                        "format_number_dot": True,
                                        "prefix": "UYU",
                                        "prefix_size": 37,
                                        "prefix_y_offset": 10,
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sf_pro_text_bold",
                                        "size": 24,
                                        "color": (8, 8, 8),
                                        "pos": (725, 870),
                                        "align": "right",
                                        "template": 'UYU {amount},00',
                                        "format_number_dot": True,
                                    },
                                },
                                {
                                    "key": "sender_acc",
                                    "prompt": '🔢 Введите Номер отправителя (10 цифр)',
                                    "text_config": {
                                        "font": "sf_pro_text_bold",
                                        "size": 28,
                                        "color": (8, 8, 8),
                                        "pos": (385, 351),
                                        "align": "center",
                                        "template": 'CA UYU {sender_acc}',
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": '🏦 Введите Банк получателя (пример: Itaú)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "receiver_acc",
                                    "prompt": '🔢 Введите Номер получателя (7 цифр)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_bank_acc",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sf_pro_text_bold",
                                        "size": 28,
                                        "color": (8, 8, 8),
                                        "pos": (385, 451),
                                        "align": "center",
                                        "template": '{bank} {receiver_acc}',
                                    },
                                },
                                {
                                    "key": "name",
                                    "prompt": '👤 Введите получателя (пример: CARD BUE WILF)',
                                    "text_config": {
                                        "font": "sf_pro_text_bold",
                                        "size": 28,
                                        "color": (48, 52, 52),
                                        "pos": (304, 539),
                                        "align": "left",
                                        "max_width": 404,
                                        "template_eval": "lambda v: str(v).upper() if '*' in str(v) else ' '.join(w[:len(w)//2] + '*' * (len(w) - len(w)//2) if len(w) > 1 else w for w in str(v).upper().split())",
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": '📅 Введите дату (пример: 04.01.2026)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 15:23) (24-часовой формат)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_datetime",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sf_pro_text_bold",
                                        "size": 24,
                                        "color": (8, 8, 8),
                                        "pos": (725, 647),
                                        "align": "right",
                                        "template": '{date} {time}',
                                    },
                                },
                                {
                                    "key": "account",
                                    "prompt": "📄 Введите референс",
                                    "text_config": {
                                        "font": "sf_pro_text_bold",
                                        "size": 24,
                                        "color": (8, 8, 8),
                                        "pos": (725, 795),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "_blur_1",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (352, 354, 459, 384),
                                        "blur_radius": 15,
                                    },
                                },
                                {
                                    "key": "_blur_2",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (351, 455, 423, 482),
                                        "blur_radius": 15,
                                    },
                                },
                            ],
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "dot_slash",
                            "name_format": "raw",
                        },
                        "check3_uy": {
                            "label": "🧾 Чек 3",
                            "asset": "assets/Uruguay/Чек/Check3.jpg",
                            "preview": "assets/Uruguay/Preview/Чек/Check3_prew.jpg",
                            "fields": [
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 15:23) (24-часовой формат)',
                                    "text_config": {
                                        "font": "sf_pro_text_bold",
                                        "size": 40,
                                        "color": (8, 8, 8),
                                        "pos": (93, 38),
                                        "align": "left",
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (пример: 1700)',
                                    "text_config": {
                                        "font": "nunito_bold",
                                        "size": 62,
                                        "color": (40, 42, 59),
                                        "pos": (461, 718),
                                        "align": "center",
                                        "template": 'Enviaste UYU {amount},00',
                                        "format_number_dot": True,
                                        "stroke_width": 1,
                                        "stroke_fill": (40, 42, 59),
                                    },
                                },
                                {
                                    "key": "receiver_name",
                                    "prompt": '👤 Введите получателя (пример: VIGN FERR AYR)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "bank",
                                    "prompt": "🏦 Выберите банк:",
                                    "text_config": {"collect_only": True},
                                    "options": [
                                        {"text": "Itaú", "value": "Itaú"},
                                        {"text": "Santander", "value": "Santander"},
                                        {"text": "BBVA", "value": "BBVA"},
                                        {"text": "Scotiabank", "value": "Scotiabank"},
                                        {"text": "Oca blue", "value": 'Oca blue'},
                                    ],
                                },
                                {
                                    "key": "_info_text",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "nunito_medium",
                                        "size": 35,
                                        "color": (43, 43, 52),
                                        "pos": (461, 839),
                                        "align": "center",
                                        "line_spacing": 1.2,
                                        "template_eval": "lambda v, fv: f\"{ str(fv.get('receiver_name','')).upper() if '*' in str(fv.get('receiver_name','')) else ' '.join(w[:3] + '***' for w in str(fv.get('receiver_name','')).upper().split()[:3]) } recibe el dinero en\nsu cuenta {fv.get('bank','')}.\nSi querés podés compartirle el comprobante.\"",
                                        "template": "{_info_text}",
                                    },
                                },
                                {
                                    "key": "network",
                                    "prompt": "📶 Сеть",
                                    "text_config": {
                                        "image_paste": True,
                                        "area": (673, 44, 721, 77),
                                    },
                                },
                                {
                                    "key": "wifi",
                                    "prompt": "🌐 Интернет",
                                    "text_config": {
                                        "image_paste": True,
                                        "area": (738, 46, 778, 77),
                                    },
                                },
                                {
                                    "key": "battery",
                                    "prompt": "🔋 Зарядка",
                                    "text_config": {
                                        "image_paste": True,
                                        "area": (794, 45, 861, 78),
                                    },
                                },
                            ],
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
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
                                        "font": "montserrat_medium",
                                        "size": 27,
                                        "color": (35, 53, 65),
                                        "pos": (836, 535),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "account",
                                    "prompt": "💳 Счет Отправителя",
                                    "text_config": {
                                        "font": "sf_pro_medium",
                                        "size": 28,
                                        "color": (106, 115, 126),
                                        "pos": (835, 590),
                                        "align": "right",
                                        "template": '{account} ($)',
                                    },
                                },
                                {
                                    "key": "receiver_acc",
                                    "prompt": "💳 Счет Получателя",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "receiver_name",
                                    "prompt": "👤 Имя получателя",
                                    "text_config": {
                                        "font": "montserrat_medium",
                                        "size": 27,
                                        "color": (35, 53, 65),
                                        "pos": (835, 684),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": "🏦 Банк",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_bank_text",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sf_pro_medium",
                                        "size": 28,
                                        "color": (106, 115, 126),
                                        "pos": (835, 738),
                                        "align": "right",
                                        "template_eval": "lambda v, fv: fv.get('receiver_acc', '') if fv.get('bank') == 'Oca Blue' else f\"{fv.get('bank', '')} {fv.get('receiver_acc', '')}\"",
                                    },
                                },
                                {
                                    "key": "_bank_img",
                                    "prompt": "",
                                    "text_config": {
                                        "image_paste": True,
                                        "area": (596, 735, 707, 774),
                                        "image_eval": "lambda v, fv: 'assets/Uruguay/Чек/bank/Oca.jpg' if fv.get('bank') == 'Oca Blue' else None",
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Сумма перевода (пример: 6424)',
                                    "text_config": {
                                        "font": "sf_pro",
                                        "size": 37,
                                        "color": (35, 53, 65),
                                        "pos": (835, 851),
                                        "align": "right",
                                        "template": '$ {amount},00',
                                        "format_number_dot": True,
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": '📅 Дата (пример: 18.11.2025)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "time",
                                    "prompt": '🕐 Время (пример: 03:19)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_date_time",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sf_pro_medium",
                                        "size": 28,
                                        "color": (97, 106, 116),
                                        "pos": (62, 1304),
                                        "align": "left",
                                        "template_eval": "lambda v, fv: 'Realizada el ' + fv.get('date', '').split('.')[0] + ' ' + {'01':'enero','02':'febrero','03':'marzo','04':'abril','05':'mayo','06':'junio','07':'julio','08':'agosto','09':'septiembre','10':'octubre','11':'noviembre','12':'diciembre'}.get(fv.get('date', '').split('.')[1] if '.' in fv.get('date', '') else '', '') + '. ' + fv.get('date', '').split('.')[-1] + ' a las ' + fv.get('time', '').lower()",
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": "",
                                    "text_config": {
                                        "font": "sf_pro",
                                        "size": 37,
                                        "color": (35, 53, 65),
                                        "pos": (835, 999),
                                        "align": "right",
                                        "template": '$ {amount},00',
                                        "format_number_dot": True,
                                    },
                                },
                                {
                                    "key": "acc_2",
                                    "prompt": "🔢 Номер счета",
                                    "text_config": {
                                        "font": "sf_pro",
                                        "size": 37,
                                        "color": (35, 53, 65),
                                        "pos": (835, 1442),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "_blur_1",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (666, 594, 737, 622),
                                        "blur_radius": 15,
                                    },
                                },
                                {
                                    "key": "_blur_2",
                                    "prompt": "",
                                    "text_config": {
                                        "blur_area": (707, 742, 783, 769),
                                        "blur_radius": 15,
                                    },
                                },
                            ],
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                    },
                }
            },
        },
        "qr": {"label": "📱 Uruguay QR", "sections": {}},
        "support": {"label": "🎧 Uruguay Поддержка", "sections": {}},
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
                                        "template_eval": "lambda v: ('-$U ' if str(v).startswith('-') else '+$U ') + _format_number_comma(str(v)).lstrip('-').lstrip()",
                                        "special_number_sizes": 70,
                                        "space_size": 40,
                                    },
                                },
                            ],
                            "banks": [
                                "Itaú",
                                "Santander",
                                "BBVA",
                                "Scotiabank",
                                "Oca blue",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        }
                    },
                }
            },
        },
        "fire": {"label": "🔥 Uruguay FIRE", "sections": {}},
    },
}
