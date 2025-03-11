# Configuração do PostgreSQL
POSTGRES_URI = "postgresql://postgres:123@localhost:5432/ccb_database"

# Configuração de logging
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Tamanho do lote para commits
BATCH_SIZE = 100