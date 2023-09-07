from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sys
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import settings
import os
import tkinter.messagebox

def convert_images_to_pdf(image_paths, output_path):
    pdf_canvas = canvas.Canvas(output_path, pagesize=letter)
    for image_path in image_paths:
        image = Image.open(image_path)
        image_width, image_height = image.size
        pdf_canvas.setPageSize((image_width, image_height))
        pdf_canvas.drawImage(image_path, 0, 0, width=image_width, height=image_height)
        pdf_canvas.showPage()
    pdf_canvas.save()

def dangtaitrang(a, b, c):
    while a >= 0:
        os.system("cls")
        print(b + str(a) + "s")
        time.sleep(1)
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        a -= 1
    print(c)
    os.system("cls")

image_paths = []
output_path = "./output/" + settings.output_name + '.pdf'

# Setting trình duyệt và tạo driver
chrome_options = webdriver.ChromeOptions()
options = Options()
options.add_argument("--headless")
options.add_argument("window-size=10000,10000")

driver = webdriver.Chrome(executable_path=settings.driver_path,
                          chrome_options=options)
# Xử lý
driver.get(settings.url)
dangtaitrang(settings.thoi_gian_tai_trang, "Đang tải trang: ", "Đã tải trang. ")
driver.execute_script("""$FlowPaper("documentViewer").Zoom(""" + str(settings.zoom) + """)""")

print("Đang tải ảnh " + str(settings.trang_bat_dau), end="\r")
# Tải liên tục từ x đến hết
for i in range(settings.trang_bat_dau - 1, settings.trang_ket_thuc):
    element = driver.find_element(By.ID, "dummyPage_" + str(i) + "_documentViewer")
    element.screenshot(settings.path_luu_anh + "/" + str(i+1) + ".png")
    driver.execute_script("""$FlowPaper("documentViewer").nextPage()""")
    
    dangtaitrang(settings.thoi_gian_tai_anh, "Đang tải ảnh " + str(i+1) + ": ", "Đã tải ảnh " + str(i+1) + " ")
    image_paths.append(settings.path_luu_anh + "/" + str(i+1) + ".png")
"""
element = driver.find_element(By.ID, "dummyPage_" + str(settings.trang_ket_thuc - 1) + "_documentViewer")
element.screenshot(settings.path_luu_anh + "/" + str(settings.trang_ket_thuc) + ".png")

image_paths.append(settings.path_luu_anh + "/" + str(settings.trang_ket_thuc) + ".png")
"""
convert_images_to_pdf(image_paths, output_path)
for image_path in image_paths:
    os.remove(image_path)
print("Kết thúc")
tkinter.messagebox.showinfo("AJCdownload", "Tải Xong Rồi Nè")