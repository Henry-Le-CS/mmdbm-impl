import json
import unittest

from src.svc.qb.builder import QueryBuilder
class TestBuildTaskManagementSQL(unittest.TestCase):
    def setUp(self):
        self.builder = QueryBuilder()

    def test_basic_functionality(self):
        sql, params = self.builder.build_task_management_sql("123", "pending")
        expected_sql = "INSERT INTO tasks VALUES (:job_id, :status) ON CONFLICT (job_id) DO UPDATE SET status = :status;"
        expected_params = {"job_id": "123", "status": "pending"}
        self.assertEqual(sql, expected_sql)
        self.assertDictEqual(params, expected_params)

    def test_with_args(self):
        sql, params = self.builder.build_task_management_sql("123", "pending", args={"key": "value"})
        expected_sql = "INSERT INTO tasks VALUES (:job_id, :status, :args) ON CONFLICT (job_id) DO UPDATE SET status = :status, args = :args;"
        expected_params = {
            "job_id": "123",
            "status": "pending",
            "args": json.dumps({"key": "value"})
        }
        self.assertEqual(sql, expected_sql)
        self.assertDictEqual(params, expected_params)

    def test_with_result(self):
        sql, params = self.builder.build_task_management_sql("123", "completed", result={"outcome": "success"})
        expected_sql = "INSERT INTO tasks VALUES (:job_id, :status, :result) ON CONFLICT (job_id) DO UPDATE SET status = :status, result = :result;"
        expected_params = {
            "job_id": "123",
            "status": "completed",
            "result": json.dumps({"outcome": "success"})
        }
        self.assertEqual(sql, expected_sql)
        self.assertDictEqual(params, expected_params)

    def test_with_args_and_result(self):
        sql, params = self.builder.build_task_management_sql(
            "123",
            "in_progress",
            args={"key": "value"},
            result={"outcome": "pending"}
        )
        expected_sql = "INSERT INTO tasks VALUES (:job_id, :status, :args, :result) ON CONFLICT (job_id) DO UPDATE SET status = :status, args = :args, result = :result;"
        expected_params = {
            "job_id": "123",
            "status": "in_progress",
            "args": json.dumps({"key": "value"}),
            "result": json.dumps({"outcome": "pending"})
        }
        self.assertEqual(sql, expected_sql)
        self.assertDictEqual(params, expected_params)

    def test_edge_cases(self):
        with self.assertRaises(ValueError):  # Assuming function raises errors for invalid inputs
            self.builder.build_task_management_sql("", "pending")
        with self.assertRaises(ValueError):
            self.builder.build_task_management_sql(None, "pending")