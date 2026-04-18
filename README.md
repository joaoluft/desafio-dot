# Desafio Técnico — Backend com IA

Implementação das três questões do desafio técnico para vaga de Desenvolvedor Backend com foco em IA.

> Registros de execução (prints) disponíveis em `/Resultados`.

---

## Questão 1 — API de Biblioteca Virtual

Desenvolvi uma API REST com **FastAPI** e **SQLite** (via SQLAlchemy) para cadastro e consulta de livros.

**Endpoints:**

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/books` | Cadastra um novo livro |
| `GET` | `/books` | Lista todos os livros |
| `GET` | `/books/search?title=X&author=Y` | Busca por título ou autor |
| `GET` | `/books/{id}` | Retorna um livro pelo ID |

A documentação interativa fica em `http://localhost:8000/docs` (Swagger gerado automaticamente pelo FastAPI).

Escolhi FastAPI pela tipagem nativa com Pydantic, validação automática dos campos e geração de docs sem configuração adicional. O banco SQLite resolve bem para o escopo do desafio sem precisar subir nada externo.

Testes unitários cobrem cadastro com dados válidos, busca por título, busca por autor e retorno 404 para ID inexistente.

---

## Questão 2 — Chatbot com IA Generativa

Chatbot conversacional usando **LangChain** para integração com o LLM da OpenAI e **LangGraph** para orquestrar o fluxo de conversação.

O histórico de mensagens é mantido por sessão — cada sessão tem um `session_id` e o contexto acumulado é passado ao modelo a cada turno, então o chatbot se lembra do que foi dito antes na conversa.

O modelo utilizado é o `gpt-4o-mini`. A temperatura está em `0.7` para respostas mais naturais.

**Como funciona:**

```
mensagem → LangGraph → generate (gpt-4o-mini com histórico) → resposta
```

Usei LangGraph em vez de uma chain simples porque ele facilita a adição de checkpointers para persistência de histórico caso seja necessário escalar para múltiplos workers futuramente.

A API expõe três endpoints:

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/chat` | Envia mensagem e recebe resposta |
| `DELETE` | `/chat/{session_id}` | Limpa o histórico da sessão |
| `GET` | `/health` | Health check |

O frontend em React (rodando em `http://localhost:3000`) permite testar o chatbot visualmente com suporte a histórico de conversa.

---

## Questão 3 — Busca Semântica com Embeddings e Vector Store

Sistema de busca semântica standalone usando **FAISS** como vector store e **OpenAI embeddings** (`text-embedding-3-small`) para indexar e consultar documentos.

O corpus é composto por 10 artigos sobre Python extraídos do Real Python, cobrindo tópicos como listas, decorators, asyncio, generators, comprehensions, classes, context managers, type hints, dataclasses e exceptions. Cada arquivo `.txt` em `q3_semantic_search/docs/` é um documento independente.

**Pipeline:**

```
docs/*.txt → Document (com metadado source) → embeddings → FAISS index (disco)
                                                                    ↓
                                              query → similarity_search_with_score → top-K docs
```

O índice é persistido em disco (`/app/data/faiss_index`). Na primeira execução ele é construído do zero; nas seguintes é carregado direto do arquivo, evitando reprocessar.

O score retornado é a **distância L2** — quanto menor, mais semanticamente próximo da query. Isso é diferente de busca por palavras-chave: a query *"como iterar sobre uma coleção"* retorna o artigo sobre listas mesmo sem usar a palavra "lista".

Para ver a demonstração no terminal:

```bash
docker compose run --rm semantic_search
```

---

## Rodando o projeto

**Pré-requisitos:** Docker e Docker Compose.

```bash
# 1. configurar a chave da OpenAI
cp .env.example .env
# editar .env e preencher OPENAI_API_KEY

# 2. subir tudo
docker compose up --build

# 3. acessar
# Frontend:       http://localhost:3000
# API Biblioteca: http://localhost:8000/docs
# API Chatbot:    http://localhost:8001/docs
```

**Rodar os testes da Q1 sem Docker:**

```bash
cd q1_api
pip install -r requirements.txt
pytest -v
```

---

## Stack

| Componente | Tecnologia |
|------------|-----------|
| Q1 — API | FastAPI, SQLAlchemy, SQLite, pytest |
| Q2 — Chatbot | LangChain, LangGraph, OpenAI gpt-4o-mini |
| Q3 — Busca semântica | LangChain, OpenAI embeddings, FAISS |
| Frontend | React 18, Vite, nginx |
| Infra | Docker Compose |
