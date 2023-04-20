from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

url = 'URL'

try:
    authenticator = IAMAuthenticator('API_KEY')
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator
    )
    language_translator.set_service_url(url)

    def english_to_french(text):
        if not text:
            return ''
        translation = language_translator.translate(
            text=text,
            source='en',
            target='fr'
        ).get_result()
        return translation['translations'][0]['translation']

    def english_to_german(text):
        if not text:
            return ''
        translation = language_translator.translate(
            text=text,
            source='en',
            target='de'
        ).get_result()
        return translation['translations'][0]['translation']

finally:
    language_translator.set_disable_ssl_verification(False)
