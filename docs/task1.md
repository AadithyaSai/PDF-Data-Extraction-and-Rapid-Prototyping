# Task 1

## Solution
Made a script to read an image and perform preprocessing and OCR on it with opencv and tesseract. For reading table data, after removing table grid, the table is dilated vertically to form column contours which are iterated through and OCR is performed column-wise on them. The remaining non-tabular data is also gathered and saved in a different CSV file

If a pdf is provided, the first page is extracted and stored as an image before OCR preprocessing is done

## Assumptions Made
* Only single page PDF supported

* Assumed there is no data to the sides of the table

* Sparse font styles are not properly supported

* Non-table data in the document is stored in a different CSV file

## Challenges Faced
* Experimented with many table detection algorithms to detect tables. However no satisfactory results were obtained so for simplicity the users have to manually enter the column coordinates

* Due to caching issues with the webapp, multi-page PDFs had to be abandoned

* The script was originally going to feature a CLI interface which as abandoned due to time constraints

* The kernel for column dilation still requires extensive fine tuning to be able to handle all cases well
