import argparse
import requests
#from headers import check_header


def check_header(header_value, header_name, show_solutions=False):
    if header_name == "Strict-Transport-Security":
        # Check if the header is missing entirely
        if not header_value:
            print("Strict-Transport-Security header is missing.")
            if show_solutions:
                print("Solution: Add a Strict-Transport-Security header to enforce HTTPS.")
            return

        # Split the header value into key-value pairs
        directives = header_value.split(";")

        # Check if max-age directive is present and set to a reasonable value (e.g., one year)
        max_age_directive = [directive.strip() for directive in directives if directive.startswith("max-age=")]
        if not max_age_directive:
            print("Strict-Transport-Security header is missing the max-age directive.")
            if show_solutions:
                print("Solution: Add the max-age directive to specify the duration.")
            return
        elif max_age_directive[0] != "max-age=31536000" and max_age_directive[0] != "max-age=63072000":
            print(f"Strict-Transport-Security max-age directive is set to {max_age_directive[0]}, which may be too short.")
            if show_solutions:
                print("Solution: Set the max-age directive to a longer duration (e.g., max-age=31536000 for one year).")

        # Check for other directives (includeSubDomains, preload, etc.)
        for directive in directives:
            directive = directive.strip()
            if directive == "includeSubDomains":
                print("Strict-Transport-Security includes the 'includeSubDomains' directive.")
                print("This is recommended to enforce HSTS for all subdomains.")
            elif directive == "preload":
                print("Strict-Transport-Security includes the 'preload' directive.")
                print("This indicates that the site is included in the HSTS preload list.")
                print("It's recommended for increased security, but you should review the preload list requirements.")
    
        # If no misconfigurations found, return Value
        print(header_value)


    #X-FRAME-OPTIONS
    elif header_name == "X-Frame-Options":
        # Check if the header is missing entirely
        if not header_value:
            print("X-Frame-Options header is missing.")
            if show_solutions:
                print("Solution: Add an X-Frame-Options header to control framing behavior.")
        else:
            # Split the header value into individual directives
            directives = header_value.split(";")

            # Check for valid directives
            for directive in directives:
                directive = directive.strip()
                if directive in ["DENY", "SAMEORIGIN"]:
                    continue
                elif directive.startswith("ALLOW-FROM"):
                    print(f"X-Frame-Options directive '{directive}' is not recommended.")
                    if show_solutions:
                        print("Solution: Use 'DENY' or 'SAMEORIGIN' to prevent clickjacking.")
                else:
                    print(f"Invalid X-Frame-Options directive: '{directive}'.")
                    if show_solutions:
                        print("Solution: Use 'DENY' or 'SAMEORIGIN' to prevent clickjacking.")

        # If no misconfigurations found, return Value
        print(header_value)
    

    #X-CONTENT-TYPE-OPTIONS
    elif header_name == "X-Content-Type-Options":
        # Check if the header is missing entirely
        if not header_value:
            print("X-Content-Type-Options header is missing.")
            if show_solutions:
                print("Solution: Add an X-Content-Type-Options header to prevent MIME sniffing.")
        else:
            # Check if the header value is 'nosniff'
            if header_value.strip().lower() != "nosniff":
                print(f"X-Content-Type-Options value '{header_value}' is not set to 'nosniff'.")
                if show_solutions:
                    print("Solution: Set the X-Content-Type-Options header value to 'nosniff'.")

        # If no misconfigurations found, return Value
        print(header_value)





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
                    #Printing the spesific header
                    print(f"Target: {target}")
                    # Checking the header with check_header func in headers.py
                    for header in headers_to_display:
                        header_value = headers.get(header)
                        check_header(header_value, header, show_solutions)
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
