import logging
from rich.logging import RichHandler

FORMAT = " %(message)s"
logging.basicConfig(
    level=logging.INFO, 
    format=FORMAT, 
    datefmt="[%X]", 
    handlers=[RichHandler(show_time=False, show_path= False)]
)

log = logging.getLogger("rich")

class AppLogger:
    @staticmethod
    def info(message):
        log.info(f"[blue]{message}", extra=dict(markup=True))
    
    def error(message):
        log.error(f"[red]{message}", extra=dict(markup=True))
    
    def warning(message):
        log.warning(f"[yellow]{message}", extra=dict(markup=True))
    
    def critical(message):
        log.critical(f"[bright_red]{message}", extra=dict(markup=True))
    
    def debug(message):
        log.debug(f"[bright_white]{message}", extra=dict(markup=True))

