import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from config import *
from models import Base, Cliente, Identidade, Endereco, Contato, DadosBancarios, Operacao, Parcela, DetalhamentoCET
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_postgres():
    engine = create_engine(POSTGRES_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def validate_cliente_data(data):
    required_fields = ['clientId', 'name', 'taxId', 'type', 'birthDate']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} é obrigatório")
    logging.debug("Dados do cliente validados com sucesso")

def validate_operacao_data(data, ccb_code):
    if not ccb_code:
        raise ValueError("ccbCode é obrigatório")
    required_fields = ['VencimentoPrimeiraParcela', 'ValorBruto', 'ValorLiquido']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} é obrigatório na operação")
    logging.debug("Dados da operação validados com sucesso")

def migrate_data():
    postgres_session = connect_postgres()

    try:
        # Aqui você carregaria os dados do MongoDB ou de um arquivo JSON
        # Por enquanto, vamos usar o documento que você forneceu
        doc = {
            "_id": "K9NBx1d00WcMEpOBKmwg",
            "clientId": "qbxL3XKAL7MOev9rvs94RbPYAma",
            "name": "FERNANDO PEIXOTO CAMILO",
            "taxId": "05633022456",
            "type": "PF",
            "birthDate": "1980-12-08",
            "maritalStatus": "casado",
            "identity": {
                "number": "24.094.218",
                "issuer": "PCMG",
                "issuerState": "MG"
            },
            "birthPlace": "Santa Maria do Suacui",
            "address": {
                "zipCode": "39775-000",
                "state": "MG",
                "city": "José Raydan",
                "address": "CORREGO BOA VISTA",
                "neighbourhood": "Rural",
                "number": "0"
            },
            "pep": False,
            "structure": "FIDC - Nagro",
            "state": "MG",
            "motherName": "Irani Camilo Peixoto",
            "gender": "masculino",
            "contacts": {
                "email": "fernandocamilo654@gmail.com",
                "phone": "(11) 95502-9939"
            },
            "averageMonthlyIncome": 10788,
            "bankData": {
                "branchNumber": 4103,
                "accountNumber": 8079,
                "bankNumber": "756"
            },
            "operation": {
                "VencimentoPrimeiraParcela": "2021-12-07",
                "Carencia": None,
                "FinanIOF": True,
                "Conta": "110000000",
                "ValorBruto": "15448.41",
                "ValorDoSeguro": "0",
                "ValorDaCAD": "0",
                "ValorDoIOF": "448.41",
                "ValorLiquido": "15000.0",
                "TaxaDeJuros": "2.8178",
                "TaxaDeJurosAnual": "39.58",
                "CET": "3.22",
                "CET_ANUAL": "46.27",
                "DataDeLiberacao": "2021-10-07",
                "DataDeVencimentoInicial": "2021-12-07",
                "DataDeVencimentoFinal": "2022-11-07",
                "NumeroDeParcelas": 12,
                "parcelas": {
                    "PrevisaoDeParcela": [
                        # ... (parcelas omitidas para brevidade)
                    ]
                },
                "TotalDeAmortizacao": "15898.23",
                "TotalDaTaxaDeServico": "0",
                "TotalDoSeguro": "0",
                "TotalDaTaxaDeCorrecao": "0",
                "TotalDeJuros": "3509.79",
                "TotalDoValorDasParcelas": "18958.20",
                "detalhamentoDaCET": {
                    "PorcentagemDeJuros": "2.80",
                    "PorcentagemDeImpostos": "0.42",
                    "PorcentagemDeTarifas": "0.00",
                    "PorcentagemDeServicos": "0.00"
                }
            },
            "status": "Enviada",
            "updatedAt": {
                "$date": "2022-05-03T19:28:10.454Z"
            },
            "createdAt": "2021-10-07T12:20:19.093830+00:00",
            "ccbCode": "A0988020-000",
            "emitedAt": {
                "$date": "2021-10-07T12:28:25.832Z"
            }
        }

        logging.info(f"Processando documento para o cliente {doc['clientId']}")

        # Log para verificar o valor de ccbCode antes da validação
        logging.debug(f"ccbCode antes da validação: {doc.get('ccbCode')}")

        validate_cliente_data(doc)
        validate_operacao_data(doc['operation'], doc.get('ccbCode'))

        cliente = Cliente(
            client_id=doc['clientId'],
            name=doc['name'],
            tax_id=doc['taxId'],
            type=doc['type'],
            birth_date=datetime.strptime(doc['birthDate'], '%Y-%m-%d'),
            marital_status=doc['maritalStatus'],
            birth_place=doc['birthPlace'],
            pep=doc['pep'],
            structure=doc['structure'],
            state=doc['state'],
            mother_name=doc['motherName'],
            gender=doc['gender'],
            average_monthly_income=doc['averageMonthlyIncome']
        )
        postgres_session.merge(cliente)
        logging.debug(f"Cliente {doc['clientId']} processado")

        identidade = Identidade(
            client_id=doc['clientId'],
            number=doc['identity']['number'],
            issuer=doc['identity']['issuer'],
            issuer_state=doc['identity']['issuerState']
        )
        postgres_session.merge(identidade)
        logging.debug(f"Identidade do cliente {doc['clientId']} processada")

        endereco = Endereco(
            client_id=doc['clientId'],
            zip_code=doc['address']['zipCode'],
            state=doc['address']['state'],
            city=doc['address']['city'],
            address=doc['address']['address'],
            neighbourhood=doc['address']['neighbourhood'],
            number=doc['address']['number']
        )
        postgres_session.merge(endereco)
        logging.debug(f"Endereço do cliente {doc['clientId']} processado")

        contato = Contato(
            client_id=doc['clientId'],
            email=doc['contacts']['email'],
            phone=doc['contacts']['phone']
        )
        postgres_session.merge(contato)
        logging.debug(f"Contato do cliente {doc['clientId']} processado")

        dados_bancarios = DadosBancarios(
            client_id=doc['clientId'],
            branch_number=doc['bankData']['branchNumber'],
            account_number=doc['bankData']['accountNumber'],
            bank_number=doc['bankData']['bankNumber']
        )
        postgres_session.merge(dados_bancarios)
        logging.debug(f"Dados bancários do cliente {doc['clientId']} processados")

        operacao_data = doc['operation']
        operacao = Operacao(
            client_id=doc['clientId'],
            ccb_code=doc['ccbCode'],
            vencimento_primeira_parcela=datetime.strptime(operacao_data['VencimentoPrimeiraParcela'], '%Y-%m-%d'),
            carencia=operacao_data['Carencia'],
            finan_iof=operacao_data['FinanIOF'],
            conta=operacao_data['Conta'],
            valor_bruto=float(operacao_data['ValorBruto']),
            valor_seguro=float(operacao_data['ValorDoSeguro']),
            valor_cad=float(operacao_data['ValorDaCAD']),
            valor_iof=float(operacao_data['ValorDoIOF']),
            valor_liquido=float(operacao_data['ValorLiquido']),
            taxa_juros=float(operacao_data['TaxaDeJuros']),
            taxa_juros_anual=float(operacao_data['TaxaDeJurosAnual']),
            cet=float(operacao_data['CET']),
            cet_anual=float(operacao_data['CET_ANUAL']),
            data_liberacao=datetime.strptime(operacao_data['DataDeLiberacao'], '%Y-%m-%d'),
            data_vencimento_inicial=datetime.strptime(operacao_data['DataDeVencimentoInicial'], '%Y-%m-%d'),
            data_vencimento_final=datetime.strptime(operacao_data['DataDeVencimentoFinal'], '%Y-%m-%d'),
            numero_parcelas=operacao_data['NumeroDeParcelas'],
            total_amortizacao=float(operacao_data['TotalDeAmortizacao']),
            total_taxa_servico=float(operacao_data['TotalDaTaxaDeServico']),
            total_seguro=float(operacao_data['TotalDoSeguro']),
            total_taxa_correcao=float(operacao_data['TotalDaTaxaDeCorrecao']),
            total_juros=float(operacao_data['TotalDeJuros']),
            total_valor_parcelas=float(operacao_data['TotalDoValorDasParcelas']),
            status=doc['status'],
            emited_at=datetime.strptime(doc['emitedAt']['$date'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            created_at=datetime.strptime(doc['createdAt'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            updated_at=datetime.strptime(doc['updatedAt']['$date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        )
        postgres_session.merge(operacao)
        logging.debug(f"Operação do cliente {doc['clientId']} processada")

        for parcela_data in operacao_data['parcelas']['PrevisaoDeParcela']:
            parcela = Parcela(
                operacao_id=operacao.id,
                numero_parcela=int(parcela_data['NumeroDaParcela']),
                data_vencimento=datetime.strptime(parcela_data['DataDeVencimento'], '%Y-%m-%dT%H:%M:%S'),
                valor_amortizacao=float(parcela_data['ValorDaAmortizacao']),
                valor_correcao=float(parcela_data['ValorDaCorrecao']),
                valor_juros=float(parcela_data['ValorDoJuros']),
                valor_seguro=float(parcela_data['ValorDoSeguro']),
                valor_taxa_bancaria=float(parcela_data['ValorTaxaBancaria']),
                valor_prestacao=float(parcela_data['ValorDaPrestacao']),
                valor_saldo_anterior=float(parcela_data['ValorDoSaldoAnterior']),
                valor_juros_capitalizados=float(parcela_data['ValorDoJurosCapitalizados']),
                valor_saldo_atual=float(parcela_data['ValorDoSaldoAtual'])
            )
            postgres_session.merge(parcela)
        logging.debug(f"Parcelas da operação do cliente {doc['clientId']} processadas")

        detalhamento_cet_data = operacao_data['detalhamentoDaCET']
        detalhamento_cet = DetalhamentoCET(
            operacao_id=operacao.id,
            porcentagem_juros=float(detalhamento_cet_data['PorcentagemDeJuros']),
            porcentagem_impostos=float(detalhamento_cet_data['PorcentagemDeImpostos']),
            porcentagem_tarifas=float(detalhamento_cet_data['PorcentagemDeTarifas']),
            porcentagem_servicos=float(detalhamento_cet_data['PorcentagemDeServicos'])
        )
        postgres_session.merge(detalhamento_cet)
        logging.debug(f"Detalhamento CET da operação do cliente {doc['clientId']} processado")

        postgres_session.commit()
        logging.info(f"Migração concluída com sucesso para o cliente {doc['clientId']}")

    except Exception as e:
        postgres_session.rollback()
        logging.error(f"Erro na migração: {str(e)}")
    finally:
        postgres_session.close()

if __name__ == "__main__":
    migrate_data()