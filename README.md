# 🧞 Flow Genius

## 👷‍♀️ One time setup

- Install [pyenv](https://github.com/pyenv/pyenv).
- Install Python with:

```bash
pyenv install 3.10
```

- Activate environment locally:

```bash
pyenv local 3.10
```

- Install [poetry]().
- Configure poetry to create virtual environments inside the project's root directory:

```bash
poetry config virtualenvs.in-project true
```

- Install dependencies:

```bash
poetry install
```

## 🔑 Set project secrets

Store your secrets in the `.env` file and refer to the `.env.example` file for guidance.

- [OpenAI API Key](https://platform.openai.com/account/api-keys)
- [AI21](https://studio.ai21.com/account)

## 💁‍♀️ How to use

```bash
poetry run uvicorn app.main:app --reload
```

## 📝 Notes

- To learn about how to use FastAPI with most of its features, you can visit the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- FastAPI provides automatic documentation to call and test your API directly from the browser. You can access it at `/docs` with [Swagger](https://github.com/swagger-api/swagger-ui) or at `/redoc` with [Redoc](https://github.com/Rebilly/ReDoc).