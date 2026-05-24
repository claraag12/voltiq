# main.py - menu principal do VoltIQ
from empresa import listar_empresas, cadastrar_empresa, editar_empresa, excluir_empresa
from leitura import listar_leituras, registrar_leitura, editar_leitura, excluir_leitura
from meta    import listar_metas, cadastrar_meta, excluir_meta
from calculo import calcular_custo, calcular_status, calcular_variacao, formatar_variacao
from conexao import conectar

# mostra lista de empresas formatada
def mostrar_empresas():
    empresas = listar_empresas()
    if not empresas:
        print("  Nenhuma empresa cadastrada.")
        return
    print(f"\n  {'ID':<5} {'Nome':<30} {'Cidade':<20} {'Tarifa'}")
    print("  " + "-"*65)
    for e in empresas:
        print(f"  {e[0]:<5} {e[1]:<30} {e[3]:<20} R$ {e[4]}/kWh")

# mostra leituras de uma empresa
def mostrar_leituras(id_empresa):
    leituras = listar_leituras(id_empresa)
    if not leituras:
        print("  Nenhuma leitura cadastrada.")
        return
    print(f"\n  {'ID':<5} {'Mes':<10} {'kWh':>12} {'Data'}")
    print("  " + "-"*40)
    for l in leituras:
        print(f"  {l[0]:<5} {l[2]:<10} {float(l[3]):>10.2f} kWh   {l[4]}")

# mostra metas de uma empresa
def mostrar_metas(id_empresa):
    metas = listar_metas(id_empresa)
    if not metas:
        print("  Nenhuma meta cadastrada.")
        return
    print(f"\n  {'ID':<5} {'Mes':<10} {'Limite kWh':>12}")
    print("  " + "-"*30)
    for m in metas:
        print(f"  {m[0]:<5} {m[2]:<10} {float(m[3]):>10.2f} kWh")

