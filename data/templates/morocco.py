GEO_ENTRY = {
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
                                    "prompt": '✏️ Введите Фамилия Имя (пример: Nombre Apellido)',
                                    "text_config": {
                                        "area": (815, 700, 3215, 800),
                                        "segments_align": "center_rtl",
                                        "segments": [
                                            {
                                                "text": 'تم توقيف دفعتك للزبون ',
                                                "font": "araboto",
                                                "size": 50,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "araboto",
                                                "size": 56,
                                                "color": (255, 255, 255),
                                                "template_eval": "lambda name='', **kw: name.replace(' ', ' ')",
                                            },
                                            {
                                                "text": ' عن مبلغ ',
                                                "font": "araboto",
                                                "size": 50,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "د.م. ",
                                                "font": "araboto",
                                                "size": 72,
                                                "color": (0, 255, 84),
                                            },
                                            {
                                                "text": "37,485.00",
                                                "font": "myriad_arabic_bold",
                                                "size": 72,
                                                "color": (0, 255, 84),
                                            },
                                            {
                                                "text": ' مؤقتًا.',
                                                "font": "araboto",
                                                "size": 50,
                                                "color": (255, 255, 255),
                                            },
                                        ],
                                    },
                                },
                                {
                                    "key": "line2",
                                    "text_config": {
                                        "area": (815, 792, 3215, 892),
                                        "segments_align": "center_rtl",
                                        "segments": [
                                            {
                                                "text": 'لسحب الأموال من المنصة إلى حساب المستفيد، يجب على زبونك دفع ',
                                                "font": "araboto",
                                                "size": 44,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": 'رسوم قدرها',
                                                "font": "araboto",
                                                "size": 44,
                                                "color": (255, 255, 255),
                                            },
                                        ],
                                    },
                                },
                                {
                                    "key": "commission",
                                    "prompt": '💰 Введите сумму (рекомендуется 1280)',
                                    "text_config": {
                                        "area": (815, 842, 3215, 942),
                                        "segments_align": "center_rtl",
                                        "segments": [
                                            {
                                                "text": "د.م. ",
                                                "font": "araboto",
                                                "size": 80,
                                                "color": (255, 0, 0),
                                            },
                                            {
                                                "text": "{commission}.00",
                                                "font": "myriad_arabic_bold",
                                                "size": 80,
                                                "color": (255, 0, 0),
                                                "format_number_comma": True,
                                            },
                                        ],
                                    },
                                },
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
                        "rd2_ma": {
                            "label": "Morocco RD 2",
                            "asset": "assets/Morocco/RD/rd2.jpg",
                            "preview": "assets/Morocco/Preview/RD/RD2_prew.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": "✏️ Введите Фамилия Имя",
                                    "text_config": {
                                        "area": (1000, 1426, 3021, 1500),
                                        "segments_align": "right",
                                        "segments": [
                                            {
                                                "text": "حساب ",
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (57, 62, 67),
                                            },
                                            {
                                                "text": "بنكي ",
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (57, 62, 67),
                                            },
                                            {
                                                "text": "للزبون ",
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (57, 62, 67),
                                            },
                                            {
                                                "text": ".",
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (57, 62, 67),
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (57, 62, 67),
                                                "template_eval": "lambda name='', **kw: name.replace(' ', ' ')",
                                            },
                                        ],
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": "💰 Введите сумму",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_body",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (2253, 532, 2980, 700),
                                        "segments_align": "right",
                                        "line_spacing": 1.2,
                                        "segments": [
                                            {
                                                "text": """من الضروري دفع رسوم لتحويل
""",
                                                "font": "araboto",
                                                "size": 44,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "MAD.\xa0",
                                                "font": "myriad_arabic_bold",
                                                "size": 44,
                                                "color": (254, 68, 92),
                                            },
                                            {
                                                "text": "إلى\xa0",
                                                "font": "araboto",
                                                "size": 44,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "USDT\n",
                                                "font": "myriad_arabic_bold",
                                                "size": 44,
                                                "color": (136, 255, 164),
                                            },
                                            {
                                                "text": 'مقدار الرسوم: ',
                                                "font": "araboto",
                                                "size": 44,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "د.م.\xa0",
                                                "font": "araboto",
                                                "size": 44,
                                                "color": (255, 13, 13),
                                            },
                                            {
                                                "text": "{amount}",
                                                "font": "myriad_arabic_bold",
                                                "size": 44,
                                                "color": (255, 13, 13),
                                                "format_number_comma": True,
                                            },
                                        ],
                                    },
                                },
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
                        "rd3_ma": {
                            "label": "Morocco RD 3",
                            "asset": "assets/Morocco/RD/rd3.jpg",
                            "preview": "assets/Morocco/Preview/RD/RD3_prew.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Nilda Mamani Apaza)',
                                    "text_config": {
                                        "area": (68, 460, 2412, 560),
                                        "segments_align": "right",
                                        "segments": [
                                            {
                                                "text": 'إشعار لـ ',
                                                "font": "araboto_bold",
                                                "size": 59,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "araboto_bold",
                                                "size": 59,
                                                "color": (0, 0, 0),
                                                "template_eval": "lambda name='', **kw: name.replace(' ', ' ')",
                                            },
                                        ],
                                    },
                                },
                                {
                                    "key": "gender",
                                    "prompt": "👤 Выберите обращение (введите 'y' для мужского (عزيزي), 't' для женского (عزيزتي)):",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (рекомендуется 2 343)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_greeting",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (69, 1230, 2412, 1350),
                                        "segments_align": "right",
                                        "segments": [
                                            {
                                                "text": "{gender}",
                                                "font": "araboto",
                                                "size": 59,
                                                "color": (0, 0, 0),
                                                "template_eval": "lambda gender='', **kw: 'عزيزي ' if str(gender).lower() in ['y', 'м'] else 'عزيزتي '",
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "araboto_bold",
                                                "size": 59,
                                                "color": (0, 0, 0),
                                                "template_eval": "lambda name='', **kw: name.replace(' ', ' ')",
                                            },
                                            {
                                                "text": ":",
                                                "font": "araboto",
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
                                        "segments_align": "right",
                                        "line_spacing": 0.76,
                                        "segments": [
                                            {
                                                "text": 'نحيطكم علماً بوجود شرط هام يتعلق بسحب الأموال إلى الحساب البنكي الذي حددته. ستكون عملية الدفع متاحة فقط بعد دفع رسوم الخدمات بمبلغ ',
                                                "font": "araboto",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": "د.م. ",
                                                "font": "araboto",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": "{amount}",
                                                "font": "myriad_arabic_bold",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                                "format_number_comma": True,
                                            },
                                            {
                                                "text": '. يرجى سداد الدفعة المذكورة في أقرب وقت ممكن؛ بعد تأكيدها ومعالجتها من قبل أقسامنا، ستتلقى على الفور في حسابك البنكي المبلغ الإجمالي وقدره ',
                                                "font": "araboto",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": "35,511",
                                                "font": "myriad_arabic_bold",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": ' د.م.',
                                                "font": "araboto",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                        ],
                                    },
                                },
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
                        "rd4_ma": {
                            "label": "Morocco RD 4",
                            "asset": "assets/Morocco/RD/rd4.jpg",
                            "preview": "assets/Morocco/Preview/RD/RD4_prew.jpg",
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
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (рекомендуется 2 258)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_body",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (84, 758, 743, 1022),
                                        "segments_align": "right",
                                        "line_spacing": 1.2,
                                        "blank_line_size": 14,
                                        "segments": [
                                            {
                                                "text": 'من أجل إتمام عملية الدفع لزبونك بنجاح وأمان ',
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (255, 255, 255),
                                                "template_eval": "lambda name='', **kw: name.replace(' ', ' ')",
                                            },
                                            {
                                                "text": '، يجب عليك سداد رسوم عملية الفصل بمبلغ ',
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": "د.م. ",
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (255, 0, 0),
                                            },
                                            {
                                                "text": "{amount}",
                                                "font": "myriad_arabic_bold",
                                                "size": 30,
                                                "color": (255, 0, 0),
                                                "format_number_comma": True,
                                            },
                                            {
                                                "text": """.

""",
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (255, 255, 255),
                                            },
                                            {
                                                "text": 'بمجرد دفع رسوم الفصل، سيتم تحويل جميع الأموال تلقائيًا إلى حساب زبونك.',
                                                "font": "araboto",
                                                "size": 30,
                                                "color": (255, 255, 255),
                                            },
                                        ],
                                    },
                                },
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
                        "rd5_ma": {
                            "label": "Morocco RD 5",
                            "asset": "assets/Morocco/RD/rd5.jpg",
                            "preview": "assets/Morocco/Preview/RD/RD5_prew.jpg",
                            "fields": [
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО (пример: Nilda Mamani Apaza)',
                                    "text_config": {
                                        "area": (68, 460, 2412, 560),
                                        "segments_align": "right",
                                        "segments": [
                                            {
                                                "text": 'إشعار لـ ',
                                                "font": "araboto_bold",
                                                "size": 59,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "araboto_bold",
                                                "size": 59,
                                                "color": (0, 0, 0),
                                                "template_eval": "lambda name='', **kw: name.replace(' ', ' ')",
                                            },
                                        ],
                                    },
                                },
                                {
                                    "key": "gender",
                                    "prompt": "👤 Выберите обращение (введите 'y' для мужского (عزيزي), 't' для женского (عزيزتي)):",
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (рекомендуется 2 100)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_greeting",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (69, 1230, 2412, 1350),
                                        "segments_align": "right",
                                        "segments": [
                                            {
                                                "text": "{gender}",
                                                "font": "araboto",
                                                "size": 59,
                                                "color": (0, 0, 0),
                                                "template_eval": "lambda gender='', **kw: 'عزيزي ' if str(gender).lower() in ['y', 'м'] else 'عزيزتي '",
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "araboto_bold",
                                                "size": 59,
                                                "color": (0, 0, 0),
                                                "template_eval": "lambda name='', **kw: name.replace(' ', ' ')",
                                            },
                                            {
                                                "text": ":",
                                                "font": "araboto",
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
                                        "segments_align": "right",
                                        "line_spacing": 1.45,
                                        "segments": [
                                            {
                                                "text": 'يظهر في النظام دفعة معلقة كقسط تأمين بمبلغ ',
                                                "font": "araboto",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": "د.م. ",
                                                "font": "araboto",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": "{amount}",
                                                "font": "myriad_arabic_bold",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                                "format_number_comma": True,
                                            },
                                            {
                                                "text": '، وهو أمر ضروري لتفعيل الضمانات والوصول الكامل إلى ميزات الحماية. يرجى سداد هذه الدفعة من خلال طرق الشحن المتاحة. بعد تأكيد الدفع، سيتم استعادة الوصول إلى السحوبات ويمكنك بدء تحويل المبلغ الإجمالي البالغ ',
                                                "font": "araboto",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": "35,511",
                                                "font": "myriad_arabic_bold",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": ' د.م.',
                                                "font": "araboto",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                            {
                                                "text": ' إلى الحساب البنكي المحدد.',
                                                "font": "araboto",
                                                "size": 60,
                                                "color": (0, 0, 0),
                                            },
                                        ],
                                    },
                                },
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
                        "rd6_ma": {
                            "label": "Morocco RD 6",
                            "asset": "assets/Morocco/RD/rd6.jpg",
                            "preview": "assets/Morocco/Preview/RD/RD6_prew.jpg",
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
                                    "prompt": '🏦 Название банка (пример: CIH Bank)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "tx_time",
                                    "prompt": '🕐 Время транзакции (пример: 10:00)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "name",
                                    "prompt": '✏️ Введите ФИО клиента (пример: Ivan Ivanov)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "commission",
                                    "prompt": '💰 Введите сумму налога (рекомендуется 1.920)',
                                    "text_config": {"collect_only": True},
                                },
                                {
                                    "key": "_body",
                                    "prompt": "",
                                    "text_config": {
                                        "area": (655, 457, 1620, 795),
                                        "segments_align": "right",
                                        "line_spacing": 1.15,
                                        "blank_line_size": 10,
                                        "segments": [
                                            {
                                                "text": """عزيزي خوسيه غارسيا!

""",
                                                "font": "araboto_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": 'لقد قمت بتبادل USDT بمبلغ ',
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "35,511",
                                                "font": "myriad_arabic_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": """ د.م. لدفعها لزبونك.

""",
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": """تفاصيل المعاملة:
""",
                                                "font": "araboto_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": '  معرف المعاملة: ',
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "9489-4921-3991-002\n",
                                                "font": "myriad_arabic_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": '  بنك المستلم: ',
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "{bank}\n",
                                                "font": "araboto_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                                "template_eval": "lambda bank='', **kw: bank.replace(' ', ' ')",
                                            },
                                            {
                                                "text": '  المبلغ المراد استلامه: ',
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "35,511",
                                                "font": "myriad_arabic_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": """ د.م.
""",
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": '  المبلغ بالـ USDT: ',
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "3,855\n",
                                                "font": "myriad_arabic_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": '  وقت المعاملة: ',
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": """{tx_time}

""",
                                                "font": "myriad_arabic_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "زبونك، ",
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "{name}",
                                                "font": "araboto_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                                "template_eval": "lambda name='', **kw: name.replace(' ', ' ')",
                                            },
                                            {
                                                "text": '، ملزم بموجب القانون بدفع ضريبة بنسبة 7% على صرف العملات المشفرة، أي بمبلغ ',
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "د.م. ",
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                            {
                                                "text": "{commission}",
                                                "font": "myriad_arabic_bold",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                                "format_number_comma": True,
                                            },
                                            {
                                                "text": ".",
                                                "font": "araboto",
                                                "size": 20,
                                                "color": (44, 44, 44),
                                            },
                                        ],
                                    },
                                },
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
                        "rd7_ma": {
                            "label": "Morocco RD 7",
                            "asset": "assets/Morocco/RD/rd7.jpg",
                            "preview": "assets/Morocco/Preview/RD/RD7_prew.jpg",
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
                                    "prompt": '🏦 Введите название банка (пример: CIH Bank)',
                                    "text_config": {
                                        "font": "araboto_medium",
                                        "size": 29,
                                        "color": (0, 0, 0),
                                        "area": (398, 850, 710, 880),
                                        "align": "right",
                                    },
                                },
                                {
                                    "key": "fullname",
                                    "prompt": '✏️ Введите ФИО (пример: Ivanov Ivan)',
                                    "text_config": {
                                        "font": "araboto_medium",
                                        "size": 29,
                                        "color": (0, 0, 0),
                                        "area": (398, 913, 710, 944),
                                        "align": "right",
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
                                        "align": "right",
                                        "blur_area": (398, 994, 663, 1025),
                                        "blur_radius": 15,
                                    },
                                },
                                {
                                    "key": "amount",
                                    "prompt": '💰 Введите сумму (рекомендуется 1 745)',
                                    "text_config": {
                                        "area": (395, 1206, 710, 1242),
                                        "segments_align": "right",
                                        "segments": [
                                            {
                                                "text": "{amount}",
                                                "font": "myriad_arabic_bold",
                                                "size": 29,
                                                "color": (0, 0, 0),
                                                "format_number_comma": True,
                                            },
                                            {
                                                "text": ' د.م.',
                                                "font": "araboto_medium",
                                                "size": 29,
                                                "color": (0, 0, 0),
                                            },
                                        ],
                                    },
                                },
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
                    },
                }
            },
        }
    },
}
