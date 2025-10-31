#!/usr/bin/env python3
"""
Database migration script for International Payment System
"""

import asyncio
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class PaymentSystemMigrator:
    def __init__(self, db_path: str = "payments.db"):
        self.db_path = db_path
        self.migrations_dir = Path("migrations")
        self.migrations_dir.mkdir(exist_ok=True)

    def initialize_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create migrations table to track applied migrations
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Create transactions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT UNIQUE NOT NULL,
                sender_data TEXT NOT NULL,
                recipient_data TEXT NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                currency TEXT NOT NULL,
                target_currency TEXT NOT NULL,
                status TEXT NOT NULL,
                exchange_rate DECIMAL(10,6),
                converted_amount DECIMAL(15,2),
                security_token TEXT,
                compliance_status TEXT,
                risk_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Create users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                country TEXT NOT NULL,
                default_currency TEXT DEFAULT 'USD',
                kyc_status TEXT DEFAULT 'pending',
                risk_level TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Create wallets table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                currency TEXT NOT NULL,
                balance DECIMAL(15,2) DEFAULT 0.0,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id, currency)
            )
        """
        )

        # Create exchange_rates table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                base_currency TEXT NOT NULL,
                target_currency TEXT NOT NULL,
                rate DECIMAL(10,6) NOT NULL,
                source TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(base_currency, target_currency, timestamp)
            )
        """
        )

        # Create audit_log table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                user_id TEXT,
                transaction_id TEXT,
                description TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Create indexes
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_transactions_created ON transactions(created_at)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_wallets_user ON wallets(user_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_log_created ON audit_log(created_at)"
        )

        conn.commit()
        conn.close()

        print("✅ Database initialized successfully")

    def create_initial_migration(self):
        """Create initial migration file"""
        migration_content = {
            "version": "001",
            "description": "Initial database schema",
            "up": [
                "CREATE TABLE IF NOT EXISTS transactions (...)",
                "CREATE TABLE IF NOT EXISTS users (...)",
                "CREATE TABLE IF NOT EXISTS wallets (...)",
            ],
            "down": [
                "DROP TABLE IF EXISTS transactions",
                "DROP TABLE IF EXISTS users",
                "DROP TABLE IF EXISTS wallets",
            ],
        }

        migration_file = self.migrations_dir / "001_initial_schema.json"
        with open(migration_file, "w") as f:
            json.dump(migration_content, f, indent=2)

        print(f"✅ Created initial migration: {migration_file}")

    def apply_migrations(self):
        """Apply all pending migrations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get applied migrations
        cursor.execute("SELECT name FROM migrations ORDER BY id")
        applied_migrations = {row[0] for row in cursor.fetchall()}

        # Find migration files
        migration_files = sorted(self.migrations_dir.glob("*.json"))

        for migration_file in migration_files:
            migration_name = migration_file.stem

            if migration_name in applied_migrations:
                print(f"⏩ Migration already applied: {migration_name}")
                continue

            print(f"🔄 Applying migration: {migration_name}")

            try:
                with open(migration_file, "r") as f:
                    migration = json.load(f)

                # Execute migration commands
                for command in migration.get("up", []):
                    cursor.execute(command)

                # Record migration
                cursor.execute(
                    "INSERT INTO migrations (name, applied_at) VALUES (?, ?)",
                    (migration_name, datetime.utcnow()),
                )

                conn.commit()
                print(f"✅ Applied migration: {migration_name}")

            except Exception as e:
                conn.rollback()
                print(f"❌ Failed to apply migration {migration_name}: {e}")
                break

        conn.close()

    def seed_sample_data(self):
        """Seed database with sample data for testing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Sample users
        sample_users = [
            (
                "user_001",
                "john.doe@example.com",
                "John Doe",
                "US",
                "USD",
                "verified",
                "low",
            ),
            (
                "user_002",
                "maria.garcia@example.com",
                "Maria Garcia",
                "ES",
                "EUR",
                "verified",
                "low",
            ),
            (
                "user_003",
                "taro.yamada@example.com",
                "Taro Yamada",
                "JP",
                "JPY",
                "pending",
                "medium",
            ),
        ]

        cursor.executemany(
            """
            INSERT OR IGNORE INTO users (user_id, email, name, country, default_currency, kyc_status, risk_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            sample_users,
        )

        # Sample wallets
        sample_wallets = [
            ("wallet_001", "user_001", "USD", 5000.00),
            ("wallet_002", "user_001", "EUR", 2500.00),
            ("wallet_003", "user_002", "EUR", 8000.00),
            ("wallet_004", "user_003", "JPY", 500000.00),
        ]

        cursor.executemany(
            """
            INSERT OR IGNORE INTO wallets (wallet_id, user_id, currency, balance)
            VALUES (?, ?, ?, ?)
        """,
            sample_wallets,
        )

        # Sample exchange rates
        sample_rates = [
            ("USD", "EUR", 0.85, "system"),
            ("USD", "JPY", 110.5, "system"),
            ("EUR", "USD", 1.18, "system"),
            ("EUR", "JPY", 130.0, "system"),
        ]

        cursor.executemany(
            """
            INSERT OR IGNORE INTO exchange_rates (base_currency, target_currency, rate, source)
            VALUES (?, ?, ?, ?)
        """,
            sample_rates,
        )

        conn.commit()
        conn.close()

        print("✅ Sample data seeded successfully")

    def run(self):
        """Run complete migration process"""
        print("🚀 Starting Payment System Database Migration...")

        try:
            self.initialize_database()
            self.create_initial_migration()
            self.apply_migrations()
            self.seed_sample_data()

            print("\n🎉 Migration completed successfully!")

        except Exception as e:
            print(f"\n💥 Migration failed: {e}")
            raise


def main():
    """Main migration execution"""
    import argparse

    parser = argparse.ArgumentParser(description="Payment System Database Migrator")
    parser.add_argument(
        "--db-path", default="payments.db", help="Path to database file"
    )
    parser.add_argument("--seed", action="store_true", help="Seed with sample data")

    args = parser.parse_args()

    migrator = PaymentSystemMigrator(db_path=args.db_path)

    if args.seed:
        migrator.seed_sample_data()
    else:
        migrator.run()


if __name__ == "__main__":
    main()
