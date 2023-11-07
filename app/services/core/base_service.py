class BaseService:
    def __init__(self, token: str = None) -> None:
        self._token = token
        self._logging = True

    def _models_to_dict(self, models=None, model=None, rel: dict = None):
        """
        Convert a list of SQLAlchemy models or a single model to a list of dictionaries.

        Args:
            models (list, optional): List of SQLAlchemy models.
            model (SQLAlchemy model, optional): A single SQLAlchemy model.
            rel (dict, optional): converts relations to dict
            >>> rel = {'attr_with_relation': True}
        Returns:
            list or dict or False: List of dictionaries representing the models, 
            a dictionary representing a single model, or False if no models provided.
        """
        if models is not None:
            return [m.to_dict(rel=rel) for m in models]
        if model is not None:
            return model.to_dict(rel=rel)
        return False

    def _response(self, status: str, data=None, error: str = None):
        """
        Create a response dictionary with status, data, and error.

        Args:
            status (str): Response status.
            data (any, optional): Data to include in the response.
            error (str, optional): Error message to include in the response.

        Returns:
            dict: Response dictionary.
        """
        _response = {"status": status}
        if data is not None:
            _response["data"] = data
        if error is not None:
            _response["error"] = error
        return _response
