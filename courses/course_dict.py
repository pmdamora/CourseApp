from CourseApp.courses.models import Course

# A dictionary for with 4 letter subject codes as keys and the full name as value
course_list = {"ALAN":"ALANA U.S. Ethnic Studies", "ANFS":"Animal,Nutrition & Food Sci", "ANNB":"Anatomy & Neurobiology", "ANPS":"Anatomy/Physiology", "ANTH":"Anthropology", "ARBC":"Arabic", "ARTH":"Art History", "ARTS":"Art Studio", "AS":"A&S Interdisciplinary", "ASCI":"Animal Science", "ASL":"American Sign Language", "ASTR":"Astronomy", "AT":"Athletic Training", "BCOR":"BioCore", "BIOC":"Biochemistry", "BIOE":"Bioengineering", "BIOL":"Biology", "BSAD":"Business Administration", "BSCI":"Biological Sciences", "BUCK":"Buckham Overseas Program", "CALS":"Agriculture & Life Sciences", "CDAE":"Cmty Dev & Apld Econ", "CE":"Civil & Environmental Engr", "CEMS":"Engr & Math Sciences", "CHEM":"Chemistry", "CHIN":"Chinese", "CLAS":"Classics", "CLBI":"Cell Biology", "CS":"Computer Science", "CSD":"Comm Sciences & Disorders", "CSYS":"Complex Systems", "CTS":"Clinical&Translational Science", "DNCE":"Dance", "EC":"Economics", "ECSP":"Early Childhood Special Educ", "EDAR":"Art Education", "EDCI":"Curriculum & Instruction", "EDCO":"Counseling", "EDEC":"Early Childhood Pre K-3 ", "EDEL":"Elementary Education", "EDFS":"Foundations", "EDHE":"Health Education", "EDHI":"Higher Education", "EDLI":"Library Science", "EDLP":"Leadership and Policy Studies", "EDLT":"Literacy", "EDML":"Middle Level Teacher Education", "EDPE":"Physical Education-Prof ", "EDSC":"Secondary Education ", "EDSP":"Special Education", "EDSS":"Education", "EDTE":"Teacher Education", "EE":"Electrical Engineering", "ENGR":"Engineering", "ENGS":"English", "ENSC":"Environmental Sciences", "ENVS":"Environmental Studies", "ESOL":"Engl for Spkrs of Other Langs", "EXMS":"Exercise & Movement Science", "FOR":"Forestry", "FREN":"French", "FS":"Food Systems", "FTS":"Film & Television Studies ", "GEOG":"Geography", "GEOL":"Geology", "GERM":"German", "GKLT":"Greek & Latin", "GRAD":"Graduate", "GRK":"Greek", "GRMD":"Graduate Medical", "GRNS":"Graduate Nursing", "GRS":"Global and Regional Studies", "GSWS":"Gndr, Sexuality, & Wms Stdies", "HCOL":"Honors College", "HDFS":"Human Development & Fam Stdies", "HEBR":"Hebrew", "HLTH":"Health", "HON":"Honors", "HP":"Historic Preservation", "HS":"Holocaust Studies", "HST":"History", "ITAL":"Italian", "JAPN":"Japanese", "LAT":"Latin", "LING":"Linguistics", "MAED":"Mathematics for Educators", "MATH":"Mathematics", "MATS":"Materials Science", "MBA":"Master of Business Admin", "ME":"Mechanical Engineering", "MLRS":"Medical Lab & Radiation Sci", "MLS":"Medical Laboratory Science", "MMG":"Micr & Molecular Genetics", "MPBP":"Molecular Physiology & Biophys", "MS":"Military Studies", "MU":"Music", "NFS":"Nutrition and Food Sciences", "NH":"Nursing & Health Sciences", "NMT":"Nuclear Medicine Technology", "NR":"Natural Resources", "NSCI":"Neuroscience", "NURS":"Nursing", "ORTH":"Orthopedic Surgery", "OSSP":"Overseas Study Program", "PA":"Public Administration", "PATH":"Pathology", "PBIO":"Plant Biology", "PEAC":"Physical Education ", "PH":"Public Health", "PHIL":"Philosophy", "PHRM":"Pharmacology", "PHYS":"Physics", "POLS":"Political Science", "PRNU":"Professional Nursing", "PRT":"Parks, Recreation and Tourism", "PSS":"Plant & Soil Science", "PSTG":"Public Serv Tech Gen", "PSYC":"Psychology", "PT":"Physical Therapy", "RADT":"Radiation Therapy", "REL":"Religion", "RMS":"Rehabilitation & Movement Sci ", "RUSS":"Russian", "SOC":"Sociology", "SPAN":"Spanish", "SPCH":"Speech", "STAT":"Statistics", "SURG":"Surgery", "SWSS":"Social Work", "THE":"Theatre", "TRC":"Transportation Rsch Ctr", "VS":"Vermont Studies", "WFB":"Wildlife & Fisheries Biology", "WLIT":"World Literature","EMGT":"Engineering Management"}


# This function is incredibly inefficient and slow and has been removed from the release version
# create a dictionary of all professors and net ids
#
# def get_instructor_list():
# 	instructors = Course.query.all()
# 	instructor_list = {}
# 	
# 	for person in instructors:
# 		if person.instructor_netid not in instructor_list:
# 				instructor_list[person.instructor_netid] = person.instructor
# 
# 	return instructor_list








