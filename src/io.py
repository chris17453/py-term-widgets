
from .utils import utils

class io(utils):
    def save_file(self):
            """Saves the current file."""
            try:
                if self.filename:
                    # File saving logic
                    self.logger.info("File saved successfully.")
                else:
                    self.status_message = "No filename specified."
                    self.logger.warning("Attempted to save file without a filename.")
            except Exception as e:
                self.logger.error(f"Error saving file: {e}")
                self.status_message = f"Error saving file: {e}"
