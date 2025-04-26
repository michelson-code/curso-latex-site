from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Configurações do Gmail
GMAIL_USER = 'seuemail@gmail.com'
GMAIL_PASS = 'suasenhadeaplicativo'  # Não usar a senha normal, usa senha de app!

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

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASS)
    server.sendmail(GMAIL_USER, [to_email], msg.as_string())
    server.quit()

# Endpoint para receber o webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print('Recebido:', data)

    # Verifica se é pagamento aprovado
    if data.get('type') == 'payment':
        payment_id = data['data']['id']

        # Aqui você consultaria a API do Mercado Pago para confirmar
        # Para simplificar, vamos simular que o pagamento é aprovado
        status = "approved"  # Ideal seria consultar!

        # Pega o email do comprador (no mundo real, teria que consultar detalhes)
        buyer_email = 'emaildopagador@example.com'  # << Aqui você buscaria real.

        if status == 'approved':
            send_email(buyer_email)
            return jsonify({'message': 'Email enviado'}), 200

    return jsonify({'message': 'Webhook recebido'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
