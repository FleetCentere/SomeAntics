from ProjectFiles import app, db
from ProjectFiles.models import userTable, dayTable, taskTable, newsTable, eventTable, contentTable, exerciseTable, personsTable, ideaTable, sourcesTable, companyTable, csTable, csPosts, jobTable, financePostsTable

def idLookup(category, parent_id):
    if category == "task":
        parent = taskTable.query.get_or_404(parent_id)
    elif category == "content":
        parent = contentTable.query.get_or_404(parent_id)
    elif category == "exercise":
        parent = exerciseTable.query.get_or_404(parent_id)
    elif category == "job":
        parent = jobTable.query.get_or_404(parent_id)
    elif category == "news":
        parent = newsTable.query.get_or_404(parent_id)
    elif category == "company":
        parent = companyTable.query.get_or_404(parent_id)
    elif category == "cs":
        parent = csTable.query.get_or_404(parent_id)
    elif category == "event":
        parent = eventTable.query.get_or_404(parent_id)
    elif category == "people":
        parent = personsTable.query.get_or_404(parent_id)
    else:
        parent = None
    
    return parent

if "__main__" == __name__:
    parent = idLookup(category, parent_id)
    print(parent)