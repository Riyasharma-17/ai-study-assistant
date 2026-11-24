from PIL import Image, ImageDraw
import pypdfium2 as pdfium

# Create a scanned-style image page
img = Image.new("RGB", (800, 300), color="white")
draw = ImageDraw.Draw(img)
draw.text((40, 80), "Invoice #4092 - Vendor: Acme Cloud Systems", fill="black")
draw.text((40, 130), "Total Due: $4,250.00 | Payment Terms: Net 30", fill="black")
img.save("documents/scanned_sample.pdf", "PDF", resolution=150.0)
print("Saved documents/scanned_sample.pdf")
