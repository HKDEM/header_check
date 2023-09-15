import argparse
import requests
from termcolor import colored  # Import termcolor for colored output

def check_header(header_value, header_name):
    
    #STRICT-TRANSPORT-SECURİTY (HSTS)
    if header_name == "Strict-Transport-Security":
        # Check if the header is missing entirely
        if not header_value:
            # High severity for missing header
            print(colored("Strict-Transport-Security header is missing.", "red"))
            print(colored("Security Risk: Without HSTS, your site may be vulnerable to downgrade attacks, where an attacker can force the use of HTTP instead of HTTPS, potentially exposing sensitive data.", "red"))
            print("Solution: Add a Strict-Transport-Security header to enforce HTTPS.")
            return

        # Split the header value into key-value pairs
        directives = header_value.split(";")

        # Check if max-age directive is present and set to a reasonable value (e.g., one year)
        max_age_directive = [directive.strip() for directive in directives if directive.startswith("max-age=")]
        if not max_age_directive:
            # High severity for missing directive
            print(colored("Strict-Transport-Security header is missing the max-age directive. See solutions with -solution", "red"))
            print(colored("Security Risk: Without a max-age directive, HSTS effectiveness is limited, and your site may remain vulnerable to downgrade attacks.", "red"))
            print("Solution: Add the max-age directive to specify the duration.")
            return
        elif max_age_directive[0] != "max-age=31536000" and max_age_directive[0] != "max-age=63072000":
            # Medium severity for short max-age
            print(colored(f"Strict-Transport-Security max-age directive is set to {max_age_directive[0]}, which may be too short.", "yellow"))
            print(colored("Security Risk: A short max-age directive reduces the effectiveness of HSTS and may require more frequent updates.", "red"))
            print("Solution: Set the max-age directive to a longer duration (e.g., max-age=31536000 for one year).")
            return

        # Check for other directives (includeSubDomains, preload, etc.)
        for directive in directives:
            directive = directive.strip()
            if directive == "includeSubDomains":
                # Low severity for optional directive
                print(colored("Strict-Transport-Security includes the 'includeSubDomains' directive.", "green"))
                print(colored("This is recommended to enforce HSTS for all subdomains.", "green"))
                return
            elif directive == "preload":
                # Low severity for optional directive
                print(colored("Strict-Transport-Security includes the 'preload' directive.", "green"))
                print(colored("This indicates that the site is included in the HSTS preload list.", "green"))
                print(colored("It's recommended for increased security, but you should review the preload list requirements.", "green"))
                return
    
        # If no misconfigurations found, return Value
        print(colored(header_value, "blue"))
        print(colored("No security risks identified. Strict-Transport-Security header is properly configured.", "blue"))



    #X-FRAME-OPTIONS
    elif header_name == "X-Frame-Options":
        # Check if the header is missing entirely
        if not header_value:
            print(colored("Severity: High", "red"))
            print(colored("X-Frame-Options header is missing.", "red"))
            print(colored("Security Risk: Without X-Frame-Options, your site may be vulnerable to clickjacking attacks. Clickjacking is a technique where an attacker embeds your site in a malicious iframe to trick users into performing unintended actions on your site.", "red"))
            print("Solution: Add an X-Frame-Options header to control framing behavior.")
            return

        # Split the header value into individual directives
        directives = header_value.split(";")

        # Check for valid directives
        for directive in directives:
            directive = directive.strip()
            if directive in ["DENY", "SAMEORIGIN"]:
                continue
            elif directive.startswith("ALLOW-FROM"):
                print(colored(f"X-Frame-Options directive '{directive}' is not recommended.", "yellow"))
                print(colored("Security Risk: ALLOW-FROM directive allows framing from specific domains, but it can be risky if not configured properly. It may open your site to clickjacking attacks if misconfigured.", "red"))
                print("Solution: Use 'DENY' or 'SAMEORIGIN' to prevent clickjacking.")
                return
            else:
                print(colored(f"Invalid X-Frame-Options directive: '{directive}'.", "yellow"))
                print(colored("Security Risk: Invalid or unrecognized directives in X-Frame-Options may not provide the intended protection against clickjacking.", "red"))
                print("Solution: Use 'DENY' or 'SAMEORIGIN' to prevent clickjacking.")
                return

        # If no misconfigurations found, return Value
        print(colored(header_value, "blue"))
        print(colored("No security risks identified. X-Frame-Options header is properly configured.", "blue"))



    #X-CONTENT-TYPE-OPTIONS
    elif header_name == "X-Content-Type-Options":
        # Check if the header is missing entirely
        if not header_value:
            print(colored("X-Content-Type-Options header is missing.","red"))
            print(colored("Security Risk: Without X-Content-Type-Options, your site may be vulnerable to MIME type sniffing attacks. Attackers can trick the browser into interpreting content as a different MIME type.", "red"))
            print("Solution: Add an X-Content-Type-Options header to prevent MIME type sniffing.")
            return
        else:
            # Check if the header value is 'nosniff'
            if header_value.strip().lower() != "nosniff":
                print(colored(f"The X-Content-Type-Options header value '{header_value}' is not set to 'nosniff', which can lead to MIME type sniffing attacks.", "red"))
                print("Solution: Set the X-Content-Type-Options header value to 'nosniff'.")
                return

        # If no misconfigurations found, return Value
        print(colored(header_value, "blue"))
        print(colored("No security risks identified. X-Frame-Options header is properly configured.", "blue"))



    #X-XSS-PROTECTION
    elif header_name == "X-XSS-Protection":
        # Check if the header is missing entirely
        if not header_value:
            print(colored("X-XSS-Protection header is missing.", "red"))
            print(colored("Security Risk: Without X-XSS-Protection, your site may be vulnerable to cross-site scripting (XSS) attacks. Enabling XSS protection helps prevent these attacks.", "red"))
            print("Solution: Add an X-XSS-Protection header to enable or configure XSS protection.")
            return
        else:
            # Check the header value for specific configurations
            if header_value.lower() == "0":
                print(colored("X-XSS-Protection is disabled.", "yellow"))
                print(colored("Security Risk: X-XSS-Protection is currently disabled, which may leave your site vulnerable to XSS attacks.", "red"))
                print("Solution: Set X-XSS-Protection to '1; mode=block' to enable protection.")
                return
            elif header_value.lower() != "1; mode=block":
                print(colored(f"X-XSS-Protection is set to an unexpected value: '{header_value}'", "yellow"))
                print(colored("Security Risk: X-XSS-Protection is not properly configured, which may leave your site vulnerable to XSS attacks.", "red"))
                print("Solution: Configure X-XSS-Protection with '1; mode=block' for maximum protection.")
                return
        
        # If no misconfigurations found, return Value
        print(colored(header_value, "blue"))
        print(colored("No security risks identified. X-Frame-Options header is properly configured.", "blue"))


   
    #ACCESS-CONTROL-ALLOW-ORIGIN
    elif header_name == "Access-Control-Allow-Origin":
        # Check if the header is missing entirely
        if not header_value:
            print(colored("Access-Control-Allow-Origin header is missing.", "red"))
            print(colored("Security Risk: Without Access-Control-Allow-Origin, cross-origin requests may not be properly restricted, potentially exposing your site to cross-site request forgery (CSRF) and other security vulnerabilities.", "red"))
            print("Solution: Add an Access-Control-Allow-Origin header to specify allowed origins.")
            return
        else:
            # Check if the value is a valid origin or wildcard
            if header_value != "*" :
                print(colored("Access-Control-Allow-Origin allows all domains ('*').", "yellow"))
                print(colored("Security Risk: Allowing all domains may be too permissive and pose security risks. It's recommended to limit the allowed origins to specific trusted domains.", "red"))
                print("Solution: Limit the Access-Control-Allow-Origin header to specific trusted domains.")
                return
          
        # If no misconfigurations found, return Value
        print(colored(header_value, "blue"))
        print(colored("No security risks identified. Access-Control-Allow-Origin header is properly configured.", "blue"))

    
    # PUBLIC-KEY-PINS
    elif header_name == "Public-Key-Pins":
        # Check if the header is missing entirely
        if not header_value:
            print(colored("Public-Key-Pins header is missing.", "red"))
            print(colored("Security Risk: Without Public-Key-Pins, your site may be vulnerable to various attacks, including man-in-the-middle (MITM) attacks. Public-Key-Pins enhance security by associating your site with specific public keys.", "red"))
            print("Solution: Add a Public-Key-Pins header to enhance security.")
            return

        # Split the header value into key-value pairs
        pins = header_value.split(";")

        # Check for required pins
        has_required_pins = False
        for pin in pins:
            if pin.strip().startswith("pin-sha256"):
                has_required_pins = True
                break

        if not has_required_pins:
            print(colored("Public-Key-Pins header is missing required pins.", "yellow"))
            print(colored("Security Risk: The Public-Key-Pins header is missing the required 'pin-sha256' directive, which is crucial for security. Without it, the header is ineffective.", "red"))
            print("Solution: Include at least one 'pin-sha256' directive in the header.")
            return
        
        print(colored(header_value, "blue"))
        print(colored("No security risks identified. Public-Key-Pins header is properly configured.", "blue"))



    # CONTENT-SECURITY-POLICY (CSP)
    elif header_name == "Content-Security-Policy":
        # Check if the CSP header is missing entirely
        if not header_value:
            print(colored("Content Security Policy (CSP) header is missing.", "red"))
            print(colored("Security Risk: Without CSP, the site is vulnerable to various web attacks, including Cross-Site Scripting (XSS) and data injection attacks.", "red"))
            print("Solution: Add a CSP header to enhance security.")
            return
            
        # Split the CSP value into directives
        directives = header_value.split(";")

        # Check for unsafe-inline or unsafe-eval directives
        for directive in directives:
            if 'unsafe-inline' in directive:
                print(colored("Content Security Policy (CSP) contains 'unsafe-inline' directive.", "red"))
                print(colored("Security Risk: 'unsafe-inline' defeats the purpose of CSP and allows inline script execution.", "red"))
                print("Solution: Remove 'unsafe-inline' from the CSP header.")
                return

            if 'unsafe-eval' in directive:
                print(colored("Content Security Policy (CSP) contains 'unsafe-eval' directive.", "red"))
                print(colored("Security Risk: 'unsafe-eval' defeats the purpose of CSP and allows script execution from string literals.", "red"))
                print("Solution: Remove 'unsafe-eval' from the CSP header.")
                return
                
        # Check for script-src directive without script nonce
        script_src_directive = [directive.strip() for directive in directives if directive.startswith("script-src")]
        if script_src_directive:
            if "'nonce'" not in script_src_directive[0]:
                print(colored("Content Security Policy (CSP) contains 'script-src' directive without 'nonce' attribute.", "red"))
                print(colored("Security Risk: Without 'nonce', it may allow execution of unauthorized scripts.", "red"))
                print("Solution: Add a 'nonce' attribute to 'script-src' in the CSP header.")
                return

        # Check for frame-src directive without sandbox
        frame_src_directive = [directive.strip() for directive in directives if directive.startswith("frame-src")]
        if frame_src_directive:
            if "'sandbox'" not in frame_src_directive[0]:
                print(colored("Content Security Policy (CSP) contains 'frame-src' directive without 'sandbox' attribute.", "red"))
                print(colored("Security Risk: Without 'sandbox', it may allow embedding content in frames without restrictions.", "red"))
                print("Solution: Add a 'sandbox' attribute to 'frame-src' in the CSP header.")
                return

        # Check for multiple instances of CSP header
        if csp_value.count("Content-Security-Policy") > 1:
            print(colored("Multiple instances of 'Content-Security-Policy' header found in the response.", "yellow"))
            print(colored("Security Risk: Conflicting policies may lead to unexpected behavior.", "yellow"))
            print("Solution: Remove duplicate CSP headers to ensure consistent policy enforcement.")
            return

        # Check for repeated directives within the same CSP header
        unique_directives = set()
        repeated_directives = set()
        for directive in directives:
            directive = directive.strip()
            if directive not in unique_directives:
                unique_directives.add(directive)
            else:
                repeated_directives.add(directive)

        if repeated_directives:
            print(colored("Repeated CSP directives found within the same CSP header.", "yellow"))
            print(colored("Security Risk: Repeated directives have no additional effect and can lead to policy misconfigurations.", "yellow"))
            print("Solution: Remove duplicated directives to ensure proper CSP configuration.")
            return

        # If no misconfigurations found, return Value
        print(colored(header_value, "blue"))
        print(colored("No security risks identified. CSP header is properly configured.", "blue"))

    #For other headers that doesn't get checked
    else:
        # Header name is not recognized
        print(colored(f"Header '{header_name}' is missing.","red"))
        print("This header is not checked for misconfigurations.")




def check_headers(target, headers_to_display=None):
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
                # Checking the header with check_header func in headers.py
                for header in headers_to_display:
                    header_value = headers.get(header)
                    check_header(header_value, header)
                    
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

    # assigns parsed command line argumants to args
    args = parser.parse_args()
    # assigns target to target veriable
    target = args.target
    
    
    # check if -heaader called
    if args.header:
        if not target:
            target = input("Enter the target URL or IP address: ")
        # go to the fucntion with the header that wanted
        check_headers(target, args.header)
    else:
        if not target:
            target = input("Enter the target URL or IP address: ")
        check_headers(target)
        
#makes sure scripts runs on main program
if __name__ == "__main__":
    main()
