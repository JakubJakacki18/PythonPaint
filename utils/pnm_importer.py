import os
import re
import sys
import time
from collections.abc import Generator
from enum import Enum
from functools import wraps
from typing import List, Tuple, Union

import numpy as np

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"⏱️ Funkcja {func.__name__} wykonana w {end - start:.4f} s")
        return result
    return wrapper

class PnmFormat(Enum):
    PBM_TEXT = "P1"
    PGM_TEXT = "P2"
    PPM_TEXT = "P3"
    PBM_BINARY = "P4"
    PGM_BINARY = "P5"
    PPM_BINARY = "P6"

class PnmImporter:
    @staticmethod
    @measure_time
    def export_file(filename : str, algorithm : PnmFormat, arr, max_value : int):
        with open(filename, "wb") as f:
            f.write(algorithm.value.encode("utf-8"))


        pass
    @staticmethod
    @measure_time
    def get_pixels_and_max_value_from_file(filename) -> Tuple[Union[List[List[int]], List[List[List[int]]]],int]:
        print(f"Trwa praca nad plikiem {filename}")
        with open(filename, 'rb') as f:
            matched_header, width,height,max_value = PnmImporter._extract_header(f)
            print(f'width={width} height={height}')
            print(f'matched_header={matched_header.value} max_value={max_value}')
            # if matched_header in (PnmFormat.PPM_TEXT, PnmFormat.PGM_TEXT,PnmFormat.PPM_BINARY, PnmFormat.PGM_BINARY):
                # try:
                #
                #     max_value = PnmImporter._get_first_value(f, line)
                # except ValueError:
                #     max_value=255
            match matched_header:
                case PnmFormat.PPM_TEXT | PnmFormat.PGM_TEXT:
                    # pixels = list(PnmImporter._from_rgb_elements_to_3d_list(PnmImporter._iter_rgb(PnmImporter._pnm_text_generator(f)),width))
                    pixels = bytes(PnmImporter._pnm_text_generator(f))
                case PnmFormat.PBM_BINARY:
                    pixels = list(PnmImporter._from_rgb_elements_to_3d_list(PnmImporter._pnm_text_generator(f),width))

                    # for line in f:
                    #     tokens = line.strip().split()
                    #     for token in tokens:
                    #         if token.startswith(b'#'):
                    #             break
                    #         pixels.append(int(token))

                    # def read_pnm_tokens():
                    #     buffer_size = 1024
                    #     while True:
                    #         lines = [f.readline() for _ in range(buffer_size)]
                    #         if not any(lines):
                    #             break
                    #         for line in lines:
                    #             if not line:
                    #                 continue
                    #             tokens = line.strip().split()
                    #             for token in tokens:
                    #                 if token.startswith(b'#'):
                    #                     break
                    #                 yield int(token)
                    #
                    # pixels = list(read_pnm_tokens())

                    # pixels = np.fromiter(read_pnm_tokens(f), dtype=np.uint8)

                case PnmFormat.PBM_BINARY:
                    pixel_data = f.read(width * height)
                    arr = np.frombuffer(pixel_data, dtype=np.uint8)
                    pixels = arr.reshape((height, width))


                # case PnmFormat.PGM_BINARY:
                #     chunk_size_bytes = 4096
                #     while chunk := f.read(chunk_size_bytes):
                #         tokens = chunk.strip().split()
                #         for token in tokens:
                #             if token.startswith(b'#'):
                #                 break
                #             pixels.append(int(token))

                case PnmFormat.PPM_BINARY | PnmFormat.PGM_BINARY:
                    pixel_data = f.read(width * height * 3)
                    arr = np.frombuffer(pixel_data, dtype=np.uint8)
                    pixels = arr.reshape((height, width, 3))
                    # chunk_size_bytes = 4096 * 3
                    # async def read_binary_data(f,chunk_size_bytes):
                    #     if chunk := f.read(chunk_size_bytes):


                    # while chunk := f.read(chunk_size_bytes):
                    #     tokens = chunk.strip().split()
                    #     for token in tokens:
                    #         if token.startswith(b'#'):
                    #             break
                    #         pixels.append(int(token))



                        # for i in range(0, len(chunk), 3):
                        #     r, g, b = chunk[i:i + 3]
                        #     pixels.extend([r, g, b])
                case _:
                    pass

            print("Pierwsze pixel", pixels[:2][:2])
            # print("Ilości pikseli, iloczyny", sum(len(row) for row in pixels), width * height, width * height * 3)
            # assert sum(len(row) for row in pixels) in (width * height,width*height*3), "Len of pixels does not match width and height"
            print("✅ Zwracam dane z get_pixels_and_max_value_from_file")
            return pixels, width,height, max_value


    # @staticmethod
    # def _extract_header(f, line,with_max_value)-> (int,int):
    #     width_and_height=[]
    #     max_len = 3 if with_max_value else 2
    #
    #     while len(width_and_height)!=max_len:
    #         print(f"line {line}")
    #         tokens = line.strip().split()
    #         print(f"tokens {tokens}")
    #         for token in tokens:
    #             if token.startswith(b'#'):
    #                 break
    #             width_and_height.append(int(token))
    #             match max_len:
    #                 case 2:
    #                     if len(width_and_height) == max_len:
    #                         return width_and_height[0], width_and_height[1], None
    #                 case 3:
    #                     if len(width_and_height) == max_len:
    #                         return width_and_height[0], width_and_height[1], width_and_height[2]
    #         line = f.readline()
    #     return None
    @staticmethod
    def _from_rgb_elements_to_3d_list(generator : Generator,width:int):
        it = iter(generator)
        while True:
            try:
                yield [next(it) for _ in range(width)]
            except StopIteration:
                break


    @staticmethod
    def _iter_rgb(generator : Generator):
        it = iter(generator)
        while True:
            try:
                yield [next(it), next(it), next(it)]
            except StopIteration:
                break

    @staticmethod
    def _find_nth(text: bytes, number: bytes, n: int) -> int:
        pattern = rb'(?<!\d)' + re.escape(number) + rb'(?!\d)'
        matches = re.finditer(pattern, text)
        for i, match in enumerate(matches, start=1):
            if i == n:
                return match.end()
        return -1

    @staticmethod
    def _pnm_text_generator(f):
        WHITESPACE = b" \t\r\n"

        chunk_size = 1 << 20
        buf = b""

        in_comment = False
        while chunk := f.read(chunk_size):
            start = None
            data = buf + chunk
            for i in range(0, len(data)):
                data_char = data[i]
                if in_comment:
                    if data_char in (10, 13):  # koniec linii
                        in_comment = False
                    continue
                if data_char == 35:  # '#'
                    in_comment = True
                    continue
                if data_char in WHITESPACE:
                    if start is not None:
                        yield int(data[start:i].decode("ascii"))
                        start = None
                    continue
                if start is None:
                    start = i
            if start is not None:
                buf = data[start:len(data)]
            else:
                buf = b""
        if buf:
            yield int(buf.decode("ascii", errors="strict"))

    @staticmethod
    def _extract_header(f) -> tuple[PnmFormat,int, int, int] | None:
        matched_header = None
        pos = f.tell()
        index_after_header = 0
        last_pos = pos
        while matched_header is None and (line := f.readline()):
            stripped = line.strip()
            matched_header = next(
                (pnm_format for pnm_format in PnmFormat if stripped.startswith(pnm_format.value.encode())),
                None
            )
            if matched_header is not None:
                index_after_header = line.find(matched_header.value.encode())+2
                pos = last_pos + index_after_header

            last_pos = f.tell()


        if matched_header is None:
            raise Exception(f'Could not find header of format')
        line = line[index_after_header:] if not len(line.strip().split()) in (0, 1) else f.readline()
        header_data = []
        with_max_value = matched_header in (
            PnmFormat.PGM_TEXT,
            PnmFormat.PPM_TEXT,
            PnmFormat.PGM_BINARY,
            PnmFormat.PPM_BINARY,
        )
        needed = 3 if with_max_value else 2
        while len(header_data) < needed:
            tokens = line.strip().split()
            token_occurrence = {key : 0 for key in tokens}
            for token in tokens:
                token_occurrence[token] += 1
                if token.startswith(b"#"):
                    break
                header_data.append(int(token))

                index_after_last_value = PnmImporter._find_nth(line, token, token_occurrence[token])
                if len(header_data) == needed:
                    pos = last_pos + index_after_last_value
                    f.seek(pos)
                    return (
                        matched_header,
                        header_data[0],
                        header_data[1],
                        header_data[2] if with_max_value else 1,
                    )

            last_pos = f.tell()
            line = f.readline()


        return None
    # @staticmethod
    # def _get_first_value(f, line)-> int:
    #     x = None
    #     while x is None:
    #         tokens = line[0].strip().split()
    #         print(f"tokens {tokens}")
    #         for token in tokens:
    #             if token.startswith(b'#'):
    #                 break
    #             return int(token)
    #         line[0] = f.readline()


if __name__ == '__main__':
    pnm_importer = PnmImporter()
    os.chdir("tests")
    list_of_files = os.listdir(".")
    for name_of_file in list_of_files:
        pnm_importer.get_pixels_and_max_value_from_file(name_of_file)