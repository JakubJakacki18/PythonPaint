import sys
from enum import Enum

import numpy as np


class PnmFormat(Enum):
    PBM_TEXT = "P1"
    PGM_TEXT = "P2"
    PPM_TEXT = "P3"
    PBM_BINARY = "P4"
    PGM_BINARY = "P5"
    PPM_BINARY = "P6"

class PnmImporter:
    @staticmethod
    def import_pbm_text(filename):
        with open(filename, 'rb') as f:
            matched_header = None
            while matched_header is None and (line := f.readline()):
                matched_header = next(
                    (pnm_format for pnm_format in PnmFormat if line.startswith(pnm_format.value.encode())),
                    None
                )
            if matched_header is None:
                raise Exception(f'Could not find header of format')
            line = line[2:] if not len(line.strip().split()) in (0,1) else f.readline()
            width,height,max_value = PnmImporter._extract_header(f,line, matched_header in (PnmFormat.PPM_TEXT, PnmFormat.PGM_TEXT,PnmFormat.PPM_BINARY, PnmFormat.PGM_BINARY))
            print(f'width={width} height={height}')
            # if matched_header in (PnmFormat.PPM_TEXT, PnmFormat.PGM_TEXT,PnmFormat.PPM_BINARY, PnmFormat.PGM_BINARY):
                # try:
                #
                #     max_value = PnmImporter._get_first_value(f, line)
                # except ValueError:
                #     max_value=255



            pixels = []
            match matched_header:
                case PnmFormat.PPM_TEXT | PnmFormat.PGM_TEXT | PnmFormat.PBM_TEXT:
                    for line in f:
                        tokens = line.strip().split()
                        for token in tokens:
                            if token.startswith(b'#'):
                                break
                            pixels.append(int(token))
                case PnmFormat.PBM_BINARY:
                    chunk_size_bytes = 4096
                    while chunk := f.read(chunk_size_bytes):
                        tokens = chunk.strip().split()
                        for token in tokens:
                            if token.startswith(b'#'):
                                break
                            pixels.append(int(token))


                case PnmFormat.PGM_BINARY:
                    chunk_size_bytes = 4096
                    while chunk := f.read(chunk_size_bytes):
                        tokens = chunk.strip().split()
                        for token in tokens:
                            if token.startswith(b'#'):
                                break
                            pixels.append(int(token))

                case PnmFormat.PPM_BINARY:
                    chunk_size_bytes = 655363*3
                    counter = 0
                    while chunk := f.read(chunk_size_bytes):
                        counter += 1
                        arr = np.frombuffer(chunk, dtype=np.uint8)
                        pixels.extend(arr)
                        # tokens = chunk.strip().split()
                        # for token in tokens:
                        #     if token.startswith(b'#'):
                        #         break
                        #     pixels.append(int(token))



                        # for i in range(0, len(chunk), 3):
                        #     r, g, b = chunk[i:i + 3]
                        #     pixels.extend([r, g, b])
                case _:
                    pass

            # assert len(pixels) in (width * height,width*height*3), "Len of pixels does not match width and height"

            print(pixels)
            print(len(pixels),width * height,width*height*3)

    @staticmethod
    def _extract_header(f, line,with_max_value)-> (int,int):
        width_and_height=[]
        max_len = 3 if with_max_value else 2

        while len(width_and_height)!=2:
            print(f"line {line}")
            tokens = line.strip().split()
            print(f"tokens {tokens}")
            for token in tokens:
                if token.startswith(b'#'):
                    break
                width_and_height.append(int(token))
                if len(width_and_height) == 2:
                    return width_and_height[0], width_and_height[1], None
                elif len(width_and_height) == 3:
                    return width_and_height[0], width_and_height[1], width_and_height[2]
            line = f.readline()

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
    pnm_importer.import_pbm_text("test-08.ppm")