import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from ultralytics import YOLO
from transformers import pipeline

# --- INITIALIZE MODELS ---
print("Loading Safety Engines... please wait.")
# Model 1: NSFW Detector
safety_model = pipeline("image-classification", model="AdamCodd/vit-base-nsfw-detector")
# Model 2: Weapon Detector (YOLOv8)
weapon_model = YOLO("yolov8n.pt")  # Initial download is ~6MB

class ImageVerifierApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Startup Image Moderator & Weapon Detector")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        
        # UI Elements
        self.label = ctk.CTkLabel(self, text="Image Verification System", font=("Arial", 24))
        self.label.pack(pady=20)

        self.btn_select = ctk.CTkButton(self, text="Select Image to Verify", command=self.verify_image)
        self.btn_select.pack(pady=10)

        self.result_text = ctk.CTkTextbox(self, width=500, height=200)
        self.result_text.pack(pady=20)
        self.result_text.insert("0.0", "Waiting for image...")

    def verify_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", f"Analyzing: {os.path.basename(file_path)}\n\n")
        
        try:
            # --- STEP 1: Check for NSFW Content ---
            safety_results = safety_model(Image.open(file_path))
            nsfw_score = next(item['score'] for item in safety_results if item['label'] == 'nsfw')
            
            # --- STEP 2: Check for Weapons (COCO Classes: 43=knife, 0=person... we want 'firearm' categories) ---
            # Using standard YOLOv8n, we check for 'knife' (class 43)
            # For a dedicated 'Gun' detector, you'd load a specialized .pt file
            weapon_results = weapon_model(file_path)[0]
            detected_objects = [weapon_model.names[int(box.cls)] for box in weapon_results.boxes]
            
            # Specific weapon list
            illegal_items = ["knife", "scissors", "gun", "pistol", "rifle"]
            found_weapons = [item for item in detected_objects if item in illegal_items]

            # --- STEP 3: Display Results ---
            self.result_text.insert("end", f"Safety Score (NSFW): {round(nsfw_score * 100, 2)}%\n")
            self.result_text.insert("end", f"Detected Objects: {', '.join(detected_objects) if detected_objects else 'None'}\n\n")

            if nsfw_score > 0.4 or found_weapons:
                self.result_text.insert("end", "VERDICT: [!] REJECTED\n", "red")
                if found_weapons:
                    self.result_text.insert("end", f"REASON: Weapon detected ({', '.join(found_weapons)})")
                else:
                    self.result_text.insert("end", "REASON: Inappropriate content.")
            else:
                self.result_text.insert("end", "VERDICT: [✓] APPROVED\n", "green")

        except Exception as e:
            self.result_text.insert("end", f"Error analyzing image: {e}")

if __name__ == "__main__":
    app = ImageVerifierApp()
    app.mainloop()