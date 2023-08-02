from pydantic import BaseModel
import stat
import os

class Input(BaseModel):
    contents: str

    def save(self, path: str):
        mode = os.O_RDWR
        
        # Create directory if needed
        if not os.path.exists(os.path.dirname(path)):
            print(f"Creating directory {path}")
            os.makedirs(os.path.dirname(path))
            
        # if last character is a slash, return
        if path[-1] == "/":
            return None
        
        with open(path, "w") as file:
            file.write(self.contents) # Note, files aren't going to be updated or written on the local fs, only within Docker
        with open(path, "r") as file:
            return file.read()
