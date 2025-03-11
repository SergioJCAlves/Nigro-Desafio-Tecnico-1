# Projeto de Migração de Dados CCB

Este projeto implementa um pipeline de dados para migrar informações de contratos CCB (Cédula de Crédito Bancária) do MongoDB para o PostgreSQL, garantindo a integridade, consistência e confiabilidade dos dados.

```
## Estrutura do Projeto

ccb-migration/
├── models.py          # Definição das tabelas PostgreSQL com SQLAlchemy
├── migration_script.py  # Lógica principal de extração, transformação e carregamento
├── data_validation.py # Funções de validação dos dados
├── ccb_migration_dag.py # DAG do Apache Airflow para agendamento
├── config.py          # Configurações de conexão e variáveis de ambiente
├── requirements.txt   # Lista de dependências do projeto
└── README.md          # Documentação do projeto
```

## Configuração

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as credenciais:


Edite o arquivo config.py com as URIs de conexão para MongoDB e PostgreSQL.
Utilize variáveis de ambiente para informações sensíveis.

Local
# Execução local
python data_migration.py

## Estrutura de Dados no PostgreSQL

Tabelas Principais

clientes: Informações básicas dos clientes.
identidades: Dados de identificação (CPF, RG).
enderecos: Endereços residenciais e comerciais.
contatos: Informações de contato (telefones, e-mails).
dados_bancarios: Dados bancários para transações.
operacoes: Detalhes das operações financeiras.
parcelas: Informações sobre as parcelas das operações.
detalhamento_cet: Detalhamento do Custo Efetivo Total (CET).

## Relacionamentos

As tabelas são relacionadas através de chaves estrangeiras, garantindo a integridade referencial.
Índices são utilizados para otimizar as consultas.

# Tratamento de Falhas e Dados Duplicados

1. Falhas de Conexão:

Implementada função de retry em database_utils.py.
Tentativas de reconexão com intervalo de espera.


2. Registros Duplicados:

Utilizada cláusula ON CONFLICT do PostgreSQL via SQLAlchemy em data_migration.py.
Atualização ou omissão de registros duplicados.


3. Inconsistências nos Dados:

Funções de validação implementadas em data_validation.py.
Verificação de integridade dos dados antes da inserção.



## Estratégia de Execução Periódica

- Utilizado Apache Airflow para agendamento e execução periódica.
- DAG definido em ccb_migration_dag.py, programado para executar diariamente às 02:00 AM.
- Monitoramento e alertas configurados no Airflow.

## Decisões Técnicas

1. SQLAlchemy ORM:

Abstração do banco de dados para facilitar a manipulação.
Pooling de conexões para otimizar o desempenho.

2. Apache Airflow:

Orquestração de workflows para automatizar a migração.
Monitoramento e alertas para garantir a confiabilidade.



##Monitoramento e Alertas

Para garantir a execução bem-sucedida e contínua do pipeline de migração, é crucial implementar um sistema de monitoramento e alertas.

# Monitoramento

Apache Airflow UI: Utilize a interface web do Airflow para monitorar o status dos DAGs e das tarefas. A UI fornece informações detalhadas sobre a execução de cada tarefa, incluindo logs, tempo de execução e erros.

Logging: Configure o logging para registrar informações importantes sobre o progresso da migração, erros e avisos. Utilize ferramentas de análise de logs, como ELK Stack (Elasticsearch, Logstash, Kibana) ou Graylog, para monitorar os logs em tempo real e identificar padrões e tendências.

Métricas: Colete métricas sobre o desempenho do pipeline, como o tempo de execução, o número de registros processados e o consumo de recursos (CPU, memória, disco). Utilize ferramentas de monitoramento, como Prometheus e Grafana, para visualizar as métricas e configurar alertas.
