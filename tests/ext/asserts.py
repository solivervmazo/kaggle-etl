from unittest import TestCase


class _Helpers:
    def convert_to_dict(obj):
        return (
            obj.to_dict()
            if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict"))
            else obj
        )


class AssertCommons:
    def in_results(self: TestCase, result: dict, ext_msg: str = None):
        ext_msg = f"({ext_msg}):" if ext_msg else ""
        # Assert that result is a dictionary
        self.assertIsInstance(result, dict, "Result is not a dictionary")

        # Assert that the result dictionary has the required keys
        self.assertIn("data", result, f"{ext_msg}Key 'data' not found in result")
        self.assertIn("status", result, f"{ext_msg}Key 'status' not found in result")

        # Assert that the 'status' value is 200
        self.assertEqual(
            result["status"],
            200,
            f"{ext_msg}Expected status 200, but got {result['status']}",
        )

    def should_keys_exists_in_data(
        self, data: dict, keys=list[str], ext_msg: str = None
    ):
        ext_msg = f"({ext_msg}):" if ext_msg else ""
        for k in keys:
            self.assertIn(k, data, f"{ext_msg} Key '{k}' not found in data")

    def should_length_and_values_matched(
        self: TestCase,
        result: list,
        expected: list,
        use_key: str = "id",
        ignore_keys: list = [],
        ext_msg: str = None,
    ):
        ext_msg = f"({ext_msg}):" if ext_msg else ""
        # Assert equal length
        self.assertEqual(
            len(result),
            len(expected),
            f"{ext_msg}Expecting {len(expected)} rows received {len(result)}",
        )

        # Assert values
        for i, e in enumerate(expected):
            exp = _Helpers.convert_to_dict(e)
            res = next(
                filter(
                    lambda x: x.get(use_key) == exp.get(use_key),
                    list(_Helpers.convert_to_dict(r) for r in result),
                )
            )
            self.assertGreater(
                len(res),
                0,
                f"{ext_msg} Expecting {exp.get(use_key)} in result got none",
            )
            for k in exp:
                if k not in ignore_keys:
                    r = res[k]
                    self.assertEqual(
                        r,
                        exp[k],
                        f"{ext_msg} Expecting {exp[k]} recieved {r} at row {i} column {k}",
                    )

    def in_db_update(
        self: TestCase,
        result: dict,
        expected: dict,
        ignore_keys: list = [],
        ext_msg: str = None,
    ):
        ext_msg = f"({ext_msg}):" if ext_msg else ""
        expected = _Helpers.convert_to_dict(expected)
        result = _Helpers.convert_to_dict(result)
        for k in expected:
            if k not in ignore_keys:
                self.assertEqual(
                    expected.get(k),
                    result.get(k),
                    f"{ext_msg} Expecting {expected.get(k)} recieved {result.get(k)} at key {k}",
                )

    def in_data_delete(self: TestCase, result: dict, ext_msg: str = None):
        pass

    def in_data_all(self: TestCase, result: dict, ext_msg: str = None):
        ext_msg = f"({ext_msg}):" if ext_msg else ""
        # with result.data
        # Assert of same length
        # Assert of expecting identifier
