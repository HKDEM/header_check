

def check_header(header_value, header_name, show_solutions=False):
    
    #ACCEPT-PATCH
    if header_name == "Accept-Patch":
        # Check if the header is missing entirely
        if not header_value:
            print("Accept-Patch header is missing.")
            if show_solutions:
                print("Solution: Add an Accept-Patch header with supported media types.")
        else:
            # Split the header value into individual media types
            media_types = header_value.split(",")

            # Check for unsupported or empty media types
            for media_type in media_types:
                if not media_type.strip():
                    print("Accept-Patch header contains empty media types.")
                    if show_solutions:
                        print("Solution: Remove the empty media types from the header.")

                # Give solution if the server doesn't support the media type
                if header_value == "415 Unsupported Media Type" :
                    print("Unsupported Media Type" )
                    if show_solutions:
                        print("Solution: Use a supported media type in the Accept-Patch header.")

        # If no misconfigurations found, return Value
        print(header_value)
    
    #ACCEPT-RANGERS
    elif header_name == "Accept-Ranges":
        # Check if the header is missing entirely
        if not header_value:
            print("Accept-Ranges header is missing.")
            if show_solutions:
                print("Solution: Add an Accept-Ranges header with a valid value (e.g., 'bytes').")

        # Check if the value is not a valid range unit
        elif header_value.strip() != "bytes":
            print(f"Accept-Ranges header has an invalid value: {header_value.strip()}")
            if show_solutions:
                print("Solution: Use 'bytes' as the value for the Accept-Ranges header.")

        # If no misconfigurations found, return Value
        print(header_value)
       
    #AGE
    elif header_name == "Age":
        # Check if the header is missing entirely
        if not header_value:
            print("Age header is missing.")
            if show_solutions:
                print("Solution: Add an Age header with a valid age value (e.g., seconds).")

        # Check if the value is not a valid age
        elif not header_value.strip().isdigit():
            print(f"Age header has an invalid value: {header_value.strip()}")
            if show_solutions:
                print("Solution: Use a valid integer value for the Age header (e.g., seconds).")

        # If no misconfigurations found, return Value
        print(header_value)


    #ALLOW
    elif header_name == "Allow":
        # Check if the header is missing entirely
        if not header_value:
            print("Allow header is missing.")
            if show_solutions:
                print("Solution: Add an Allow header with a list of valid HTTP methods (e.g., 'GET, POST').")
        else:
            # Split the header value into individual HTTP methods
            http_methods = header_value.split(",")

            # Check for empty or invalid HTTP methods
            for http_method in http_methods:
                method = http_method.strip()
                if not method:
                    print("Allow header contains empty HTTP methods.")
                    if show_solutions:
                        print("Solution: Remove the empty HTTP methods from the header.")
                elif header_value == "405 Method Not Allowed":
                    print(f"Allow header specifies an invalid HTTP method: {method}")
                    if show_solutions:
                        print("Solution: Use valid HTTP methods in the Allow header.")

        # If no misconfigurations found, return Value
        print(header_value)

    
