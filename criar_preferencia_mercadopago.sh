curl --location --request POST 'https://api.mercadopago.com/checkout/preferences' \
--header 'Authorization: Bearer APP_USR-2932416334016747-042609-d20f53cc9d7816e795fb8b0aeea2c2a1-2410853434' \
--header 'Content-Type: application/json' \
--data-raw '{
  "items": [
    {
      "title": "Curso de LaTeX",
      "quantity": 1,
      "currency_id": "BRL",
      "unit_price": 24.90
    }
  ],
  "back_urls": {
    "success": "https://michelson-code.github.io/curso-latex/pagamento-sucesso.html",
    "pending": "https://michelson-code.github.io/curso-latex/pagamento-pendente.html",
    "failure": "https://michelson-code.github.io/curso-latex/pagamento-erro.html"
  },
  "auto_return": "approved"
}'
