from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os
from urllib.parse import quote  # Substituindo url_quote por quote do urllib.parse

app = Flask(__name__)

# Configurações do Gmail (use variáveis de ambiente para segurança)
GMAIL_USER = os.getenv('GMAIL_USER', 'seuemail@gmail.com')
GMAIL_PASS = os.getenv('GMAIL_PASS', 'suasenhadeaplicativo')

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
        return False
    return True

# Endpoint para receber o webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Recebe os dados do webhook
        data = request.get_json()
        print('Recebido:', data)

        # Verifica se o evento é um pagamento aprovado
        if data.get('type') == 'payment' and data['data'].get('status') == 'approved':
            payment_id = data['data']['id']

            # Pega o email do comprador da resposta do Mercado Pago
            buyer_email = data['data']['payer']['email']  # Acessa o e-mail do comprador

            # Envia o email de confirmação
            email_sent = send_email(buyer_email)
            if email_sent:
                return jsonify({'message': 'Email enviado com sucesso!'}), 200
            else:
                return jsonify({'message': 'Erro ao enviar email para o comprador.'}), 500

        return jsonify({'message': 'Pagamento não aprovado ou tipo de evento incorreto.'}), 400

    except Exception as e:
        print(f'Erro no processamento do webhook: {e}')
        return jsonify({'message': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
