import connexion
from connexion.resolver import RestyResolver
from connexion.decorators.response import ResponseValidator
from connexion.exceptions import NonConformingResponseBody, NonConformingResponseHeaders
import db.base as db


# By default validate_response will return the full stack trace to the client.
# This will instead return a simple 500
class CustomResponseValidator(ResponseValidator):
    def validate_response(self, data, status_code, headers, url):
        try:
            super().validate_response(data, status_code, headers, url)
        except(NonConformingResponseBody, NonConformingResponseHeaders):
            raise Exception()


db.init()
validator_map = {
    'response': CustomResponseValidator
}
app = connexion.App('tag', specification_dir='swagger/',
                    validator_map=validator_map)
app.add_api('api.spec.yaml', resolver=RestyResolver(
    'api'), validate_responses=True)
app.run(port=8080)
