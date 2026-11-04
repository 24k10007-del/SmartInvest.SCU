import logging
import os

# Membuat folder logs (jika belum ada)
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/backend.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("backend")