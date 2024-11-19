import requests
from pypdf import PdfWriter, PdfReader
import io

lectures = {
    "Introduction and History": 1,
    "The Superposition Principle": 2,
    "Unitary Evolution and the Bloch Sphere": 3,
    "Quantum Measurements": 4,
    "Joint Quantum Systems and Tensor Products": 5,
    "More Tensor Products (Measurements of Joint Systems)": 6,
    "Classical Boolean circuits": 7,
    "Reversible Boolean circuits": 8,
    "Quantum gates I": 9,
    "Quantum gates II": 10,
    "Quantum Teleportation": 11,
    "Density Matrices I": 12,
    "Density Matrices II": 13,
    "The GHZ Experiment (theory)": 14,
    "Quantum Optics and the GHZ Experiment": 15,
    "The Deutsch-Jozsa Algorithm": 16,
    "Classical computational complexity theory": 17,
    "Simon's algorithm": 18,
    "The quantum Fourier transform": 19,
    "Phase Estimation": 20,
    "Quantum factoring algorithm": 21,
    "The Number Theory Needed for the Factoring Algorithm": 22,
    "The Discrete Log Algorithm": 23,
    "Grover's search algorithm": 24,
    "Proof that Grover Search is Optimal": 25,
    "Lecture on Hamiltonian Simulation": 26,
    "Introduction to Quantum error correcting codes --- the 9-qubit code": 27,
    "More on the 9-qubit code": 28,
    "The 7-qubit Quantum Hamming Code": 29,
    "Quantum CSS Codes": 30,
    "The BB84 Quantum Key Distribution Protocol and the Proof of Its Security": 31
}


# Base URL for the lectures
base_url = "https://math.mit.edu/~shor/435-LN/Lecture_"

# Output file name for the concatenated PDF
output_pdf = "Lecture Notes for 8.370-18.435 Quantum Computation from Fall 2022 Peter Shor.pdf"

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
    for title, num in lectures.items():
        url = f"{base_url}{num:02}.pdf"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pdf_content = io.BytesIO(response.content)
                reader = PdfReader(pdf_content)
                num_pages = len(reader.pages)
                
                # Add bookmark for this lecture
                writer.add_outline_item(
                    title=f"Lecture {num} --- {title}",
                    page_number=current_page,
                    color=[0, 0, 0],
                    bold=True
                )
                
                # Add all pages from this lecture
                for page in reader.pages:
                    writer.add_page(page)
                
                current_page += num_pages
                print(f"Added Lecture {num:02} ({num_pages} pages)")
            else:
                print(f"Failed to download Lecture {num:02}")
        except Exception as e:
            print(f"Error processing Lecture {num:02}: {str(e)}")
    
    # Write the final PDF
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"\nCreated PDF with {current_page} pages")
    print(f"Output saved as: {output_pdf}")

if __name__ == "__main__":
    create_pdf()
