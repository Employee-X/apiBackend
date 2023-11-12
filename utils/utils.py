from enum import Enum
import uuid
import math, random
from datetime import date,timezone,datetime,timedelta

JOB_COUNT_CATEGORY_WISE     =  {"programmingJobs":0,
                            "financeAndAccountingJobProfiles": 0, 
                            "musicAndAudioJobProfiles": 0 , 
                            "videoAndAnimationJobProfiles": 0,
                            "digitalMarketingJobProfiles": 0, 
                            "designJobProfiles":0, 
                            "productAndMarketingJobProfiles":0,
                            "healthAndPharmacyJobProfiles":0,
                            "others":0,
                            }

class Roles(str, Enum):
    job_seeker = "job_seeker"
    college = "college"
    recruiter = "recruiter"
    admin = "admin"


class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class Job_Status(str,Enum):
    active = "active"
    inactive = "inactive"

class Applicant_Status(str,Enum):
    unapplied = "unapplied"
    applied = "applied"
    rejected = "rejected"

class Recruiter_Status(str,Enum):
    allowed = "allowed"
    awaiting = "awaiting"
    denied = "denied"

class Job_Approval_Status(str,Enum):
    hold = "hold"
    unhold = "unhold"

class Profession(str, Enum):
    student = "student"
    software_engineer = "software_engineer"
    data_scientist = "data_scientist"
    data_analyst = "data_analyst"
    data_engineer = "data_engineer"
    business_analyst = "business_analyst"
    product_manager = "product_manager"
    product_designer = "product_designer"
    ui_ux_designer = "ui_ux_designer"
    graphic_designer = "graphic_designer"
    web_developer = "web_developer"
    full_stack_developer = "full_stack_developer"
    front_end_developer = "front_end_developer"
    back_end_developer = "back_end_developer"
    mobile_developer = "mobile_developer"
    android_developer = "android_developer"
    ios_developer = "ios_developer"
    devops_engineer = "devops_engineer"
    cloud_architect = "cloud_architect"
    cloud_engineer = "cloud_engineer"
    cloud_consultant = "cloud_consultant"
    cloud_administrator = "cloud_administrator"
    cloud_security_engineer = "cloud_security_engineer"
    cloud_network_engineer = "cloud_network_engineer"
    cloud_operations_engineer = "cloud_operations_engineer"

class Skills(str, Enum):
    python = "Python"
    java = "Java"
    javascript = "JavaScript"
    c = "C"
    c_plus_plus = "C++"
    c_sharp = "C#"
    php = "PHP"
    r = "R"
    swift = "Swift"
    sql = "SQL"
    ruby = "Ruby"
    go = "Go"
    kotlin = "Kotlin"
    typescript = "TypeScript"
    scala = "Scala"
    rust = "Rust"
    dart = "Dart"
    perl = "Perl"
    matlab = "MATLAB"
    visual_basic = "Visual Basic"
    assembly_language = "Assembly Language"
    vba = "VBA"
    objective_c = "Objective-C"
    groovy = "Groovy"
    abap = "ABAP"
    cobol = "COBOL"
    fortran = "FORTRAN"
    lua = "Lua"
    scheme = "Scheme"
    ada = "Ada"
    prolog = "Prolog"
    lisp = "Lisp"
    racket = "Racket"
    clojure = "Clojure"
    erlang = "Erlang"
    haskell = "Haskell"
    f_sharp = "F#"
    pascal = "Pascal"
    delphi = "Delphi"
    julia = "Julia"
    apex = "Apex"
    bash = "Bash"
    shell = "Shell"
    powershell = "PowerShell"
    html = "HTML"
    css = "CSS"
    react = "React"
    angular = "Angular"
    vue_js = "Vue.js"
    node_js = "Node.js"
    django = "Django"
    flask = "Flask"
    laravel = "Laravel"
    spring = "Spring"
    express_js = "Express.js"
    ruby_on_rails = "Ruby on Rails"
    asp_net = "ASP.NET"
    jsp = "JSP"
    jquery = "jQuery"
    bootstrap = "Bootstrap"
    tailwind_css = "Tailwind CSS"
    sass = "Sass"
    less = "Less"
    mysql = "MySQL"
    postgresql = "PostgreSQL"
    mongodb = "MongoDB"
    redis = "Redis"
    sqlite = "SQLite"
    oracle = "Oracle"
    microsoft_sql_server = "Microsoft SQL Server"
    elasticsearch = "Elasticsearch"
    firebase = "Firebase"
    mariadb = "MariaDB"
    cassandra = "Cassandra"
    couchbase = "Couchbase"
    neo4j = "Neo4j"
    dynamodb = "DynamoDB"
    memcached = "Memcached"
    aws = "AWS"
    azure = "Azure"
    google_cloud = "Google Cloud"
    docker = "Docker"
    kubernetes = "Kubernetes"
    jenkins = "Jenkins"
    ansible = "Ansible"
    terraform = "Terraform"
    puppet = "Puppet"
    chef = "Chef"
    prometheus = "Prometheus"
    grafana = "Grafana"
    nagios = "Nagios"
    splunk = "Splunk"
    elk_stack = "ELK Stack"
    git = "Git"
    github = "GitHub"
    gitlab = "GitLab"
    jira = "Jira"
    confluence = "Confluence"
    trello = "Trello"
    notion = "Notion"

def unique_filename_generator(filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (uuid.uuid4(), ext)
    return new_filename

def otp_generator():
    otp = random.randint(100000, 999999)
    return otp