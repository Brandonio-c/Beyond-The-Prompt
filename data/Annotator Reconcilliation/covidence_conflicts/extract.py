from bs4 import BeautifulSoup
import json
import pandas as pd
import os
import re


def clean_json_like_data(script_text):
    """
    Clean and convert JavaScript-like objects into valid JSON format.
    """
    try:
        # Locate the fourth opening bracket as the start of the JSON-like data
        bracket_indices = [i for i, char in enumerate(script_text) if char == '{']
        if len(bracket_indices) < 4:
            raise ValueError("Unable to find the fourth opening bracket in the script.")
        start_idx = bracket_indices[3]

        # Locate the end of the JSON object by finding the last valid closing curly brace
        open_braces = 0
        end_idx = None
        for i, char in enumerate(script_text[start_idx:], start=start_idx):
            if char == '{':
                open_braces += 1
            elif char == '}':
                open_braces -= 1
                if open_braces == 0:
                    end_idx = i + 1
                    break

        if end_idx is None:
            raise ValueError("Could not locate the end of the JSON object.")

        json_like_content = script_text[start_idx:end_idx]

        # Save the raw content for debugging
        #with open('raw_json_like_content.txt', 'w', encoding='utf-8') as debug_file:
        #    debug_file.write(json_like_content)

        # Handle colons and escaped double quotes only within the "title" part
        def remove_colons_in_title(match):
            title_content = match.group(1)
            title_content = re.sub(r':', '', title_content)  # Remove colons within the title content
            title_content = title_content.replace('\"', "'")  # Replace escaped double quotes with single quotes
            title_content = title_content.replace('"', "'")  # Replace double quotes with single quotes
            return f'"title": "{title_content}"'

        json_like_content = re.sub(
            r'"title":\s*"(.*?)"',  # Match the "title" field
            remove_colons_in_title,
            json_like_content
        )

        # Handle colons and escaped double quotes only within the "abstract" part
        def remove_colons_in_abstract(match):
            abstract_content = match.group(1)
            abstract_content = re.sub(r':', '', abstract_content)  # Remove colons within the abstract content
            abstract_content = abstract_content.replace('\"', "'")  # Replace escaped double quotes with single quotes
            abstract_content = abstract_content.replace('"', "'")  # Replace double quotes with single quotes
            return f'"abstract": "{abstract_content}"'

        json_like_content = re.sub(
            r'"abstract":\s*"(.*?)"',  # Match the "abstract" field
            remove_colons_in_abstract,
            json_like_content
        )


        json_like_content = json_like_content.replace('\\"', '"')
        json_like_content = re.sub(r"(?<=\{|,)\s*([\w$]+)\s*:", r'"\1":', json_like_content)
        json_like_content = re.sub(r",\s*}", "}", json_like_content)
        json_like_content = re.sub(r",\s*]", "]", json_like_content)
        

        # Parse and return valid JSON
        return json.loads(json_like_content)

    except json.JSONDecodeError as e:
        # Save problematic content for debugging
        with open('error_json_content.txt', 'w', encoding='utf-8') as error_file:
            error_file.write(json_like_content)  # Save problematic content
        print(f"JSON decoding error at line {e.lineno}, column {e.colno}: {e.msg}")
        return None

    except Exception as e:
        # Save problematic content for debugging
        with open('error_json_content.txt', 'w', encoding='utf-8') as error_file:
            error_file.write(json_like_content)
        print(f"Error parsing JSON in script: {e}")
        return None


def extract_script_data(html_file, intermediate_json_file):
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all <script> tags
    script_tags = soup.find_all('script')

    # Extract JSON data
    json_data_list = []
    for script in script_tags:
        if 'Covidence.StudiesController.initialize' in script.text:
            cleaned_data = clean_json_like_data(script.text)
            if cleaned_data:
                json_data_list.append(cleaned_data)

    # Save intermediate JSON data
    with open(intermediate_json_file, 'w', encoding='utf-8') as file:
        json.dump(json_data_list, file, indent=4)
    print(f"Intermediate JSON saved to {intermediate_json_file}")

import json
import pandas as pd

