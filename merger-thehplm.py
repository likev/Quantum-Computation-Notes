import requests
from pypdf import PdfWriter, PdfReader
import io

lectures = {
    "Preface": "preface.pdf",
    "About the Book": "about.pdf",
    "Chapter 1. Machine Learning Basics": "chapter_1.pdf",
    "Chapter 2. Language Modeling Basics": "chapter_2.pdf",
    "Chapter 3. Recurrent Neural Network": "chapter_3.pdf",
    "Chapter 4. Transformer": "chapter_4.pdf",
    "Chapter 5. Large Language Model": "chapter_5.pdf",
    "Chapter 6. Further Reading": "chapter_6.pdf"
}


# Base URL for the lectures
base_url = "https://github.com/likev/thelmbook/raw/main/"

# Output file name for the concatenated PDF
output_pdf = "Andriy Burkov 2025 The Hundred-Page Language Models.pdf"

def create_pdf():
    writer = PdfWriter()
    current_page = 0
    
    '''
    # TODO
    # Add blank pages for TOC
    for _ in range(3):
        writer.add_blank_page(width=612, height=792)
    current_page += 3
    '''
    
    # Download and add PDFs
    for title, filename in lectures.items():
        url = f"{base_url}{filename}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pdf_content = io.BytesIO(response.content)
                reader = PdfReader(pdf_content)
                num_pages = len(reader.pages)
                
                # Add bookmark for this lecture
                writer.add_outline_item(
                    title=f"{title}",
                    page_number=current_page,
                    color=[0, 0, 0],
                    bold=True
                )
                
                # Add all pages from this lecture
                for page in reader.pages:
                    writer.add_page(page)
                
                current_page += num_pages
                print(f"Added Lecture {title} ({num_pages} pages)")
            else:
                print(f"Failed to download Lecture {title}")
        except Exception as e:
            print(f"Error processing Lecture {title}: {str(e)}")
    
    # Write the final PDF
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"\nCreated PDF with {current_page} pages")
    print(f"Output saved as: {output_pdf}")

if __name__ == "__main__":
    create_pdf()
