#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""history-collector utilities"""

from enum import Enum, unique


@unique
class OperationType(Enum):
    # https://www.stellar.org/developers/horizon/reference/resources/operation.html
    CREATE_ACCOUNT = 0
    PAYMENT = 1
    PATH_PAYMENT = 2
    MANAGE_OFFER = 3
    CREATE_PASSIVE_OFFER = 4
    SET_OPTIONS = 5
    CHANGE_TRUST = 6
    ALLOW_TRUST = 7
    ACCOUNT_MERGE = 8
    INFLATION = 9
    MANAGE_DATA = 10
    BUMP_SEQUENCE = 11

    def __str__(self):
        """By default, enum prefixes members with the class name, i.e. OperationType.PAYMENT. Remove the prefix."""
        return self.name


def verify_file_sequence(sequence):
    """Verifies the ledger file sequence."""
    return (int(sequence, 16) + 1) % 64 == 0


def get_new_file_sequence(old_file_name):
    """
    Return the name of the next file to scan.

    Transaction files are stored with an ascending hexadecimal name, for example:
    └── transactions
    └── 00
        └── 72
            ├── 6a
            │   ├── transactions-00726a3f.xdr.gz
            │   ├── transactions-00726a7f.xdr.gz
            │   ├── transactions-00726abf.xdr.gz
            │   └── transactions-00726aff.xdr.gz

    So get the sequence of the last file scanned > convert to decimal > add 64 > convert back to hex >
    remove the '0x' prefix > and add '0' until the file name is 8 letters long
    """
    new_file_name = int(old_file_name, 16)
    new_file_name = new_file_name + 64
    new_file_name = hex(new_file_name)
    new_file_name = new_file_name.replace('0x', '')
    new_file_name = '0' * (8 - len(new_file_name)) + new_file_name

    return new_file_name


def get_s3_bucket_subdir(file_name):
    """ Return S3 subdirectory of the given arhive file."""
    # File transactions-004c93bf.xdr.gz will be in:
    # BUCKET_NAME/CORE_DIRECTORY/transactions/00/4c/93/
    # "ledger-004c93bf" -> "00/4c/93/"
    [file_prefix, file_number] = file_name.split('-')
    subdir = '/'.join(file_number[i:i+2] for i in range(0, len(file_number), 2))
    subdir = file_prefix + '/' + subdir[:9]
    return subdir