def extract_data_from_json(json_file, output_excel):
    """
    Extract study data from the intermediate JSON file and save it to an Excel file.
    Additionally, create individual reports for each annotator with Annotator 1 being the report's owner.
    Generate a conflict summary report showing disagreements between annotators.
    """
    try:
        # Load the JSON data
        with open(json_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    # Extract studies
    extracted_data = []
    annotator_reports = {}
    disagreement_matrix = {}

    for entry in json_data:
        # Check for the 'studies' key
        studies = entry.get('studies', [])
        for study in studies:
            # Prepare votes information
            votes = study.get('votes', [])
            annotators = [vote.get('reviewer_name', 'N/A') for vote in votes]
            vote_values = [vote.get('vote', 'N/A') for vote in votes]

            # Ensure we have up to 2 annotators
            annotator_1 = annotators[0] if len(annotators) > 0 else 'N/A'
            vote_1 = vote_values[0] if len(vote_values) > 0 else 'N/A'
            annotator_2 = annotators[1] if len(annotators) > 1 else 'N/A'
            vote_2 = vote_values[1] if len(vote_values) > 1 else 'N/A'

            study_entry = {
                'Study ID': study.get('id'),
                'Unique Index': study.get('unique_index'),
                'Title': study.get('title'),
                'Authors': study.get('authors'),
                'Abstract': study.get('abstract'),
                'Journal Info': study.get('journal_info'),
                'Publisher Info': study.get('publisher_info'),
                'DOI': study.get('references', [{}])[0].get('doi') if study.get('references') else None,
                'Annotator 1': annotator_1,
                'Vote 1': vote_1,
                'Annotator 2': annotator_2,
                'Vote 2': vote_2,
            }
            extracted_data.append(study_entry)

            # Check for disagreement
            if vote_1 != vote_2 and vote_1 != 'N/A' and vote_2 != 'N/A':
                disagreement_matrix.setdefault(annotator_1, {}).setdefault(annotator_2, 0)
                disagreement_matrix[annotator_1][annotator_2] += 1
                disagreement_matrix.setdefault(annotator_2, {}).setdefault(annotator_1, 0)
                disagreement_matrix[annotator_2][annotator_1] += 1

            # Add study to each annotator's report
            for i, annotator in enumerate(annotators):
                vote = vote_values[i]
                report_entry = {**study_entry}
                # Adjust Annotator 1 and 2 for the specific report
                report_entry['Annotator 1'] = annotator
                report_entry['Vote 1'] = vote
                report_entry['Annotator 2'] = annotators[1 - i] if len(annotators) > 1 else 'N/A'
                report_entry['Vote 2'] = vote_values[1 - i] if len(vote_values) > 1 else 'N/A'

                if annotator not in annotator_reports:
                    annotator_reports[annotator] = []
                annotator_reports[annotator].append(report_entry)

    # Save all studies to a single Excel file
    if extracted_data:
        df = pd.DataFrame(extracted_data)
        df.to_excel(output_excel, index=False)
        print(f"Data extracted and saved to {output_excel}")
    else:
        print("No data extracted from the JSON file.")

    # Save individual reports for each annotator
    reports_dir = "annotator_reports"
    os.makedirs(reports_dir, exist_ok=True)

    for annotator, studies in annotator_reports.items():
        report_file = os.path.join(reports_dir, f"{annotator.replace(' ', '_')}_report.xlsx")
        pd.DataFrame(studies).to_excel(report_file, index=False)
        print(f"Annotator report saved for {annotator}: {report_file}")

    # Generate the conflict report summary
    conflict_summary = []
    annotators = list(disagreement_matrix.keys())
    total_disagreements = {annotator: 0 for annotator in annotators}

    for annotator_1 in sorted(disagreement_matrix.keys()):
        annotator_disagreements = []
        for annotator_2, count in sorted(disagreement_matrix[annotator_1].items(), key=lambda x: -x[1]):
            conflict_summary.append({
                'Annotator 1': annotator_1,
                'Annotator 2': annotator_2,
                'Disagreements': count
            })
            annotator_disagreements.append(count)
            total_disagreements[annotator_1] += count

        # Add a row for total disagreements per Annotator 1
        conflict_summary.append({
            'Annotator 1': annotator_1,
            'Annotator 2': 'Total',
            'Disagreements': sum(annotator_disagreements)
        })

    # Add final total disagreements summary
    conflict_summary.append({})
    conflict_summary.append({'Annotator 1': 'Total Disagreements Across All Annotators:'})
    for annotator, total in total_disagreements.items():
        conflict_summary.append({'Annotator 1': annotator, 'Disagreements': total})

    # Save the conflict summary to an Excel file
    conflict_summary_file = "conflict_report_summary.xlsx"
    conflict_df = pd.DataFrame(conflict_summary)
    conflict_df.to_excel(conflict_summary_file, index=False)
    print(f"Conflict summary report saved to {conflict_summary_file}")



# Example usage
current_directory = os.path.dirname(__file__)
html_file = os.path.join(current_directory, 'conflict_info.html')
intermediate_json_file = os.path.join(current_directory, 'intermediate_data.json')
json_file = os.path.join(current_directory, 'intermediate_data.json')
output_excel = os.path.join(current_directory, 'conflicts.xlsx')

# Step 1: Extract JSON from HTML and save as intermediate file
# extract_script_data(html_file, intermediate_json_file)

# Step 2: Process intermediate JSON file to extract and save data to Excel
extract_data_from_json(intermediate_json_file, output_excel)