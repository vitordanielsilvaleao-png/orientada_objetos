from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from emprestimo.router.emprestimo_router import EmprestimoRouter
from src.modulos.reserva.router.reserva_router import ReservaRouter
from src.modulos.cliente.router.cliente_router import ClienteRouter
from src.modulos.revista.router.revista_router import RevistaRouter
from src.modulos.material.routers.editora_router import EditoraRouter
from src.modulos.material.routers.categoria_router import CategoriaRouter
from src.modulos.livro.routers.livro_router import LivroRouter
from src.modulos.livro.routers.autor_router import AutorRouter

#Instanciação da classe FastAPI
app = FastAPI()

#Liberações necessárias para receber requisições do Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Instancia um objeto da Router da Classe LivroRouter
livro_router = LivroRouter()
app.include_router(livro_router.router, prefix="/livro")

#Instancia um objeto da Router da Classe RevistaRouter
revista_router = RevistaRouter()
app.include_router(revista_router.router, prefix="/revista")

#Instancia um objeto da Router da Classe AutorRouter
autor_router = AutorRouter()
app.include_router(autor_router.router, prefix="/autor")

#Instancia um objeto da Router da Classe CategoriaRouter
categoria_router = CategoriaRouter()
app.include_router(categoria_router.router, prefix="/categoria")

#Instancia um objeto da Router da Classe EditoraRouter
editora_router = EditoraRouter()
app.include_router(editora_router.router, prefix="/editora")

#Instancia um objeto da Router da Classe ClienteRouter
cliente_router = ClienteRouter()
app.include_router(cliente_router.router, prefix="/cliente")

#Instancia um objeto da Router da Classe ReservaRouter
reserva_router = ReservaRouter()
app.include_router(reserva_router.router, prefix="/reserva")

#Instancia um objeto da Router da Classe EmprestimoRouter
emprestimo_router = EmprestimoRouter()
app.include_router(emprestimo_router.router, prefix="/emprestimo")


#Tratamento de erro de ValueError
@app.exception_handler(ValueError)
async def generic_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": str(exc),
            "data": {"status_code": 400}
        }
    )

#Tratamentos de erro de HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    print(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": {"status_code": exc.status_code}
        }
    )

#Tratamento de erros inesperados
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal_Error!",
            "data": {"status_code": 500}
        }
    )