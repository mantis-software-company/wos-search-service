from slugify import slugify
from wos import WosClient


def author_name_to_query(author_name):
    """
    Converts an author name combinations to a wos query string.
    :param author_name: E.g. "Yaşar Ahmet Tonta", "Tonta, Yaşar Ahmet"
    """

    if "," in author_name:
        pass
    else:
        author_parts = author_name.split(" ")
        author_parts = [x.strip() for x in author_parts]
        author_name_patterns = []
        if len(author_parts) == 1:
            author_name_patterns.append(author_parts[0])  # TONTA
        elif len(author_parts) == 2:
            author_name_patterns.append(f"{author_parts[1]}, {author_parts[0]}")  # TONTA, YASAR
            author_name_patterns.append(f"{author_parts[1]}, {author_parts[0][0]}")  # TONTA, Y
        elif len(author_parts) == 3:
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[0]}")  # TONTA, YASAR
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[0][0]}")  # TONTA, Y
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[1]}")  # TONTA, AHMET
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[1][0]}")  # TONTA, A
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[0]} {author_parts[1]}")  # TONTA, YASAR AHMET
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[1]} {author_parts[0]}")  # TONTA, AHMET YASAR
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[0][0]}{author_parts[1][0]}")  # TONTA, YA
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[1][0]}{author_parts[0][0]}")  # TONTA, AY
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[0][0]} {author_parts[1]}")  # TONTA, Y AHMET
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[1][0]} {author_parts[0]}")  # TONTA, A YASAR
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[0]} {author_parts[1][0]}")  # TONTA, YASAR A
            author_name_patterns.append(f"{author_parts[2]}, {author_parts[1]} {author_parts[0][0]}")  # TONTA, AHMET Y
        elif len(author_parts) == 4:
            author_name_patterns.append(f"{author_parts[3]}, {author_parts[0]}")  # GEZGIN, FATMA
            author_name_patterns.append(f"{author_parts[3]}, {author_parts[0][0]}")  # GEZGIN, F
            author_name_patterns.append(f"{author_parts[3]}, {author_parts[1]}")  # GEZGIN, MUNEVVER
            author_name_patterns.append(f"{author_parts[3]}, {author_parts[1][0]}")  # GEZGIN, M
            author_name_patterns.append(
                f"{author_parts[3]}, {author_parts[0]} {author_parts[1]}")  # GEZGIN, FATMA MUNEVVER
            author_name_patterns.append(
                f"{author_parts[3]}, {author_parts[1]} {author_parts[0]}")  # GEZGIN, MUNEVVER FATMA
            author_name_patterns.append(f"{author_parts[3]}, {author_parts[0][0]}{author_parts[1][0]}")  # GEZGIN, FM
            author_name_patterns.append(f"{author_parts[3]}, {author_parts[1][0]}{author_parts[0][0]}")  # GEZGIN, MF
            author_name_patterns.append(
                f"{author_parts[3]}, {author_parts[0]} {author_parts[1]} {author_parts[2]}")  # GEZGIN, FATMA MUNEVVER AKYOL
            author_name_patterns.append(
                f"{author_parts[3]}, {author_parts[1]} {author_parts[0]} {author_parts[2]}")  # GEZGIN, MUNEVVER FATMA AKYOL
            author_name_patterns.append(
                f"{author_parts[3]}, {author_parts[0][0]}{author_parts[1][0]}{author_parts[2][0]}")  # GEZGIN, FMA
        else:
            raise Exception("Author name is too long.")

        format_as_query = lambda x: f"AU={slugify(x, separator=' ').upper()}"
        author_name_patterns = [f"({format_as_query(x)})" for x in author_name_patterns]

        return " OR ".join(author_name_patterns)


class CustomWosClient(WosClient):
    """ Our custom WosClient """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Don't close the connection on exit
        pass

    def __del__(self):
        # Don't close the connection on class deletion
        pass
