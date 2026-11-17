import unittest

from fastapi.testclient import TestClient

from src.compartilhado.tradutor_validacao import TradutorValidacao
from src.main import app


class TestTradutorValidacao(unittest.TestCase):

    def test_traduz_erro_de_tamanho_minimo(self):
        erro = {"type": "string_too_short", "loc": ("body", "cpf"), "msg": "String should have at least 11 characters", "ctx": {"min_length": 11}}

        self.assertEqual(
            TradutorValidacao.traduzir_erro(erro),
            "CPF: deve ter pelo menos 11 caractere(s)"
        )

    def test_traduz_campo_obrigatorio(self):
        erro = {"type": "missing", "loc": ("body", "cliente_id"), "msg": "Field required"}

        self.assertEqual(
            TradutorValidacao.traduzir_erro(erro),
            "Cliente: é obrigatório"
        )

    def test_traduz_id_invalido_na_url(self):
        erro = {"type": "int_parsing", "loc": ("path", "livro_id"), "msg": "Input should be a valid integer"}

        self.assertEqual(
            TradutorValidacao.traduzir_erro(erro),
            "ID: deve ser um número inteiro"
        )

    def test_traduz_json_invalido(self):
        erro = {"type": "json_invalid", "loc": ("body", 1), "msg": "JSON decode error"}

        self.assertEqual(
            TradutorValidacao.traduzir_erro(erro),
            "O corpo da requisição não é um JSON válido"
        )

    def test_tipo_desconhecido_nao_devolve_ingles(self):
        erro = {"type": "tipo_novo", "loc": ("body", "nome"), "msg": "Some english message"}

        self.assertEqual(
            TradutorValidacao.traduzir_erro(erro),
            "Nome: possui um valor inválido"
        )

    def test_junta_varios_erros(self):
        erros = [
            {"type": "greater_than", "loc": ("body", "numero"), "ctx": {"gt": 0}},
            {"type": "string_too_long", "loc": ("body", "bairro"), "ctx": {"max_length": 50}}
        ]

        self.assertEqual(
            TradutorValidacao.traduzir(erros),
            "Número: deve ser maior que 0; Bairro: deve ter no máximo 50 caracteres"
        )

    def test_api_devolve_mensagem_traduzida_no_422(self):
        cliente = TestClient(app)

        resposta = cliente.post("/emprestimo", json={"material_id": "x"})

        self.assertEqual(resposta.status_code, 422)
        self.assertEqual(
            resposta.json()["message"],
            "Material: deve ser um número inteiro; Cliente: é obrigatório"
        )


if __name__ == "__main__":
    unittest.main()
