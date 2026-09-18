from src.database.database import db

from src.modulos.emprestimo.emprestimo import Emprestimo
from src.modulos.reserva.reserva import Reserva

def atualizar_status_atrasados():
    sessao = db.session()

    try:
        emprestimos = sessao.query(Emprestimo).filter_by(
            is_active=True,
            status="ABERTO"
        ).all()

        for emprestimo in emprestimos:
            emprestimo.marcar_atrasado()

        sessao.commit()

    except Exception:
        sessao.rollback()
        raise

    finally:
        sessao.close()

def atualizar_expiradas():
    sessao = db.session()

    try:
        reservas = sessao.query(Reserva).filter_by(
            is_active=True
        ).all()

        for reserva in reservas:
            reserva.verificar_expiracao()

        sessao.commit()

    except Exception:
        sessao.rollback()
        raise

    finally:
        sessao.close()