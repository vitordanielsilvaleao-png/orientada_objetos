# importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Livro
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates
from src.modulos.material.entidades.material import Material

# Criação da entidade Livro que herda atributos da entidade Material
class Livro(Material):
    __tablename__ = "livro"

    id: Mapped[int] = mapped_column(
        ForeignKey("material.id"),
        primary_key=True
    )

    isbn: Mapped[str] = mapped_column(
        String(13),
        nullable=False,
        unique=True,
        primary_key=True
    )

    autor_id: Mapped[int] = mapped_column(
        ForeignKey("autor.id"),
        nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": "livro",
    }

    #Declaração do construtor da Classe
    def __init__(
            self,
            titulo,
            ano_publi,
            categoria_id,
            editora_id,
            isbn,
            autor_id
    ):
        super().__init__(
            titulo,
            ano_publi,
            categoria_id,
            editora_id
        )

        self.isbn = isbn
        self.autor_id = autor_id

    #Validação de dados recebidos
    @validates("isbn")
    def validar_isbn(self, chave, isbn):
        isbn_normalizado = self._normalizar_isbn(isbn)
        self._validar_isbn(isbn_normalizado)
        return isbn_normalizado

    # Métodos para validação e normalização de dados do construtor
    @staticmethod
    def _normalizar_isbn(isbn):
        return isbn.replace(".", "").replace("-", "")

    @staticmethod
    def _validar_isbn(isbn):
        if len(isbn) != 13 or not isbn.isdigit():
            raise ValueError(
                "O ISBN informado é inválido"
            )

    #Método para atualizar livros
    def atualizar(
            self,
            titulo=None,
            ano_publi=None,
            categoria_id=None,
            editora_id=None,
            autor_id=None
    ):
        super().atualizar(
            titulo,
            ano_publi,
            categoria_id,
            editora_id
        )

        if autor_id is not None:
            self.autor_id = autor_id
