


async def do_setup(db):
    companies_q = """
    CREATE TABLE public.companies (
        id serial4 NOT NULL,
        company_name varchar(255) NOT NULL,
        website varchar(255) NOT NULL,
        country varchar(100) NOT NULL,
        CONSTRAINT companies_pkey PRIMARY KEY (id)
    );
    """
    await db.execute(query=companies_q)
    contacts_q = \
        """
        CREATE TABLE public.contacts (
            id serial4 NOT NULL,
            company_id int4 NOT NULL,
            contact_name varchar(255) NULL,
            job_title varchar(255) NULL,
            job_level varchar(100) NULL,
            job_function varchar(100) NULL,
            CONSTRAINT contacts_pkey PRIMARY KEY (id)
        );
    """
    await db.execute(query=contacts_q)
    return