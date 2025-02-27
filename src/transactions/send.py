#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import time

from wallet.wallet import Ecdsa, PrivateKey

from accounts.get_sequance_number import GetSequanceNumber

from blockchain.block.get_block import GetBlock


def send(my_public_key, my_private_key, to_user, password, data=None, amount=None):
    """
    The main function for sending the transaction.

    Inputs:
      * my_public_key: Sender's public key.
      * my_private_key: Sender's private key.
      * to_user: Receiver's address.
      * data: A text that can be written into the transaction. (Can be None)
      * amount: A int or float amount to be sent. (Can be None)
    """

    my_public_key = "".join(
        [
            l.strip()
            for l in my_public_key.splitlines()
            if l and not l.startswith("-----")
        ]
    )

    system = GetBlock()
    sequance_number = GetSequanceNumber(my_public_key, system) + 1

    # Get the current fee
    transaction_fee = system.transaction_fee

    tx_time = int(time.time())

    system.createTrans(
        sequance_number=sequance_number,
        signature=Ecdsa.sign(
            str(sequance_number)
            + str(my_public_key)
            + str(to_user)
            + str(data)
            + str(amount)
            + str(transaction_fee)
            + str(tx_time),
            PrivateKey.fromPem(my_private_key),
        ).toBase64(),
        fromUser=str(my_public_key),
        toUser=str(to_user),
        data=data,
        amount=amount,
        transaction_fee=transaction_fee,
        transaction_sender=None,
        transaction_time=tx_time,
    )
