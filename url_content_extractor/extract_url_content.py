import requests
import re
from bs4 import BeautifulSoup
from typing import Optional

negative_tags = re.compile(
        r"header|combx|comment|com-|contact|foot|footer|footnote|masthead|media|meta|outbrain|promo|related|scroll|shoutbox|sidebar|sponsor|shopping|tags|tool|widget",
        re.I,
    )

positive_tags = re.compile(
        r"article|body|content|entry|hentry|main|page|pagination|post|text|blog|story",
        re.I,
    )

text_tags = re.compile(
        r"p|ul|table|li|row|col|h1|h2|h3|h4|h5|h6",
        re.I,
    )

def extract_url_content(url:str, output_file: Optional[str] = None):
    """
    Extracts the contents of a URL. If output file argument is provided the content is then saved to a Markdown or TXT file.
    
    Args:
    -----
        url (str): The URL to extract contents from.
        output_file (str, optional): The output file name. Defaults to None.
    
    Returns:
    -------
        str: The extracted contents."""
    if url == '' or url is None:
        raise ValueError('URL cannot be empty or None.')
    
    try:
        # Fetch HTML content from the URL
        response = requests.get(url)
        html_content = response.text
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException(f"Failed to fetch HTML content from {url}")
    
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    
    # Remove negative tags
    for tag in soup.find_all(True, {'class': negative_tags}):
        tag.decompose()
        
    # Check if the body tag exists
    if soup.body is None:
        raise ValueError('No body tag found.')
    
    # Extract contents from the <p> and <ul> tags
    elements = soup.body.find_all(['p', 'ul', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' , 'row' , 'col'])
    element_texts = []
    for element in elements:
        if element.name == 'p':
            element_texts.append(element.get_text())
        elif element.name == 'h1' or element.name == 'h2' or element.name == 'h3' or element.name == 'h4' or element.name == 'h5' or element.name == 'h6':
            element_texts.append('#'+element.get_text())
        elif element.name == 'ul':
            for li in element.find_all('li'):
                element_texts.append('- '+li.get_text())
        elif element.name == 'table':
            for row in element.find_all('tr'):
                for cell in row.find_all(['td', 'th']):
                    element_texts.append(cell.get_text())

    # Join the paragraphs and lists with newline characters
    body_content = '\n'.join(element_texts)
    
    if output_file is None:
        return body_content
    
    try:
        # Write contents to a Markdown file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(body_content)
    except Exception as e:
        raise ValueError(f"Failed to write to file {output_file}. Original error: {str(e)}")

    print(f"Contents extracted and saved to {output_file}")
    return body_content
