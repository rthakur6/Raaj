import os
import re
import fitz  # PyMuPDF

# Define the folder path
folder_path = '/Volumes/SanDisk/NDA - PDF'

# Function to extract emails from a PDF file
def extract_emails_from_pdf(filepath):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = set()  # Using a set to avoid duplicates within a single PDF
    try:
        with fitz.open(filepath) as pdf:
            for page in pdf:
                text = page.get_text()
                emails.update(re.findall(email_pattern, text))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return emails

# Main script logic
def main():
    total_pdfs = 0
    pdfs_with_emails = 0
    all_emails = set()  # Collect all unique emails
    skipped_pdfs = []
    no_email_pdfs = []  # PDFs without emails

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            total_pdfs += 1
            filepath = os.path.join(folder_path, filename)

            try:
                emails = extract_emails_from_pdf(filepath)
                if emails:
                    pdfs_with_emails += 1
                    all_emails.update(emails)
                    # Append document name and emails to results file
                    with open("Extracted Emails.txt", "a", encoding="utf-8") as file:
                        file.write(f'"{filename}": {", ".join(sorted(emails))}\n')
                else:
                    # Track PDFs without emails
                    no_email_pdfs.append(filename)
            except Exception as e:
                skipped_pdfs.append(filename)
                print(f"Error processing {filename}: {e}")

    # Save the unique emails list
    with open("All Emails List.txt", "w", encoding="utf-8") as file:
        file.write(", ".join(sorted(all_emails)))

    # Save the skipped PDFs
    if skipped_pdfs:
        with open("Skipped PDFs.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(skipped_pdfs))

    # Save the PDFs without emails
    if no_email_pdfs:
        with open("No Emails PDFs.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(no_email_pdfs))

    # Summary output
    print("Email extraction completed. Results saved to Extracted Emails.txt and All Emails List.txt")
    print(f"Total PDFs indexed: {total_pdfs}")
    print(f"Total PDFs with emails extracted: {pdfs_with_emails}")
    if skipped_pdfs:
        print(f"Total PDFs skipped: {len(skipped_pdfs)}. See Skipped PDFs.txt for details.")
    if no_email_pdfs:
        print(f"Total PDFs without emails: {len(no_email_pdfs)}. See No Emails PDFs.txt for details.")

# Run the script
if __name__ == "__main__":
    main()