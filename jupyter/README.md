## Author Data Processing

This folder contains Jupyter notebooks for processing and integrating author data into a Django-based library system.

1. **001_generate_authors.csv.ipynb**

   - Converts `authors.json` to `authors.csv` for analysis.
   - Uses `pandas` to transform JSON data into CSV format.
   - Outputs `authors.csv` for further filtering.
2. **002_filter_authors.ipynb**

   - Filters authors based on criteria such as valid photo URLs, English names, and book data
   - Validates author details and extracts book titles from the `about` field.
   - Outputs a filtered `authors_filtered.csv` file containing valid authors with their books.
3. **003_integrate_with_django.ipynb**

   - Processes the filtered author data and inserts it into a PostgreSQL database.
   - Reads data from CSV, validates authors, and inserts them into the `library_author` table.
   - Books associated with each author are inserted into the `library_book` table.
   - Inserts data in chunks, avoiding duplicates with the `ON CONFLICT` clause.
   - Ensures only valid author data is added, with a limit on the number of authors processed.

# Authors Dataset

This project utilizes the **Large Books Metadata Dataset** from Kaggle, specifically the `authors.json` file, which contains detailed author information. The dataset is used to enrich the book recommendation system.

You can download the dataset from:
[Kaggle - Large Books Metadata Dataset](https://www.kaggle.com/datasets/opalskies/large-books-metadata-dataset-50-mill-entries/data).

### Dataset Path

The `authors.json` file is saved locally at:

```bash
   /authors/authors.json
```

Adjust the file path as needed for your setup.

---
