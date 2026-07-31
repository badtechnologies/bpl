from bdsh import get_shell_path
from paramiko import RSAKey

key = RSAKey.generate(bits=2048)
key.write_private_key_file(get_shell_path('cfg', 'badbandssh_rsa_key'))
