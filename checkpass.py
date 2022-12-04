import requests
import hashlib
import sys

def request_api(check_query):
    url = 'https://api.pwnedpasswords.com/range/' + check_query
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError('Featching error :  {}'.format(response.status_code))
    return response

def read_response(response):
    print(response.text)
    
def password_leake_count(hashes,hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0
        
def password_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail = sha1_password[:5],sha1_password[5:]
    response = request_api(first5_char)
    return password_leake_count(response,tail)

def main(args):
    for password in args:
        count = password_api_check(password)
        if count:
            print('{} was found {} times.......'.format(password,count))
        else:
            print('{} was not found'.format(password))
    return 'done'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))