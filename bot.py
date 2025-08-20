import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from nlp import ProcessadorFrase
from speach_to_text import TranscritorGoogle
from insert_sheets import GerenciadorGastos

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Mande um áudio que eu vou transcrever')

async def receber_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.voice:
            file = await context.bot.get_file(update.message.voice.file_id)
            
            if not os.path.exists('audios'):
                os.makedirs('audios')

            file_path = f'audios/{update.message.from_user.id}_{update.message.message_id}.ogg'
            
            await file.download_to_drive(file_path)
            await update.message.reply_text(f'Processando..')
            TranscritorGoogle().transcrever(file_path)
            resultado = await ProcessadorFrase().processar_de_json("./transcricao.json")
            print(resultado)
            
            gestor = GerenciadorGastos(resultado)
            gestor.inserir_gasto()

            await update.message.reply_text(f'Valor cadastrado em "{resultado['categoria']}": {resultado['frase']} ')
    except Exception as error:
        print(error)
        await update.message.reply_text(f'Algo deu errado: {str(error)}')
        
        
    
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.VOICE, receber_audio))

print('Bot rodando...')
app.run_polling()