from fpdf import FPDF


main_heading = "Rudrastra OSINT REPORT"
sub_heading = """NOTE: This report is strictly confidential and only for police officers.  
    Don't share it with anyone else or post it on WhatsApp, Telegram, or anywhere else public."""


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            self.set_fill_color(0, 150, 255)  # Navy blue
            self.rect(0, 0, 210, 20, "F")
            self.set_y(10)
            self.set_font("Arial", "B", 12)
            self.image("logo.png", 10, 5, 20)
            self.set_text_color(255, 255, 255)  # White
            self.cell(0, 10, main_heading, 0, 1, "C")
            self.set_text_color(0, 0, 0)  # White
            self.set_font("Arial", "I", 10)
            self.multi_cell(0, 10, sub_heading, 0, "C")
            self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")

    def add_table(self, data):
        self.set_font("Arial", "", 12)
        key_width = 50  # Adjust as necessary
        for key, value in data.items():
            self.set_text_color(105, 105, 105)  # Dark gray
            self.set_font("Arial", "B", 12)
            self.cell(key_width, 10, f"{key}:", 0, 0, "L")
            self.set_font("Arial", "", 12)
            self.set_text_color(0, 0, 0)  # Black

            if isinstance(value, dict):
                self.cell(0, 10, "", 0, 1, "L")
                self.add_table(value)  # Recursively add nested dictionary
            elif isinstance(value, list):
                self.cell(0, 10, "", 0, 1, "L")
                for item in value:
                    if isinstance(item, dict):
                        self.add_table(item)
                    else:
                        self.multi_cell(0, 10, f"- {item}", 0, "L")
            else:
                self.multi_cell(0, 10, f" {value}", 0, "L")
