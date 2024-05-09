from fastapi import Query
from typing import List
from src.models.companies import Company
from src.constants import CompanyFilters


async def fetch_companies(db, filter_type, filter_text: str = None, filter_name: List[CompanyFilters] = Query(None)):
    query = "SELECT id, company_name, website, country FROM companies WHERE TRUE"
    values = {}
    if filter_text and filter_name:
        conditions = []
        if "company_name" in filter_name:
            if "fuzzy" in filter_type:
                conditions.append("company_name ILIKE '%' || :filter_text || '%'")
            else:
                conditions.append("company_name = :filter_text")
            values["filter_text"] = filter_text
        if "website" in filter_name:
            conditions.append("website = :filter_text")
            values["filter_text"] = filter_text
        if "country" in filter_name:
            conditions.append("country = :filter_text")
            values["filter_text"] = filter_text
        query += " AND " + " AND ".join(conditions)
    companies_data = await db.fetch_all(query, values=values)
    await db.disconnect()
    return [Company(**company) for company in companies_data]