import unittest
from datetime import datetime, timedelta

from src.modulos.reserva.reserva import Reserva

class TestReserva(unittest.TestCase):
    def test_cancelar_reserva(self):
        reserva = Reserva()

        reserva.is_active = True

        reserva.cancelar()

        self.assertFalse(reserva.is_active)

    def test_cancelar_reserva_inativa(self):
        reserva = Reserva()

        reserva.is_active = False

        with self.assertRaises(ValueError):
            reserva.cancelar()

    def test_verificar_expiracao(self):
        reserva = Reserva()

        reserva.is_active = True
        reserva.data = (
            datetime.now() - timedelta(days=11)
        )

        resultado = reserva.verificar_expiração()

        self.assertTrue(resultado)
        self.assertFalse(reserva.is_active)

    def test_reserva_nao_expirada(self):
        reserva = Reserva()

        reserva.is_active = True
        reserva.data = (
            datetime.now() - timedelta(days=5)
        )

        resultado = reserva.verificar_expiração()

        self.assertFalse(resultado)
        self.assertTrue(reserva.is_active)

    def test_verificar_expiracao_reserva_inativa(self):
        reserva = Reserva()

        reserva.is_active = False

        resultado = reserva.verificar_expiração()

        self.assertFalse(resultado)

if __name__ == "__main__":
    unittest.main()