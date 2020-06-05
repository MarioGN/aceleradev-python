import pytest

from main import create_token, verify_signature


class TestChallenge4:
    token = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYW5ndWFnZSI6IlB5dGhvbiJ9.sM_VQuKZe_VTlqfS3FlAm8XLFhgvQQLk2kkRTpiXq7M'

    def test_create_token(self):
        assert create_token({"language": "Python"}, "acelera") == self.token

    def test_create_token_should_raise_type_error(self):
        '''Testcase para data seja inválida.'''
        with pytest.raises(TypeError):
            create_token(None, "acelera")

    def test_verify_signature(self):
        result = verify_signature(self.token)
        assert result == {"language": "Python"}

    def test_verify_signature_should_return_error_message_to_invalid_key(self):
        '''Testcase para chave secreta inválida.'''
        invalid_token = b'abc0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYW5ndWFnZSI6IlB5dGhvbiJ9.sM_VQuKZe_VTlqfS3FlAm8XLFhgvQQLk2kkRTpiXq7M'
        result = verify_signature(invalid_token)
        assert result == {"error": 2}

    def test_verify_signature_should_return_error_message_to_invalid_token(self):
        '''Testcase para token inválido.'''
        invalid_token = b'abc0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYW5ndWFnZSI6IlB5dGhvbiJ9.'
        result = verify_signature(invalid_token)
        assert result == {"error": 2}
