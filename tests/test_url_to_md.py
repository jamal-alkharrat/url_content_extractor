import pytest
from unittest import mock
import requests_mock
import requests

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from url_content_extractor.extract_url_content import extract_url_content

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def test_extract_url_content_with_empty_url():
    with pytest.raises(ValueError, match="URL cannot be empty or None."):
        extract_url_content('', 'test_output.md')

def test_extract_url_content_with_request_exception():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', exc=requests.exceptions.RequestException)
        with pytest.raises(requests.exceptions.RequestException, match=f"Failed to fetch HTML content from http://test.com"):
            extract_url_content('http://test.com', 'test_output.md')

def test_extract_url_content_with_no_body():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='<p>Hello, world!</p>')
        with pytest.raises(ValueError, match="No body tag found."):
            extract_url_content('http://test.com', 'test_output.md')
        
def test_extract_url_content():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='<body><p>Hello, world!</p></body>')
        result = extract_url_content('http://test.com', 'test_output.md')
        assert result == 'Hello, world!'

def test_extract_url_content_with_list():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='<body><ul><li>Item 1</li><li>Item 2</li></ul></body>')
        result = extract_url_content('http://test.com', 'test_output.md')
        assert result == '- Item 1\n- Item 2'

def test_extract_url_content_with_table():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='<body><table><tr><td>Cell 1</td><td>Cell 2</td></tr></table></body>')
        result = extract_url_content('http://test.com', 'test_output.md')
        assert result == 'Cell 1\nCell 2'

def test_extract_url_content_with_headers():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='<body><h1>Header 1</h1><h2>Header 2</h2></body>')
        result = extract_url_content('http://test.com', 'test_output.md')
        assert result == '#Header 1\n#Header 2'
        
def test_extract_url_content_with_negative_tags():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='<body><script>console.log("Hello, world!")</script></body>')
        result = extract_url_content('http://test.com', 'test_output.md')
        assert result == ''
        
def test_extract_url_content_with_file_write_error():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='<html><body><h1>Hello, world!</h1></body></html>')
        with mock.patch('builtins.open', mock.mock_open()) as m:
            m.side_effect = Exception('File write error')
            with pytest.raises(ValueError, match="Failed to write to file test_output.md. Original error: File write error"):
                extract_url_content('http://test.com', 'test_output.md')