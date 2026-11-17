#Declaração da classe TradutorValidacao, que converte os erros de validação do Pydantic (em inglês) em mensagens em português
class TradutorValidacao:

    #Nomes amigáveis dos campos usados nos schemas e nas rotas
    NOMES_CAMPOS = {
        "titulo": "Título",
        "ano_publi": "Ano de publicação",
        "categoria_id": "Categoria",
        "editora_id": "Editora",
        "autor_id": "Autor",
        "material_id": "Material",
        "cliente_id": "Cliente",
        "isbn": "ISBN",
        "issn": "ISSN",
        "edicao": "Edição",
        "nome": "Nome",
        "cpf": "CPF",
        "telefone": "Telefone",
        "rua": "Rua",
        "numero": "Número",
        "complemento": "Complemento",
        "bairro": "Bairro"
    }

    #Mensagens por tipo de erro do Pydantic; os valores entre chaves vêm do "ctx" do erro
    MENSAGENS = {
        "missing": "é obrigatório",
        "string_too_short": "deve ter pelo menos {min_length} caractere(s)",
        "string_too_long": "deve ter no máximo {max_length} caracteres",
        "string_type": "deve ser um texto",
        "greater_than": "deve ser maior que {gt}",
        "greater_than_equal": "deve ser maior ou igual a {ge}",
        "less_than": "deve ser menor que {lt}",
        "less_than_equal": "deve ser menor ou igual a {le}",
        "int_parsing": "deve ser um número inteiro",
        "int_type": "deve ser um número inteiro",
        "int_from_float": "deve ser um número inteiro",
        "bool_parsing": "deve ser verdadeiro ou falso",
        "enum": "possui um valor inválido"
    }

    #Erros que se referem ao corpo da requisição inteiro, e não a um campo
    MENSAGENS_CORPO = {
        "json_invalid": "O corpo da requisição não é um JSON válido",
        "model_attributes_type": "O corpo da requisição deve ser um objeto JSON",
        "dict_type": "O corpo da requisição deve ser um objeto JSON",
        "missing": "O corpo da requisição é obrigatório"
    }

    #Método para traduzir a lista de erros devolvida por RequestValidationError.errors()
    @classmethod
    def traduzir(cls, erros: list[dict]) -> str:
        mensagens = [cls.traduzir_erro(erro) for erro in erros]

        #Remove mensagens repetidas mantendo a ordem
        return "; ".join(dict.fromkeys(mensagens))

    #Método para traduzir um único erro no formato "Campo: mensagem"
    @classmethod
    def traduzir_erro(cls, erro: dict) -> str:
        tipo = erro.get("type", "")
        campo = cls._obter_campo(erro.get("loc", ()))

        if campo is None:
            return cls.MENSAGENS_CORPO.get(tipo, "O corpo da requisição é inválido")

        modelo = cls.MENSAGENS.get(tipo, "possui um valor inválido")

        try:
            mensagem = modelo.format(**erro.get("ctx", {}))
        except KeyError:
            mensagem = "possui um valor inválido"

        return f"{cls._nome_amigavel(campo)}: {mensagem}"

    #Método para obter o nome do campo a partir do "loc" do erro, ignorando a origem (body, path, query) e posições numéricas
    @staticmethod
    def _obter_campo(loc) -> str | None:
        partes = [parte for parte in loc if isinstance(parte, str) and parte not in ("body", "path", "query")]

        return partes[-1] if partes else None

    #Método para obter o nome amigável de um campo
    @classmethod
    def _nome_amigavel(cls, campo: str) -> str:
        if campo in cls.NOMES_CAMPOS:
            return cls.NOMES_CAMPOS[campo]

        #Ids da URL, como livro_id ou reserva_id
        if campo.endswith("_id"):
            return "ID"

        return campo.replace("_", " ").capitalize()
