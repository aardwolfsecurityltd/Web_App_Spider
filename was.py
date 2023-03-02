import os
import sys
import argparse
import requests
import pyfiglet
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

result = pyfiglet.figlet_format("Web App Spider")
print(result)

print('				   		   By Aardwolf Security\n\n')

# Define the user-agent string to use
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

# Define the maximum depth to spider
MAX_DEPTH = 10

def get_arguments():
    """
    Parse command line arguments and return them as a dictionary.
    """
    parser = argparse.ArgumentParser(description='Web spider that follows links and lists URLs discovered.')
    parser.add_argument('url', nargs='?', help='The URL to spider')
    parser.add_argument('-f', '--file', help='A file containing a list of URLs to spider')
    parser.add_argument('-o', '--output', default='output.txt', help='The name of the output file (default: output.txt)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output')
    return vars(parser.parse_args())

def check_dependencies():
    """
    Check if the required dependencies are installed and offer to install them if they are not.
    """
    try:
        import requests
        import bs4
    except ImportError:
        print('Some dependencies are missing. Do you want to install them? (y/n)')
        choice = input().lower()
        if choice == 'y':
            os.system('pip install requests')
            os.system('pip install beautifulsoup4')
        else:
            sys.exit()

def get_urls(url, depth, visited, output_file, verbose):
    """
    Recursively spider a website starting from the given URL.
    """
    # Check if the URL has already been visited
    if url in visited:
        return
    visited.add(url)

    # Parse the URL to extract the domain and path
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    # Check if the URL is out of scope
    if domain != parsed_start_url.netloc or depth > MAX_DEPTH:
        return

    # Make a request to the URL
    headers = {'User-Agent': USER_AGENT}
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        if verbose:
            print(f'Error while fetching {url}: {e}')
        return

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Write the URL to the output file
    output_file.write(url + '\n')

    # Find all the links in the page
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            # Join the link URL with the base URL to get the absolute URL
            absolute_url = urljoin(url, href)
            # Recursively spider the absolute URL
            get_urls(absolute_url, depth+1, visited, output_file, verbose)

if __name__ == '__main__':
    # Parse the command line arguments
    args = get_arguments()

    # Check if the required dependencies are installed
    check_dependencies()

    # Create the output file
    output_file = open(args['output'], 'w')

    # Determine the list of URLs to spider
    urls = []
    if args['url']:
        urls.append(args['url'])
    elif args['file']:
        with open(args['file']) as f:
            for line in f:
                urls.append(line.strip())

    # Check that at least one URL has been provided
    if not urls:
        print('Please provide a URL or a file containing a list of URLs.')
        sys.exit()

    # Create a set to keep track of visited URLs
    visited = set()

    # Start spidering the URLs
    if args['verbose']:
        print('Spidering...')
    for url in urls:
        # Parse the start URL to extract the domain and path
        parsed_start_url = urlparse(url)

        # Spider the URL
        get_urls(url, 0, visited, output_file, args['verbose'])

    # Close the output file
    output_file.close()

    # Remove duplicate lines from the output file
    lines_seen = set()
    output_file = open(args['output'], 'r+')
    lines = output_file.readlines()
    output_file.seek(0)
    output_file.truncate()
    for line in sorted(lines):
        if line not in lines_seen:
            lines_seen.add(line)
            output_file.write(line)

    # Print a message to indicate success
    if args['verbose']:
        print('Done.')
