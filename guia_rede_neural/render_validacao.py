from pathlib import Path
import fitz

pdf = fitz.open(Path(__file__).parents[1] / "Guia_Projeto_Rede_Neural.pdf")
out = Path(__file__).parent / "validacao"
out.mkdir(exist_ok=True)
for page_number in [0, 2, 5, 10, 16]:
    page = pdf[page_number]
    pix = page.get_pixmap(matrix=fitz.Matrix(1.35, 1.35), alpha=False)
    pix.save(out / f"pagina_{page_number + 1:02d}.png")
print("rendered", len([0, 2, 5, 10, 16]))
