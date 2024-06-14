import os
import argparse
import json
import shutil
import pymupdf
import pprint
import settings

from pathlib import Path


OUTPUT_FILE = "output.pdf"

if __name__ == "__main__":
  print(f"Input: '{settings.INPUT_FILE}'")
  shutil.copy(settings.INPUT_FILE, OUTPUT_FILE)
  print(f"Output: '{OUTPUT_FILE}'")
  print(f"Json file: '{settings.JSON_FILE}'")
  with open(settings.JSON_FILE, "r", encoding='utf-8') as f:
    json_data = json.load(f)
  pprint.pp(json_data, indent=2, sort_dicts=False)

  out_doc = pymupdf.open(OUTPUT_FILE)


  # test stamping text
  page = out_doc[0]  # new or existing page via doc[n]
  p = pymupdf.Point(32, 120)  # start point of 1st line4
  
  print(f"is_wrapped: {page.is_wrapped}")
  if not(page.is_wrapped):
    page.wrap_contents() # reset page origin
  page.clean_contents() # reset page origin

  text = "Some text,\nspread across\nseveral lines."
  # the same result is achievable by
  # text = ["Some text", "spread across", "several lines."]

  rc = page.insert_text(p,  # bottom-left of 1st char
                       text,  # the text (honors '\n')
                       fontname = "helv",  # the default font
                       fontsize = 20,  # the default font size
                       rotate = 0,  # also available: 90, 180, 270
                       )

  print()
  print("%i lines printed on page %i." % (rc, page.number))

  out_doc.save(out_doc.name, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)

  # test stamping html text
  rect = pymupdf.Rect(0, 0, 400, 300)
  html_text = "<b>Bold</b> t<b style='color:#1f1;font-size:40'>eशि क्या </b>xt </br><li style='color:#f00'> - list</li>"
  arch = pymupdf.Archive("./")
  css = ""
  css += "\n@font-face {font-family: Noto Sans; src: url(NotoSans-VariableFont_wdth,wght.ttf);}"
  css += "\n@font-face {font-family: Tiny5; src: url(Tiny5-Regular.ttf);}"
  css += "\n* {font-family: Noto Sans; font-size:14px; color:#11d}"
  html = page.insert_htmlbox(rect=rect, text=html_text, css=css, archive=arch)
  out_doc.subset_fonts(verbose=True)  # build subset fonts to reduce file size
  out_doc.save(out_doc.name, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)

  # 11 lines
  GRID = True
  breakpoint()
  if GRID:
    for page in out_doc.pages():
      # breakpoint()
      mediabox = page.mediabox
      start_pt = pymupdf.Point(mediabox.x0, mediabox.y0)
      end_pt = pymupdf.Point(mediabox.x1, mediabox.y1)
      page.add_line_annot(start_pt, end_pt)
      step_px = 25
      grid_font_size = 5
      print(f"grid with step_px: {step_px}")
      print(f"mediabox: {mediabox}")
      for x in range(int(mediabox.x0), int(mediabox.x1), int(step_px)):
        start_pt = pymupdf.Point(x, mediabox.y0)
        end_pt = pymupdf.Point(x, mediabox.y1)
        page.add_line_annot(start_pt, end_pt)
        text_pt = start_pt + pymupdf.Point(2, grid_font_size + 1)
        rc = page.insert_text(text_pt,
                             f"{x:.1f}",
                             fontname = "helv",
                             fontsize = grid_font_size,
                             color=(1,0,0),
                             )
      for y in range(int(mediabox.y0), int(mediabox.y1), int(step_px)):
        start_pt = pymupdf.Point(mediabox.x0, y)
        end_pt = pymupdf.Point(mediabox.x1, y)
        page.add_line_annot(start_pt, end_pt)
        text_pt = start_pt + pymupdf.Point(2, grid_font_size + 1)
        rc = page.insert_text(text_pt,
                             f"{y:.1f}",
                             fontname = "helv",
                             fontsize = grid_font_size,
                             color=(1,0,0),
                             )
      out_doc.save(out_doc.name, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)

    
  # test coords
  page = out_doc[0]
  print(f"is_wrapped: {page.is_wrapped}")
  if not(page.is_wrapped):
    page.wrap_contents() # reset page origin
  page.clean_contents() # reset page origin
  
  p = pymupdf.Point(151, 286)  # start point of 1st line
  p = p * page.transformation_matrix
  p = pymupdf.Point(118, 212)  # start point of 1st line
  print(p)
  # breakpoint()
  # p = pymupdf.Point(0, 20)  # start point of 1st line

  text = f"Test coords {p}"
  # the same result is achievable by
  # text = ["Some text", "spread across", "several lines."]

  rc = page.insert_text(p,  # bottom-left of 1st char
                       text,  # the text (honors '\n')
                       fontname = "Tiny5",
                       fontfile = "Tiny5-Regular.ttf",
                       # fontname = "helv",  # the default font
                       fontsize = 20,  # the default font size
                       rotate = 0,  # also available: 90, 180, 270
                       )

  out_doc.save(out_doc.name, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)

  
 