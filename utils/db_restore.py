import os
import boto3
import psycopg2
import time
import subprocess


class DbRestore:
    def __init__(self):
        self.conn = None
        self.s3_bucket = os.getenv("S3_BUCKET_NAME")  # Name of the S3 bucket
        self.s3_backup_key = os.getenv("S3_BACKUP_KEY")  # Object key (file path in S3)
        self.local_backup_path = (
            "./tmp/db_backup.dump"  # Local path to store downloaded backup
        )

    def connect(self):
        self.conn = self.create_connection()
        self.conn.autocommit = True

    def create_connection(self, super: bool = False):
        return psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            user=os.getenv("PG_SUPERUSER") if super else os.getenv("PG_USER"),
            password=os.getenv("PG_SUPERPASS") if super else os.getenv("PG_PASS"),
            dbname="postgres" if super else os.getenv("PG_DBNAME"),
        )

    def recreate_db(self):
        db_name = os.getenv("PG_DBNAME")
        with self.conn.cursor() as cur:
            cur.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
            cur.execute(f'CREATE DATABASE "{db_name}"')

    def disconnect(self):
        """Close the database connection."""
        if self.conn:
            try:
                self.conn.close()
            except Exception as e:
                print(f"NO connection found to disconnect from! - {e}")

    def download_backup_from_s3(self):
        """Download the database backup from S3 to a local temporary file."""

        try:
            session = boto3.Session(profile_name="bs-select-rw-user-730319765130")
            s3 = session.client("s3")
            s3.download_file(self.s3_bucket, self.s3_backup_key, self.local_backup_path)
        except Exception as e:
            raise

    def restore_backup(self):
        """Restore the database from the downloaded backup."""
        os.environ["PGPASSWORD"] = os.getenv("PG_PASS")
        subprocess.run(
            [
                "pg_restore",
                "--clean",
                "-h",
                os.getenv("PG_HOST"),
                "-p",
                os.getenv("PG_PORT"),
                "-U",
                os.getenv("PG_USER"),
                "-d",
                os.getenv("PG_DBNAME"),
                "-j",
                os.getenv("J_VALUE"),
                self.local_backup_path,
            ],
            check=False,
        )

    def kill_all_db_sessions(self):
        """Terminate all active sessions for the target database."""
        dbname = os.getenv("PG_DBNAME")

        try:
            self.conn = self.create_connection(super=True)
            with self.conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE datname = '{dbname}' AND pid <> pg_backend_pid();"""
                )
                self.conn.commit()
            print("Deleted all connections")
        except Exception as e:
            print(e)
            print(
                "Could not connect to DB. Check if other connections are present or if DB exists."
            )
        finally:
            self.disconnect()

    def full_db_restore(self):
        # self.connect()
        # self.recreate_db()
        # self.disconnect()
        start_time = time.time()
        self.restore_backup()
        end_time = time.time()
        elapsed = end_time - start_time
