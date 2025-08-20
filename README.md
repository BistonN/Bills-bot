# 📝 Bills Bot

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-green)](https://core.telegram.org/bots)

O **Bills Bot** é um bot do Telegram criado para ajudar no controle de gastos pessoais. Ele permite que os usuários enviem áudios com informações sobre suas despesas, que são salvos localmente no servidor para processamento posterior.

## ⚙️ Funcionalidades:
- Recebimento de Áudios: O bot escuta e recebe mensagens de áudio dos usuários.
- Salvamento Local: Os arquivos de áudio são salvos em um diretório no servidor.

## 🚀 Tecnologias:
- Python 3.13
- python-telegram-bot: Biblioteca para criação e interação com o bot do Telegram
- python-dotenv: Usado para carregar variáveis de ambiente de forma segura

## 📝 Pré-requisitos:
- Python 3 instalado
- Token de Bot do Telegram (obtido através do @BotFather)

## ⚙️ Instalação e Execução:
1. Instale as dependências com o comando:
pip install -r requirements.txt

2. Crie um arquivo `.env` na raiz do projeto e adicione seu token do Telegram:
TELEGRAM_TOKEN=seu_token_aqui
⚠️ Não compartilhe seu token! Adicione o `.env` ao `.gitignore` para que ele não seja enviado ao GitHub.

3. Ative o ambiente virtual (dependendo do seu sistema):
venv\Scripts\activate

4. Execute o bot com:
python bot.py

No Telegram:
- Envie `/start` para iniciar a interação
- Envie áudios para testar o recebimento e salvamento