# loop principal
while True:
    print("\n" + "="*48)
    print("   VoltIQ -- Energy Intelligence System")
    print("="*48)
    print("  [1] Gerenciar empresas")
    print("  [2] Gerenciar leituras")
    print("  [3] Gerenciar metas")
    print("  [4] Ver relatorio do mes")
    print("  [0] Sair")
    print("-"*48)
    opcao = input("  Escolha: ").strip()

    # ---- EMPRESAS ----
    if opcao == "1":
        while True:
            print("\n  -- EMPRESAS --")
            print("  [1] Listar")
            print("  [2] Cadastrar")
            print("  [3] Editar")
            print("  [4] Excluir")
            print("  [0] Voltar")
            sub = input("  Escolha: ").strip()

            if sub == "1":
                mostrar_empresas()

            elif sub == "2":
                nome   = input("  Nome: ")
                cnpj   = input("  CNPJ: ")
                cidade = input("  Cidade: ")
                try:
                    tarifa = float(input("  Tarifa R$/kWh: "))
                    r = cadastrar_empresa(nome, cnpj, cidade, tarifa)
                    print(f"  {r.get('mensagem') or r.get('erro')}")
                except:
                    print("  Valor invalido!")

            elif sub == "3":
                mostrar_empresas()
                try:
                    id_emp = int(input("  ID para editar: "))
                    nome   = input("  Novo nome: ")
                    cidade = input("  Nova cidade: ")
                    tarifa = float(input("  Nova tarifa: "))
                    r = editar_empresa(id_emp, nome, cidade, tarifa)
                    print(f"  {r['mensagem']}")
                except:
                    print("  Valor invalido!")

            elif sub == "4":
                mostrar_empresas()
                try:
                    id_emp = int(input("  ID para excluir: "))
                    conf   = input("  Confirma? (s/n): ")
                    if conf.lower() == "s":
                        r = excluir_empresa(id_emp)
                        print(f"  {r['mensagem']}")
                except:
                    print("  ID invalido!")

            elif sub == "0":
                break

    # ---- LEITURAS ----
    elif opcao == "2":
        mostrar_empresas()
        try:
            id_emp = int(input("  ID da empresa: "))
        except:
            print("  ID invalido!")
            continue

        while True:
            print("\n  -- LEITURAS --")
            print("  [1] Listar")
            print("  [2] Registrar")
            print("  [3] Editar")
            print("  [4] Excluir")
            print("  [0] Voltar")
            sub = input("  Escolha: ").strip()

            if sub == "1":
                mostrar_leituras(id_emp)

            elif sub == "2":
                mes = input("  Mes (ex: 2026-06): ").strip()
                try:
                    kwh = float(input("  kWh consumido: "))
                    r   = registrar_leitura(id_emp, mes, kwh)
                    print(f"  {r.get('mensagem') or r.get('erro')}")
                except:
                    print("  Valor invalido!")

            elif sub == "3":
                mostrar_leituras(id_emp)
                try:
                    id_lei = int(input("  ID para editar: "))
                    kwh    = float(input("  Novo kWh: "))
                    r      = editar_leitura(id_lei, kwh)
                    print(f"  {r.get('mensagem') or r.get('erro')}")
                except:
                    print("  Valor invalido!")

            elif sub == "4":
                mostrar_leituras(id_emp)
                try:
                    id_lei = int(input("  ID para excluir: "))
                    r      = excluir_leitura(id_lei)
                    print(f"  {r['mensagem']}")
                except:
                    print("  ID invalido!")

            elif sub == "0":
                break

    # ---- METAS ----
    elif opcao == "3":
        mostrar_empresas()
        try:
            id_emp = int(input("  ID da empresa: "))
        except:
            print("  ID invalido!")
            continue

        while True:
            print("\n  -- METAS --")
            print("  [1] Listar")
            print("  [2] Cadastrar")
            print("  [3] Excluir")
            print("  [0] Voltar")
            sub = input("  Escolha: ").strip()

            if sub == "1":
                mostrar_metas(id_emp)

            elif sub == "2":
                mes = input("  Mes (ex: 2026-06): ").strip()
                try:
                    limite = float(input("  Limite kWh: "))
                    r      = cadastrar_meta(id_emp, mes, limite)
                    print(f"  {r.get('mensagem') or r.get('erro')}")
                except:
                    print("  Valor invalido!")

            elif sub == "3":
                mostrar_metas(id_emp)
                try:
                    id_meta = int(input("  ID para excluir: "))
                    r       = excluir_meta(id_meta)
                    print(f"  {r['mensagem']}")
                except:
                    print("  ID invalido!")

            elif sub == "0":
                break

    # ---- RELATORIO ----
    elif opcao == "4":
        mostrar_empresas()
        try:
            id_emp = int(input("  ID da empresa: "))
            mes    = input("  Mes (ex: 2026-06): ").strip()
        except:
            print("  Valor invalido!")
            continue

        conn   = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM empresa WHERE id_empresa = %s", (id_emp,))
        empresa = cursor.fetchone()
        if not empresa:
            print("  Empresa nao encontrada!")
            conn.close()
            continue

        cursor.execute(
            "SELECT * FROM leitura WHERE id_empresa = %s AND mes_referencia = %s",
            (id_emp, mes)
        )
        leitura = cursor.fetchone()
        if not leitura:
            print("  Leitura nao encontrada para esse mes!")
            conn.close()
            continue

        cursor.execute(
            "SELECT limite_kwh FROM meta WHERE id_empresa = %s AND mes_referencia = %s",
            (id_emp, mes)
        )
        meta   = cursor.fetchone()
        limite = float(meta[0]) if meta else None

        cursor.execute("""
            SELECT kwh_consumido FROM leitura
            WHERE id_empresa = %s AND mes_referencia < %s
            ORDER BY mes_referencia DESC LIMIT 1
        """, (id_emp, mes))
        anterior     = cursor.fetchone()
        kwh_anterior = float(anterior[0]) if anterior else None
        conn.close()

        kwh    = float(leitura[3])
        tarifa = float(empresa[4])
        custo  = calcular_custo(kwh, tarifa)
        status = calcular_status(kwh, limite)
        var    = calcular_variacao(kwh, kwh_anterior)
        icone  = "CRITICO" if status == "CRITICO" else "ATENCAO" if status == "ATENCAO" else "OK"

        print("\n" + "="*48)
        print(f"  RELATORIO -- {empresa[1]}")
        print("="*48)
        print(f"  Mes:      {mes}")
        print(f"  Consumo:  {kwh:.2f} kWh")
        if limite:
            print(f"  Meta:     {limite:.2f} kWh")
        print(f"  Custo:    R$ {custo:.2f}")
        print(f"  Variacao: {formatar_variacao(var)}")
        print(f"  Status:   {icone}")
        if limite and kwh >= limite:
            print(f"  Meta ultrapassada em {round(kwh - limite, 2):.2f} kWh!")
        print("="*48)

    elif opcao == "0":
        print("  Saindo... Ate logo!")
        break
    else:
        print("  Opcao invalida!")
