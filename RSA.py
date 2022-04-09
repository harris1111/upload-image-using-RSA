def encrypt(message,n,e, block_size=2):
    encrypted_blocks = []
    ciphertext = -1

    if (len(message) > 0):
        ciphertext = ord(message[0])

    for i in range(1, len(message)):
        if (i % block_size == 0):
            encrypted_blocks.append(ciphertext)
            ciphertext = 0

        # multiply by 1000 to shift the digits over to the left by 3 places
        # because ASCII codes are a max of 3 digits in decimal
        ciphertext = ciphertext * 1000 + ord(message[i])

    # add the last block to the list
    encrypted_blocks.append(ciphertext)

    # encrypt all of the numbers by taking it to the power of e
    # and modding it by n
    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str((encrypted_blocks[i]**e) % n)

    encrypted_message = "".join(encrypted_blocks)

    return str(encrypted_message)
