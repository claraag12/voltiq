# servidor.py - liga o frontend ao banco de dados
# para rodar: python servidor.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse
from datetime import date

from empresa import listar_empresas, buscar_empresa, cadastrar_empresa, editar_empresa, excluir_empresa
from leitura import listar_leituras, registrar_leitura, editar_leitura, excluir_leitura
from meta    import listar_metas, cadastrar_meta, excluir_meta
from calculo import calcular_custo, calcular_status, calcular_variacao, formatar_variacao
from conexao import conectar

# converte tipos do Python para JSON
def para_json(obj):
    if isinstance(obj, (list, tuple)):
        return [para_json(i) for i in obj]
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    if hasattr(obj, '__float__'):
        return float(obj)
    if hasattr(obj, '__int__'):
        return int(obj)
    return obj

class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # desativa logs no terminal

    def enviar_json(self, dados, status=200):
        corpo = json.dumps(para_json(dados), ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(corpo)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def ler_body(self):
        tamanho = int(self.headers.get('Content-Length', 0))
        if tamanho:
            return json.loads(self.rfile.read(tamanho))
        return {}

    def do_GET(self):
        partes = [x for x in urlparse(self.path).path.split('/') if x]
        try:
            if partes == ['empresas']:
                self.enviar_json(listar_empresas())

            elif len(partes) == 2 and partes[0] == 'empresas':
                self.enviar_json(buscar_empresa(int(partes[1])))

            elif len(partes) == 2 and partes[0] == 'leituras':
                self.enviar_json(listar_leituras(int(partes[1])))

            elif len(partes) == 2 and partes[0] == 'metas':
                self.enviar_json(listar_metas(int(partes[1])))

            elif len(partes) == 3 and partes[0] == 'relatorio':
                id_emp = int(partes[1])
                mes    = partes[2]
                conn   = conectar()
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM empresa WHERE id_empresa = %s", (id_emp,))
                emp = cursor.fetchone()
                if not emp:
                    self.enviar_json({"erro": "Empresa nao encontrada"}, 404)
                    return

                cursor.execute("SELECT * FROM leitura WHERE id_empresa = %s AND mes_referencia = %s", (id_emp, mes))
                lei = cursor.fetchone()
                if not lei:
                    self.enviar_json({"erro": "Leitura nao encontrada para esse mes"}, 404)
                    return

                cursor.execute("SELECT limite_kwh FROM meta WHERE id_empresa = %s AND mes_referencia = %s", (id_emp, mes))
                meta   = cursor.fetchone()
                limite = float(meta[0]) if meta else None

                cursor.execute("""
                    SELECT kwh_consumido FROM leitura
                    WHERE id_empresa = %s AND mes_referencia < %s
                    ORDER BY mes_referencia DESC LIMIT 1
                """, (id_emp, mes))
                ant          = cursor.fetchone()
                kwh_anterior = float(ant[0]) if ant else None
                conn.close()

                kwh = float(lei[3])
                var = calcular_variacao(kwh, kwh_anterior)

                self.enviar_json({
                    "empresa":      emp[1],
                    "mes":          mes,
                    "kwh":          kwh,
                    "custo":        calcular_custo(kwh, float(emp[4])),
                    "limite":       limite,
                    "status":       calcular_status(kwh, limite),
                    "variacao":     var,
                    "variacao_fmt": formatar_variacao(var),
                })

            elif partes == ['dashboard']:
                conn   = conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM empresa")
                total_emp = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM leitura")
                total_lei = cursor.fetchone()[0]
                cursor.execute("SELECT COALESCE(SUM(kwh_consumido), 0) FROM leitura")
                total_kwh = float(cursor.fetchone()[0])
                cursor.execute("""
                    SELECT e.nome, l.mes_referencia, l.kwh_consumido,
                           ROUND(l.kwh_consumido * e.tarifa_reais, 2), m.limite_kwh
                    FROM leitura l
                    JOIN empresa e ON e.id_empresa = l.id_empresa
                    LEFT JOIN meta m ON m.id_empresa = l.id_empresa
                           AND m.mes_referencia = l.mes_referencia
                    ORDER BY l.data_registro DESC LIMIT 6
                """)
                recentes = []
                for r in cursor.fetchall():
                    kwh    = float(r[2])
                    limite = float(r[4]) if r[4] else None
                    recentes.append({
                        "empresa": r[0],
                        "mes":     r[1],
                        "kwh":     kwh,
                        "custo":   float(r[3]),
                        "status":  calcular_status(kwh, limite)
                    })
                conn.close()
                self.enviar_json({
                    "total_empresas": total_emp,
                    "total_leituras": total_lei,
                    "total_kwh":      total_kwh,
                    "recentes":       recentes
                })

            elif partes == ['historico'] and len(urlparse(self.path).query) > 0:
                from urllib.parse import parse_qs
                qs     = parse_qs(urlparse(self.path).query)
                id_emp = int(qs.get('id', [0])[0])
                conn   = conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT l.mes_referencia, l.kwh_consumido,
                           ROUND(l.kwh_consumido * e.tarifa_reais, 2), m.limite_kwh
                    FROM leitura l
                    JOIN empresa e ON e.id_empresa = l.id_empresa
                    LEFT JOIN meta m ON m.id_empresa = l.id_empresa
                           AND m.mes_referencia = l.mes_referencia
                    WHERE l.id_empresa = %s
                    ORDER BY l.mes_referencia
                """, (id_emp,))
                dados = []
                for r in cursor.fetchall():
                    dados.append({
                        "mes":    r[0],
                        "kwh":    float(r[1]),
                        "custo":  float(r[2]),
                        "limite": float(r[3]) if r[3] else None
                    })
                conn.close()
                self.enviar_json(dados)

            elif partes == ['comparar']:
                conn   = conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT e.id_empresa, e.nome,
                           COALESCE(SUM(l.kwh_consumido), 0),
                           COALESCE(ROUND(SUM(l.kwh_consumido * e.tarifa_reais), 2), 0),
                           COUNT(l.id_leitura)
                    FROM empresa e
                    LEFT JOIN leitura l ON l.id_empresa = e.id_empresa
                    GROUP BY e.id_empresa, e.nome
                    ORDER BY SUM(l.kwh_consumido) DESC
                """)
                dados = []
                for r in cursor.fetchall():
                    dados.append({
                        "id":       r[0],
                        "empresa":  r[1],
                        "kwh":      float(r[2]),
                        "custo":    float(r[3]),
                        "leituras": r[4]
                    })
                conn.close()
                self.enviar_json(dados)

            else:
                self.enviar_json({"erro": "Rota nao encontrada"}, 404)

        except Exception as e:
            self.enviar_json({"erro": str(e)}, 500)

    def do_POST(self):
        partes = [x for x in urlparse(self.path).path.split('/') if x]
        body   = self.ler_body()
        try:
            if partes == ['empresas']:
                r = cadastrar_empresa(body['nome'], body['cnpj'], body['cidade'], float(body['tarifa_reais']))
                self.enviar_json(r, 400 if 'erro' in r else 201)
            elif partes == ['leituras']:
                r = registrar_leitura(int(body['id_empresa']), body['mes_referencia'], float(body['kwh_consumido']))
                self.enviar_json(r, 400 if 'erro' in r else 201)
            elif partes == ['metas']:
                r = cadastrar_meta(int(body['id_empresa']), body['mes_referencia'], float(body['limite_kwh']))
                self.enviar_json(r, 400 if 'erro' in r else 201)
            else:
                self.enviar_json({"erro": "Rota nao encontrada"}, 404)
        except Exception as e:
            self.enviar_json({"erro": str(e)}, 500)

    def do_PUT(self):
        partes = [x for x in urlparse(self.path).path.split('/') if x]
        body   = self.ler_body()
        try:
            if len(partes) == 2 and partes[0] == 'empresas':
                r = editar_empresa(int(partes[1]), body['nome'], body['cidade'], float(body['tarifa_reais']))
                self.enviar_json(r)
            elif len(partes) == 2 and partes[0] == 'leituras':
                r = editar_leitura(int(partes[1]), float(body['kwh_consumido']))
                self.enviar_json(r)
            else:
                self.enviar_json({"erro": "Rota nao encontrada"}, 404)
        except Exception as e:
            self.enviar_json({"erro": str(e)}, 500)

    def do_DELETE(self):
        partes = [x for x in urlparse(self.path).path.split('/') if x]
        try:
            if len(partes) == 2 and partes[0] == 'empresas':
                self.enviar_json(excluir_empresa(int(partes[1])))
            elif len(partes) == 2 and partes[0] == 'leituras':
                self.enviar_json(excluir_leitura(int(partes[1])))
            elif len(partes) == 2 and partes[0] == 'metas':
                self.enviar_json(excluir_meta(int(partes[1])))
            else:
                self.enviar_json({"erro": "Rota nao encontrada"}, 404)
        except Exception as e:
            self.enviar_json({"erro": str(e)}, 500)

if __name__ == '__main__':
    porta = 8000
    print("")
    print("  VoltIQ -- Servidor iniciado!")
    print(f"  API rodando em: http://localhost:{porta}")
    print("  Abra o index.html no navegador para usar o sistema")
    print("  Para parar: Ctrl + C")
    print("")
    HTTPServer(('', porta), Handler).serve_forever()
