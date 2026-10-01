import bcrypt

'''
1) Normal Hashing -> SHA256
2) Password Hashing -> bcrypt
'''

reg_pass = 'password@123'
encoded = reg_pass.encode('utf-8')
salt = bcrypt.gensalt(rounds=12)
hashed_pass = bcrypt.hashpw(encoded,salt).decode('utf-8')
# $2b$12$.tNhdbDS71xXC0Jw1GY6.eKYG3brRQLEOhgjlHQo3kxL3KYuwFmwW
login_pass = input('Enter your password:')
encoded1 = login_pass.encode('utf-8')
if bcrypt.checkpw(encoded1,hashed_pass.encode('utf-8')):
    print('Login Success!')
else:
    print('Login Failed!')
