# README

## Covidence Conflict Data Extractor

This project provides a script to extract conflict information from Covidence by processing JSON data embedded in the webpage's `<script>` tags. It handles pagination and supports processing up to 1108 entries per page by saving the webpage and manually copying the required JSON data.

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8+
- `pip` (Python package manager)

### Installation
1. Clone the repository or download the script files.
2. Navigate to the project directory in your terminal.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Steps to Extract Data
1. **Navigate to the Correct URL:**
   Open your browser and navigate to:
   ```
   https://app.covidence.org/reviews/495872/review_studies/screen?filter=votes_in_conflict&per_page=1108
   ```

2. **Save the Webpage:**
   Save the webpage content (including the `<script>` tags) to your local machine. This ensures you have access to the embedded JSON data.

3. **Extract JSON Data:**
   Open the saved webpage file and locate the `<script>` tag containing JSON data. Copy the JSON content into a new file named `conflict_info.html` in the project directory.

4. **Run the Script:**
   Execute the script to extract and save the data:
   ```bash
   python extract_v2.py
   ```

5. **Handle Double Quotes:**
   If you encounter errors related to unescaped double quotes in titles or abstracts, manually edit the JSON data in `conflict_info.html` to escape them (e.g., `"`).

### Output
The script generates:
- `all_studies.xlsx`: An Excel file containing extracted conflict data, saved in the project directory.

### Customization
If needed, you can:
- Modify the `base_url` variable in the script to point to different Covidence review IDs or filters.
- Adjust JSON parsing logic to handle additional or alternative data formats.

### Troubleshooting
- **Unauthorized Errors:** Ensure the URL you save contains the correct `per_page=1108` parameter.
- **JSON Decoding Errors:** Review and fix any unescaped characters in the JSON data.
- **Missing Data:** Verify that the correct `<script>` tag with JSON data has been copied into `conflict_info.html`.

---

## File Structure
- `extract_v2.py`: The main script to process and extract data.
- `conflict_info.html`: The manually prepared file containing JSON data from Covidence.
- `all_studies.xlsx`: The output Excel file containing extracted data.
- `requirements.txt`: Dependencies required to run the script.

---

# REQUIREMENTS.TXT
```
pandas
requests
openpyxl
```

