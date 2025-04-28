from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Configurações do Gmail (use variáveis de ambiente para segurança)
GMAIL_USER = 'michelson.geofisica@gmail.com'
GMAIL_PASS =  '3353A14YK27'

# Função para enviar o email
def send_email(to_email):
    subject = 'Bem-vindo ao Curso de LaTeX! 🎉'
    body = """
    Olá!

    Seu pagamento foi confirmado com sucesso! 👏

    Seja muito bem-vindo(a) ao nosso curso!

    Para acessar o nosso grupo no Discord, clique no link abaixo:
    👉 https://discord.gg/RtbC9afagp

    Grande abraço!
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = to_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, [to_email], msg.as_string())
        server.quit()
        print(f'Email enviado para {to_email}')
    except Exception as e:
        print(f'Erro ao enviar email: {e}')

# Endpoint para receber o webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print('Recebido:', data)

    # Verifica se o evento é um pagamento aprovado
    if data.get('type') == 'payment' and data['data'].get('status') == 'approved':
        payment_id = data['data']['id']

        # Pega o email do comprador da resposta do Mercado Pago
        buyer_email = data['data']['payer']['email']  # Acessa o e-mail do comprador

        # Envia o email de confirmação
        send_email(buyer_email)
        return jsonify({'message': 'Email enviado'}), 200

    return jsonify({'message': 'Webhook recebido, mas sem pagamento aprovado'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
