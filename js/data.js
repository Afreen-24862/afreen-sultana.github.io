/* ============================================================
   EDIT ME — every piece of content on the site lives here.
   Source of truth: Afreen's resume.
   ============================================================ */
window.DATA = {
  name: "Afreen Sultana",
  roles: ["AI / ML Engineer", "Software Engineer", "DevOps-Aware Product Engineer", "Forward Deployed Engineer"],
  tagline: "Computer Science student in Hyderabad with strong foundations in Python, Java, AI/ML and DevOps — building practical projects and learning fast.",
  email: "afreensultana24862@gmail.com",
  links: { linkedin: "#", github: "https://github.com/Afreen-24862", resume: "#", leetcode: "#" },
  location: "Hyderabad, India", college: "B.Tech CSE · Final Year",

  aboutHeading: ["I build <b>practical</b>", "software where <b>AI</b>,", "<b>engineering</b>,", "and <b>people</b>", "meet."],
  about: [
    "I'm a Computer Science Engineering student with strong foundations in Python, Java, C, data structures, web development, AI/ML fundamentals and DevOps-aware software delivery.",
    "I translate requirements into clean technical workflows, build practical projects, document my solutions and learn new tools quickly. I'm targeting entry-level software, AI/ML, DevOps and forward deployed engineering roles where problem solving, communication and ownership matter."
  ],
  facts: [
    { k: "Target roles", v: "AI/ML · Software · DevOps · FDE" },
    { k: "Studying", v: "B.Tech CSE · 2023 – 2027" },
    { k: "College", v: "Malla Reddy Engineering College for Women" },
    { k: "CGPA", v: "8.20 / 10 (current)" },
    { k: "Based in", v: "Hyderabad, India" },
    { k: "Languages", v: "English (B2) · Hindi · Telugu" }
  ],
  stats: [
    { n: 8.2, d: 1, s: "", l: "B.Tech CGPA (current)" },
    { n: 92, s: "%", l: "Class X" },
    { n: 72, s: "%", l: "Intermediate" },
    { n: 3, s: "", l: "Certifications" }
  ],

  skills: {
    "AI/ML & GenAI": [["Machine Learning Basics"],["Data Preprocessing"],["Feature Engineering"],["Model Training"],["Model Evaluation"],["NumPy"],["Pandas"],["Scikit-learn Basics"],["Prompt Engineering"],["RAG Fundamentals"],["Embeddings"],["Chatbot Workflows"]],
    "Programming & CS": [["Python"],["Java"],["C"],["Data Structures"],["Algorithms"],["OOP"],["Logical Reasoning"],["Debugging"]],
    "Web, APIs & Product": [["HTML"],["CSS"],["JavaScript"],["Responsive Design"],["REST API Fundamentals"],["Requirement Understanding"],["Technical Documentation"]],
    "DevOps & Deployment": [["Git"],["GitHub"],["CI/CD Basics"],["Docker Fundamentals"],["Linux Commands"],["Cloud Deployment Concepts"],["Monitoring"],["Logging"],["Release Workflows"]],
    "Forward Deployed Engineering": [["Stakeholder Communication"],["Client Workflow Automation"],["Rapid Prototyping"],["Debugging"],["API Integration Concepts"],["Handover Notes"],["Solution Support"]]
  },

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
    { tab: "Core Strengths", role: "What I bring", org: "Software · AI/ML · DevOps", when: "Now", type: "Strengths",
      tags: ["Problem Solving","Communication","Ownership","Documentation"],
      intro: "Practical engineering across software development, AI/ML fundamentals and DevOps workflows.",
      points: [
        ["Build:", "Practical solutions across software development, AI/ML fundamentals, DevOps workflows, APIs and documentation."],
        ["Translate:", "Breaking business requirements into technical tasks, prototypes, workflows and clear handover notes."],
        ["Communicate:", "Explaining technical ideas clearly to team members, users and non-technical stakeholders."],
        ["Own:", "Continuous learning, debugging discipline, clean work habits and a willingness to improve."]
      ]},
    { tab: "B.Tech CSE", role: "B.Tech — Computer Science & Engineering", org: "Malla Reddy Engineering College for Women", when: "Aug 2023 — 2027", type: "Current CGPA 8.20",
      tags: ["Programming","Data Structures","Algorithms","Web Development","AI/ML Foundations","Software Engineering"],
      intro: "Hyderabad, India. Current CGPA: 8.20 / 10.",
      points: [
        ["Focus:", "Programming, data structures, algorithms, web development, AI/ML foundations and software engineering practices."],
        ["Applied:", "Turning coursework into working projects — from a resume screener and a prediction model to a CI/CD pipeline."]
      ]}
  ],

  now: [
    { cmd: "practice", name: "dsa", flags: "--lang python,java,c --daily", title: "Data Structures & Algorithms", text: "Building problem-solving speed and clean, debuggable code.", status: "ONGOING" },
    { cmd: "learn", name: "genai", flags: "--prompting --rag --embeddings", title: "GenAI & RAG", text: "Prompt engineering, embeddings and chatbot workflows.", status: "LEARNING" },
    { cmd: "explore", name: "devops", flags: "--docker --ci-cd --linux", title: "DevOps & Deployment", text: "CI/CD, Docker, Linux and release workflows.", status: "EXPLORING" }
  ],

  projects: [
    { id: "p1", tag: "Hyderabad’s air, explained by AI.", name: "CityAir AI", cat: "AI", sub: "Hyderabad Pollution Insights & Control Assistant", year: "2026", featured: true,
      desc: "An LLM-powered assistant built around Hyderabad’s pollution data that explains the air in plain language and guides people toward reducing it.",
      problem: "Hyderabad’s air-quality numbers are hard for everyday residents to interpret and rarely turn into clear, actionable guidance.",
      solution: "Feed Hyderabad’s pollution data into an AI / LLM model that interprets it, answers questions in plain language and recommends practical steps for residents.",
      impact: "Helps people in Hyderabad understand the air they breathe and take actions that help control pollution across the city.",
      stack: ["Python","LLM","Machine Learning","Data Analysis"], hue: 200, live: "#", repo: "#" },
    { id: "p7", tag: "Score a resume against any job.", name: "Resume Screening Helper", cat: "AI", sub: "AI Resume Screening Helper", year: "",
      desc: "A Python workflow that extracts skills from a resume, compares them with job-description keywords and generates a relevance score.",
      problem: "Reading every resume by hand against a job description is slow and inconsistent.",
      solution: "Python-based screening workflow: preprocess the text, extract skills, match them against the job-description keywords (ATS-style) and generate a relevance score.",
      impact: "Strengthened practical understanding of text preprocessing, ATS-style keyword matching, scoring logic and AI-assisted recruitment use cases.",
      stack: ["Python","NLP Concepts","Keyword Matching"], hue: 290, live: "#", repo: "#" },
    { id: "p9", tag: "Predict how a student will perform.", name: "Student Performance Predictor", cat: "ML", sub: "Student Performance Prediction System", year: "",
      desc: "An ML workflow that predicts student performance from structured academic data.",
      problem: "Understanding which factors drive student performance — and spotting students who may struggle — from raw academic records.",
      solution: "Data cleaning, exploratory analysis, feature selection, model training and evaluation with Pandas, NumPy and Scikit-learn, followed by interpreting the results.",
      impact: "Covers the full machine-learning project lifecycle: from messy data to an evaluated, interpretable prediction.",
      stack: ["Python","Pandas","NumPy","Scikit-learn"], hue: 160, live: "#", repo: "#" },
    { id: "p10", tag: "From commit to deploy, automated.", name: "CI/CD Deployment Pipeline", cat: "DevOps", sub: "DevOps CI/CD Deployment Pipeline", year: "",
      desc: "A structured deployment workflow for a web application: build, test and deploy stages with release documentation.",
      problem: "Manual releases are slow and error-prone, and broken code can reach users.",
      solution: "Version control with GitHub, build-test-deploy stages, basic containerization concepts with Docker and written release documentation.",
      impact: "Shows an understanding of automation, deployment discipline, quality checks and production-ready engineering habits.",
      stack: ["GitHub","Docker Concepts","CI/CD"], hue: 215, live: "#", repo: "#" },
    { id: "p11", tag: "Turn client needs into a working plan.", name: "FDE Case Study", cat: "Product", sub: "Forward Deployed Engineering Case Study", year: "",
      desc: "A client workflow-automation case study: requirements, pain points, a solution flow and handover notes.",
      problem: "Client teams know their pain points but rarely express them as technical work.",
      solution: "Gathered requirements, mapped user pain points, converted business needs into technical tasks, drafted a solution flow and wrote handover notes.",
      impact: "Connects stakeholder communication with practical technical execution — the core of forward deployed engineering.",
      stack: ["Requirements","APIs","Documentation"], hue: 35, live: "#", repo: "#" },
    { id: "p12", tag: "This site: one layout for every screen.", name: "Responsive Portfolio", cat: "Web", sub: "Responsive Portfolio Website", year: "",
      desc: "A responsive personal portfolio with structured sections for profile, skills, projects and contact details.",
      problem: "A portfolio must present technical work professionally on every screen size.",
      solution: "Semantic page structure, clean navigation, a mobile-friendly layout, strong visual hierarchy and accessibility-aware design in HTML, CSS and JavaScript.",
      impact: "A fast, accessible site that works from small phones to large monitors — the one you are looking at now.",
      stack: ["HTML","CSS","JavaScript"], hue: 255, live: "#", repo: "#" },
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
    { id: "p8", tag: "Plan work: To do, Doing, Done.", name: "TaskFlow", cat: "Full Stack", sub: "Productivity & Task Manager", year: "2024",
      desc: "A clean to-do and planner app with reminders and progress charts.",
      problem: "Students juggle deadlines across notes and chats.",
      solution: "React front end with a Node API, login, reminders and weekly progress analytics.",
      impact: "A polished full-stack app deployed online.",
      stack: ["React","Node.js","MongoDB","Tailwind"], hue: 180, live: "#", repo: "#" }
  ],

  education: [
    { deg: "B.Tech — Computer Science & Engineering", org: "Malla Reddy Engineering College for Women, Hyderabad", when: "Aug 2023 — 2027", note: "Current CGPA 8.20 / 10" },
    { deg: "Intermediate (Class XII)", org: "Kendriya Vidyalaya", when: "Completed", note: "72%" },
    { deg: "Class X", org: "Kendriya Vidyalaya", when: "Completed", note: "92%" }
  ],
  achievements: [
    "Cambridge English Empower B2 Level — Cambridge University Press & Assessment",
    "Cisco Certification — Python and C programming",
    "Oracle Participation Certificate — course participation"
  ]
};
