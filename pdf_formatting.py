from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            self.set_fill_color(0, 0, 128)  # Navy blue
            self.rect(0, 0, 210, 20, "F")
            self.set_y(10)
            self.set_font("Arial", "B", 12)
            self.image("logo.png", 10, 5, 20)
            self.cell(0, 10, "Main Heading", 0, 1, "C")
            self.set_font("Arial", "I", 10)
            self.cell(0, 10, "Sub Heading", 0, 1, "C")
            self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")

    def add_table(self, data, indent=0):
        self.set_font("Arial", "", 12)
        key_width = 40
        self.set_x(indent)
        for key, value in data.items():
            self.set_text_color(105, 105, 105)  # Dark gray
            self.set_font("Arial", "B", 12)
            self.cell(key_width, 10, f"{key}:", 0, 0, "L")
            self.set_font("Arial", "", 12)
            self.set_text_color(0, 0, 0)  # Black

            if isinstance(value, dict):
                self.cell(0, 10, "", 0, 1, "L")
                self.add_table(value, indent)  # Recursively add nested dictionary
            elif isinstance(value, list):
                self.cell(0, 10, "", 0, 1, "L")
                for item in value:
                    if isinstance(item, dict):
                        self.add_table(item, indent)
                    else:
                        self.cell(indent, 10, f"- {item}", 0, 1, "L")
            else:
                self.cell(0, 10, str(value), 0, 1, "L")
