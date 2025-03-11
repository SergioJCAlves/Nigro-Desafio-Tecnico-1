from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    client_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    tax_id = Column(String(20))
    type = Column(String(2))
    birth_date = Column(Date)
    marital_status = Column(String(50))
    birth_place = Column(String(255))
    pep = Column(Boolean)
    structure = Column(String(255))
    state = Column(String(2))
    mother_name = Column(String(255))
    gender = Column(String(20))
    average_monthly_income = Column(Numeric(15, 2))

    identidades = relationship("Identidade", back_populates="cliente")
    enderecos = relationship("Endereco", back_populates="cliente")
    contatos = relationship("Contato", back_populates="cliente")
    dados_bancarios = relationship("DadosBancarios", back_populates="cliente")
    operacoes = relationship("Operacao", back_populates="cliente")

class Identidade(Base):
    __tablename__ = 'identidades'

    id = Column(Integer, primary_key=True)
    client_id = Column(String(255), ForeignKey('clientes.client_id'))
    number = Column(String(20), nullable=False)
    issuer = Column(String(50))
    issuer_state = Column(String(2))

    cliente = relationship("Cliente", back_populates="identidades")

class Endereco(Base):
    __tablename__ = 'enderecos'

    id = Column(Integer, primary_key=True)
    client_id = Column(String(255), ForeignKey('clientes.client_id'))
    zip_code = Column(String(10))
    state = Column(String(2))
    city = Column(String(255))
    address = Column(String(255))
    neighbourhood = Column(String(255))
    number = Column(String(10))

    cliente = relationship("Cliente", back_populates="enderecos")

class Contato(Base):
    __tablename__ = 'contatos'

    id = Column(Integer, primary_key=True)
    client_id = Column(String(255), ForeignKey('clientes.client_id'))
    email = Column(String(255))
    phone = Column(String(20))

    cliente = relationship("Cliente", back_populates="contatos")

class DadosBancarios(Base):
    __tablename__ = 'dados_bancarios'

    id = Column(Integer, primary_key=True)
    client_id = Column(String(255), ForeignKey('clientes.client_id'))
    branch_number = Column(Integer)
    account_number = Column(Integer)
    bank_number = Column(String(10))

    cliente = relationship("Cliente", back_populates="dados_bancarios")

class Operacao(Base):
    __tablename__ = 'operacoes'

    id = Column(Integer, primary_key=True)
    client_id = Column(String(255), ForeignKey('clientes.client_id'))
    ccb_code = Column(String(20), unique=True, nullable=False)
    vencimento_primeira_parcela = Column(Date)
    carencia = Column(Integer)
    finan_iof = Column(Boolean)
    conta = Column(String(20))
    valor_bruto = Column(Numeric(15, 2))
    valor_seguro = Column(Numeric(15, 2))
    valor_cad = Column(Numeric(15, 2))
    valor_iof = Column(Numeric(15, 2))
    valor_liquido = Column(Numeric(15, 2))
    taxa_juros = Column(Numeric(10, 4))
    taxa_juros_anual = Column(Numeric(10, 2))
    cet = Column(Numeric(10, 2))
    cet_anual = Column(Numeric(10, 2))
    data_liberacao = Column(Date)
    data_vencimento_inicial = Column(Date)
    data_vencimento_final = Column(Date)
    numero_parcelas = Column(Integer)
    total_amortizacao = Column(Numeric(15, 2))
    total_taxa_servico = Column(Numeric(15, 2))
    total_seguro = Column(Numeric(15, 2))
    total_taxa_correcao = Column(Numeric(15, 2))
    total_juros = Column(Numeric(15, 2))
    total_valor_parcelas = Column(Numeric(15, 2))
    status = Column(String(50))
    emited_at = Column(Date)

    cliente = relationship("Cliente", back_populates="operacoes")
    parcelas = relationship("Parcela", back_populates="operacao")
    detalhamento_cet = relationship("DetalhamentoCET", back_populates="operacao")

class Parcela(Base):
    __tablename__ = 'parcelas'

    id = Column(Integer, primary_key=True)
    operacao_id = Column(Integer, ForeignKey('operacoes.id'))
    numero_parcela = Column(Integer)
    data_vencimento = Column(Date)
    valor_amortizacao = Column(Numeric(15, 2))
    valor_correcao = Column(Numeric(15, 2))
    valor_juros = Column(Numeric(15, 2))
    valor_seguro = Column(Numeric(15, 2))
    valor_taxa_bancaria = Column(Numeric(15, 2))
    valor_prestacao = Column(Numeric(15, 2))
    valor_saldo_anterior = Column(Numeric(15, 2))
    valor_juros_capitalizados = Column(Numeric(15, 2))
    valor_saldo_atual = Column(Numeric(15, 2))

    operacao = relationship("Operacao", back_populates="parcelas")

class DetalhamentoCET(Base):
    __tablename__ = 'detalhamento_cet'

    id = Column(Integer, primary_key=True)
    operacao_id = Column(Integer, ForeignKey('operacoes.id'))
    porcentagem_juros = Column(Numeric(5, 2))
    porcentagem_impostos = Column(Numeric(5, 2))
    porcentagem_tarifas = Column(Numeric(5, 2))
    porcentagem_servicos = Column(Numeric(5, 2))

    operacao = relationship("Operacao", back_populates="detalhamento_cet")