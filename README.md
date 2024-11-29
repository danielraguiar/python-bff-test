# Projeto Python-bff-test

Este é um projeto FastAPI configurado para integrar com serviços fakes RESTful. Abaixo você encontrará instruções detalhadas sobre como configurar, executar e testar o projeto.

---

## 📋 Requisitos

Certifique-se de que você possui os seguintes itens instalados:

1. **Python**: Versão 3.8 ou superior
2. **Pip**: Gerenciador de pacotes do Python
3. **Virtualenv** (opcional, mas recomendado): Para isolamento do ambiente virtual
4. **Git**: Para clonar o repositório

---

## 🚀 Configuração do Ambiente

1. **Clone o repositório**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETORIO>
   
2. **Crie um ambiente virtual**

   ```bash
   python -m venv .venv

3. **Instale as dependencias**

   ```bash
   pip install -r requirements.txt

4. **Execute a aplicação**

   ```bash
   uvicorn main:app --reload

5. **Testando o projeto**
   ```bash
   pytest -v
