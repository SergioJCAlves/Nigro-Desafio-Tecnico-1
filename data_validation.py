import logging

def validate_cliente_data(data):
    """
    Valida os dados do cliente.
    """
    if not data.get('clientId'):
        raise ValueError("clientId é obrigatório")
    if not data.get('name'):
        raise ValueError("name é obrigatório")
    # Adicione mais validações conforme necessário
    logging.info(f"Dados do cliente {data['clientId']} validados com sucesso")

def validate_operacao_data(data):
    """
    Valida os dados da operação.
    """
    if not data:
        logging.warning("Dados da operação ausentes")
        return
    if not data.get('ccbCode'):
        raise ValueError("ccbCode é obrigatório")
    # Adicione mais validações conforme necessário
    logging.info(f"Dados da operação {data.get('ccbCode')} validados com sucesso")