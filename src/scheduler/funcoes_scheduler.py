from src.database.database import db
import logging

from src.modulos.emprestimo.emprestimo import Emprestimo
from src.modulos.reserva.reserva import Reserva

logger = logging.getLogger(__name__)

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

        logger.info("Status dos empréstimos atrasados atualizado com sucesso.")

    except Exception:
        sessao.rollback()

        logger.exception(
            "Erro ao atualizar status dos empréstimos atrasados."
        )

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

        logger.info("Reservas expiradas atualizadas com sucesso.")

    except Exception:
        sessao.rollback()

        logger.exception(
            "Erro ao atualizar reservas expiradas."
        )

    finally:
        sessao.close()