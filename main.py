import pc

if __name__ == '__main__':
    pc = pc.PC()

    pc.start_listening()

    pc.send_messages_to_neighbors("hello")