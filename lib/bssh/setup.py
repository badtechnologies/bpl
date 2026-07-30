from bdsh.shell import Shell
from paramiko import RSAKey

key = RSAKey.generate(bits=2048)
key.write_private_key_file(Shell.get_path('cfg', 'badbandssh_rsa_key'))
