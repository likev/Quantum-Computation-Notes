import requests
from pypdf import PdfWriter, PdfReader
import io

lectures = {
    "Preface": "Preface.pdf",
    "Chapter 1: Introduction": "Chapter1.pdf",
    "Chapter 2: Notation and Definitions": "Chapter2.pdf",
    "Chapter 3: Fundamental Algorithms": "Chapter3.pdf",
    "Chapter 4: Anatomy of a Learning Algorithm": "Chapter4.pdf",
    "Chapter 5: Basic Practice": "Chapter5.pdf",
    "Chapter 6: Neural Networks and Deep Learning": "Chapter6.pdf",
    "Chapter 7: Problems and Solutions": "Chapter7.pdf",
    "Chapter 8: Advanced Practice": "Chapter8.pdf",
    "Chapter 9: Unsupervised Learning": "Chapter9.pdf",
    "Chapter 10: Other Forms of Learning": "Chapter10.pdf",
    "Chapter 11: Conclusion and additional reading": "Chapter11.pdf"
}


# Base URL for the lectures
base_url = "https://github.com/likev/themlbook/raw/main/"

# Output file name for the concatenated PDF
output_pdf = "Andriy Burkov 2019 The Hundred-Page Machine Learning.pdf"

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
    
    is_chapter = False
    skip_pages = 2
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
                count_page = 0
                for page in reader.pages:
                    count_page += 1
                    if is_chapter and count_page <= skip_pages:
                        continue

                    writer.add_page(page)
                
                if is_chapter:
                    num_pages -= skip_pages
                
                print(f"Added Lecture {title} ({num_pages} pages)")

                current_page += num_pages
                
            else:
                print(f"Failed to download Lecture {title}")
            
            is_chapter = True # after Preface we set is_chapter to True
        except Exception as e:
            print(f"Error processing Lecture {title}: {str(e)}")
    
    # Write the final PDF
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"\nCreated PDF with {current_page} pages")
    print(f"Output saved as: {output_pdf}")

if __name__ == "__main__":
    create_pdf()
