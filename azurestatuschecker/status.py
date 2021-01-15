MINECRAFT_SERVER_PORT = 25565

def is_mc_server_online(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((address, MINECRAFT_SERVER_PORT))
    if result == 0:
        return True
    else:
        return False