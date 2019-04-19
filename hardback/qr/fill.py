from . qr import DEFAULT, ERRORS, MAX_VERSION


def fill(qr):
    def fill_error():
        for qr.error in reversed(ERRORS):
            if qr.chunk_size <= qr.max_chunk_size:
                return
        raise ValueError('Not enough space for chunk: %d < %d' %
                         (qr.chunk_size, qr.max_chunk_size))

    def fill_version():
        err = qr.error
        qr.error = qr.error or DEFAULT.error

        for qr.version in range(1, MAX_VERSION):
            if qr.chunk_size <= qr.max_chunk_size:
                return True
        qr.error = err

    if not (qr.version or qr.error or qr.block_size):
        qr.version = DEFAULT.version
        qr.error = DEFAULT.error
        qr.block_size = DEFAULT.block_size

    if qr.version and qr.error and qr.block_size:
        qr.check_chunk_size()

    elif not qr.block_size:
        qr.version = qr.version or DEFAULT.version
        qr.error = qr.error or DEFAULT.error
        qr.block_size = qr.max_chunk_size - qr.chunk_size

    elif qr.version:
        fill_error()

    elif not fill_version():
        if qr.error:
            qr.check_chunk_size()
        else:
            qr.version = MAX_VERSION
            fill_error()
