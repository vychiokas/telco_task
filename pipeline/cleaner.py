from .controller.db_manager import DatabaseManager
from .model.data_model import Usage
import datetime
from utils.logger import LOG
class Cleaner:
    _EXPIRATION_DAYS = 181
    
    @classmethod
    def delete_old_entries(cls, dbm:DatabaseManager):
        limit = datetime.datetime.now() - datetime.timedelta(days=Cleaner._EXPIRATION_DAYS)
        dbm().session.query(Usage).filter(Usage.event_start_time < limit).delete()
        dbm().session.commit()
        LOG.info("Uneccessary data removed")
