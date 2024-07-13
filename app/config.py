#Parameters for local deploy
WORKERS = 4
HOST = "127.0.0.1"
PORT = 8080
RELOAD = True
LOG_LEVEL = "info"

# Configuration for Vertex AI and model parameters
VERTEXAI_PROJECT = ' '
VERTEXAI_LOCATION = ' '
CREDENTIALS_FILE = 'data/credentials.json'

# Parameters for text generation models
PARAMETERS = {'max_output_tokens': 1024, 'temperature': 0.2, 'top_p': 0.8, 'top_k': 40}
PARAMETERS_32 = {'max_output_tokens': 8192, 'temperature': 0.2, 'top_p': 0.8, 'top_k': 40}

# Model names
MODEL_NAME = 'text-bison'
MODEL_NAME_32 = 'text-bison-32k'

# Logging configuration
LOGGING_CONFIG = {
    'filename': 'data/api.log',
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

#Cache configuration
TTL_CACHE_MAXSIZE = 1000
TTL_CACHE_TTL = 300

# LLM configuration
PROMPT = """
            Eu preciso que você classifique cada produto entre Direto e Indireto.
            Produtos do tipo Direto são aqueles comprados para consumo da própria empresa. Normalmente eles não têm relação imediata com a atividade comercial da empresa.
            Produtos do tipo Indireto são aqueles comprados para revenda, ou para manter a produção da empresa. Normalmente eles são produtos relacionados a atividade comercial da empresa.
            Retorne apenas um JSON contendo os produtos da lista original e suas classificações.
            Não retorne nenhum item que não esteja na lista.
            Não retorne nada além do JSON.

            Exemplos:
            Para uma empresa no ramo de Pesca, anzol é um produto Indireto.
            Para uma empresa no ramo de Turismo, garrafa d'água é um produto Indireto.
            Para uma empresa no ramo de Construção, azulejos é um produto Indireto.

            Para uma empresa no ramo de Pesca, garrafa d'água é um produto Direto.
            Para uma empresa no ramo de Turismo, azulejos é um produto Direto.
            Para uma empresa no ramo de Construção, anzol é um produto Direto.

            Formato de resposta necessário para cada item da lista:
            "product": produto
            "type": classificação
"""

# OpenAI Config
OPENAI_API_KEY = " "
OPENAI_MODEL = "gpt-3.5-turbo-16k"

