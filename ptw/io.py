import os
from .utils import utils

class io(utils):
    def save_file(self):
            """Saves the current file."""
            try:
                if self.filename:
                    # File saving logic
                    output="\n".join(self.text)
                    # Writing the joined string to the file
                    with open(self.filename, 'w') as file:
                        file.write(output)

                    print(f"Joined string written to {self.filename}")
                    self.logger.info("File saved successfully.")
                else:
                    self.logger.warning("Attempted to save file without a filename.")
            except Exception as e:
                self.logger.error(f"Error saving file: {e}")

    def open_file(self,filename):
            try:
                if filename and os.path.exists(filename):
                    with open(filename, 'r') as file:
                        self.text = [line.strip('\n\r') for line in file.readlines()]
            except Exception as e:
                self.logger.error(f"Error loading file: {e}")
