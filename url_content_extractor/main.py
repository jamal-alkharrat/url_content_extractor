import argparse
from extract_url_content import extract_url_content

def main():
    parser = argparse.ArgumentParser(description='Convert a URL to Markdown.')
    parser.add_argument('--url', type=str, help='The URL to convert.')
    parser.add_argument('--output', type=str, default=None, help='The output file name.')
    args = parser.parse_args()

    print(extract_url_content(args.url, args.output))

if __name__ == '__main__':
    main()