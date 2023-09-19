import logging
import fmcapi


def test__backup(fmc):
    logging.info("Test Backup.  Get, delete Backups.")

    obj1 = fmcapi.Backup(fmc=fmc)
    obj1.get()
    del(obj1)

    # Requires existing backup and there does not seem to be a way to initiate an FMC backup from the API
    # There is a way to initiate a device backup with /backup/operational/devicebackup

    # obj1 = fmcapi.Backup(fmc=fmc)
    # obj1.delete(targetId='manager', backupVersion=1694394505)

    logging.info("Test Backup done.\n")
