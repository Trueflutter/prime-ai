import os
import json
from datetime import datetime
from pathlib import Path
import pdfkit
from jinja2 import Environment, FileSystemLoader

class ProfileDocumentGenerator:
    def __init__(self, templates_dir, output_dir):
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Set up Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
    def generate_profile_document(self, user_data):
        """Generate a formatted profile document for the user"""
        try:
            # Load the profile document template
            template = self.env.get_template('profile_document_template.html')
            
            # Prepare context data for the template
            context = {
                'user': user_data,
                'generated_date': datetime.now().strftime('%B %d, %Y'),
                'logo_path': os.path.join(self.templates_dir, 'static', 'logo.png')
            }
            
            # Render the template with the context data
            html_content = template.render(**context)
            
            # Generate a unique filename for the PDF
            filename = f"{user_data['first_name']}_{user_data['user_id'][:8]}_profile.pdf"
            output_path = self.output_dir / filename
            
            # Convert HTML to PDF
            pdfkit.from_string(html_content, str(output_path))
            
            return str(output_path)
        
        except Exception as e:
            print(f"Error generating profile document: {e}")
            return None
    
    def generate_html_preview(self, user_data):
        """Generate an HTML preview of the profile document"""
        try:
            # Load the profile document template
            template = self.env.get_template('profile_document_template.html')
            
            # Prepare context data for the template
            context = {
                'user': user_data,
                'generated_date': datetime.now().strftime('%B %d, %Y'),
                'preview_mode': True
            }
            
            # Render the template with the context data
            html_content = template.render(**context)
            
            # Generate a unique filename for the HTML preview
            filename = f"{user_data['first_name']}_{user_data['user_id'][:8]}_profile_preview.html"
            output_path = self.output_dir / filename
            
            # Save the HTML preview
            with open(output_path, 'w') as f:
                f.write(html_content)
            
            return str(output_path)
        
        except Exception as e:
            print(f"Error generating HTML preview: {e}")
            return None
