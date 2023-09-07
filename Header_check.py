import argparse
import requests
# Define a dictionary with headers as keys and their solutions as values
HEADER_SOLUTIONS = {
    "E-tag": "Solution: Hey",
}

def check_headers(target, headers_to_display=None, show_solutions = False):
    # Opening try catch against http request problems
    try:
        if target:
            # Check if the target is a URL if not add http://
            if not target.startswith("http://") and not target.startswith("https://"):
                target = "http://" + target
            # Get response headers with request
            response = requests.get(target)
            # Get all headers app provides
            headers = response.headers
            
            # Headers_to_display for spesific header request with -header arg
            if headers_to_display:
                #Printing the spesific header
                print(f"Target: {target}")
                for header in headers_to_display:
                    if header in headers:
                        print("Requested Headers:")
                        print(f"{header}: {headers[header]}")
                    elif show_solutions and header in HEADER_SOLUTIONS:
                        print(f"{header}: Header not found or misconfigured")
                        print(HEADER_SOLUTIONS[header])
                    else:
                        print(f"{header}: Header not found or misconfigured. For solutions -solution")
            # in case of not getting a spesific header prints all headers that can be found
            else:
                print(f"Target: {target}")
                print("All Headers:")
                for key, value in headers.items():
                    print(f"{key}: {value}")
        else:
            print("Error: Please provide a target URL or IP address.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def main():
    #--help arg explantions
    parser = argparse.ArgumentParser(description="Check HTTP response headers of a target URL or IP. Can be used directly putting target url/IP after py file or can be put in when run")
    parser.add_argument("target", nargs="?", help="The URL or IP address to check")
    # -header header arg for spesific header check
    parser.add_argument("-header", nargs="+", help="Specify which response headers to check")
    # Solutions for missing or misconfigured headers
    parser.add_argument("-solution", action="store_true", help="Show solutions for missing or misconfigured headers")

    # assigns parsed command line argumants to args
    args = parser.parse_args()
    # assigns url/ip to target veriable if it given as arg 
    target = args.target
    
    
    # check if -heaader called
    if args.header:
        # Ask for url/ip if not given as arg
        if not target:
            target = input("Enter the target URL or IP address: ")
        # go to the fucntion with the header that wanted and solution arg info
        check_headers(target, args.header, args.solution)
    else:
        if not target:
            target = input("Enter the target URL or IP address: ")
        check_headers(target)
        
#makes sure scripts runs on main program
if __name__ == "__main__":
    main()
