from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request

async def traduzir_erro_validacao(request: Request, exc: RequestValidationError):
    """
    Traduz e formata os erros de validação (422) do Pydantic para um formato amigável.
    """
    erros_formatados = []
    for erro in exc.errors():
        campo = " -> ".join(str(loc) for loc in erro["loc"])
        mensagem = erro["msg"]
        erros_formatados.append({
            "campo": campo,
            "erro": mensagem
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Erro de validação nos dados enviados.",
            "erros": erros_formatados,
            "data": {"status_code": 422}
        }
    )