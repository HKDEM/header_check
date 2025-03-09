def check_header(header_value, header_name, show_solutions=False):
    
    #ACCEPT-PATCH
    if header_name == "Accept-Patch":
        # Check if the header is missing entirely
        if not header_value:
            print("Accept-Patch header is missing.")
            print("Solution: Add an Accept-Patch header with supported media types.")
            return
        else:
            # Split the header value into individual media types
            media_types = header_value.split(",")

            # Check for unsupported or empty media types
            for media_type in media_types:
                if not media_type.strip():
                    print("Accept-Patch header contains empty media types.")
                    print("Solution: Remove the empty media types from the header.")
                    return
