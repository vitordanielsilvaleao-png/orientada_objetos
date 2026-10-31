import unittest
from datetime import datetime, timedelta

from src.compartilhado.enum import StatusEmprestimo
from src.modulos.emprestimo.entidade.emprestimo import Emprestimo

class TestEmprestimo(unittest.TestCase):
    def test_devolver_emprestimo(self):
        emprestimo = Emprestimo(material_id=1, cliente_id=1)

        emprestimo.devolver()

        self.assertEqual(emprestimo.status, StatusEmprestimo.DEVOLVIDO)
        self.assertFalse(emprestimo.is_active)
        self.assertIsNotNone(emprestimo.data_devolucao)

    def test_devolver_emprestimo_encerrado(self):
        emprestimo = Emprestimo(material_id=1, cliente_id=1)

        emprestimo.devolver()

        with self.assertRaises(ValueError):
            emprestimo.devolver()

    def test_validar_emprestimo_aberto(self):
        emprestimo = Emprestimo(material_id=1, cliente_id=1)

        resultado = emprestimo.validar_emprestimo_ativo()

        self.assertTrue(resultado)

    def test_validar_emprestimo_devolvido(self):
        emprestimo = Emprestimo(material_id=1, cliente_id=1)

        emprestimo.devolver()

        resultado = emprestimo.validar_emprestimo_ativo()

        self.assertFalse(resultado)

    def test_verificar_atraso(self):
        emprestimo = Emprestimo(material_id=1, cliente_id=1)

        emprestimo.data_emprestimo = (
            datetime.now() - timedelta(days=31)
        )

        resultado = emprestimo.verificar_atraso()

        self.assertTrue(resultado)

    def test_emprestimo_nao_atrasado(self):
        emprestimo = Emprestimo(material_id=1, cliente_id=1)

        emprestimo.data_emprestimo = (
            datetime.now() - timedelta(days=10)
        )

        resultado = emprestimo.verificar_atraso()

        self.assertFalse(resultado)