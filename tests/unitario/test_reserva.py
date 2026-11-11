import unittest
from datetime import datetime, timedelta

from src.compartilhado.enum import StatusReserva
from src.modulos.reserva.entidade.reserva import Reserva

class TestReserva(unittest.TestCase):
    def test_criar_reserva_normaliza_titulo(self):
        reserva = Reserva(
            titulo="   MEU BRASIL BRASILEIRO   ",
            cliente_id=1
        )

        self.assertEqual(
            reserva.titulo,
            "meu brasil brasileiro"
        )

    def test_criar_reserva_estado_inicial(self):
        reserva = Reserva(titulo="Dom Casmurro", cliente_id=1)

        self.assertEqual(reserva.status, StatusReserva.ABERTA)
        self.assertTrue(reserva.is_active)
        self.assertIsNone(reserva.material_id)
        self.assertIsNotNone(reserva.data)

    def test_cancelar_reserva(self):
        reserva = Reserva(titulo="Dom Casmurro", cliente_id=1)

        reserva.cancelar()

        self.assertFalse(reserva.is_active)
        self.assertEqual(reserva.status, StatusReserva.CANCELADA)

    def test_cancelar_reserva_inativa(self):
        reserva = Reserva(titulo="Dom Casmurro", cliente_id=1)

        reserva.cancelar()

        with self.assertRaises(ValueError):
            reserva.cancelar()

    def test_concluir_reserva(self):
        reserva = Reserva(titulo="Dom Casmurro", cliente_id=1)

        reserva.concluir()

        self.assertFalse(reserva.is_active)
        self.assertEqual(reserva.status, StatusReserva.ATENDIDA)

    def test_concluir_reserva_inativa(self):
        reserva = Reserva(titulo="Dom Casmurro", cliente_id=1)

        reserva.cancelar()

        with self.assertRaises(ValueError):
            reserva.concluir()

    def test_verificar_expiracao(self):
        reserva = Reserva(titulo="Dom Casmurro", cliente_id=1)

        reserva.data = (
            datetime.now() - timedelta(days=11)
        )

        resultado = reserva.verificar_expiracao()

        self.assertTrue(resultado)
        self.assertFalse(reserva.is_active)
        self.assertEqual(reserva.status, StatusReserva.EXPIRADA)

    def test_reserva_nao_expirada(self):
        reserva = Reserva(titulo="Dom Casmurro", cliente_id=1)

        reserva.data = (
            datetime.now() - timedelta(days=5)
        )

        resultado = reserva.verificar_expiracao()

        self.assertFalse(resultado)
        self.assertTrue(reserva.is_active)
        self.assertEqual(reserva.status, StatusReserva.ABERTA)

    def test_verificar_expiracao_reserva_inativa(self):
        reserva = Reserva(titulo="Dom Casmurro", cliente_id=1)

        reserva.cancelar()

        resultado = reserva.verificar_expiracao()

        self.assertFalse(resultado)
        self.assertEqual(reserva.status, StatusReserva.CANCELADA)

    def test_vincular_material(self):
        reserva = Reserva(titulo="Dom Casmurro", cliente_id=1)

        reserva.vincular_material(7)

        self.assertEqual(reserva.material_id, 7)

if __name__ == "__main__":
    unittest.main()
