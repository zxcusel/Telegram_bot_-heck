GEO_ENTRY = {
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
                                    "prompt": '✏️ Введите ФИО (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "font": "montserrat",
                                        "size": 36,
                                        "color": (0, 0, 0),
                                        "pos": (100, 120),
                                    },
                                }
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "fd_proof2_pe": {
                            "label": "Peru FD 2",
                            "asset": "assets/Peru/FD/proofs/psd2.png",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "font": "montserrat",
                                        "size": 36,
                                        "color": (0, 0, 0),
                                        "pos": (100, 120),
                                    },
                                }
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "fd_proof3_pe": {
                            "label": "Peru FD 3",
                            "asset": "assets/Peru/FD/proofs/psd3.png",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "font": "montserrat",
                                        "size": 36,
                                        "color": (0, 0, 0),
                                        "pos": (100, 120),
                                    },
                                }
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                    },
                }
            },
        },
        "rd": {
            "label": "📁 Peru RD",
            "sections": {
                "rd_main": {
                    "label": "Peru RD",
                    "items": {
                        "rd1": {
                            "label": "Peru RD 1",
                            "asset": "assets/Peru/RD/rd1.png",
                            "preview": "assets/Peru/Prew/RD1_prew.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите Фамилия Имя (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "area": (1250, 700, 2780, 925),
                                        "line_spacing": 1.4,
                                        "segments": [
                                            {
                                                "text": 'Su pago al cliente ',
                                                "font": "montserrat",
                                                "size": 46,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "montserrat",
                                                "size": 46,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": ' por un monto de ',
                                                "font": "montserrat",
                                                "size": 46,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": 'S/. 17,811.00',
                                                "font": "montserrat",
                                                "size": 46,
                                                "color": (0, 255, 84),
                                            },
                                            {
                                                "text": ' ha sido bloqueado temporalmente. Para retirar los fondos de la plataforma a la cuenta del beneficiario, su cliente está obligado a pagar una tarifa de ',
                                                "font": "montserrat",
                                                "size": 46,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": 'S/. 567.00.',
                                                "font": "montserrat",
                                                "size": 46,
                                                "color": (255, 0, 0),
                                            },
                                        ],
                                    },
                                }
                            ],
                            "banks": [
                                "Banco Mercantil Santa Cruz",
                                "Banco Fie",
                                "Banco Bisa",
                                "Banco Union",
                                "Banco Económico",
                                "Banco Nacional de Bolivia",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd2_pe": {
                            "label": "Peru RD 2",
                            "asset": "assets/Peru/RD/rd2.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите Фамилия Имя (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "font": "montserrat",
                                        "size": 30,
                                        "color": (57, 62, 67),
                                        "template": 'Cuenta bancaria del cliente {name}.',
                                        "area": (2235, 1420, 3050, 1460),
                                        "line_spacing": 1.2,
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (рекомендуется 809)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_body_line1",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (2240, 490, 2992, 540),
                                        "segments": [
                                            {
                                                "text": 'Es necesario pagar una tarifa por la',
                                                "font": "montserrat_light",
                                                "size": 44,
                                                "color": (255, 255, 255),
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
                                                "text": 'conversión de ',
                                                "font": "montserrat_light",
                                                "size": 44,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "USDT",
                                                "font": "montserrat_medium",
                                                "size": 44,
                                                "color": (136, 255, 164),
                                            },
                                            {
                                                "text": ' a ',
                                                "font": "montserrat_light",
                                                "size": 44,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "PEN.",
                                                "font": "montserrat_medium",
                                                "size": 44,
                                                "color": (254, 68, 92),
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
                                                "text": 'Importe de la tarifa: ',
                                                "font": "montserrat_light",
                                                "size": 44,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": 'S/. {amount}',
                                                "font": "montserrat_medium",
                                                "size": 44,
                                                "color": (255, 13, 13),
                                                "format_number_comma": True,
                                            },
                                            {
                                                "text": ".",
                                                "font": "montserrat_light",
                                                "size": 44,
                                                "color": (255, 255, 255),
                                            },
                                        ],
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd3_pe": {
                            "label": "Peru RD 3",
                            "asset": "assets/Peru/RD/rd3.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Nilda Mamani Apaza)',
                                    "text_config": {
                                        "font": "times_bold",
                                        "size": 59,
                                        "color": (0, 0, 0),
                                        "pos": (68, 474),
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
                                    "prompt": '💰 Введите сумму (рекомендуется 1 165)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_greeting",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (69, 1230, 2412, 1350),
                                        "segments": [
                                            {
                                                "text": "Estimad{gender} ",
                                                "font": "times_roman",
                                                "size": 59,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": "{name}:",
                                                "font": "times_bold",
                                                "size": 59,
                                                "color": (0, 0, 0),
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
                                                "text": """Le informamos acerca de una condición importante relacionada con la retirada de fondos a
la cuenta bancaria que usted indicó. El pago estará disponible únicamente después de
realizar el abono por servicios por un importe de """,
                                                "font": "times_roman",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": 'S/. {amount}',
                                                "font": "times_bold",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                                "format_number": True,
                                            },
                                            {
                                                "text": """. Le rogamos efectuar dicho
pago a la mayor brevedad; tras su confirmación y el procesamiento por parte de nuestros
departamentos, recibirá inmediatamente en su cuenta bancaria la suma total de """,
                                                "font": "times_roman",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": 'S/. 17 811',
                                                "font": "times_bold",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": ".",
                                                "font": "times_roman",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                        ],
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd4_pe": {
                            "label": "Peru RD 4",
                            "asset": "assets/Peru/RD/rd4.png",
                            "preview": "assets/Peru/Prew/RD4_prew.jpg",
                            "fields": [
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 10:00) (24-часовой формат)',
                                    "text_config": {
                                        "font": "sf_pro_bold",
                                        "size": 34,
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
                                            {
                                                "text": 'Para una ejecución exitosa y segura del pago a su cliente ',
                                                "font": "sf_pro",
                                                "size": 30,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "sf_pro",
                                                "size": 30,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": ', es necesario que abone el proceso de segregación por un monto de ',
                                                "font": "sf_pro",
                                                "size": 30,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": 'S/. 2.258.',
                                                "font": "sf_pro",
                                                "size": 30,
                                                "color": (255, 0, 0),
                                            },
                                            {
                                                "text": """

""",
                                                "font": "sf_pro",
                                                "size": 30,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": 'Una vez abonada la segregación, todo el dinero se acreditará automáticamente en la cuenta de su cliente.',
                                                "font": "sf_pro",
                                                "size": 30,
                                                "color": (255, 255, 255),
                                            },
                                        ],
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd5_pe": {
                            "label": "Peru RD 5",
                            "asset": "assets/Peru/RD/rd5.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Nilda Mamani Apaza)',
                                    "text_config": {
                                        "font": "times_bold",
                                        "size": 59,
                                        "color": (0, 0, 0),
                                        "pos": (68, 474),
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
                                    "prompt": '💰 Введите сумму (рекомендуется 739)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_greeting",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (69, 1230, 2412, 1350),
                                        "segments": [
                                            {
                                                "text": "Estimad{gender} ",
                                                "font": "times_roman",
                                                "size": 59,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": "{name}:",
                                                "font": "times_bold",
                                                "size": 59,
                                                "color": (0, 0, 0),
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
                                                "text": 'En el sistema figura un pago pendiente por concepto de prima de seguro por ',
                                                "font": "times_roman",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": 'S/. {amount}',
                                                "font": "times_bold",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                                "format_number": True,
                                            },
                                            {
                                                "text": ', necesario para activar las garantías y el acceso completo a las funciones de protección. Le rogamos efectuar dicho pago a través de los métodos de recarga disponibles. Tras la confirmación del pago, se restaurará el acceso a los retiros y podrá iniciar la transferencia del monto total de ',
                                                "font": "times_roman",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": 'S/. 17 811',
                                                "font": "times_bold",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": ' a la cuenta bancaria indicada.',
                                                "font": "times_roman",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                        ],
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd6_pe": {
                            "label": "Peru RD 6",
                            "asset": "assets/Peru/RD/rd6.jpg",
                            "fields": [
                                {
                                    "key": "date",
                                    "prompt": "📅 Дата 1 (пример: Fr 01/01)",
                                    "text_config": {
                                        "font": "opensans",
                                        "size": 14,
                                        "color": (44, 44, 44),
                                        "area": (540, 210, 613, 222),
                                    },
                                },
                                {
                                    "key": "date2",
                                    "prompt": '📅 Дата 2 (пример: Fr 01/01/2026)',
                                    "text_config": {
                                        "font": "opensans",
                                        "size": 14,
                                        "color": (147, 147, 147),
                                        "area": (1730, 236, 1845, 247),
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
                                    "prompt": '💰 Введите сумму налога (рекомендуется 1 246)',
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
                                            {
                                                "text": 'Estimado José García!',
                                                "font": "arial_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": """

""",
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": 'Ha realizado un intercambio de USDT por un monto de ',
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": 'S/. 17.811',
                                                "font": "arial_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": ' para el pago a su cliente.',
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": """

""",
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": 'Detalles de la transacción:',
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "\n",
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": '  ID de la transacción: ',
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "9489-4921-3991-002",
                                                "font": "arial_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "\n",
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": '  Banco del destinatario: ',
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "{bank}",
                                                "font": "arial_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "\n",
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": '  Monto a recibir: ',
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": 'S/. 17.811',
                                                "font": "arial_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "\n",
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": '  Monto en USDT: ',
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "4.690",
                                                "font": "arial_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "\n",
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": '  Hora de la transacción: ',
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "{tx_time}",
                                                "font": "arial_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": """

""",
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": 'Su cliente, ',
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": ', está obligado a pagar el 7% de impuesto sobre el intercambio de criptomonedas, es decir, ',
                                                "font": "arial",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": 'S/. {commission}.',
                                                "font": "arial_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                                "format_number_dot": True,
                                            },
                                        ],
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd7_pe": {
                            "label": "Peru RD 7",
                            "asset": "assets/Peru/RD/rd7.jpg",
                            "fields": [
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 10:00) (24-часовой формат)',
                                    "text_config": {
                                        "font": "sf_pro_bold",
                                        "size": 32,
                                        "color": (255, 255, 255),
                                        "area": (100, 33, 200, 67),
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": '🏦 Введите название банка (пример: YAPE)',
                                    "text_config": {
                                        "font": "sf_pro_medium",
                                        "size": 29,
                                        "color": (0, 0, 0),
                                        "area": (398, 850, 710, 880),
                                    },
                                },
                                {
                                    "key": "fullname",
                                    "prompt": '✏️ Введите ФИО (пример: Ivanov Ivan Ivanovich)',
                                    "text_config": {
                                        "font": "sf_pro_medium",
                                        "size": 29,
                                        "color": (0, 0, 0),
                                        "area": (398, 913, 710, 944),
                                    },
                                },
                                {
                                    "key": "number",
                                    "prompt": '🔢 Введите номер счёта (пример: 1234567890)',
                                    "text_config": {
                                        "font": "sf_pro_medium",
                                        "size": 29,
                                        "color": (0, 0, 0),
                                        "area": (398, 994, 663, 1025),
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (например: 1250)',
                                    "text_config": {
                                        "font": "sf_pro_medium",
                                        "size": 29,
                                        "color": (0, 0, 0),
                                        "area": (395, 1206, 710, 1242),
                                        "template": 'S/. {amount}.00',
                                        "format_number_comma": True,
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd8_pe": {
                            "label": "Peru RD 8",
                            "asset": "assets/Peru/RD/rd8.png",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "font": "montserrat",
                                        "size": 36,
                                        "color": (0, 0, 0),
                                        "pos": (100, 120),
                                    },
                                }
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd9_pe": {
                            "label": "Peru RD 9",
                            "asset": "assets/Peru/RD/rd9.png",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "font": "montserrat",
                                        "size": 36,
                                        "color": (0, 0, 0),
                                        "pos": (100, 120),
                                    },
                                }
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
                        "rd10_pe": {
                            "label": "Peru RD 10",
                            "asset": "assets/Peru/RD/rd10.png",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "font": "montserrat",
                                        "size": 36,
                                        "color": (0, 0, 0),
                                        "pos": (100, 120),
                                    },
                                }
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        },
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
                                    "prompt": '🕐 Введите время устройства (пример: 10:45) (24-часовой формат)',
                                    "text_config": {
                                        "font": "sf_pro_semibold",
                                        "size": 25,
                                        "color": (0, 0, 0),
                                        "pos": (75, 26),
                                    },
                                },
                                {
                                    "key": "interval",
                                    "prompt": '⏳ Введите промежуток (пример: 04.23 - 04.23)',
                                    "text_config": {
                                        "font": "sf_pro_semibold",
                                        "size": 17,
                                        "color": (165, 166, 168),
                                        "pos": (23, 272),
                                        "template": "2026.{interval}",
                                    },
                                },
                                {
                                    "key": "date1",
                                    "prompt": "📅 Дата 1 (пример: 04-23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold",
                                        "size": 17.5,
                                        "color": (165, 166, 168),
                                        "pos": (23, 518),
                                        "template": '2026-{date1} 09:01:04',
                                    },
                                },
                                {
                                    "key": "date2",
                                    "prompt": "📅 Дата 2 (пример: 04-23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold",
                                        "size": 17.5,
                                        "color": (165, 166, 168),
                                        "pos": (23, 644),
                                        "template": '2026-{date2} 09:01:04',
                                    },
                                },
                                {
                                    "key": "date3",
                                    "prompt": "📅 Дата 3 (пример: 04-23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold",
                                        "size": 17.5,
                                        "color": (165, 166, 168),
                                        "pos": (23, 800),
                                        "template": '2026-{date3} 09:01:04',
                                    },
                                },
                                {
                                    "key": "date4",
                                    "prompt": "📅 Дата 4 (пример: 04-23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold",
                                        "size": 17.5,
                                        "color": (165, 166, 168),
                                        "pos": (23, 955),
                                        "template": '2026-{date4} 09:01:04',
                                    },
                                },
                                {
                                    "key": "date5",
                                    "prompt": "📅 Дата 5 (пример: 04-23)",
                                    "text_config": {
                                        "font": "sf_pro_semibold",
                                        "size": 17.5,
                                        "color": (165, 166, 168),
                                        "pos": (23, 1085),
                                        "template": '2026-{date5} 09:01:04',
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        }
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
                            "preview": "assets/Peru/Preview/Чек/Check1_prew.jpg",
                            "fields": [
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (пример: 120)',
                                    "text_config": {
                                        "font": "araboto_bold",
                                        "size": 93,
                                        "color": (63, 48, 79),
                                        "pos": (124, 324),
                                        "format_number_none": True,
                                    },
                                },
                                {
                                    "key": "fullname",
                                    "prompt": '✏️ Введите ФИО получателя (пример: Dennis Fabricio Estrada Garcia)',
                                    "text_config": {
                                        "font": "araboto_medium",
                                        "size": 36,
                                        "color": (37, 34, 41),
                                        "pos": (59, 432),
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": '📅 Введите дату (пример: 22 abr. 2026)',
                                    "text_config": {
                                        "font": "araboto",
                                        "size": 26,
                                        "color": (104, 102, 105),
                                        "pos": (96, 487),
                                    },
                                },
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 04:07 p.m.)',
                                    "text_config": {
                                        "font": "araboto",
                                        "size": 26,
                                        "color": (104, 102, 105),
                                        "pos": (315, 487),
                                    },
                                },
                                {
                                    "key": "account",
                                    "prompt": '🔢 Введите три цифры карты (пример: 266)',
                                    "text_config": {
                                        "font": "araboto",
                                        "size": 25,
                                        "color": (37, 34, 41),
                                        "pos": (553, 638),
                                    },
                                },
                                {
                                    "key": "transaction",
                                    "prompt": '🔢 Введите номер транзакции (пример: 01750451)',
                                    "text_config": {
                                        "font": "araboto",
                                        "size": 25,
                                        "color": (37, 34, 41),
                                        "pos": (481, 727),
                                    },
                                },
                                {
                                    "key": "bank",
                                    "prompt": '🏦 Введите название банка (пример: BCP)',
                                    "text_config": {
                                        "font": "araboto",
                                        "size": 26,
                                        "color": (37, 34, 41),
                                        "pos": (596, 680),
                                        "align": "right",
                                        "cover_area": (530, 678, 610, 710),
                                        "cover_color": (255, 255, 255),
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "es_long",
                            "name_format": "raw",
                        },
                        "check2_pe": {
                            "label": "Peru Чек 2",
                            "asset": "assets/Peru/Чек/Check2.jpg",
                            "preview": "assets/Peru/Preview/Чек/Check2_prew.jpg",
                            "fields": [
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (пример: 22)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "date",
                                    "prompt": '📅 Введите дату (пример: 22.04.2026)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 09:47) (24-часовой формат)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "fullname",
                                    "prompt": '✏️ ФИО получателя (пример: Dennis Fabricio Estrada G.)',
                                    "text_config": {
                                        "font": "flexo_bold",
                                        "size": 33,
                                        "color": (32, 36, 48),
                                        "area": (100, 478, 629, 515),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "sender_name",
                                    "prompt": "✏️ ФИО отправителя",
                                    "text_config": {
                                        "font": "flexo_bold",
                                        "size": 33,
                                        "color": (32, 36, 48),
                                        "pos": (628, 894),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "card_recipient",
                                    "prompt": '💳 Последние 4 цифры карты получателя (пример: 3899)',
                                    "text_config": {
                                        "font": "flexo_demibold",
                                        "size": 32,
                                        "color": (103, 107, 110),
                                        "area": (300, 519, 629, 555),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "card_sender",
                                    "prompt": '💳 Последние 4 цифры карты отправителя (пример: 4013)',
                                    "text_config": {
                                        "font": "flexo_demibold",
                                        "size": 32,
                                        "color": (103, 107, 110),
                                        "area": (300, 936, 629, 972),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "operation",
                                    "prompt": '🔢 Номер операции (пример: 01097102)',
                                    "text_config": {
                                        "font": "flexo_bold",
                                        "size": 32,
                                        "color": (42, 44, 59),
                                        "area": (300, 1046, 629, 1082),
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
                                            {
                                                "text": 'S/ {amount}.00',
                                                "font": "flexo_medium",
                                                "size": 87,
                                                "color": (7, 41, 138),
                                                "format_number": True,
                                            }
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
                                        "template": '{date} - {time}',
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
                                            {
                                                "text": 'S/ {amount}.00',
                                                "font": "flexo_bold",
                                                "size": 32,
                                                "color": (0, 0, 0),
                                                "format_number": True,
                                            }
                                        ],
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "es_slash",
                            "name_format": "raw",
                        },
                        "check3_pe": {
                            "label": "Peru Чек 3",
                            "asset": "assets/Peru/Чек/Check3.jpg",
                            "preview": "assets/Peru/Preview/Чек/Check3_prew.jpg",
                            "fields": [
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (пример: 169)',
                                    "text_config": {
                                        "area": (0, 353, 729, 470),
                                        "line_spacing": 1.0,
                                        "segments_align": "center",
                                        "segments": [
                                            {
                                                "text": "S/ ",
                                                "font": "geometria_bold",
                                                "size": 45,
                                                "color": (18, 170, 80),
                                            },
                                            {
                                                "text": "{amount}",
                                                "font": "geometria_bold",
                                                "size": 70,
                                                "color": (18, 170, 80),
                                                "format_number": True,
                                            },
                                            {
                                                "text": ".00",
                                                "font": "geometria_bold",
                                                "size": 70,
                                                "color": (18, 170, 80),
                                            },
                                        ],
                                    },
                                },
                                {
                                    "key": "fullname",
                                    "prompt": '✏️ Введите ФИО получателя',
                                    "text_config": {
                                        "font": "geometria_medium",
                                        "size": 35,
                                        "color": (19, 24, 27),
                                        "pos": (90, 558),
                                    },
                                },
                                {
                                    "key": "date",
                                    "prompt": '📅 Введите дату (пример: 19 Abr 2026)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 12:32 PM)',
                                    "text_config": {
                                        "font": "geometria_medium",
                                        "size": 35,
                                        "color": (19, 24, 27),
                                        "pos": (91, 856),
                                        "template": '{date}   {time}',
                                    },
                                },
                                {
                                    "key": "operation",
                                    "prompt": '🔢 Номер операции (пример: 02688276)',
                                    "text_config": {
                                        "font": "geometria_medium",
                                        "size": 35,
                                        "color": (19, 24, 27),
                                        "pos": (90, 973),
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "es_short",
                            "name_format": "raw",
                        },
                        "check4_pe": {
                            "label": "Peru Чек 4",
                            "asset": "assets/Peru/Чек/Check4.jpg",
                            "preview": "assets/Peru/Preview/Чек/Check4_prew.jpg",
                            "fields": [
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (пример: 22)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "date",
                                    "prompt": '📅 Введите дату (пример: 22.04.2026)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "time",
                                    "prompt": '🕐 Введите время (пример: 09:47) (24-часовой формат)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "fullname",
                                    "prompt": '✏️ ФИО получателя (пример: Shumi Claudia Aro C.)',
                                    "text_config": {
                                        "font": "flexo_medium",
                                        "size": 22,
                                        "color": (32, 36, 48),
                                        "area": (100, 543, 543, 580),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "sender_name",
                                    "prompt": "✏️ ФИО отправителя",
                                    "text_config": {
                                        "font": "flexo_medium",
                                        "size": 22,
                                        "color": (32, 36, 48),
                                        "pos": (543, 843),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "card_recipient",
                                    "prompt": '💳 Последние 4 цифры карты получателя (пример: 3899)',
                                    "text_config": {
                                        "font": "flexo_medium",
                                        "size": 22,
                                        "color": (103, 107, 110),
                                        "area": (250, 571, 543, 607),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "card_sender",
                                    "prompt": '💳 Последние 4 цифры карты отправителя (пример: 4013)',
                                    "text_config": {
                                        "font": "flexo_medium",
                                        "size": 22,
                                        "color": (103, 107, 110),
                                        "area": (250, 873, 543, 972),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "operation",
                                    "prompt": '🔢 Номер операции (пример: 02043395)',
                                    "text_config": {
                                        "font": "flexo_medium",
                                        "size": 22,
                                        "color": (42, 44, 59),
                                        "area": (250, 956, 543, 1082),
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
                                            {
                                                "text": 'S/ {amount}.00',
                                                "font": "flexo_medium",
                                                "size": 65,
                                                "color": (7, 41, 138),
                                                "format_number": True,
                                            }
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
                                        "template": '{date} - {time}',
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
                                            {
                                                "text": 'S/ {amount}.00',
                                                "font": "flexo_medium",
                                                "size": 22,
                                                "color": (64, 66, 70),
                                                "format_number": True,
                                            }
                                        ],
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "es_slash",
                            "name_format": "raw",
                        },
                    },
                }
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
                                    "prompt": '⏱ Введите таймер в формате MM:SS (пример: 59:48)',
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
                                    "prompt": '🖼 Отправьте QR-изображение (квадрат 1:1)',
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
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        }
                    },
                }
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
                                    "prompt": '✉️ Введите текст первого сообщения (синий пузырь, справа)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "msg2",
                                    "prompt": '✉️ Введите текст второго сообщения (тёмный пузырь, слева)',
                                    "text_config": {"collect_only": True},
                                },
                            ],
                            "render_mode": "support_bubbles",
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        }
                    },
                }
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
                                        "template_eval": "lambda v: ('-S/. ' if str(v).startswith('-') else '+S/. ') + _format_number_comma(str(v)).lstrip('-').lstrip()",
                                        "special_number_sizes": 70,
                                        "space_size": 40,
                                    },
                                },
                            ],
                            "banks": [
                                "BCP",
                                "BBVA",
                                "Scotiabank",
                                "Interbank",
                                "Banco de la Nación",
                                "Banco Falabella Perú",
                            ],
                            "date_format": "raw",
                            "name_format": "raw",
                        }
                    },
                }
            },
        },
    },
}
