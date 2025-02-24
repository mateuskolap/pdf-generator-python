from dataclasses import dataclass, field

from reportlab.pdfgen import canvas


@dataclass
class HeaderInfo:
    title: str
    date: str
    header_font_size: float = 14


@dataclass
class CanvasGenerator(canvas.Canvas):
    filename: str
    infos: HeaderInfo
    pages: list = field(default_factory=list, init=False)

    def __post_init__(self):
        super().__init__(self.filename)
        self.width, self.height = self._pagesize

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            if self._pageNumber >= 1:
                self.draw_footer(page_count)
                if self._pageNumber == 1:
                    self.draw_header()
            super().showPage()
        super().save()

    def draw_header(self):
        self.setFont('Helvetica-Bold', self.infos.header_font_size)
        self.drawCentredString(self.width // 2, self.height - 50, self.infos.title)

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont('Helvetica', 7)

        page_counter = f'Página {self._pageNumber} de {page_count}'
        size_page_counter = self.stringWidth(page_counter)

        self.drawString(self.width - 20 - size_page_counter, 20, page_counter)
        self.drawString(20, 20, self.infos.date)
