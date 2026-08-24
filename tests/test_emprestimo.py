import unittest
from datetime import datetime, timedelta

from src.modulos.emprestimo.emprestimo import Emprestimo

class TestEmprestimo(unittest.TestCase):
    def test_devolver_emprestimo(self):
        emprestimo = Emprestimo()

        emprestimo.is_active = True
        emprestimo.status = "ABERTO"
        emprestimo.data_devolucao = None

        emprestimo.devolver()

        self.assertEqual(
            emprestimo.status,
            "DEVOLVIDO"
        )

        self.assertFalse(
            emprestimo.is_active
        )

        self.assertIsNotNone(
            emprestimo.data_devolucao
        )

        self.assertIsInstance(
            emprestimo.data_devolucao,
            datetime
        )

    def test_devolver_emprestimo_encerrado(self):
        emprestimo = Emprestimo()

        emprestimo.is_active = False
        emprestimo.status = "DEVOLVIDO"

        with self.assertRaises(ValueError):
            emprestimo.devolver()

    def test_validar_emprestimo_aberto(self):
        emprestimo = Emprestimo()

        emprestimo.data_devolucao = None

        resultado = emprestimo.validar_emprestimo()

        self.assertTrue(resultado)

    def test_validar_emprestimo_devolvido(self):
        emprestimo = Emprestimo()

        emprestimo.data_devolucao = datetime.now()

        resultado = emprestimo.validar_emprestimo()

        self.assertFalse(resultado)

    def test_verificar_atraso(self):
        emprestimo = Emprestimo()

        emprestimo.is_active = True
        emprestimo.status = "ABERTO"

        emprestimo.data_emprestimo = (
            datetime.now() - timedelta(days=31)
        )

        resultado = emprestimo.verificar_atraso()

        self.assertTrue(resultado)
        self.assertEqual(
            emprestimo.status,
            "ATRASADO"
        )

    def test_emprestimo_nao_atrasado(self):
        emprestimo = Emprestimo()

        emprestimo.is_active = True
        emprestimo.status = "ABERTO"

        emprestimo.data_emprestimo = (
            datetime.now() - timedelta(days=10)
        )

        resultado = emprestimo.verificar_atraso()

        self.assertFalse(resultado)
        self.assertEqual(
            emprestimo.status,
            "ABERTO"
        )


if __name__ == "__main__":
    unittest.main()