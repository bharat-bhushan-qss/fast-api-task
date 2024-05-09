from src.models.contacts import ContactBaseOut


async def fetch_contacts(db, job_title: str = None, job_level: str = None, job_function: str = None, limit: int = None):
    query = """
    SELECT 
    c.id, c.company_id, c.contact_name, c.job_title, c.job_level, 
    c.job_function, comp.company_name, comp.website, comp.country 
    FROM contacts c 
    JOIN companies comp ON c.company_id = comp.id 
    WHERE TRUE
    """
    values = {}
    conditions = []
    if job_title:
        conditions.append("c.job_title = :job_title")
        values["job_title"] = job_title
    if job_level:
        conditions.append("c.job_level = :job_level")
        values["job_level"] = job_level
    if job_function:
        conditions.append("c.job_function = :job_function")
        values["job_function"] = job_function
    if conditions:
        query += " AND " + " AND ".join(conditions)
    if limit:
        query += " LIMIT :limit"
        values["limit"] = limit
    contacts_data = await db.fetch_all(query, values=values)
    await db.disconnect()
    contacts = []
    for contact in contacts_data:
        company_info = {
            "company_name": contact["company_name"],
            "website": contact["website"],
            "country": contact["country"]
        }
        contacts.append(ContactBaseOut(**contact, company=company_info))
    return contacts