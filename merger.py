import requests
from PyPDF2 import PdfMerger

# Base URL for the lectures
base_url = "https://math.mit.edu/~shor/435-LN/Lecture_"

# Number of lectures (in this case, 31)
num_lectures = 31

# Output file name for the concatenated PDF
output_pdf = "Lecture Notes for 8.370-18.435 Quantum Computation from Fall 2022 Peter Shor.pdf"

# Initialize PdfMerger object
merger = PdfMerger()

# Loop through all lecture numbers and download each PDF
for i in range(1, num_lectures + 1):
    # Construct the full URL for each lecture
    url = f"{base_url}{i:02}.pdf"  # Format lecture number as two digits (e.g., Lecture_01.pdf)
    
    # Download the PDF
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save the PDF temporarily
        temp_pdf = f"Lecture_{i:02}.pdf"
        with open(temp_pdf, 'wb') as f:
            f.write(response.content)
        
        # Append the PDF to the merger object
        merger.append(temp_pdf)
        print(f"Downloaded and added Lecture {i:02}")
    else:
        print(f"Failed to download Lecture {i:02}")

# Write all merged PDFs into a single output file
with open(output_pdf, 'wb') as output_file:
    merger.write(output_file)

# Close the PdfMerger object
merger.close()

print(f"All lectures have been concatenated into {output_pdf}")
