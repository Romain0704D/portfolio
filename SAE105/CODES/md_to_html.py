
import markdown
import sys

def convert(md_filename, html_filename):
    try:
        with open(md_filename, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()
        html_content = markdown.markdown(md_content)
        with open(html_filename, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
        
        print(f"Le fichier Markdown {md_filename} a été converti en HTML sous {html_filename}.")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {md_filename} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python3 md_to_html.py <fichier_markdown> <fichier_html>")
    else:
        md_file = sys.argv[1]
        html_file = sys.argv[2]
        
        convert(md_file, html_file)
