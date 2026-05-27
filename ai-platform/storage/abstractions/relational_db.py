"""
Relational database abstraction (PostgreSQL)
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from dataclasses import dataclass

from .base import StorageBackend, StorageConfig


@dataclass
class ColumnDefinition:
    """Column definition for table schema."""
    name: str
    type: str
    primary_key: bool = False
    nullable: bool = True
    unique: bool = False
    default: Optional[Any] = None


@dataclass
class TableSchema:
    """Table schema definition."""
    name: str
    columns: List[ColumnDefinition]
    indexes: Optional[List[Dict[str, Any]]] = None


class RelationalDB(StorageBackend):
    """
    Abstract relational database backend.
    
    Provides unified interface for relational database operations.
    """
    
    @abstractmethod
    async def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Execute a SQL query.
        
        Args:
            query: SQL query string
            parameters: Query parameters
            
        Returns:
            Query results as list of dictionaries
        """
        pass
    
    @abstractmethod
    async def execute_command(
        self,
        command: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Execute a SQL command (INSERT, UPDATE, DELETE).
        
        Args:
            command: SQL command string
            parameters: Command parameters
            
        Returns:
            Number of affected rows
        """
        pass
    
    @abstractmethod
    async def create_table(
        self,
        schema: TableSchema,
        if_not_exists: bool = True,
    ) -> bool:
        """
        Create a new table.
        
        Args:
            schema: Table schema definition
            if_not_exists: Skip if table already exists
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def drop_table(
        self,
        table_name: str,
        if_exists: bool = True,
    ) -> bool:
        """
        Drop a table.
        
        Args:
            table_name: Name of the table
            if_exists: Skip if table doesn't exist
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def table_exists(self, table_name: str) -> bool:
        """
        Check if table exists.
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if table exists
        """
        pass
    
    @abstractmethod
    async def list_tables(self) -> List[str]:
        """
        List all tables in the database.
        
        Returns:
            List of table names
        """
        pass
    
    @abstractmethod
    async def get_table_schema(
        self,
        table_name: str,
    ) -> Optional[TableSchema]:
        """
        Get table schema information.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Table schema or None if not found
        """
        pass
    
    @abstractmethod
    async def insert(
        self,
        table_name: str,
        data: Union[Dict[str, Any], List[Dict[str, Any]]],
    ) -> List[int]:
        """
        Insert data into table.
        
        Args:
            table_name: Name of the table
            data: Single record or list of records
            
        Returns:
            List of inserted row IDs
        """
        pass
    
    @abstractmethod
    async def select(
        self,
        table_name: str,
        columns: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Select data from table.
        
        Args:
            table_name: Name of the table
            columns: Columns to select (None = all)
            where: WHERE clause conditions
            limit: Maximum number of rows
            offset: Number of rows to skip
            order_by: Ordering columns
            
        Returns:
            List of rows as dictionaries
        """
        pass
    
    @abstractmethod
    async def update(
        self,
        table_name: str,
        data: Dict[str, Any],
        where: Dict[str, Any],
    ) -> int:
        """
        Update data in table.
        
        Args:
            table_name: Name of the table
            data: Data to update
            where: WHERE clause conditions
            
        Returns:
            Number of affected rows
        """
        pass
    
    @abstractmethod
    async def delete(
        self,
        table_name: str,
        where: Dict[str, Any],
    ) -> int:
        """
        Delete data from table.
        
        Args:
            table_name: Name of the table
            where: WHERE clause conditions
            
        Returns:
            Number of affected rows
        """
        pass
    
    @abstractmethod
    async def begin_transaction(self) -> str:
        """
        Begin a transaction.
        
        Returns:
            Transaction ID
        """
        pass
    
    @abstractmethod
    async def commit_transaction(self, transaction_id: str) -> bool:
        """
        Commit a transaction.
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def rollback_transaction(self, transaction_id: str) -> bool:
        """
        Rollback a transaction.
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            True if successful
        """
        pass


class PostgreSQL(RelationalDB):
    """
    PostgreSQL database implementation.
    
    Provides relational database operations using asyncpg.
    """
    
    def __init__(self, config: StorageConfig):
        """
        Initialize PostgreSQL backend.
        
        Args:
            config: Storage configuration
        """
        super().__init__(config)
        self._pool = None
        self._transactions = {}
    
    async def connect(self) -> None:
        """Establish PostgreSQL connection."""
        import asyncpg
        
        dsn = (
            f"postgresql://{self.config.username}:{self.config.password}"
            f"@{self.config.host}:{self.config.port}"
            f"/{self.config.database}"
        )
        
        self._pool = await asyncpg.create_pool(
            dsn,
            min_size=self.config.pool_size,
            max_size=self.config.pool_size + self.config.max_overflow,
            command_timeout=self.config.pool_timeout,
        )
        
        self._is_connected = True
    
    async def disconnect(self) -> None:
        """Close PostgreSQL connection."""
        if self._pool:
            await self._pool.close()
            self._pool = None
        self._is_connected = False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check PostgreSQL health."""
        try:
            result = await self.execute_query("SELECT 1 as status")
            if result:
                return {
                    "status": "healthy",
                    "backend": "postgresql",
                    "details": {
                        "endpoint": f"{self.config.host}:{self.config.port}",
                        "database": self.config.database
                    }
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": "postgresql",
                "error": str(e)
            }
    
    async def ping(self) -> bool:
        """Ping PostgreSQL backend."""
        try:
            result = await self.execute_query("SELECT 1 as status")
            return len(result) > 0
        except:
            return False
    
    async def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Execute SQL query."""
        parameters = parameters or {}
        
        async with self._pool.acquire() as conn:
            result = await conn.fetch(query, *parameters.values())
            return [dict(row) for row in result]
    
    async def execute_command(
        self,
        command: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Execute SQL command."""
        parameters = parameters or {}
        
        async with self._pool.acquire() as conn:
            result = await conn.execute(command, *parameters.values())
            # Parse "INSERT 0 1" or "UPDATE 5" to get row count
            if result:
                parts = result.split()
                if len(parts) >= 2:
                    try:
                        return int(parts[-1])
                    except ValueError:
                        pass
            return 0
    
    async def create_table(
        self,
        schema: TableSchema,
        if_not_exists: bool = True,
    ) -> bool:
        """Create table in PostgreSQL."""
        column_defs = []
        
        for col in schema.columns:
            col_def = f"{col.name} {col.type}"
            
            if col.primary_key:
                col_def += " PRIMARY KEY"
            if not col.nullable:
                col_def += " NOT NULL"
            if col.unique:
                col_def += " UNIQUE"
            if col.default is not None:
                col_def += f" DEFAULT {col.default}"
            
            column_defs.append(col_def)
        
        if_not = "IF NOT EXISTS " if if_not_exists else ""
        query = f"CREATE TABLE {if_not}{schema.name} ({', '.join(column_defs)})"
        
        await self.execute_command(query)
        return True
    
    async def drop_table(
        self,
        table_name: str,
        if_exists: bool = True,
    ) -> bool:
        """Drop table from PostgreSQL."""
        if_exists = "IF EXISTS " if if_exists else ""
        query = f"DROP TABLE {if_exists}{table_name}"
        
        await self.execute_command(query)
        return True
    
    async def table_exists(self, table_name: str) -> bool:
        """Check if table exists in PostgreSQL."""
        query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = $1
        )
        """
        result = await self.execute_query(query, {"table_name": table_name})
        return result[0]["exists"] if result else False
    
    async def list_tables(self) -> List[str]:
        """List all tables in PostgreSQL."""
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        """
        result = await self.execute_query(query)
        return [row["table_name"] for row in result]
    
    async def get_table_schema(
        self,
        table_name: str,
    ) -> Optional[TableSchema]:
        """Get table schema from PostgreSQL."""
        query = """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = $1
        ORDER BY ordinal_position
        """
        
        result = await self.execute_query(query, {"table_name": table_name})
        
        if not result:
            return None
        
        columns = []
        for row in result:
            columns.append(ColumnDefinition(
                name=row["column_name"],
                type=row["data_type"],
                nullable=row["is_nullable"] == "YES",
                default=row["column_default"]
            ))
        
        return TableSchema(name=table_name, columns=columns)
    
    async def insert(
        self,
        table_name: str,
        data: Union[Dict[str, Any], List[Dict[str, Any]]],
    ) -> List[int]:
        """Insert data into PostgreSQL table."""
        if isinstance(data, dict):
            data = [data]
        
        if not data:
            return []
        
        columns = list(data[0].keys())
        placeholders = [f"${i+1}" for i in range(len(columns))]
        
        query = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({', '.join(placeholders)})
        RETURNING id
        """
        
        inserted_ids = []
        for row in data:
            values = [row[col] for col in columns]
            result = await self.execute_query(query, dict(zip(columns, values)))
            if result and "id" in result[0]:
                inserted_ids.append(result[0]["id"])
        
        return inserted_ids
    
    async def select(
        self,
        table_name: str,
        columns: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Select data from PostgreSQL table."""
        columns = columns or ["*"]
        query = f"SELECT {', '.join(columns)} FROM {table_name}"
        
        params = {}
        param_count = 0
        
        if where:
            conditions = []
            for key, value in where.items():
                param_count += 1
                conditions.append(f"{key} = ${param_count}")
                params[f"param_{param_count}"] = value
            query += " WHERE " + " AND ".join(conditions)
        
        if order_by:
            query += " ORDER BY " + ", ".join(order_by)
        
        if limit:
            param_count += 1
            query += f" LIMIT ${param_count}"
            params[f"param_{param_count}"] = limit
        
        if offset:
            param_count += 1
            query += f" OFFSET ${param_count}"
            params[f"param_{param_count}"] = offset
        
        return await self.execute_query(query, params)
    
    async def update(
        self,
        table_name: str,
        data: Dict[str, Any],
        where: Dict[str, Any],
    ) -> int:
        """Update data in PostgreSQL table."""
        set_clause = []
        params = {}
        param_count = 0
        
        for key, value in data.items():
            param_count += 1
            set_clause.append(f"{key} = ${param_count}")
            params[f"param_{param_count}"] = value
        
        where_clause = []
        for key, value in where.items():
            param_count += 1
            where_clause.append(f"{key} = ${param_count}")
            params[f"param_{param_count}"] = value
        
        query = f"""
        UPDATE {table_name}
        SET {', '.join(set_clause)}
        WHERE {' AND '.join(where_clause)}
        """
        
        return await self.execute_command(query, params)
    
    async def delete(
        self,
        table_name: str,
        where: Dict[str, Any],
    ) -> int:
        """Delete data from PostgreSQL table."""
        where_clause = []
        params = {}
        param_count = 0
        
        for key, value in where.items():
            param_count += 1
            where_clause.append(f"{key} = ${param_count}")
            params[f"param_{param_count}"] = value
        
        query = f"""
        DELETE FROM {table_name}
        WHERE {' AND '.join(where_clause)}
        """
        
        return await self.execute_command(query, params)
    
    async def begin_transaction(self) -> str:
        """Begin PostgreSQL transaction."""
        import uuid
        transaction_id = str(uuid.uuid4())
        
        async with self._pool.acquire() as conn:
            self._transactions[transaction_id] = conn
            await conn.execute("BEGIN")
        
        return transaction_id
    
    async def commit_transaction(self, transaction_id: str) -> bool:
        """Commit PostgreSQL transaction."""
        if transaction_id not in self._transactions:
            return False
        
        conn = self._transactions.pop(transaction_id)
        await conn.execute("COMMIT")
        await conn.close()
        
        return True
    
    async def rollback_transaction(self, transaction_id: str) -> bool:
        """Rollback PostgreSQL transaction."""
        if transaction_id not in self._transactions:
            return False
        
        conn = self._transactions.pop(transaction_id)
        await conn.execute("ROLLBACK")
        await conn.close()
        
        return True