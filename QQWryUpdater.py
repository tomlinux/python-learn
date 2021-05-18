import struct
import zlib
import requests
import logging
import time
import shutil
import os

logging.getLogger().setLevel(logging.INFO)

class QQWryUpdater(object):
    version_file = "./tmp/qqwry_version.bin"
    tmp_file = "./tmp/qqwry.dat"
    target_file = "./data/qqwry.dat"
    copywrite_url = "http://update.cz88.net/ip/copywrite.rar"
    qqwry_url = "http://update.cz88.net/ip/qqwry.rar"
    headers = {
        "User-Agent": "Mozilla/3.0 (compatible; Indy Library)",
        "Accept": "text/html, */*",
    }

    @classmethod
    def update(cls):
        curr_version, check_time, update_time = (0, 0, 0)
        with open(cls.version_file, "rb+") as handle:
            content = handle.read()
            if len(content) > 0:
                curr_version, check_time, update_time = struct.unpack("<3I", content)

        check_time = int(time.time())
        copywrite = requests.get(cls.copywrite_url, headers = cls.headers).content
        # copywrite[:4] == b"CZIP" # 纯真IP

        version, unknown1, size, unknown2, key = struct.unpack_from("<5I", copywrite, 4)
        if version == curr_version:
            logging.info("no update for version %d", curr_version)
            with open(cls.version_file, "wb+") as handle:
                handle.write(struct.pack("<3I", version, check_time, update_time))
            return
        logging.info("new version %d, size %d", version, size)

        update_time = int(time.time())
        qqwry = requests.get(cls.qqwry_url, headers = cls.headers).content

        head = bytearray(0x200)
        for i in range(0x200):
            key = (key * 0x805 + 1) & 0xFF
            head[i] = qqwry[i] ^ key

        qqwry = head + qqwry[0x200:]
        data = zlib.decompress(qqwry)
        with open(cls.tmp_file, "wb") as handle:
            handle.write(data)

        with open(cls.version_file, "wb+") as handle:
            handle.write(struct.pack("<3I", version, check_time, update_time))

    @classmethod
    def cover(cls):
        if os.path.isfile(cls.tmp_file):
            shutil.move(cls.tmp_file, cls.target_file)

    @classmethod
    def updateAndCover(cls):
        cls.update()
        cls.cover()
        logging.info("[DONE]")

if __name__ == '__main__':
    QQWryUpdater.updateAndCover()