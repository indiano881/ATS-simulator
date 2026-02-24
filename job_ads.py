JOB_ADS = {
    "fullstack": {
        "id": "fullstack",
        "title": "Fullstack Engineer",
        "company": "Embark Studios",
        "description": (
            "About the job\n\n"
            "As a Fullstack Engineer at Embark, you will be a Gamemaker in a technical "
            "team that builds and maintains internal tools that empower our game teams "
            "and improve the studio's efficiency. Your role will directly support game "
            "development by creating solutions that automates and streamlines workflows, "
            "and provides valuable analytics. You will also be contributing to commercial "
            "projects like tools for monetization and customer support.\n\n"
            "The team's goal is to deliver scalable, user-friendly, and cost-efficient "
            "solutions that help our teams create dynamic and engaging player experiences. "
            "You'll collaborate closely with game teams, data teams, and the commercial "
            "team, reporting to the Tech Lead in Commercial Tech.\n\n"
            "As an integral part of a creative and autonomous team, you'll contribute to "
            "high-quality tools and systems for both developers and players. For the "
            "frontend we use technologies like React, TypeScript and NextJS. For the "
            "backend we use Go, protobuf, Python, and OpenAPI.\n\n"
            "Example Of Responsibilities:\n"
            "- Develop and improve internal tools for game teams and studio-wide use.\n"
            "- Automate workflows to reduce manual effort and enhance efficiency.\n"
            "- Build personalized store recommendation systems and tools.\n"
            "- Continuously refine engineering practices to ensure services are easy to "
            "deploy, scale, and maintain.\n"
            "- Collaborate with multiple teams to deliver tools and solutions that improve "
            "both developer and player experiences.\n\n"
            "We would love if you have:\n"
            "- A creative and curious mind\n"
            "- Solid experience with React, TypeScript, NextJS, Go, Python and the GCP stack.\n"
            "- Proven ability to build internal data-driven tools and services.\n"
            "- Experience deploying and maintaining services on cloud infrastructure.\n"
            "- Strong background in analytics and data-driven tooling.\n"
            "- Analytical mindset, self-driven and capable of taking projects from idea "
            "to implementation.\n"
            "- Experience in the gaming industry or other consumer-facing products.\n"
            "- Passion for games, interactive experiences and new technologies.\n"
            "- Professional English communication skills."
        ),
        "keywords": [
            "react",
            "typescript",
            "nextjs",
            "go",
            "python",
            "protobuf",
            "openapi",
            "gcp",
            "fullstack",
            "internal tools",
            "analytics",
            "data-driven",
            "cloud infrastructure",
            "automation",
            "scalable",
            "gaming",
            "api",
            "deploy",
            "frontend",
            "backend",
            "engineering",
            "ci/cd",
            "monetization",
        ],
    },
    "project_manager": {
        "id": "project_manager",
        "title": "Project Manager",
        "company": "SS&C Eze",
        "description": (
            "About the job\n\n"
            "As a leading financial services and healthcare technology company based on "
            "revenue, SS&C is headquartered in Windsor, Connecticut, and has 27,000+ "
            "employees in 35 countries. Some 20,000 financial services and healthcare "
            "organizations, from the world's largest companies to small and mid-market "
            "firms, rely on SS&C for expertise, scale, and technology.\n\n"
            "Job Title: Project Manager\n"
            "Location: Stockholm, Sweden\n\n"
            "Get To Know Us:\n\n"
            "SS&C Eze is a premier provider of global investment technology to support "
            "the front, middle and back office. The Eze Software Investment Suite "
            "addresses the core business needs of the asset management community, "
            "including Order Management, Trade Execution & Analytics, Portfolio Analytics "
            "& Modelling, Compliance & Regulatory Reporting, Commission Management, Data "
            "Management and Portfolio Accounting.\n\n"
            "Eze Software partners with more than 2,000 buy-and sell-side institutions "
            "in 30 countries across North and South America, EMEA, and Asia Pacific. "
            "Clients include hedge funds, institutional asset managers, mutual funds, "
            "pension funds, endowments, family offices, wealth managers, and "
            "broker-dealers across a range of strategies, investment products, and asset "
            "classes.\n\n"
            "What You Will Get To Do:\n\n"
            "As a Project Manager, you will own and manage all activities relating to "
            "projects you manage for our clients, with full responsibility of delivery "
            "of client projects. You will apply knowledge, skills, tools, and techniques "
            "to project activities in order to meet business requirements and resolve any "
            "deviation from project plans regarding scope, resources, schedule, and "
            "budget, with the ultimate goal of creating delighted and referenceable "
            "clients. In addition to this, you will proactively contribute to continuous "
            "improvement within SS&C's Project Management team, and seek mentorship from "
            "more experienced staff.\n\n"
            "Travel within EMEA is expected, with the amount depending on client and "
            "project location.\n\n"
            "Your Key Duties will include:\n"
            "- Build strong relationships with internal and client stakeholders, managing "
            "them and their expectations according to the needs of the project.\n"
            "- Initiate and establish strong project governance frameworks, leveraging "
            "industry and SS&C best practices.\n"
            "- Ensure project objectives are in line with client needs, and are understood "
            "by relevant internal and external stakeholders.\n"
            "- Collaborate with internal and external teams on relevant decisions to "
            "deliver successful projects.\n"
            "- Thoroughly plan project execution and activities, tracking and reporting "
            "progress, and managing any deviations as needed through effective Change "
            "Management.\n"
            "- Establish and review project baselines (scope, resources, schedule, budget).\n"
            "- Proactively manage project risks, creating appropriate mitigation plans.\n"
            "- Manage issues and any escalations, drive these to satisfactory resolution.\n"
            "- Proactively contribute to continuous improvement items relating to how SS&C "
            "delivers client projects.\n\n"
            "What You Will Bring:\n"
            "- 4+ years of experience in investment finance or adjacent industries.\n"
            "- 2+ years of experience leading business and technology transformation "
            "projects, preferably with external client stakeholders.\n"
            "- Solid understanding of project management practices, with experience in "
            "using project management, ERP and CRM software.\n"
            "- Demonstrable ability to communicate with and present to stakeholders of "
            "all levels, up to and including C-Suite.\n"
            "- Knowledge of EMS, OMS and IBOR/ABOR software strongly preferred."
        ),
        "keywords": [
            "project management",
            "stakeholder management",
            "investment finance",
            "oms",
            "ems",
            "ibor",
            "risk management",
            "change management",
            "governance",
            "budget",
            "crm",
            "erp",
            "c-suite",
            "emea",
            "compliance",
            "transformation",
            "continuous improvement",
            "project planning",
            "escalation",
            "client",
            "agile",
            "reporting",
            "buy-side",
            "asset management",
        ],
    },
}


def get_job_ads():
    return JOB_ADS


def get_job_ad(job_id):
    return JOB_ADS.get(job_id)
