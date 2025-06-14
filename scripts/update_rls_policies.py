import os
import re
import logging
from collections import defaultdict

import psycopg2
from psycopg2 import extras


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


def get_connection():
    """Create a connection to the Supabase Postgres database using environment variables."""
    url = os.getenv("SUPABASE_DATABASE_URL")
    if url:
        return psycopg2.connect(url, cursor_factory=extras.RealDictCursor)

    host = os.getenv("SUPABASE_DB_HOST")
    user = os.getenv("SUPABASE_DB_USER")
    password = os.getenv("SUPABASE_DB_PASSWORD")
    dbname = os.getenv("SUPABASE_DB_NAME")
    port = os.getenv("SUPABASE_DB_PORT", "5432")

    if not all([host, user, password, dbname]):
        raise RuntimeError("Missing Supabase database environment variables")

    return psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname,
        cursor_factory=extras.RealDictCursor,
    )


def rewrite_auth_calls(expr: str) -> str:
    """Rewrite direct calls to auth helpers with subqueries."""
    new_expr = re.sub(r"\bauth\.uid\(\)", "(SELECT auth.uid())", expr)
    new_expr = re.sub(r"\bauth\.role\(\)", "(SELECT auth.role())", new_expr)
    return new_expr


def fetch_policies(cur):
    cur.execute(
        """
        SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
        FROM pg_policies
        """
    )
    return cur.fetchall()


def main() -> None:
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()

    policies = fetch_policies(cur)
    grouped = defaultdict(list)

    for pol in policies:
        roles = pol["roles"] or []
        if isinstance(roles, str):
            roles = [r.strip() for r in roles.strip("{}").split(",") if r]

        rewritten = rewrite_auth_calls(pol["qual"] or "")
        pol["rewritten"] = rewritten

        for role in roles or ["public"]:
            key = (
                pol["schemaname"],
                pol["tablename"],
                role,
                pol["cmd"],
            )
            grouped[key].append(pol)

    for key, policies in grouped.items():
        schema, table, role, cmd = key
        permissive_vals = {p["permissive"] for p in policies}
        if len(permissive_vals) > 1:
            logger.warning(
                "Conflicting permissive values for %s.%s role %s %s",
                schema,
                table,
                role,
                cmd,
            )
            continue

        if len(policies) > 1 and policies[0]["permissive"]:
            combined = " OR ".join(f"({p['rewritten']})" for p in policies)
            base = policies[0]
            logger.info(
                "Combining %d policies on %s.%s for role %s %s into %s",
                len(policies),
                schema,
                table,
                role,
                cmd,
                base["policyname"],
            )
            cur.execute(
                f'ALTER POLICY "{base["policyname"]}" ON "{schema}"."{table}" USING ({combined})'
            )
            for p in policies[1:]:
                cur.execute(f'DROP POLICY "{p["policyname"]}" ON "{schema}"."{table}"')
                logger.info("Dropped policy %s", p["policyname"])
        else:
            pol = policies[0]
            if pol["qual"] != pol["rewritten"]:
                logger.info(
                    "Rewriting auth calls in policy %s on %s.%s",
                    pol["policyname"],
                    schema,
                    table,
                )
                cur.execute(
                    f'ALTER POLICY "{pol["policyname"]}" ON "{schema}"."{table}" USING ({pol["rewritten"]})'
                )

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
