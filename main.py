import pymupdf
import re
import sys
from pathlib import Path

# Made 3/27/2026
# Specifically made for my Twrite Book to easily get chapters so I can split them.

book = None
if len(sys.argv) < 2 or not Path(sys.argv[1]).is_file():
	print("[!] Please put the book in the same folder of this program and run `python main.py book-title.pdf`")
	print("[!] NOTE: File name is case sensitive!")
	sys.exit()

book = sys.argv[1]
	
def get_chapter_range(pdf_path, target_chapter):
	with pymupdf.open(pdf_path) as doc:
		toc = doc.get_toc()
	
		target_start_page = None
		target_end_page = None
		chapter_title = None

		current_chapter_num = re.search(r'(\d+)', target_chapter)

		if not current_chapter_num:
			return "Invalid chapter format"
		
		current_chapter_num = int(current_chapter_num.group(1))
		next_chapter_num = current_chapter_num + 1
		
		for level, title, start_page in toc:

			if level != 1:
				continue

			match = re.search(r'(\d+)', title)
			if not match:
				continue

			num = int(match.group(1))
			
			if num == current_chapter_num:
				target_start_page = start_page
				chapter_title = title.strip()
				continue

			if num == next_chapter_num:
				target_end_page = start_page
				break

		print(f"[✓] File: {pdf_path}")	
		if target_start_page is not None and target_end_page is not None:
			return f"[✓] {chapter_title} | pg. {target_start_page} - {target_end_page - 1}"
		else:
			return f"[!] Unable to get range of Chapter {target_chapter}"
            
chapter = input("Input chapter: ")
get_range = get_chapter_range(book, chapter)
print(get_range)