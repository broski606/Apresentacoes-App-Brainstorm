# 💬 Apresentação Interativa

Uma pequena webapp construída para permitir aos espectadores de uma apresentação colaborarem em tempo real, enviando palavras ou frases a partir do telemóvel — que aparecem, a flutuar, no ecrã projetado.

Sem apps para instalar, sem contas, sem internet. Basta apontar a câmara a um QR code.

---

## ✨ O que faz

- 📱 Os espectadores acedem a uma página simples pelo telemóvel e escrevem uma palavra ou frase associada ao que está a ser apresentado.
- 🖥️ Essa palavra aparece, a flutuar, no ecrã ligado ao projetor — em tempo real, sem refrescar a página.
- 🔁 As palavras continuam a circular pelo ecrã até seres tu a limpá-las.
- 📷 Um QR code no próprio ecrã de projeção facilita o acesso — sem escrever links à mão.
- 🌐 Funciona só com rede local (Wi-Fi da sala) — não depende de internet nem de serviços externos.

---

## 🧩 Como funciona

```
┌────────────────┐         Wi-Fi local          ┌──────────────────┐
│  Telemóvel do   │ ────────────────────────────▶│                  │
│    espectador   │        POST /enviar           │   Servidor       │
└────────────────┘                                │   Flask (PC)     │
                                                    │                  │
┌────────────────┐        GET /palavras           │                  │
│  Ecrã / projetor│ ◀────────────────────────────  │                  │
│   (projeção)    │        (polling)               └──────────────────┘
└────────────────┘
```

O PC corre um pequeno servidor que serve duas páginas:

| Página | Rota | Para quem |
|---|---|---|
| Formulário de envio | `/` | Espectadores, no telemóvel |
| Ecrã de projeção | `/projecao` | O PC ligado ao projetor |

---

## 📦 Instalação

```bash
pip install flask "qrcode[pil]"
```

> ⚠️ **Atenção:** instala sempre `qrcode[pil]`, e não apenas `qrcode`. Sem o extra `[pil]`, falta a biblioteca Pillow (usada para gerar a imagem do QR code) e a geração do `/qrcode.png` falha noutras máquinas onde o Pillow não esteja já instalado por outra dependência.

---

## 🚀 Como usar

1. Liga o PC à mesma rede Wi-Fi da sala.
2. Corre o servidor:
   ```bash
   python server.py
   ```
3. Abre `http://localhost:5000/projecao` no PC e projeta essa janela em ecrã completo.
4. Os espectadores apontam a câmara ao QR code apresentado no ecrã, ou acedem manualmente a `http://<IP-do-PC>:5000/`.
5. Cada palavra ou frase enviada aparece a flutuar no projetor pouco depois.

> 💡 O IP correto é detetado e usado automaticamente no QR code — não precisas de o configurar à mão.

---

## 🧹 Limpar o ecrã

Durante a apresentação, as palavras continuam a reaparecer em loop. Para começar do zero:

- Clica no botão **"limpar ecrã"** no canto superior direito da projeção, **ou**
- Prime a tecla **`L`** no teclado.

Por segurança, é pedida uma confirmação antes de limpar.

---

## 🛠️ Stack

- **Backend:** Python + Flask
- **Frontend:** HTML, CSS e JavaScript puro — sem frameworks, sem dependências externas
- **QR code:** gerado no servidor com a biblioteca [`qrcode`](https://pypi.org/project/qrcode/)

---

## 📡 API

| Rota | Método | Descrição |
|---|---|---|
| `/enviar` | `POST` | Recebe `{"texto": "..."}` e guarda a palavra |
| `/palavras?since=<id>` | `GET` | Devolve as palavras novas desde o último `id` conhecido |
| `/limpar` | `POST` | Limpa todas as palavras guardadas |
| `/qrcode.png` | `GET` | Imagem PNG do QR code de acesso |

---

## 📝 Nota

Feito para uma apresentação final de curso de programação — uma forma simples de tornar a audiência parte da conversa. 🎓
