import os
import zipfile
import customtkinter as ctk
import tkinter.filedialog

# Installer window using CustomTkinter
class InstallerWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Balatro CZ Patch Installer")
        self.geometry("400x300")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Status label at the top
        self.status_var = ctk.StringVar()
        self.label_status = ctk.CTkLabel(self, textvariable=self.status_var, text_color="orange")
        self.label_status.pack(pady=(10, 0))

        # Example variables (add more as needed)
        self.var_game_path = ctk.StringVar()
        self.var_backup = ctk.BooleanVar()

        # Game path input
        self.label_game_path = ctk.CTkLabel(self, text="Game Path:")
        self.label_game_path.pack(pady=(20, 0))

        # Frame for entry and browse button
        self.frame_game_path = ctk.CTkFrame(self)
        self.frame_game_path.pack(pady=5)
        self.entry_game_path = ctk.CTkEntry(self.frame_game_path, textvariable=self.var_game_path, width=220)
        self.entry_game_path.pack(side="left", padx=(0, 5))
        self.button_browse = ctk.CTkButton(self.frame_game_path, text="Browse", command=self.browse_folder, width=70)
        self.button_browse.pack(side="left")

        # Backup checkbox
        self.checkbox_backup = ctk.CTkCheckBox(self, text="Create Backup", variable=self.var_backup)
        self.checkbox_backup.pack(pady=10)

        # Frame for Patch and Restore buttons
        self.frame_buttons = ctk.CTkFrame(self)
        self.frame_buttons.pack(pady=20)
        self.button_patch = ctk.CTkButton(self.frame_buttons, text="Patch", command=self.on_patch, width=100)
        self.button_patch.pack(side="left", padx=(0, 10))
        self.button_restore = ctk.CTkButton(self.frame_buttons, text="Restore", command=self.on_restore, width=100)
        self.button_restore.pack(side="left")

    def browse_folder(self):
        folder_selected = tkinter.filedialog.askdirectory()
        if folder_selected:
            self.var_game_path.set(folder_selected)

    def on_patch(self):
        # Collect all variables when Patch button is clicked
        variables = {
            "game_path": self.var_game_path.get(),
            "backup": self.var_backup.get()
        }
        print("Collected variables:", variables)
        # You can also return or process these variables as needed
        if not self.var_game_path.get() and os.path.exists(self.var_game_path.get()):
            msg = "Please select a valid path"
        # if file named balatro.exe exists, continue, else msg = isnt balatro folder
        if not os.path.exists(os.path.join(self.var_game_path.get(), "balatro.exe")):
            msg = "Selected folder is not a valid Balatro folder"
        #open balatro.exe as zip and extract game.lua and put cz_cs.lua into localization folder
        with zipfile.ZipFile(os.path.join(self.var_game_path.get(), "balatro.exe"), 'r') as zip_ref:
            extract_path = self.var_game_path.get()
            zip_ref.extract("game.lua", extract_path)
            os.rename(
                os.path.join(extract_path, "game.lua"),
                os.path.join(extract_path, "game.lua.bak")
            )
            os.remove(os.path.join(extract_path, "game.lua"))
            with open(os.path.join(self.var_game_path.get(), "localization", "cz_cs.lua"), 'w') as f:
                f.write(open("cz_cs.lua", "r").read())
        self.status_var.set(msg)
        return msg

    def on_restore(self):
        # Implement restore functionality here
        print("Restore button clicked")

if __name__ == "__main__":
    app = InstallerWindow()
    app.mainloop()
