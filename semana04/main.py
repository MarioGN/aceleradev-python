import jwt
from jwt.api_jws import InvalidSignatureError, DecodeError


def create_token(data, secret='acelera', algorithm='HS256'):
    '''
    Esta função transforma os dados recebidos em um jwt token
    aplicando um determinado algoritmo informado.

    Attributes:
        data(dict): Representa os dados que serão criptografados.
        secret(str): Representa a chave secreta utilizada.
        algorithm(str): Representa o algoritmo aplicado para
        criptografar os dados.
    '''
    encoded_token = jwt.encode(data, secret, algorithm)
    return encoded_token


def verify_signature(token, secret='acelera', algorithm='HS256'):
    '''
    Esta função decodifica o jwt token aplicando a chave e o algoritmo
    utilizado no processo de codificação dos dados.

    Attributes:
        data(bytes): Representa os dados que serão descriptografados.
        secret(str): Representa a chave secreta utilizada.
        algorithm(str): Representa o algoritmo aplicado para
        criptografar os dados.
    '''
    try:
        decoded_token = jwt.decode(token, secret, algorithm)
    except (InvalidSignatureError, DecodeError):
        decoded_token = {"error": 2}

    return decoded_token
