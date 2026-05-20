import base64

with open('assets/Bolivia/FIRE/test_fire_output.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

html = """<!DOCTYPE html>
<html><head><style>
body{background:#111;color:#fff;text-align:center;font-family:sans-serif;padding:20px}
img{max-width:100%;border:2px solid #555;margin:20px 0}
</style></head>
<body>
<h1>Bolivia FIRE Check - Test Render</h1>
<p>Fields: amount=1234, datetime=20 mayo 2026 07:44, transaction=123456789, order=987654321</p>
<p>DESTINO: 72781074 DIEGO EDGAR ABASTO CACERES | ORIGEN: 63395815 PENIS ULTRA PENIS VAGINA</p>
<img src="data:image/png;base64,""" + img_b64 + """" />
</body></html>"""

with open('fire_test.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML created: fire_test.html')
