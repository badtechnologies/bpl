# Copywright (c) 2024 Kevin Dalli

import os
import socket
import struct
import time
import select
import argparse

ICMP_ECHO_REQUEST = 8

def checksum(source_string):
    sum = 0
    countTo = (len(source_string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2

    if countTo < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def create_packet(id):

    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = struct.pack('d', time.time())

    my_checksum = checksum(header + data)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1)
    return header + data

def do_one_ping(dest_addr, timeout):

    icmp = socket.getprotobyname("icmp")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except PermissionError as e:
        print("Operation not permitted. Run as administrator.")
        return

    my_id = os.getpid() & 0xFFFF
    packet = create_packet(my_id)

    while packet:
        sent = sock.sendto(packet, (dest_addr, 1))
        packet = packet[sent:]

    delay = receive_one_ping(sock, my_id, time.time(), timeout, dest_addr)
    sock.close()
    return delay

def receive_one_ping(sock, id, time_sent, timeout, dest_addr):

    time_left = timeout
    while True:
        started_select = time.time()
        what_ready = select.select([sock], [], [], time_left)
        how_long_in_select = (time.time() - started_select)
        if what_ready[0] == []:
            return

        time_received = time.time()
        rec_packet, addr = sock.recvfrom(1024)

        icmp_header = rec_packet[20:28]
        type, code, checksum, packet_id, sequence = struct.unpack('bbHHh', icmp_header)

        if packet_id == id:
            bytes_in_double = struct.calcsize('d')
            time_sent = struct.unpack('d', rec_packet[28:28 + bytes_in_double])[0]
            return time_received - time_sent

        time_left = time_left - how_long_in_select
        if time_left <= 0:
            return

def ping(host, timeout=1):

    dest = socket.gethostbyname(host)
    print(f'Pinging {dest} ({host}) with Python:')

    try:
        while True:
            delay = do_one_ping(dest, timeout)
            if delay is None:
                print(f'Ping to {dest} timed out')
            else:
                delay = delay * 1000
                print(f'Ping to {dest} took {delay:.2f} ms')
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nPing stopped.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ping a host.')
    parser.add_argument('host', type=str, help='The host to ping.')
    parser.add_argument('--timeout', '-t', type=int, default=1, help='Timeout in seconds for each ping (default: 1 second).')

    args = parser.parse_args()

    ping(args.host, args.timeout)
