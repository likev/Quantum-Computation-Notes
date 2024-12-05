import requests
from pypdf import PdfWriter, PdfReader
import io

lectures = {
    "Contents": "Contents.pdf",
    "1. The Basics": "Ch1.pdf",
    "2. Matching, covering and packing": "Ch2.pdf",
    "3. Connectivity": "Ch3.pdf",
    "4. Planar graphs": "Ch4.pdf",
    "5. Colouring": "Ch5.pdf",
    "6. Flows": "Ch6.pdf",
    "7. Extremal graph theory": "Ch7.pdf",
    "8. Infinite graphs": "Ch8.pdf",
    "9. Ramsey theory for graphs": "Ch9.pdf",
    "10. Hamilton cycles": "Ch10.pdf",
    "11. Random graphs": "Ch11.pdf",
    "12. Minors, trees and WQO": "Ch12.pdf",
    "Appendices": "Appendices.pdf",
}


# Base URL for the lectures
base_url = "https://www.math.uni-hamburg.de/home/diestel/books/graph.theory/preview/"

# Output file name for the concatenated PDF
output_pdf = "Graph Theory Reinhard Diestel Sixth edition 2024 Free Preview.pdf"

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
