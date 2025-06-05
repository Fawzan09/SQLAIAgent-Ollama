# flexible_sql_tool.py
import json
from typing import Optional

from phi.tools import Toolkit
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class FlexibleSQLTool(Toolkit):
    def __init__(self, db_url: str):
        super().__init__(name="flexible_sql_tool")

        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

        # Регистрируем подкоманды (если будут использоваться напрямую)
        self.register(self.use)

    def use(self, sql: str, format: str = "table", limit: Optional[int] = None) -> str:
        """
        Выполняет SQL-запрос и возвращает результат как таблицу или краткую сводку.
        :param sql: SQL-запрос
        :param format: 'table' | 'summary'
        :param limit: ограничение по числу строк
        :return: строка с результатом
        """
        try:
            with self.Session() as session, session.begin():
                result = session.execute(text(sql))
                try:
                    rows = result.fetchmany(limit) if limit else result.fetchall()
                    parsed = [row._asdict() for row in rows]
                    if format == "summary":
                        return self._summarise(parsed)
                    return self._render_table(parsed)
                except Exception as parse_error:
                    return f"[⚠] Query OK, but result parsing failed: {parse_error}"
        except Exception as exec_error:
            return f"[❌] Query failed: {exec_error}"

    def _render_table(self, rows: list[dict]) -> str:
        if not rows:
            return "[ℹ] No results."
        keys = list(rows[0].keys())
        header = "| " + " | ".join(keys) + " |"
        separator = "| " + " | ".join(["---"] * len(keys)) + " |"
        body = "\n".join("| " + " | ".join(str(row.get(k, "")) for k in keys) + " |" for row in rows)
        return "\n".join([header, separator, body])

    def _summarise(self, rows: list[dict]) -> str:
        if not rows:
            return "[ℹ] No results to summarise."
        summary_lines = [f"- {len(rows)} rows returned."]
        # Optionally: pick representative fields
        fields = rows[0].keys() if rows else []
        summary_lines.append(f"- Columns: {', '.join(fields)}")
        return "\n".join(summary_lines)
