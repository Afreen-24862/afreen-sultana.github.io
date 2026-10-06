/* ============================================================
   EDIT ME — every piece of content on the site lives here.
   Anything marked [PLACEHOLDER] is sample text: replace with real details.
   ============================================================ */
window.DATA = {
  name: "Afreen Sultana",
  first: "AFREEN", last: "SULTANA",
  roles: ["AI Engineer", "Full Stack Developer", "LLM & Agents Builder", "Problem Solver"],
  tagline: "Final-year B.Tech CSE student in Hyderabad turning curiosity into shipped products — AI agents, RAG systems and full-stack apps.",
  email: "afreensultana24862@gmail.com",
  links: { linkedin: "#", github: "#", resume: "#", leetcode: "#" }, 
  location: "Hyderabad, India", college: "B.Tech CSE · Final Year",

  aboutHeading: ["I build <b>intelligent</b>", "products where <b>AI</b>,", "<b>engineering</b>,", "and <b>people</b>", "meet."],
  about: [
    "I'm a final-year Computer Science student who likes shipping more than slides. I care about software that is fast, reliable and genuinely useful.",
    "Right now I'm deep into LLM applications — retrieval, tool use, agents, evaluation — and the full-stack craft needed to put them in front of real users."
  ],
  facts: [
    { k: "Focus", v: "Agentic AI · RAG · Full-Stack" },
    { k: "Currently", v: "Final-year B.Tech CSE" },
    { k: "Based in", v: "Hyderabad, India" },
    { k: "Looking for", v: "AI / Software roles & internships" },
    { k: "Studying at", v: "Malla Reddy Engineering College for Women" }
  ],
  stats: [
    { n: 8, s: "+", l: "B.Tech CGPA" },
    { n: 92, s: "%", l: "Class X" },
    { n: 72, s: "%", l: "Intermediate" },
    { n: 1, s: "", l: "Flagship AI project" }
  ],

  skills: {
    "GenAI & Agents": [
      ["LLM Apps (OpenAI / Claude / Gemini)", 92], ["RAG Pipelines", 90], ["AI Agents & Tool Use", 88],
      ["Model Context Protocol (MCP)", 80], ["LangChain / LangGraph", 84], ["Prompt & Context Engineering", 90],
      ["Vector DBs (FAISS, pgvector, Pinecone)", 82], ["LLM Evals & Guardrails", 76], ["Fine-tuning (LoRA / PEFT)", 72], ["Embeddings & Reranking", 82]
    ],
    "Machine Learning": [
      ["Python", 94], ["PyTorch", 80], ["Scikit-learn", 88], ["NLP / Transformers", 84], ["Pandas · NumPy", 92],
      ["XGBoost", 78], ["Computer Vision (OpenCV)", 70], ["Hugging Face", 84], ["MLOps basics (MLflow)", 68]
    ],
    "Full Stack": [
      ["React.js", 90], ["Next.js 15 (App Router)", 88], ["TypeScript", 86], ["Node.js · Express", 88], ["FastAPI · Flask", 86],
      ["Tailwind CSS · shadcn/ui", 92], ["REST · GraphQL · WebSockets", 84], ["Auth (JWT · OAuth · NextAuth)", 85], ["Streaming UIs (SSE)", 80]
    ],
    "Cloud & DevOps": [
      ["Docker", 84], ["Git · GitHub Actions CI/CD", 88], ["AWS (EC2 · S3 · Lambda · SES)", 74], ["GCP", 68],
      ["Vercel · Render · Railway", 90], ["Kubernetes (basics)", 56], ["Observability (LangSmith · Sentry)", 70], ["Linux & Shell", 82]
    ],
    "Data & Databases": [
      ["PostgreSQL", 86], ["MongoDB", 86], ["MySQL", 84], ["Redis", 74], ["Supabase", 88], ["Prisma / Drizzle ORM", 80], ["Data Viz (Plotly · Matplotlib)", 82]
    ],
    "CS Fundamentals": [
      ["Data Structures & Algorithms", 90], ["Java", 88], ["C / C++", 80], ["OOP & Design Patterns", 86],
      ["DBMS", 88], ["Operating Systems", 82], ["Computer Networks", 78], ["System Design", 80]
    ]
  },
  marquee: ["Python","TypeScript","Next.js","React","FastAPI","Node.js","LangGraph","RAG","MCP","PyTorch","Docker","PostgreSQL","pgvector","Redis","AWS","Tailwind","Hugging Face","Java","GitHub Actions"],

  /* College-only journey. sample:true entries show a "Sample" tag until she confirms them (set showSampleBadges:false when all are real) */
  showSampleBadges: false,
  experience: [
    { tab: "Final-Year Project", role: "AI for Urban Air Quality", org: "B.Tech Project", when: "2026", type: "Flagship",
      tags: ["Python","LLM","Machine Learning","Pollution Data","Data Analysis"],
      intro: "An AI assistant for Hyderabad that uses the city’s pollution data together with an LLM to help people understand air quality and take steps to reduce their exposure and impact.",
      points: [
        ["Problem:", "Hyderabad’s air-quality numbers are hard for ordinary people to interpret, and rarely tell them what to actually do."],
        ["Approach:", "Combine Hyderabad’s real pollution data with an AI / LLM model that explains conditions in plain language and suggests practical actions."],
        ["Goal:", "Help users make better daily decisions and reduce pollution at an individual and community level."]
      ]},
    { tab: "Academic Projects", role: "Mini & Major Projects", org: "B.Tech CSE", when: "2023 — 2026", type: "College",
      tags: ["Python","Java","MySQL","Machine Learning","Web Dev"],
      intro: "Hands-on projects built alongside coursework, each taking a classroom concept to a working application.",
      points: [
        ["Machine learning:", "Built classification, recommendation and NLP models from raw data to evaluation."],
        ["Full stack:", "Designed database-backed web applications with authentication and clean UI."],
        ["Fundamentals:", "Applied DSA, DBMS and OOP in lab projects with documented design and testing."]
      ]},
    { tab: "Technical Learning", role: "Workshops, Courses & Self-Learning", org: "College & online", when: "2024 — Present", type: "Ongoing",
      tags: ["Generative AI","Prompt Engineering","Python","Cloud","DSA"],
      intro: "Continuously learning the tools the industry uses today, beyond the syllabus.",
      points: [
        ["Generative AI:", "Studying LLMs, prompt engineering and retrieval-augmented generation."],
        ["Problem solving:", "Regular data-structures and algorithms practice."],
        ["Cloud & tooling:", "Git/GitHub workflows, deployment basics and API usage."]
      ]},
    { tab: "Campus Activities", role: "Student Club & Events", org: "Malla Reddy Engineering College for Women", when: "2024 — Present", type: "Leadership",
      tags: ["Teamwork","Presentation","Event Coordination"],
      intro: "Active in campus technical and cultural life, building communication and teamwork alongside engineering skills.",
      points: [
        ["Participation:", "Took part in technical events, paper/poster presentations and project expos."],
        ["Collaboration:", "Worked in teams to plan, build and present projects within deadlines."]
      ]},
    { tab: "B.Tech CSE", role: "B.Tech — Computer Science & Engineering", org: "Malla Reddy Engineering College for Women", when: "2023 — Present", type: "Final Year",
      tags: ["DSA","DBMS","OS","Computer Networks","OOP","Machine Learning"],
      intro: "Scoring 8+ CGPA while building a strong base in core computer science and applied AI.",
      points: [
        ["Core CS:", "Data structures & algorithms, DBMS, operating systems, networks and object-oriented design."],
        ["Applied AI:", "Machine learning and LLM-based applications through coursework and the final-year project."]
      ]}
  ],

  now: [
    { cmd: "practice", name: "dsa", flags: "--lang java --daily", title: "Data Structures & Algorithms", text: "Building problem-solving speed with dynamic programming, graphs and backtracking.", status: "ONGOING" },
    { cmd: "learn", name: "llm-agents", flags: "--rag --tool-use", title: "LLMs & AI Agents", text: "Understanding how modern AI systems retrieve information, reason and use tools.", status: "LEARNING" },
    { cmd: "explore", name: "system-design", flags: "--scale --cloud", title: "System Design & Cloud", text: "Learning how real products scale: caching, queues and deployment.", status: "EXPLORING" }
  ],

  projects: [
    { id: "p1", tag: "Hyderabad’s air, explained by AI.", name: "CityAir AI", cat: "AI", sub: "Hyderabad Pollution Insights & Control Assistant", year: "2026", featured: true,
      desc: "An LLM-powered assistant built around Hyderabad’s pollution data that explains the air in plain language and guides people toward reducing it.",
      problem: "Hyderabad’s air-quality numbers are hard for everyday residents to interpret and rarely turn into clear, actionable guidance.",
      solution: "Feed Hyderabad’s pollution data into an AI / LLM model that interprets it, answers questions in plain language and recommends practical steps for residents.",
      impact: "Helps people in Hyderabad understand the air they breathe and take actions that help control pollution across the city.",
      stack: ["Python","LLM","Machine Learning","Data Analysis"], hue: 200, live: "#", repo: "#" },
    { id: "p2", tag: "Ask Malla Reddy’s documents anything.", name: "CampusBot", cat: "AI", sub: "Malla Reddy College FAQ Chatbot (RAG)", year: "2025",
      desc: "A chatbot for students of Malla Reddy Engineering College for Women that answers questions about timetables, rules and notices from official college documents.",
      problem: "Students at Malla Reddy Engineering College for Women dig through PDFs, circulars and notice boards for simple answers.",
      solution: "Index the college’s documents, retrieve the right passages and let an LLM answer with the source shown.",
      impact: "Quicker answers for students on campus and less load on faculty and office staff.",
      stack: ["Python","RAG","FAISS","Streamlit"], hue: 265, live: "#", repo: "#" },
    { id: "p3", tag: "Attendance by face, in seconds.", name: "FaceMark", cat: "ML", sub: "Face-Recognition Attendance", year: "2025",
      desc: "Marks classroom attendance automatically from a camera feed.",
      problem: "Manual roll calls waste lecture time and allow proxies.",
      solution: "Detect and recognise faces with OpenCV, log attendance to a database and export reports.",
      impact: "Faster, more reliable attendance records.",
      stack: ["Python","OpenCV","SQLite","Flask"], hue: 150, live: "#", repo: "#" },
    { id: "p4", tag: "Movies matched to your taste.", name: "ReelPick", cat: "ML", sub: "Movie Recommendation Engine", year: "2024",
      desc: "Suggests movies using content-based and collaborative filtering.",
      problem: "Too many choices make it hard to find something good.",
      solution: "Compare similarity of genres, cast and ratings and rank personalised picks.",
      impact: "A working recommender with a clean search UI.",
      stack: ["Python","Scikit-learn","Pandas","Streamlit"], hue: 330, live: "#", repo: "#" },
    { id: "p5", tag: "Read the mood of any review.", name: "SentiScope", cat: "AI", sub: "Sentiment Analysis Dashboard", year: "2025",
      desc: "Classifies reviews and tweets as positive, negative or neutral with live charts.",
      problem: "Raw opinions are hard to summarise at scale.",
      solution: "Clean text, train an NLP classifier and visualise trends over time.",
      impact: "Turns thousands of comments into one clear picture.",
      stack: ["Python","NLP","Transformers","Plotly"], hue: 20, live: "#", repo: "#" },
    { id: "p6", tag: "Issue, return and fines — sorted.", name: "LibraryHub", cat: "Full Stack", sub: "Library Management System", year: "2024",
      desc: "Web app to issue, return and track books with fines and roles.",
      problem: "Paper registers cause lost records and overdue confusion.",
      solution: "Role-based login, searchable catalogue and automated fine calculation on a relational database.",
      impact: "A complete CRUD system showing DBMS and backend fundamentals.",
      stack: ["Java","Spring Boot","MySQL","HTML/CSS"], hue: 45, live: "#", repo: "#" },
    { id: "p7", tag: "Score a resume against any job.", name: "ResumeLens", cat: "AI", sub: "AI Resume Screener", year: "2025",
      desc: "Scores resumes against a job description and highlights missing skills.",
      problem: "Reading every resume by hand is slow and inconsistent.",
      solution: "Extract skills with NLP, compare against the role using embeddings and rank candidates.",
      impact: "Faster shortlisting with transparent reasons.",
      stack: ["Python","Embeddings","FastAPI","React"], hue: 290, live: "#", repo: "#" },
    { id: "p8", tag: "Plan work: To do, Doing, Done.", name: "TaskFlow", cat: "Full Stack", sub: "Productivity & Task Manager", year: "2024",
      desc: "A clean to-do and planner app with reminders and progress charts.",
      problem: "Students juggle deadlines across notes and chats.",
      solution: "React front end with a Node API, login, reminders and weekly progress analytics.",
      impact: "A polished full-stack app deployed online.",
      stack: ["React","Node.js","MongoDB","Tailwind"], hue: 180, live: "#", repo: "#" }
  ],

  education: [
    { deg: "B.Tech — Computer Science & Engineering", org: "Malla Reddy Engineering College for Women", when: "2023 — Present", note: "CGPA 8+ · Final Year" },
    { deg: "Intermediate (Class XII)", org: "Kendriya Vidyalaya", when: "Completed", note: "72%" },
    { deg: "Class X", org: "Kendriya Vidyalaya", when: "Completed", note: "92%" }
  ],
  achievements: [
    "Scored 92% in Class X",
    "Maintaining 8+ CGPA in B.Tech CSE",
    "Building a final-year AI project for cleaner cities"
  ]
};
